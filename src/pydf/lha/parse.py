# -*- coding: utf-8 -*-
"""Read LHA format."""
import numpy as np
import yaml

from ..pdf import PDF
from . import configuration as conf


def parse(setname: str) -> PDF:
    """Parse PDF in LHA format."""
    pdfdir = conf.lhapdf_datapath() / setname

    if not pdfdir.exists():
        raise FileNotFoundError(
            f"No PDF set '{setname}' available in '{pdfdir.parent}'"
        )

    infopath = pdfdir / f"{setname}.info"
    info = yaml.safe_load(infopath.read_text(encoding="utf-8"))

    return PDF(np.array([]), np.array([]), np.array([]), np.array([]), info=info)
