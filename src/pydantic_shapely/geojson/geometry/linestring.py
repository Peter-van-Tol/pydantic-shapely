"""_summary_
"""

import typing

try:
    from typing import Annotated
except ImportError:
    # This import is required in Python 3.8
    from typing_extensions import Annotated  # type: ignore

import shapely
from pydantic import BaseModel, Field

from ._base import GeometryBase
from .point import CoordinatesPoint2D, CoordinatesPoint3D

CoordinatesLineString2D = Annotated[
    typing.List[CoordinatesPoint2D], Field(min_length=2)
]
CoordinatesLineString3D = Annotated[
    typing.List[CoordinatesPoint3D], Field(min_length=2)
]
CoordinatesLineString = typing.Union[CoordinatesLineString2D, CoordinatesLineString3D]
LinesStringTypeVar = typing.TypeVar(
    "LinesStringTypeVar",
    CoordinatesLineString2D,
    CoordinatesLineString3D,
    CoordinatesLineString,
)


class LineStringBase(GeometryBase, typing.Generic[LinesStringTypeVar]):
    """A line string geometry."""

    type: str = "LineString"
    coordinates: LinesStringTypeVar

    def to_shapely(self) -> shapely.LineString:
        """Convert the line string to a Shapely line string."""
        return shapely.LineString(self.coordinates)


LineString2D = LineStringBase[CoordinatesLineString2D]
LineString3D = LineStringBase[CoordinatesLineString3D]
LineString = LineStringBase[CoordinatesLineString]
