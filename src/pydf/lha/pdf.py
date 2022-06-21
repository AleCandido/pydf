# -*- coding: utf-8 -*-
"""LHAPDF mimicing data structure."""
from collections.abc import Sequence
from typing import Optional

import numpy as np
import numpy.typing as npt

from .. import pdf


class PDFMember:
    """Member of an LHA loaded set."""

    def __init__(self, blocks: Sequence[pdf.Block], header: Optional[dict] = None):
        """Build from blocks and header."""
        # TODO: construct a single block representation from multiple ones
        # TODO: maybe? i.e.
        # Maybe the member blocks should be aligned in flavors, but is it too
        # strict to align even in x?
        # TODO: for sure they should be concatenated in Q2, but the
        # interpolation should happen only within a single block, so at the
        # least the blocks boundaries should be stored, and used during
        # interpolation
        self.info = header
        self.blocks = blocks

    @classmethod
    def from_block(
        cls,
        xgrid: npt.NDArray[np.float_],
        qgrid: npt.NDArray[np.float_],
        flavors: npt.NDArray[np.int_],
        values: npt.NDArray[np.float_],
        info: Optional[dict] = None,
    ):
        """Initialize a PDF member from arrays."""
        return cls(blocks=[(xgrid, qgrid, flavors, values)], header=info)


class PDF:
    """LHA loaded set.

    Attributes
    ----------
    info: dict
        set level metadata table
    members: list(PDFMember)
        list of members objects

    """

    def __init__(self, members: PDFMember, info: Optional[dict] = None):
        """Initialize set object."""
        self.info = info
        self.members = members

    def upgrade(self) -> pdf.PDF:
        """Upgrade to the package native representation of PDF.

        Returns
        -------
        pdf.PDF
            set object, wrapping an `xr.DataSet`

        """
        return pdf.create(self.info, self.members)
