"""_summary_
"""

import typing
from pydantic import BaseModel
import shapely

from .polygon import CoordinatesPolygon2D, CoordinatesPolygon3D


CoordinatesMultiPolygon2D = typing.List[CoordinatesPolygon2D]
CoordinatesMultiPolygon3D = typing.List[CoordinatesPolygon3D]
CoordinatesMultiPolygon = typing.Union[
    CoordinatesMultiPolygon2D, CoordinatesMultiPolygon3D
]
MultiPolygonTypeVar = typing.TypeVar(
    "MultiPolygonTypeVar",
    CoordinatesMultiPolygon2D,
    CoordinatesMultiPolygon3D,
    CoordinatesMultiPolygon,
)


class MultiPolygonBase(BaseModel, typing.Generic[MultiPolygonTypeVar]):
    """A multi-polygon geometry."""

    type: str = "MultiPolygon"
    coordinates: MultiPolygonTypeVar

    def to_shapely(self) -> shapely.MultiPolygon:
        """Convert the multi-polygon to a Shapely multi-polygon."""
        return shapely.MultiPolygon(
            [
                shapely.Polygon(sequence[0], sequence[1:])
                for sequence
                in self.coordinates
            ]
        )


MultiPolygon2D = MultiPolygonBase[CoordinatesMultiPolygon2D]
MultiPolygon3D = MultiPolygonBase[CoordinatesMultiPolygon3D]
MultiPolygon = MultiPolygonBase[CoordinatesMultiPolygon]
