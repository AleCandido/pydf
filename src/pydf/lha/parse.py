# -*- coding: utf-8 -*-
"""Read LHA format."""
import functools
import pathlib
import re
import warnings
from typing import Optional

import numpy as np
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


def member(
    path: pathlib.Path, errortype: Optional[str] = None
) -> tuple[dict, list[np.ndarray]]:
    """Parse PDF member file."""
    matched = re.fullmatch(member_filename(path.parent.name), path.name)
    if matched is None:
        raise ValueError(f"File '{path.name}' does not match members name convention")

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
    for patch in parts[1:]:
        __import__("pdb").set_trace()
        pass

    return header, [np.array([])]


def parse(setname: str) -> PDF:
    """Parse PDF in LHA format."""
    pdfdir = path.locate(setname)

    infopath = pdfdir / f"{setname}.info"
    info = yaml.safe_load(infopath.read_text(encoding="utf-8"))

    members = []
    unidentified = []
    for memberpath in sorted(pdfdir.glob(f"{setname}_*.dat")):
        print(memberpath)
        try:
            head, patches = member(memberpath)
            members.append(patches)
        except ValueError as verr:
            unidentified.append((memberpath, verr.args[0]))

    return PDF(np.array([]), np.array([]), np.array([]), np.array([]), info=info)
