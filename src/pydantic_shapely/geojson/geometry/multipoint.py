"""_summary_
"""

import typing

import shapely

from ._base import GeometryBase
from .point import CoordinatesPoint2D, CoordinatesPoint3D

CoordinatesMultiPoint2D = typing.List[CoordinatesPoint2D]
CoordinatesMultiPoint3D = typing.List[CoordinatesPoint3D]
CoordinatesMultiPoint = typing.Union[CoordinatesMultiPoint2D, CoordinatesMultiPoint3D]
MultiPointTypeVar = typing.TypeVar(
    "MultiPointTypeVar",
    CoordinatesMultiPoint2D,
    CoordinatesMultiPoint3D,
    CoordinatesMultiPoint,
)


class MultiPointBase(GeometryBase, typing.Generic[MultiPointTypeVar]):
    """A multi-point geometry."""

    type: str = "MultiPoint"
    coordinates: MultiPointTypeVar

    def to_shapely(self) -> shapely.MultiPoint:
        """Convert the multi-point to a Shapely multi-point."""
        return shapely.MultiPoint(self.coordinates)


class MultiPoint2D(MultiPointBase[CoordinatesMultiPoint2D]):
    """A 2D multi-point geometry."""


class MultiPoint3D(MultiPointBase[CoordinatesMultiPoint3D]):
    """A 3D multi-point geometry."""


class MultiPoint(MultiPointBase[CoordinatesMultiPoint]):
    """A multi-point geometry, both 2D and 3D points are allowed."""
