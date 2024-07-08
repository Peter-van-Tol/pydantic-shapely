import typing

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

import pytest
from pydantic import BaseModel
from shapely import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from shapely.geometry.base import BaseGeometry

from pydantic_shapely import FeatureBaseModel, GeometryField
from pydantic_shapely.geojson import (
    GeoJsonFeatureBaseModel,
    create_geojson_datamodel,
    geometry,
)

S = typing.TypeVar("S", bound=BaseGeometry)


def test_create_featuremodel():

    class TestModel(FeatureBaseModel):
        geometry: Annotated[Point, GeometryField()]
        a: int
        b: str

    class TestModelGeoJsonProperties(BaseModel):
        a: int
        b: str

    class TestModelGeoJsonFeature(GeoJsonFeatureBaseModel[geometry.Point]):
        properties: TestModelGeoJsonProperties

    assert (
        create_geojson_datamodel(TestModel, "geometry").model_json_schema()
        == TestModelGeoJsonFeature.model_json_schema()
    )


def test_create_featuremodel_union():

    class TestModel(FeatureBaseModel):
        geometry: Annotated[typing.Union[Point, LineString], GeometryField()]
        a: int
        b: str

    class TestModelGeoJsonProperties(BaseModel):
        a: int
        b: str

    class TestModelGeoJsonFeature(
        GeoJsonFeatureBaseModel[typing.Union[geometry.Point, geometry.LineString]]
    ):
        properties: TestModelGeoJsonProperties

    assert (
        create_geojson_datamodel(TestModel, "geometry").model_json_schema()
        == TestModelGeoJsonFeature.model_json_schema()
    )


def test_create_featuremodel_with_boundingbox():

    class TestModel(FeatureBaseModel, bbox="export"):
        geometry: Annotated[Point, GeometryField()]
        a: int
        b: str

    FeatureModel = TestModel.GeoJsonDataModel
    assert hasattr(FeatureModel, "bbox"), True

    test = TestModel(geometry=Point(0, 0), a=1, b="test")
    assert test.to_geojson_model().bbox == (0.0, 0.0, 0.0, 0.0)
