"""
This package provides classes and functions for working with Shapely and GeoJSON data
using Pydantic models.

GeoJSON is a format for encoding geographic data structures using JSON. It represents
geographical features such as points, lines, and polygons, as well as collections of
features.

The classes in this module define Pydantic models that can be used to validate and
serialize/deserialize GeoJSON data. The models represent different types of geometries
such as points, lines, polygons, etc., as well as GeoJSON features.

A basic example is shown below.

.. code-block:: python

    import typing
    from pydantic_shapely.fields import GeometryField, FeatureBaseModel

    from shapely import Point

    class MyModel(FeatureBaseModel):
        geometry: typing.Annotated[
            Point,
            GeometryField()
        ]
        test: str = "Hello World"
        answer: int = 42

    example = MyModel(geometry=Point(0, 0))
    example.model_dump_json()
    # Output: '{"geometry": "POINT (0 0)", "test": "Hello World", "answer": 42}'

    example.model_dump_geojson(ident=2)
    # Output: 
    # '{
    #   "type": "Feature",
    #   "geometry": {
    #     "type": "Point",
    #     "coordinates": [
    #       0,
    #       0
    #     ]
    #   },
    #   "properties": {
    #     "name": "Hello World",
    #     "answer": 42
    #   }
    # }'

These models can also be used in a FastAPI application to serialize/deserialize GeoJSON:

.. code-block:: python

    from fastapi import FastAPI
    from shapely import Point

    from pydantic_shapely import GeometryField FeatureBaseModel


    app = FastAPI()


    class Test(FeatureBaseModel):
        '''Test class for a feature which supports GeoJSON serialization.
        '''
        geometry: typing.Annotated[
            Point,
            GeometryField()
        ]
        name: str = "Hello World"
        answer: int = 42


    @app.get("/")
    async def root() -> Test.GeoJsonDataModel:
        return Test(geometry=Point(0,0)).to_geojson_model()


    @app.post("/")
    async def root(value: Test.GeoJsonDataModel) -> Test:
        return Test.from_geojson_feature(value)

For more information on GeoJSON, see: https://geojson.org/
For more information on Pydantic, see: https://pydantic-docs.helpmanual.io/
"""

from .__version__ import __version__
from .annotations import GeometryField
from .base import FeatureBaseModel

__all__ = [
    # Annotations
    "GeometryField",
    # Base
    "FeatureBaseModel",
]
