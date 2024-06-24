"""_summary_
"""

import typing

import shapely

from ._base import GeometryBase

CoordinatesPoint2D = typing.Tuple[float, float]
CoordinatesPoint3D = typing.Tuple[float, float, float]
CoordinatesPoint = typing.Union[CoordinatesPoint2D, CoordinatesPoint3D]
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


Point2D = PointBase[CoordinatesPoint2D]
Point3D = PointBase[CoordinatesPoint3D]
Point = PointBase[CoordinatesPoint]
