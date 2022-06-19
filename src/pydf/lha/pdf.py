# -*- coding: utf-8 -*-
"""LHAPDF mimicing data structure."""
from collections.abc import Sequence
from typing import Optional

import numpy as np
import numpy.typing as npt

from .. import pdf

Block = tuple[
    npt.NDArray[np.float_],
    npt.NDArray[np.float_],
    npt.NDArray[np.int_],
    npt.NDArray[np.float_],
]
"""A 4-tuple describing the content of a file block.

In particular the tuple contain:

    - xgrid: the coordinates grid in the PDF momentum fraction
    - qgrid: the coordinates grid in the PDF factorization scale
    - flavors: the PDF ID of included partons
    - values: the PDF values in the given block

"""


class PDFMember:
    """Member of an LHA loaded set."""

    def __init__(
        self,
        xgrid: npt.NDArray[np.float_],
        qgrid: npt.NDArray[np.float_],
        flavors: npt.NDArray[np.int_],
        values: npt.NDArray[np.float_],
        info: Optional[dict] = None,
    ) -> None:
        """Initialize a PDF member from arrays."""
        self.info = info
        self.xgrid = xgrid
        self.qgrid = qgrid
        self.flavors = flavors
        self.values = values

    @classmethod
    def from_blocks(cls, blocks: Sequence[Block], header: Optional[dict] = None):
        """Build from blocks and header."""
        # TODO: construct a single block representation from multiple ones
        # TODO: maybe? i.e.
        # Maybe the member blocks should be aligned in flavors, but is it too
        # strict to align even in x?
        # TODO: for sure they should be concatenated in Q2, but the
        # interpolation should happen only within a single block, so at the
        # least the blocks boundaries should be stored, and used during
        # interpolation
        return cls(*blocks[0], info=header)


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
        return pdf.PDF()
