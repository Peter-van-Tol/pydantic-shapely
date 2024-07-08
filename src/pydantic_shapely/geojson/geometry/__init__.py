"""
This sub-module contains the GeoJSON geometry classes, as defined in
`rfc7946 <https://tools.ietf.org/html/rfc7946>`_. Also, it contains the
mapping between the GeoJSON geometry types and the Shapely objects.

Each of the seven geometry types is represented by a Pydantic model in
their own respective module. The models are:
- Point;
- MultiPoint;
- LineString;
- MultiLineString;
- Polygon;
- MultiPolygon;
- GeometryCollection.

All Pydantic models have a method `to_shapely` that converts the GeoJSON
geometry to a Shapely geometry. To convert a Shapely geometry to a GeoJSON
geometry, one can use the `to_geojson` function from this sub-module.
"""

import typing

import shapely

from . import _base
from .geometry_collection import (
    GeometryCollection,
    GeometryCollection2D,
    GeometryCollection3D,
)
from .linestring import CoordinatesLineString, LineString, LineString2D, LineString3D
from .multilinestring import MultiLineString, MultiLineString2D, MultiLineString3D
from .multipoint import MultiPoint, MultiPoint2D, MultiPoint3D
from .multipolygon import MultiPolygon, MultiPolygon2D, MultiPolygon3D
from .point import CoordinatesPoint, Point, Point2D, Point3D
from .polygon import CoordinatesPolygon, Polygon, Polygon2D, Polygon3D

MAPPING_2D = {
    shapely.Point: Point2D,
    shapely.MultiPoint: MultiPoint2D,
    shapely.LineString: LineString2D,
    shapely.MultiLineString: MultiLineString2D,
    shapely.Polygon: Polygon2D,
    shapely.MultiPolygon: MultiPolygon2D,
    shapely.GeometryCollection: GeometryCollection2D,
}

MAPPING_3D = {
    shapely.Point: Point3D,
    shapely.MultiPoint: MultiPoint3D,
    shapely.LineString: LineString3D,
    shapely.MultiLineString: MultiLineString3D,
    shapely.Polygon: Polygon3D,
    shapely.MultiPolygon: MultiPolygon3D,
    shapely.GeometryCollection: GeometryCollection3D,
}

MAPPING = {
    shapely.Point: Point,
    shapely.MultiPoint: MultiPoint,
    shapely.LineString: LineString,
    shapely.MultiLineString: MultiLineString,
    shapely.Polygon: Polygon,
    shapely.MultiPolygon: MultiPolygon,
    shapely.GeometryCollection: GeometryCollection,
}

# NOTE:
# In both CONVERTERS_2D and CONVERTERS_3D, the `mypy` type checker is ignoring
# the Point and Multipoint cases. This is because the `shape.coords` attribute
# is a generic type, whilst the `Point2D` and `MultiPoint2D` classes expect a
# tuple of floats.
# The converters work as expected, as proven by the tests. To make `mypy` happy,
# adding a GuardType is required. This seems a bit out-rageous for justing making
# `mypy` happy.


def convert_shapely_geometry_collection_to_geojson_coordinates(
    geom_collection: shapely.geometry.GeometryCollection,
) -> typing.List[
    typing.Union[CoordinatesPoint, CoordinatesLineString, CoordinatesPolygon]
]:

    coordinates: typing.List[typing.Tuple[typing.Any, ...]] = []
    for geom in geom_collection.geoms:
        if geom.geom_type == "Point":
            coordinates.append(tuple(geom.coords[0]))
        elif geom.geom_type == "LineString":
            coordinates.append(tuple(geom.coords))
        elif geom.geom_type == "Polygon":
            coordinates.append(
                (geom.exterior.coords, *[hole.coords for hole in geom.interiors])
            )
        else:
            raise ValueError(f"Unsupported Shapely geometry type: {geom.geom_type}")
    return typing.cast(
        typing.List[
            typing.Union[CoordinatesPoint, CoordinatesLineString, CoordinatesPolygon]
        ],
        coordinates,
    )


CONVERTERS_2D = {
    "Point": lambda shape: Point2D(coordinates=tuple(shape.coords[0])),  # type: ignore
    "MultiPoint": lambda shape: MultiPoint2D(
        coordinates=[tuple(geom.coords[0]) for geom in shape.geoms]  # type: ignore
    ),
    "LineString": lambda shape: LineString2D(coordinates=shape.coords),
    "MultiLineString": lambda shape: MultiLineString2D(
        coordinates=[geom.coords for geom in shape.geoms]
    ),
    "Polygon": lambda shape: Polygon2D(
        coordinates=[shape.exterior.coords, *[hole.coords for hole in shape.interiors]]
    ),
    "MultiPolygon": lambda shape: MultiPolygon2D(
        coordinates=[
            [geom.exterior.coords, *[hole.coords for hole in geom.interiors]]
            for geom in shape.geoms
        ]
    ),
    "GeometryCollection": lambda shape: GeometryCollection2D(
        coordinates=convert_shapely_geometry_collection_to_geojson_coordinates(shape)
    ),
}

CONVERTERS_3D = {
    "Point": lambda shape: Point3D(coordinates=tuple(shape.coords[0])),  # type: ignore
    "MultiPoint": lambda shape: MultiPoint3D(
        coordinates=[tuple(geom.coords[0]) for geom in shape.geoms]  # type: ignore
    ),
    "LineString": lambda shape: LineString3D(coordinates=shape.coords),
    "MultiLineString": lambda shape: MultiLineString3D(
        coordinates=[geom.coords for geom in shape.geoms]
    ),
    "Polygon": lambda shape: Polygon3D(
        coordinates=[shape.exterior.coords, *[hole.coords for hole in shape.interiors]]
    ),
    "MultiPolygon": lambda shape: MultiPolygon3D(
        coordinates=[
            [geom.exterior.coords, *[hole.coords for hole in geom.interiors]]
            for geom in shape.geoms
        ]
    ),
    "GeometryCollection": lambda shape: GeometryCollection3D(
        coordinates=convert_shapely_geometry_collection_to_geojson_coordinates(shape)
    ),
}


def convert_shapely_to_geojson_object(
    shape: shapely.geometry.base.BaseGeometry,
) -> _base.GeometryBase:
    """
    Convert a Shapely geometry object to a GeoJSON geometry object.

    Parameters
    ----------
    shape : shapely.geometry.base.BaseGeometry
        The Shapely geometry object to convert.

    Returns
    -------
    dict
        The GeoJSON geometry object.
    """
    # Check which set of mappings to use
    mapping = CONVERTERS_2D
    if shape.has_z:
        mapping = CONVERTERS_3D
    try:
        return mapping[shape.geom_type](shape)
    except KeyError:
        raise ValueError(f"Unsupported Shapely geometry type: {shape.geom_type}")


def bounding_box(
    shape: shapely.geometry.base.BaseGeometry,
) -> typing.Union[
    typing.Tuple[float, float, float, float],
    typing.Tuple[float, float, float, float, float, float],
]:
    """Determine the bounding box of a Shapely geometry. This function will
    either return a 2D or 3D bounding box, depending on the presence of z-values.

    Returns:
        tuple[]: The bounding box of the geometry. Either containing 4 (2D) or
        6 (3D) values.
    """
    if not shape.has_z:
        # Use normal bounds-function for 2D geometries
        return shape.bounds
    minx, miny, maxx, maxy = shape.bounds
    # Determine bounds of the shape
    minz = float("inf")
    maxz = float("-inf")
    for coord in shapely.get_coordinates(shape, include_z=True):
        minz = min(minz, coord[2])
        maxz = max(maxz, coord[2])
    # Default behaviour for missing z-values
    if minz == float("inf"):
        minz = float("nan")
    if maxz == float("-inf"):
        maxz = float("nan")
    return (minx, miny, minz, maxx, maxy, maxz)


__all__ = [
    "Point2D",
    "Point3D",
    "Point",
    "MultiPoint2D",
    "MultiPoint3D",
    "MultiPoint",
    "LineString2D",
    "LineString3D",
    "LineString",
    "MultiLineString2D",
    "MultiLineString3D",
    "MultiLineString",
    "Polygon2D",
    "Polygon3D",
    "Polygon",
    "MultiPolygon2D",
    "MultiPolygon3D",
    "MultiPolygon",
    "GeometryCollection2D",
    "GeometryCollection3D",
    "GeometryCollection",
    "MAPPING_2D",
    "MAPPING_3D",
    "MAPPING",
    "convert_shapely_to_geojson_object",
]
