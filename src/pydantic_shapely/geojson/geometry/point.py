"""_summary_
"""

import typing

import shapely
from typing_extensions import TypeAlias

from ._base import GeometryBase

CoordinatesPoint2D: TypeAlias = typing.Tuple[float, float]
CoordinatesPoint3D: TypeAlias = typing.Tuple[float, float, float]
CoordinatesPoint: TypeAlias = typing.Union[CoordinatesPoint2D, CoordinatesPoint3D]
PointTypeVar = typing.TypeVar(
    "PointTypeVar", CoordinatesPoint2D, CoordinatesPoint3D, CoordinatesPoint
)


class PointBase(GeometryBase, typing.Generic[PointTypeVar]):
    """A point geometry."""

    type: str = "Point"
    coordinates: PointTypeVar

    def to_shapely(self) -> shapely.Point:
        """Convert the point to a Shapely point."""
        return shapely.Point(*self.coordinates)


class Point2D(PointBase[CoordinatesPoint2D]):
    """A 2D point geometry."""


class Point3D(PointBase[CoordinatesPoint3D]):
    """A 3D point geometry."""


class Point(PointBase[CoordinatesPoint]):
    """A point geometry, both 2D and 3D points are allowed."""
