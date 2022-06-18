"""PDF data structure."""
from typing import Optional

import numpy as np
import numpy.typing as npt
import xarray as xr


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
        alphas: Optional[npt.NDArray[np.float_]],
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
        alphas_ = xr.DataArray(alphas, coords=dict(Q2=q2grid))
        self.data = xr.Dataset(dict(pdf=pdf, alphas=alphas_))


class PDFMember:
    """Single member of a PDF set.

    It might be either a Monte Carlo replica or an Hessian eigenvector.

    """

    def __init__(self, grid: npt.NDArray[np.float_]):
        pass
