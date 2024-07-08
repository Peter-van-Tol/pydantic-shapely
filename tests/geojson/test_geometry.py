import pytest
from shapely import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from pydantic_shapely.geojson.geometry import (
    bounding_box,
    convert_shapely_to_geojson_object,
)

EXAMPLES_OBJ_2D = {
    Point: Point(10, 20),
    LineString: LineString([(10, 10), (20, 20), (21, 30)]),
    Polygon: Polygon(
        [(0, 0), (0, 40), (40, 40), (40, 0), (0, 0)],
    ),
    MultiPoint: MultiPoint([Point(0, 0), Point(10, 20), Point(15, 20), Point(30, 30)]),
    MultiLineString: MultiLineString(
        [LineString([(10, 10), (20, 20)]), LineString([(15, 15), (30, 15)])]
    ),
    MultiPolygon: MultiPolygon(
        [
            Polygon(
                [(10, 10), (10, 20), (20, 20), (20, 15), (10, 10)],
            ),
            Polygon([(60, 60), (70, 70), (80, 60), (60, 60)]),
        ]
    ),
    GeometryCollection: GeometryCollection(
        [
            Point(10, 10),
            LineString([(15, 15), (20, 20)]),
            Polygon([(60, 60), (70, 70), (80, 60), (60, 60)]),
        ]
    ),
}
EXAMPLES_OBJ_3D = {
    Point: Point(10, 20, 3),
    LineString: LineString([(10, 10, 1), (20, 20, 2), (21, 30, 3)]),
    Polygon: Polygon(
        [(0, 0, 0), (0, 40, 1), (40, 40, 2), (40, 0, 3), (0, 0, 0)],
    ),
    MultiPoint: MultiPoint([Point(0, 0, -1), Point(10, 20, 0), Point(15, 20, 1), Point(30, 30, 2)]),
    MultiLineString: MultiLineString(
        [LineString([(10, 10, 0.0), (20, 20, 2.0)]), LineString([(15, 15, 1.5), (30, 15, 3.5)])]
    ),
    MultiPolygon: MultiPolygon(
        [
            Polygon(
                [(10, 10, 0.0), (10, 20, 0.0), (20, 20, 0.0), (20, 15, 0.0), (10, 10, 0.0)],
            ),
            Polygon([(60, 60, 1.0), (70, 70, 1.0), (80, 60, 1.0), (60, 60, 1.0)]),
        ]
    ),
    GeometryCollection: GeometryCollection(
        [
            Point(10, 10, 3.0),
            LineString([(15, 15, 1.0), (20, 20, 5.0)]),
            Polygon([(60, 60, -1.0), (70, 70, -1.0), (80, 60, -1.0), (60, 60, -1.0)]),
        ]
    ),
}

test_geometry = {
    "Point": Point,
    "LineString": LineString,
    "Polygon": Polygon,
    "MultiPoint": MultiPoint,
    "MultiLineString": MultiLineString,
    "MultiPolygon": MultiPolygon,
    "GeometryCollection": GeometryCollection,
}


@pytest.mark.parametrize(
    "shape_type, ", test_geometry.values(), ids=test_geometry.keys()
)
def test_geometry(shape_type):
    shape = EXAMPLES_OBJ_2D[shape_type]
    # assert convert_shapely_to_geojson_object(shape).model_dump() == {"type": "Point", "coordinates": (0, 0)}
    assert convert_shapely_to_geojson_object(shape).to_shapely() == shape


testdata_bounding_box = {
    "Point2D": (Point, "2D", (10.0, 20.0, 10.0, 20.0)),
    "LineString2D": (LineString, "2D", (10.0, 10.0, 21.0, 30.0)),
    "Polygon2D": (Polygon, "2D", (0.0, 0.0, 40.0, 40.0)),
    "MultiPoint2D": (MultiPoint, "2D", (0.0, 0.0, 30.0, 30.0)),
    "MultiLineString2D": (MultiLineString, "2D", (10.0, 10.0, 30.0, 20.0)),
    "MultiPolygon2D": (MultiPolygon, "2D", (10.0, 10.0, 80.0, 70.0)),
    "GeometryCollection2D": (GeometryCollection, "2D", (10.0, 10.0, 80.0, 70.0)),
    "Point3D": (Point, "3D", (10.0, 20.0, 3.0, 10.0, 20.0, 3.0)),
    "LineString3D": (LineString, "3D", (10.0, 10.0, 1.0, 21.0, 30.0, 3.0)),
    "Polygon3D": (Polygon, "3D", (0.0, 0.0, 0.0, 40.0, 40.0, 3.0)),
    "MultiPoint3D": (MultiPoint, "3D", (0.0, 0.0, -1.0, 30.0, 30.0, 2.0)),
    "MultiLineString3D": (MultiLineString, "3D", (10.0, 10.0, 0.0, 30.0, 20.0, 3.5)),
    "MultiPolygon3D": (MultiPolygon, "3D", (10.0, 10.0, 0.0, 80.0, 70.0, 1.0)),
    "GeometryCollection3D": (GeometryCollection, "3D", (10.0, 10.0, -1.0, 80.0, 70.0, 5.0)),
}



@pytest.mark.parametrize(
    "shape_type, dim, expected_result",
    testdata_bounding_box.values(),
    ids=testdata_bounding_box.keys(),
)
def test_bounding_box(shape_type, dim, expected_result):
    if dim == "2D":
        shape = EXAMPLES_OBJ_2D[shape_type]
    else:
        shape = EXAMPLES_OBJ_3D[shape_type]
    assert bounding_box(shape) == expected_result
