# -*- coding: utf-8 -*-
"""Read LHA format."""
import numpy as np

from ..pdf import PDF
from . import configuration as conf


def parse(setname: str) -> PDF:
    pdfdir = conf.lhapdf_datapath() / setname

    if not pdfdir.exists():
        raise FileNotFoundError(
            f"No PDF set '{setname}' available in '{pdfdir.parent}'"
        )

    return PDF(np.array([]), np.array([]), np.array([]), np.array([]), None)
