"""_summary_
"""

import typing

import shapely

from ._base import GeometryBase
from .linestring import CoordinatesLineString2D, CoordinatesLineString3D

CoordinatesMultiLineString2D = typing.List[CoordinatesLineString2D]
CoordinatesMultiLineString3D = typing.List[CoordinatesLineString3D]
CoordinatesMultiLineString = typing.Union[
    CoordinatesMultiLineString2D, CoordinatesMultiLineString3D
]
MultiLineStringTypeVar = typing.TypeVar(
    "MultiLineStringTypeVar",
    CoordinatesMultiLineString2D,
    CoordinatesMultiLineString3D,
    CoordinatesMultiLineString,
)


class MultiLineStringBase(GeometryBase, typing.Generic[MultiLineStringTypeVar]):
    """A multi-line string geometry."""

    type: str = "MultiLineString"
    coordinates: MultiLineStringTypeVar

    def to_shapely(self) -> shapely.MultiLineString:
        """Convert the multi-line string to a Shapely multi-line string."""
        return shapely.MultiLineString(self.coordinates)


MultiLineString2D = MultiLineStringBase[CoordinatesMultiLineString2D]
MultiLineString3D = MultiLineStringBase[CoordinatesMultiLineString3D]
MultiLineString = MultiLineStringBase[CoordinatesMultiLineString]
