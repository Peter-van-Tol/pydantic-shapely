"""_summary_
"""

import typing
from numbers import Number

import shapely

from ._base import GeometryBase
from .linestring import CoordinatesLineString2D, CoordinatesLineString3D
from .point import CoordinatesPoint2D, CoordinatesPoint3D
from .polygon import CoordinatesPolygon2D, CoordinatesPolygon3D

CoordinatesCollection2D = typing.List[
    typing.Union[CoordinatesPoint2D, CoordinatesLineString2D, CoordinatesPolygon2D]
]
CoordinatesCollection3D = typing.List[
    typing.Union[CoordinatesPoint3D, CoordinatesLineString3D, CoordinatesPolygon3D]
]
CoordinatesCollection = typing.Union[CoordinatesCollection2D, CoordinatesCollection3D]
GeometryCollectionTypeVar = typing.TypeVar(
    "GeometryCollectionTypeVar",
    CoordinatesCollection2D,
    CoordinatesCollection3D,
    CoordinatesCollection,
)


class GeometryCollectionBase(GeometryBase, typing.Generic[GeometryCollectionTypeVar]):
    """A geometry collection."""

    type: str = "LineString"
    coordinates: GeometryCollectionTypeVar

    def to_shapely(self) -> shapely.LineString:
        """Convert the line string to a Shapely line string."""
        # Handle empty geometry
        if not self.coordinates:
            return shapely.GeometryCollection()
        # Handle the geometries in the collection
        geometries = []
        for sequence in self.coordinates:
            # If the sequence is empty, add an POINT EMPTY geometry
            if not sequence:
                geometries.append(shapely.Point())
            elif isinstance(sequence[0], Number):
                geometries.append(shapely.Point(*sequence))
            elif not sequence[0]:
                # Empty line string
                geometries.append(shapely.LineString())
            elif not sequence[0][0]:
                # Empty line string
                geometries.append(shapely.LineString(sequence))
            elif isinstance(sequence[0][0], Number):
                geometries.append(shapely.LineString(sequence))
            elif not sequence[0][0][0]:
                # Empty polygon
                geometries.append(shapely.Polygon())
            elif isinstance(sequence[0][0][0], Number):
                holes = []
                if len(sequence) > 1:
                    holes = sequence[1:]
                geometries.append(shapely.Polygon(sequence[0], holes))
            else:
                raise ValueError("Invalid geometry in the collection")
        return shapely.GeometryCollection(geometries)


class GeometryCollection2D(GeometryCollectionBase[CoordinatesCollection2D]):
    """A 2D geometry collection."""


class GeometryCollection3D(GeometryCollectionBase[CoordinatesCollection3D]):
    """A 3D geometry collection."""


class GeometryCollection(GeometryCollectionBase[CoordinatesCollection]):
    """A geometry collection, both 2D and 3D geometries are allowed."""
