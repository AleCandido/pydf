# -*- coding: utf-8 -*-
"""
    LHAPDF configuration environment

    It exposes an object (environment) that should contain
    all relevant external information
"""
import logging
import os
from pathlib import Path

from pydf.lha import configuration

logger = logging.getLogger(__name__)


# Some useful harcoded values
INDEX_FILENAME = "pdfsets.index"
CVMFSBASE = "/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current/"
URLBASE = r"http://lhapdfsets.web.cern.ch/lhapdfsets/current/"


class Environment:
    """LHAPDF environment"""

    # TODO take control of the logger

    def __init__(self):
        cvmfs_base = os.environ.get("LHAPDF_CVMFSBASE", CVMFSBASE)
        url_base = os.environ.get("LHAPDF_URLBASE", URLBASE)
        self._sources = [cvmfs_base, url_base]
        self._index_filename = INDEX_FILENAME
        self._datapath = None
        self._listdir = None

        # Create and format the log handler
        self._root_logger = logging.getLogger(__name__.split(".")[0])
        _console_handler = logging.StreamHandler()
        _console_format = logging.Formatter("[%(levelname)s] %(message)s")
        _console_handler.setFormatter(_console_format)
        self._root_logger.addHandler(_console_handler)

    @property
    def sources(self):
        """Iterator of all sources"""
        for source in self._sources:
            yield source

    @property
    def datapath(self):
        """Return the lhapdf datapath, don't populate until first used"""
        if self._datapath is None:
            self._datapath = configuration.lhapdf_datapath()
        return self._datapath

    @datapath.setter
    def datapath(self, new_datapath):
        """Set the LHAPDF datapath"""
        new_path = Path(new_datapath)
        if not new_path.is_dir():
            logger.error(
                "The new LHAPDF data path %s is not a directory but I'll believe you",
                new_path,
            )
        self._datapath = new_path

    @property
    def listdir(self):
        if self._listdir is None:
            self._listdir = self.datapath
        return self._listdir

    @property
    def index_filename(self):
        return self._index_filename

    def add_source(self, new_source):
        """Adds a source to the environment
        New sources take priority
        """
        self._sources = [new_source] + self._sources

    def debug_logger(self):
        """Set the logger to debug"""
        self._root_logger.setLevel(logging.DEBUG)


environment = Environment()
