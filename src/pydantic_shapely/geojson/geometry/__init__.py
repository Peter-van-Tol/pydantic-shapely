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

import shapely

from . import _base
from .linestring import LineString, LineString2D, LineString3D
from .multilinestring import MultiLineString, MultiLineString2D, MultiLineString3D
from .multipoint import MultiPoint, MultiPoint2D, MultiPoint3D
from .multipolygon import MultiPolygon, MultiPolygon2D, MultiPolygon3D
from .point import Point, Point2D, Point3D
from .polygon import Polygon, Polygon2D, Polygon3D

MAPPING_2D = {
    shapely.Point: Point2D,
    shapely.MultiPoint: MultiPoint2D,
    shapely.LineString: LineString2D,
    shapely.MultiLineString: MultiLineString2D,
    shapely.Polygon: Polygon2D,
    shapely.MultiPolygon: MultiPolygon2D,
    # shapely.GeometryCollection: GeometryCollection2D
}

MAPPING_3D = {
    shapely.Point: Point3D,
    shapely.MultiPoint: MultiPoint3D,
    shapely.LineString: LineString3D,
    shapely.MultiLineString: MultiLineString3D,
    shapely.Polygon: Polygon3D,
    shapely.MultiPolygon: MultiPolygon3D,
    # shapely.GeometryCollection: GeometryCollection3D
}

MAPPING = {
    shapely.Point: Point,
    shapely.MultiPoint: MultiPoint,
    shapely.LineString: LineString,
    shapely.MultiLineString: MultiLineString,
    shapely.Polygon: Polygon,
    shapely.MultiPolygon: MultiPolygon,
    # shapely.GeometryCollection: GeometryCollection
}

# NOTE:
# In both CONVERTERS_2D and CONVERTERS_3D, the `mypy` type checker is ignoring
# the Point and Multipoint cases. This is because the `shape.coords` attribute
# is a generic type, whilst the `Point2D` and `MultiPoint2D` classes expect a
# tuple of floats.
# The converters work as expected, as proven by the tests. To make `mypy` happy,
# adding a GuardType is required. This seems a bit out-rageous for justing making
# `mypy` happy.

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
    # case "GeometryCollection":
    #     return GeometryCollection(**shape.__geo_interface__)
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
    # case "GeometryCollection":
    #     return GeometryCollection(**shape.__geo_interface__)
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
    # "GeometryCollection2D",
    # "GeometryCollection3D",
    # "GeometryCollection",
    "MAPPING_2D",
    "MAPPING_3D",
    "MAPPING",
    "convert_shapely_to_geojson_object",
]
