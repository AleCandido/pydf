# -*- coding: utf-8 -*-
"""Read LHA format."""
import pathlib

import numpy as np
import yaml

from ..pdf import PDF
from . import path


def member(path: pathlib.Path) -> tuple[dict, list[np.ndarray]]:
    """Parse PDF member file."""
    content = path.read_text(encoding="utf-8")

    parts = content.split("---")

    header = yaml.safe_load(parts[0])
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
    for memberpath in sorted(pdfdir.glob("*.dat")):
        print(memberpath)
        head, patches = member(memberpath)
        members.append(patches)

    return PDF(np.array([]), np.array([]), np.array([]), np.array([]), info=info)
