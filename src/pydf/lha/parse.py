# -*- coding: utf-8 -*-
"""Read LHA format."""
import functools
import io
import os
import pathlib
import re
import warnings
from collections.abc import Sequence
from typing import Optional, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
import yaml

from ..pdf import PDF
from . import path


@functools.cache
def member_filename(setname: str) -> re.Pattern:
    """Generate pattern for member file names.

    Parameters
    ----------
    setname: str
        name of the PDF set (i.e. name of the PDF containing folder)

    Returns
    -------
    re.Pattern
        compiled pattern

    """
    return re.compile(rf"{setname}_(\d{{4}}).dat")


def member_type(
    id: str, pdftype: Optional[str], errortype: Optional[str] = None
) -> str:
    """Check or determine member type.

    Parameters
    ----------
    id: str
        the four digit ID, part of the member file name
    pdftype: None or str
        the member type, as (possibly) specified in the member header
    errortype: None or str
        the set type (usually ``hessian`` or ``replicas``) as specified by the
        set metadata

    Examples
    --------
    Mostly used to check consistency of different sources of member type, and
    determine the consistent value to be used.

    >>> pdftype = member_type(id, pdftype)

    or

    >>> pdftype = member_type(id, pdftype, errortype)

    """
    if pdftype is not None:
        if id == "0000" and pdftype != "central":
            raise ValueError(f"Member 0000 has to be 'central', found '{pdftype}'")
        return pdftype

    if id == "0000":
        return "central"

    et = errortype.lower() if errortype is not None else ""
    if et in ["hessian", "symhessian"]:
        return "error"
    if et == "replicas":
        return "replica"

    return "member"


def member_block(
    content: str,
) -> tuple[
    npt.NDArray[np.float_],
    npt.NDArray[np.float_],
    npt.NDArray[np.int_],
    npt.NDArray[np.float_],
]:
    """Parse block of a PDF member."""
    xtext, qtext, fltext, valtext = content.strip().split("\n", maxsplit=3)

    xgrid = pd.read_csv(
        io.StringIO(xtext.replace(" ", "\n")), sep=" ", names=["value"]
    ).values[:, 0]
    qgrid = pd.read_csv(
        io.StringIO(qtext.replace(" ", "\n")), sep=" ", names=["value"]
    ).values[:, 0]
    flavors = pd.read_csv(
        io.StringIO(fltext.replace(" ", "\n")), sep=" ", names=["value"]
    ).values[:, 0]
    values = pd.read_csv(
        io.StringIO(fltext + "\n" + valtext), delim_whitespace=True
    ).values

    values = values.reshape(xgrid.size, qgrid.size, flavors.size)

    return xgrid, qgrid, flavors, values


class MemberSkip(Exception):
    """Skip member element."""


def member(
    path: os.PathLike,
    errortype: Optional[str] = None,
    filter: Optional[Union[range, Sequence]] = None,
) -> tuple[dict, list[np.ndarray]]:
    """Parse PDF member file.

    Parameters
    ----------
    path: os.PathLike
        path to the member file
    errortype: str or None
        the set type (usually ``hessian`` or ``replicas``) as specified by the
        set metadata
    filter: range or Sequence
        restrict which elements should be loaded

    Returns
    -------
    dict
        header keys, as specified in the file, or reconstructed (only for
        PdfType)
    np.ndarray
        array of PDF values

    """
    path = pathlib.Path(path)

    matched = re.fullmatch(member_filename(path.parent.name), path.name)
    if matched is None:
        raise ValueError(f"File '{path.name}' does not match members name convention")
    if filter is not None and matched[1] not in filter:
        raise MemberSkip(matched[1])

    content = path.read_text(encoding="utf-8")
    parts = content.split("---")

    # parse header
    header = yaml.safe_load(parts[0])
    header["PdfType"] = member_type(matched[1], header.get("PdfType"), errortype)

    if parts[-1].strip() != "":
        warnings.warn(
            f"Member '{matched[1]}' does not end by '---', nevertheless "
            "the block after last '---' is being considered as a regular one "
            "(the specs clearly states nothing else should be there, "
            "arXiv:1412.7420v2 sec. 5.2)"
        )
    else:
        parts.pop()

    # parse following parts, one at a time
    blocks = []
    for block in parts[1:]:
        xgrid, qgrid, flavors, grid = member_block(block)

        blocks.append(grid)

    return header, [np.array([])]


def parse(setname: str, filter: Optional[Union[range, slice, Sequence]] = None) -> PDF:
    """Parse PDF in LHA format."""
    pdfdir = path.locate(setname)

    infopath = pdfdir / f"{setname}.info"
    info = yaml.safe_load(infopath.read_text(encoding="utf-8"))

    if isinstance(filter, slice):
        filter = range(*filter.indices(filter.stop))

    members = []
    unidentified = []
    for memberpath in sorted(pdfdir.glob(f"{setname}_*.dat")):
        try:
            head, patches = member(memberpath, filter=filter)
            members.append(patches)
        except ValueError as verr:
            if not any(
                marker in verr.args[0] for marker in ["0000", "name convention"]
            ):
                raise verr
            unidentified.append((memberpath, verr.args[0]))
        except MemberSkip:
            pass

    return ""
    #  return PDF(np.array([]), np.array([]), np.array([]), np.array([]), info=info)
