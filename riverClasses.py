from dataclasses import dataclass
import numpy as np


@dataclass
class CrossSection:
    """Class for keeping track of cross sections that define river boundaries."""
    order: float
    station: float
    p_left: np.ndarray
    p_right: np.ndarray


@dataclass
class PointXY:
    """Class for bottom elevation data points, with x y coordinates."""
    p: np.ndarray
    z: float


@dataclass
class PointRowCol:
    """Class for bottom elevation data points, with row col coordinates."""
    row: int
    col: int
    z: float


@dataclass
class InterpolationGrid:
    """Class for the interpolation grid."""
    num_rows: int
    num_cols: int
    dx: float
    ss: np.ndarray
    xs: np.ndarray
    ys: np.ndarray
