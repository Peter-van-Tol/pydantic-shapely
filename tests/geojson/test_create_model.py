
import typing
import pytest

from pydantic import BaseModel
from pydantic_shapely import FeatureBaseModel, GeometryField
from pydantic_shapely.geojson import GeoJsonFeatureBaseModel, create_geojson_datamodel, geometry
from shapely import (
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
)
from shapely.geometry.base import BaseGeometry

S = typing.TypeVar("S", bound=BaseGeometry)


def test_create_featuremodel():

    class TestModel(FeatureBaseModel):
        geometry: typing.Annotated[Point, GeometryField()]
        a: int
        b: str

    class TestModelGeoJsonProperties(BaseModel):
        a: int
        b: str

    class TestModelGeoJsonFeature(GeoJsonFeatureBaseModel[geometry.Point]):
        properties: TestModelGeoJsonProperties


    assert create_geojson_datamodel(TestModel, "geometry").model_json_schema() == TestModelGeoJsonFeature.model_json_schema()


def test_create_featuremodel_union():

    class TestModel(FeatureBaseModel):
        geometry: typing.Annotated[typing.Union[Point, LineString], GeometryField()]
        a: int
        b: str

    class TestModelGeoJsonProperties(BaseModel):
        a: int
        b: str

    class TestModelGeoJsonFeature(GeoJsonFeatureBaseModel[typing.Union[geometry.Point, geometry.LineString]]):
        properties: TestModelGeoJsonProperties


    assert create_geojson_datamodel(TestModel, "geometry").model_json_schema() == TestModelGeoJsonFeature.model_json_schema()
