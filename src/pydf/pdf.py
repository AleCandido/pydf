# -*- coding: utf-8 -*-
"""PDF data structure."""
import pathlib
from typing import Optional, Sequence

import numpy as np
import numpy.typing as npt
import xarray as xr

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


class Member:
    """Single member of a PDF set.

    It might be either a Monte Carlo replica or an Hessian eigenvector.

    """

    def __init__(self, blocks: Sequence[Block], info: Optional[dict] = None):
        """Initialize single PDF member.

        Parameters
        ----------
        gris: np.ndarray
            PDF member values

        """
        pass


class PDF:
    """Parton Distribution Functions set.

    Multi-dimensional data container for parton distribution functions values,
    and related attributes.

    """

    def __init__(
        self,
        grid: npt.NDArray[np.float_],
        flavors: npt.NDArray[np.int_],
        xgrid: npt.NDArray[np.float_],
        q2grid: npt.NDArray[np.float_],
        alphas: Optional[npt.NDArray[np.float_]] = None,
        info: Optional[dict] = None,
    ):
        """Fully initialize PDF instance.

        Ask for all mandatory arguments to initialize a PDF set.

        Parameters
        ----------
        grid: np.ndarray
            PDF values
        flavors: np.ndarray
            available flavors for the set
        xgrid: np.ndarray
            grid in PDF momentum fraction
        q2grid: np.ndarray
            grid in PDF factorization scale
        alphas: np.ndarray or None
            grid in PDF factorization scale

        """
        pdf = xr.DataArray(
            grid,
            coords=dict(
                member=np.arange(grid.shape[0]), flavor=flavors, x=xgrid, Q2=q2grid
            ),
        )
        if alphas is not None:
            alphas_ = xr.DataArray(alphas, coords=dict(Q2=q2grid))
        else:
            alphas_ = xr.DataArray()

        if info is None:
            info = {}

        self.data = xr.Dataset(dict(pdf=pdf, alphas=alphas_), attrs=info)

    @classmethod
    def from_lha(cls):
        """Create instance from LHA mimicing object."""


class Homogeneous(PDF):
    pass


class Inhomogeneous(PDF):
    pass


def create(info: dict, members: Sequence[Member]) -> PDF:
    return PDF()


def read(path: pathlib.Path) -> PDF:
    return PDF()
