
import typing

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

import pytest

from pydantic import create_model

from shapely import (
    GeometryCollection,
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    wkt,
)

from pydantic_shapely.annotations import GeometryField


EXAMPLES_WKT = {
    Point: "POINT(10 20)",
    LineString: "LINESTRING(10 10, 20 20, 21 30)",
    Polygon: "POLYGON((0 0, 0 40, 40 40, 40 0, 0 0))",
    MultiPoint: "MULTIPOINT((0 0), (10 20), (15 20), (30 30))",
    MultiLineString: "MULTILINESTRING((10 10, 20 20), (15 15, 30 15))",
    MultiPolygon: "MULTIPOLYGON("
            "((10 10, 10 20, 20 20, 20 15, 10 10)),"
            "((60 60, 70 70, 80 60, 60 60 ))"
        ")",
    GeometryCollection: "GEOMETRYCOLLECTION("
            "POINT (10 10), "
            "POINT (30 30), "
            "LINESTRING (15 15, 20 20)"
        ")",
}

EXAMPLES_OBJ_2D = {
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


EXAMPLES_OBJ_3D = {
    Point: Point(10, 20, 1),
    LineString: LineString([(10, 10, 1), (20, 20, 1), (21, 30, 1)]),
    Polygon: Polygon([(0, 0, 1), (0, 40, 1), (40, 40, 1), (40, 0, 1), (0, 0, 1)],),
    MultiPoint: MultiPoint([Point(0, 0, 1), Point(10, 20, 1), Point(15, 20, 1), Point(30, 30, 1)]),
    MultiLineString: MultiLineString(
        [
            LineString([(10, 10, 1), (20, 20, 1)]),
            LineString([(15, 15, 1), (30, 15, 1)])
        ]
    ),
    MultiPolygon: MultiPolygon(
        [
            Polygon([(10, 10, 1), (10, 20, 1), (20, 20, 1), (20, 15, 1), (10, 10, 1)], ),
            Polygon([(60, 60, 1), (70, 70, 1), (80, 60, 1), (60, 60, 1)])
        ]
    ),
    GeometryCollection: GeometryCollection(
        [
            Point(10, 10, 1),
            Point(30, 30, 1),
            LineString([(15, 15, 1), (20, 20, 1)])
        ]
    )
}

test_data_correct_geom_type = {
    "Point": MultiPoint,
    "LineString": MultiLineString,
    "Polygon": MultiPolygon,
    "MultiPoint": MultiPoint,
    "MultiLineString": MultiLineString,
    "MultiPolygon": MultiPolygon,
    "GeometryCollection": GeometryCollection
}

@pytest.mark.parametrize(
    "geom_type", test_data_correct_geom_type.values(), ids=test_data_correct_geom_type.keys()
)
def test_annotation_correct_geom_type_roundtrip(
    geom_type
):
    
    model = create_model(
        f"{geom_type.__name__}TestModel",
        geometry=(Annotated[geom_type, GeometryField()], ...)
    )

    instance = model(geometry=EXAMPLES_OBJ_2D[geom_type])
    assert model.model_validate_json(instance.model_dump_json()) == instance


@pytest.mark.parametrize(
    "geom_type", test_data_correct_geom_type.values(), ids=test_data_correct_geom_type.keys()
)
def test_annotation_correct_geom_type_union_roundtrip(
    geom_type
):
    
    model = create_model(
        f"{geom_type.__name__}TestModel",
        geometry=(Annotated[typing.Union[geom_type, Point], GeometryField()], ...)
    )

    instance = model(geometry=EXAMPLES_OBJ_2D[geom_type])
    assert model.model_validate_json(instance.model_dump_json()) == instance


test_data_wrong_data_type = {
    "Point -> LineString":
    (Point, EXAMPLES_OBJ_2D[LineString]),
    "Point -> Polygon":
    (Point, EXAMPLES_OBJ_2D[Polygon]),
    "Point -> MultiPoint":
    (Point, EXAMPLES_OBJ_2D[MultiPoint]),
    "Point -> MultiLineString":
    (Point, EXAMPLES_OBJ_2D[MultiLineString]),
    "Point -> MultiPolygon":
    (Point, EXAMPLES_OBJ_2D[MultiPolygon]),
    "Point -> GeometryCollection":
    (Point, EXAMPLES_OBJ_2D[GeometryCollection]),
    "LineString -> Point":
    (LineString, EXAMPLES_OBJ_2D[Point]),
    "LineString -> Polygon":
    (LineString, EXAMPLES_OBJ_2D[Polygon]),
    "LineString -> MultiPoint":
    (LineString, EXAMPLES_OBJ_2D[MultiPoint]),
    "LineString -> MultiLineString":
    (LineString, EXAMPLES_OBJ_2D[MultiLineString]),
    "LineString -> MultiPolygon":
    (LineString, EXAMPLES_OBJ_2D[MultiPolygon]),
    "LineString -> GeometryCollection":
    (LineString, EXAMPLES_OBJ_2D[GeometryCollection]),
    "Polygon -> Point":
    (Polygon, EXAMPLES_OBJ_2D[Point]),
    "Polygon -> LineString":
    (Polygon, EXAMPLES_OBJ_2D[LineString]),
    "Polygon -> MultiPoint":
    (Polygon, EXAMPLES_OBJ_2D[MultiPoint]),
    "Polygon -> MultiLineString":
    (Polygon, EXAMPLES_OBJ_2D[MultiLineString]),
    "Polygon -> MultiPolygon":
    (Polygon, EXAMPLES_OBJ_2D[MultiPolygon]),
    "Polygon -> GeometryCollection":
    (Polygon, EXAMPLES_OBJ_2D[GeometryCollection]),
    "MultiPoint -> Point":
    (MultiPoint, EXAMPLES_OBJ_2D[Point]),
    "MultiPoint -> LineString":
    (MultiPoint, EXAMPLES_OBJ_2D[LineString]),
    "MultiPoint -> Polygon":
    (MultiPoint, EXAMPLES_OBJ_2D[Polygon]),
    "MultiPoint -> MultiLineString":
    (MultiPoint, EXAMPLES_OBJ_2D[MultiLineString]),
    "MultiPoint -> MultiPolygon":
    (MultiPoint, EXAMPLES_OBJ_2D[MultiPolygon]),
    "MultiPoint -> GeometryCollection":
    (MultiPoint, EXAMPLES_OBJ_2D[GeometryCollection]),
    "MultiLineString -> Point":
    (MultiLineString, EXAMPLES_OBJ_2D[Point]),
    "MultiLineString -> LineString":
    (MultiLineString, EXAMPLES_OBJ_2D[LineString]),
    "MultiLineString -> Polygon":
    (MultiLineString, EXAMPLES_OBJ_2D[Polygon]),
    "MultiLineString -> MultiPoint":
    (MultiLineString, EXAMPLES_OBJ_2D[MultiPoint]),
    "MultiLineString -> MultiPolygon":
    (MultiLineString, EXAMPLES_OBJ_2D[MultiPolygon]),
    "MultiLineString -> GeometryCollection":
    (MultiLineString, EXAMPLES_OBJ_2D[GeometryCollection]),
    "MultiPolygon -> Point":
    (MultiPolygon, EXAMPLES_OBJ_2D[Point]),
    "MultiPolygon -> LineString":
    (MultiPolygon, EXAMPLES_OBJ_2D[LineString]),
    "MultiPolygon -> Polygon":
    (MultiPolygon, EXAMPLES_OBJ_2D[Polygon]),
    "MultiPolygon -> MultiPoint":
    (MultiPolygon, EXAMPLES_OBJ_2D[MultiPoint]),
    "MultiPolygon -> MultiLineString":
    (MultiPolygon, EXAMPLES_OBJ_2D[MultiLineString]),
    "MultiPolygon -> GeometryCollection":
    (MultiPolygon, EXAMPLES_OBJ_2D[GeometryCollection]),
    "GeometryCollection -> Point":
    (GeometryCollection, EXAMPLES_OBJ_2D[Point]),
    "GeometryCollection -> LineString":
    (GeometryCollection, EXAMPLES_OBJ_2D[LineString]),
    "GeometryCollection -> Polygon":
    (GeometryCollection, EXAMPLES_OBJ_2D[Polygon]),
    "GeometryCollection -> MultiPoint":
    (GeometryCollection, EXAMPLES_OBJ_2D[MultiPoint]),
    "GeometryCollection -> MultiLineString":
    (GeometryCollection, EXAMPLES_OBJ_2D[MultiLineString]),
    "GeometryCollection -> MultiPolygon":
    (GeometryCollection, EXAMPLES_OBJ_2D[MultiPolygon]),
}

@pytest.mark.parametrize(
    "geom_type, geom", test_data_wrong_data_type.values(), ids=test_data_wrong_data_type.keys()
)
def test_annotation_wrong_geom_type(
    geom_type, geom
):
    
    model = create_model(
        f"{geom_type.__name__}TestModel",
        geometry=(Annotated[geom_type, GeometryField()], ...)
    )

    with pytest.raises(ValueError):
        model(geometry=geom)


test_error_no_shapely_geometry = {
    "String": str,
    "Union[str, Point]": typing.Union[str, Point],
    "Union[str, int]": typing.Union[str, int],
}

@pytest.mark.parametrize(
    "type_, ", test_error_no_shapely_geometry.values(), ids=test_error_no_shapely_geometry.keys()
)
def test_no_shapely_geometry(type_: typing.Type):
    
    with pytest.raises(TypeError):
        create_model(
            "NoGeomTypeTestModel",
            geometry=(Annotated[type_, GeometryField()], ...)
        )


test_z_values = {
    "Point":
    (Point, EXAMPLES_OBJ_3D[Point], EXAMPLES_OBJ_2D[Point]),
    "LineString":
    (LineString, EXAMPLES_OBJ_3D[LineString], EXAMPLES_OBJ_2D[LineString]),
    "Polygon":
    (Polygon, EXAMPLES_OBJ_3D[Polygon], EXAMPLES_OBJ_2D[Polygon]),
    "MultiPoint":
    (MultiPoint, EXAMPLES_OBJ_3D[MultiPoint], EXAMPLES_OBJ_2D[MultiPoint]),
    "MultiLineString":
    (MultiLineString, EXAMPLES_OBJ_3D[MultiLineString], EXAMPLES_OBJ_2D[MultiLineString]),
    "MultiPolygon":
    (MultiPolygon, EXAMPLES_OBJ_3D[MultiPolygon], EXAMPLES_OBJ_2D[MultiPolygon]),
    "GeometryCollection":
    (GeometryCollection, EXAMPLES_OBJ_3D[GeometryCollection], EXAMPLES_OBJ_2D[GeometryCollection]),
}

@pytest.mark.parametrize(
    "geom_type, geom, _", test_z_values.values(), ids=test_z_values.keys()
)
def test_z_values_forbid(geom_type, geom, _):

    model = create_model(
        "NoGeomTypeTestModel",
        geometry=(Annotated[geom_type, GeometryField(z_values="forbid")], ...)
    )

    with pytest.raises(ValueError):
        model(geometry=geom)

@pytest.mark.parametrize(
    "geom_type, _, geom", test_z_values.values(), ids=test_z_values.keys()
)
def test_z_values_required(geom_type, geom, _):

    model = create_model(
        "NoGeomTypeTestModel",
        geometry=(Annotated[geom_type, GeometryField(z_values="required")], ...)
    )

    with pytest.raises(ValueError):
        model(geometry=geom)

@pytest.mark.parametrize(
    "geom_type, geom, expected", test_z_values.values(), ids=test_z_values.keys()
)
def test_z_values_strip(geom_type, geom, expected):

    model = create_model(
        "NoGeomTypeTestModel",
        geometry=(Annotated[geom_type, GeometryField(z_values="strip")], ...)
    )

    test = model(geometry=geom)
    assert test.geometry == expected
