# -*- coding: utf-8 -*-
"""LHAPDF utilities."""
import pathlib

from . import path


def list_installed() -> dict[str, pathlib.Path]:
    """List all installed PDF sets.

    Returns
    -------
    dict
        mapping from available names to paths on file system

    """
    pdfs = {}

    for pathdir in path.lhapdf_datapath():
        for pdf in pathdir.iterdir():
            if pdf.name in pdfs:
                continue

            if pdf.is_dir() and (pdf / f"{pdf.name}.info").is_file():
                pdfs[pdf.name] = pdf.absolute()

    return pdfs
