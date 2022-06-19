# -*- coding: utf-8 -*-
"""LHAPDF data path identification.

It exposes an object (environment) that should contain all relevant external
information.

"""
import os
import pathlib
import sys


def lhapdf_datapath() -> list[pathlib.Path]:
    """Look for the LHAPDF data folders.

    The look-up order is:

        - LHAPDF_DATA_PATH
        - LHAPATH
        - prefixes, sorted as:

            - local prefix (user or environment, including virtual ones)
            - content of environment variable ``$PREFIX``
            - frequent user prefix (Linux specific: ``$HOME/.local``)
            - system prefix

          only those existing and containing ``share/LHAPDF`` are appended to the
          list.
        - the one resolved by ``lhapdf`` package (if available), corresponding
          to the folder specified at build time

    Returns
    -------
    list(patlib.Path)
        the content of the first non-empty source among listed ones

    """
    # Look at environ variables
    for i in ["LHAPDF_DATA_PATH", "LHAPATH"]:
        paths = os.environ.get(i)
        if paths is not None:
            return [pathlib.Path(path) for path in paths.split(":")]

    # If we didn't find it in the environment variables, autodiscover prefix
    prefix_paths = [
        sys.prefix,  # top priority to loal environment, even virtual ones
        os.environ.get("PREFIX"),  # if defined, look for PREFIX env var
        pathlib.Path.home() / ".local",  # check if available in standard home path
        sys.base_prefix,  # finally, have a look also system wide
    ]
    paths = []
    for prefix_path in prefix_paths:
        if prefix_path is None:
            continue

        lhapdf_path = pathlib.Path(prefix_path) / "share/LHAPDF/"
        if lhapdf_path.is_dir():
            # Some sytems (such as Arch) keep things under LHAPDF/lhapdf so, check that as well
            if (lhapdf_path / "lhapdf").is_dir():
                paths.append(lhapdf_path / "lhapdf")
            else:
                paths.append(lhapdf_path)

    if len(paths) > 0:
        return paths

    # Ok, now we have an actual problem, try asking some old school lhapdf installation...
    try:
        import lhapdf

        return [pathlib.Path(path) for path in lhapdf.paths()]
    except ImportError as e:
        raise FileNotFoundError("No data directory for LHAPDF found") from e


def locate(setname: str) -> pathlib.Path:
    """Locate PDF set folder.

    Parameters
    ----------
    setname: str
        the of the PDF set to look up for

    Returns
    -------
    pathlib.Path
        the location retrieved

    Raises
    ------
    FileNotFoundError
        if location is not identified

    """
    lhapath = lhapdf_datapath()

    for path in lhapath:
        pdfdir = path / setname
        if pdfdir.exists():
            return pdfdir

    raise FileNotFoundError(f"No PDF set '{setname}' available in LHAPDF path.")


def global_resource(filename: str) -> pathlib.Path:
    """Locate global resource file.

    Parameters
    ----------
    filename: str
        the expected file name to be retrieved (including extension)

    Returns
    -------
    pathlib.Path
        the location retrieved

    Raises
    ------
    FileNotFoundError
        if location is not identified

    """
    lhapath = lhapdf_datapath()

    for path in lhapath:
        configpath = path / filename
        if configpath.is_file():
            return configpath

    raise FileNotFoundError(
        f"No global configuration file '{filename}' found in LHAPDF path."
    )


CONFIGURATION = "lhapdf.conf"


def config() -> pathlib.Path:
    """Locate global config file.

    Specialization of `global_resource` for configuration file (whose name is stored in
    `CONFIGURATION` variable).

    """
    return global_resource(CONFIGURATION)


INDEX = "lhapdf.conf"


def index() -> pathlib.Path:
    """Locate global PDF index file.

    Specialization of `global_resource` for index file (whose name is stored in
    `INDEX` variable).

    """
    return global_resource(INDEX)
