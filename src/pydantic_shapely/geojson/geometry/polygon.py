"""_summary_
"""

import typing

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

import shapely
from pydantic import AfterValidator, BaseModel, Field

from .point import CoordinatesPoint2D, CoordinatesPoint3D


def check_linearring(
    value: typing.List[CoordinatesPoint2D],
) -> typing.List[CoordinatesPoint2D]:
    """Validate that the input value is a valid LinearRing, i.e. the last coordinate should
    be equal to the first coordinate."""
    if value[0] != value[-1]:
        raise ValueError("The first and last point of a LinearRing must be the same.")
    return value


CoordinatesPolygon2D = Annotated[
    typing.List[
        Annotated[
            typing.List[CoordinatesPoint2D],
            AfterValidator(check_linearring),
            Field(min_length=4),
        ]
    ],
    Field(min_length=1),
]
CoordinatesPolygon3D = Annotated[
    typing.List[
        Annotated[
            typing.List[CoordinatesPoint3D],
            AfterValidator(check_linearring),
            Field(min_length=4),
        ]
    ],
    Field(min_length=1),
]
CoordinatesPolygon = typing.Union[CoordinatesPolygon2D, CoordinatesPolygon3D]
PolygonTypeVar = typing.TypeVar(
    "PolygonTypeVar", CoordinatesPolygon2D, CoordinatesPolygon3D, CoordinatesPolygon
)


class PolygonBase(BaseModel, typing.Generic[PolygonTypeVar]):
    """A polygon geometry."""

    type: str = "Polygon"
    coordinates: PolygonTypeVar

    def to_shapely(self) -> shapely.Polygon:
        """Convert the polygon to a Shapely polygon."""
        return shapely.Polygon(self.coordinates[0], self.coordinates[1:])


Polygon2D = PolygonBase[CoordinatesPolygon2D]
Polygon3D = PolygonBase[CoordinatesPolygon3D]
Polygon = PolygonBase[CoordinatesPolygon]
