"""_summary_
"""

import typing

import shapely
from pydantic import BaseModel

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


class MultiPointBase(BaseModel, typing.Generic[MultiPointTypeVar]):
    """A multi-point geometry."""

    type: str = "MultiPoint"
    coordinates: MultiPointTypeVar

    def to_shapely(self) -> shapely.MultiPoint:
        """Convert the multi-point to a Shapely multi-point."""
        return shapely.MultiPoint(self.coordinates)


MultiPoint2D = MultiPointBase[CoordinatesMultiPoint2D]
MultiPoint3D = MultiPointBase[CoordinatesMultiPoint3D]
MultiPoint = MultiPointBase[CoordinatesMultiPoint]
