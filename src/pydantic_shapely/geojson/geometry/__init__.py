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

from . import _base
from .point import Point2D, Point3D, Point
from .multipoint import MultiPoint2D, MultiPoint3D, MultiPoint
from .linestring import LineString2D, LineString3D, LineString
from .multilinestring import MultiLineString2D, MultiLineString3D, MultiLineString
from .polygon import Polygon2D, Polygon3D, Polygon
from .multipolygon import MultiPolygon2D, MultiPolygon3D, MultiPolygon

import shapely

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
    mapping = MAPPING_2D
    if shape.has_z:
        mapping = MAPPING_3D
    match shape.geom_type:
        case "Point":
            return Point(coordinates=tuple(shape.coords[0]))
        case "MultiPoint":
            return MultiPoint(coordinates=[tuple(geom.coords[0]) for geom in shape.geoms])
        case "LineString":
            return LineString(coordinates=shape.coords)
        case "MultiLineString":
            return MultiLineString(coordinates=[geom.coords for geom in shape.geoms])
        case "Polygon":
            return Polygon(coordinates=[
                shape.exterior.coords,
                *[hole.coords for hole in shape.interiors]
            ])
        case "MultiPolygon":
            return MultiPolygon(
                coordinates=[
                    [
                        geom.exterior.coords,
                        *[hole.coords for hole in geom.interiors]
                    ]
                    for geom in shape.geoms
                ]
            )
        # case "GeometryCollection":
        #     return GeometryCollection(**shape.__geo_interface__)
        case _:
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
    "convert_shapely_to_geojson_object"
]
