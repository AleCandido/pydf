# -*- coding: utf-8 -*-
"""
    LHAPDF configuration environment

    It exposes an object (environment) that should contain
    all relevant external information
"""
import logging
import os
import pathlib
import sys

_logger = logging.getLogger(__name__)


def lhapdf_datapath():
    """Look for the LHAPDF data folder
    The look-for order is:
    LHAPDF_DATA_PATH, LHAPATH, current prefix
    """
    # Look at environ variables
    for i in ["LHAPDF_DATA_PATH", "LHAPATH"]:
        val = os.environ.get(i)
        if val is not None:
            return pathlib.Path(val)

    # If we didn't find it in the environment variables, autodiscover prefix
    prefix_paths = [
        sys.prefix,  # top priority to loal environment, even virtual ones
        os.environ.get("PREFIX"),  # if defined, look for PREFIX env var
        pathlib.Path.home() / ".local",  # check if available in standard home path
        sys.base_prefix,  # finally, have a look also system wide
    ]
    for prefix_path in prefix_paths:
        if prefix_path is None:
            continue

        lhapdf_path = pathlib.Path(prefix_path) / "share/LHAPDF/"
        if lhapdf_path.is_dir():
            # Some sytems (such as Arch) keep things under LHAPDF/lhapdf so, check that as well
            if (lhapdf_path / "lhapdf").is_dir():
                return lhapdf_path / "lhapdf"
            return lhapdf_path
    # Ok, now we have an actual problem, try asking some old school lhapdf installation...
    try:
        import lhapdf

        return pathlib.Path(lhapdf.paths()[0])
    except ImportError as e:
        _logger.error(
            "Data directory for LHAPDF not found, you can use the LHAPDF_DATA_PATH environ variable"
        )
        raise FileNotFoundError("No data directory for LHAPDF found") from e
