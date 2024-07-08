try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pydantic import Field
from shapely.geometry import Point

from pydantic_shapely import FeatureBaseModel, GeometryField
from pydantic_shapely.geojson.feature_collection import (
    GeoJsonFeatureCollectionBaseModel,
)


class FeatureModel(FeatureBaseModel, geometry_field="point"):
    point: Annotated[Point, GeometryField(), Field(...)]
    name: str = "Hello World"
    answer: int = 42


expected_result = """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0.0,
          0.0
        ]
      },
      "properties": {
        "name": "Hello World",
        "answer": 42
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          1.0,
          1.0
        ]
      },
      "properties": {
        "name": "Hello World",
        "answer": 42
      }
    }
  ]
}"""


def test_create_feature_collection_roundtrip():
    test = GeoJsonFeatureCollectionBaseModel[
        FeatureModel.GeoJsonDataModel
    ].from_feature_models(
        [
            FeatureModel(point=Point(0, 0)),
            FeatureModel(point=Point(1, 1)),
        ]
    )
    assert test.model_dump_json(indent=2) == expected_result
    assert test.to_feature_models() == [
        FeatureModel(point=Point(0, 0)),
        FeatureModel(point=Point(1, 1)),
    ]

expected_result_bbox = """{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          0.0,
          0.0
        ]
      },
      "properties": {
        "name": "Hello World",
        "answer": 42
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          1.0,
          1.0
        ]
      },
      "properties": {
        "name": "Hello World",
        "answer": 42
      }
    },
    bbox: [
      0.0,
      0.0,
      1.0,
      1.0
    ]
  ]
}"""

def test_create_feature_collection_bbox_roundtrip():
    test = GeoJsonFeatureCollectionBaseModel[
        FeatureModel.GeoJsonDataModel
    ].from_feature_models(
        [
            FeatureModel(point=Point(0, 0)),
            FeatureModel(point=Point(1, 1)),
        ]
    )
    assert test.model_dump_json(indent=2) == expected_result
    assert test.to_feature_models() == [
        FeatureModel(point=Point(0, 0)),
        FeatureModel(point=Point(1, 1)),
    ]
