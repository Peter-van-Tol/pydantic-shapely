
import pytest

from pydantic_shapely.geojson.geometry import convert_shapely_to_geojson_object
from shapely import (
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
)



EXAMPLES_OBJ = {
    Point: Point(10, 20),
    LineString: LineString([(10, 10), (20, 20), (21, 30)]),
    Polygon: Polygon([(0, 0), (0, 40), (40, 40), (40, 0), (0, 0)],),
    MultiPoint: MultiPoint([Point(0, 0), Point(10, 20), Point(15, 20), Point(30, 30)]),
    MultiLineString: MultiLineString(
        [
            LineString([(10, 10), (20, 20)]),
            LineString([(15, 15), (30, 15)])
        ]
    ),
    MultiPolygon: MultiPolygon(
        [
            Polygon([(10, 10), (10, 20), (20, 20), (20, 15), (10, 10)], ),
            Polygon([(60, 60), (70, 70), (80, 60), (60, 60)])
        ]
    ),
    GeometryCollection: GeometryCollection(
        [
            Point(10, 10),
            Point(30, 30),
            LineString([(15, 15), (20, 20)])
        ]
    )
}

test_geometry = {
    "Point": Point,
    "LineString": MultiLineString,
    "Polygon": Polygon,
    "MultiPoint": MultiPoint,
    "MultiLineString": MultiLineString,
    "MultiPolygon": MultiPolygon,
    # "GeometryCollection": GeometryCollection
}

@pytest.mark.parametrize(
    "shape_type, ",
    test_geometry.values(),
    ids=test_geometry.keys())
def test_geometry(shape_type):
    shape = EXAMPLES_OBJ[shape_type]
    # assert convert_shapely_to_geojson_object(shape).model_dump() == {"type": "Point", "coordinates": (0, 0)}
    assert convert_shapely_to_geojson_object(shape).to_shapely() == shape
