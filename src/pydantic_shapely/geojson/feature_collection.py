from __future__ import annotations
import typing
from inspect import isclass
from pydantic import BaseModel

from pydantic_shapely.base import FeatureBaseModel
from .feature import GeoJsonFeatureBaseModel


S = typing.TypeVar("S", bound=GeoJsonFeatureBaseModel)


class GeoJsonFeatureCollectionBaseModel(BaseModel, typing.Generic[S]):
    """Base class for GeoJSON Feature Collection. This class should not be used directly,
    but is subclassed by the various geometry types.
    
    Example usage:
    
    .. code-block:: python

        import typing
        from pydantic_shapely import FeatureBaseModel, GeometryField
        from pydantic_shapely.geojson import GeoJsonFeatureCollectionBaseModel
        from shapely import Point

        class TestModel(FeatureBaseModel):
            '''Test class for a feature which supports GeoJSON serialization.
            '''
            geometry: Annotated[
                typing.Point,
                GeometryField()
            ]
            name: str = "Hello World"
            answer: int = 42

        TestFeatureCollection = GeoJsonFeatureCollectionBaseModel[TestModel.GeoJsonDataModel]

        test = TestFeatureCollection(
            features=[
                TestModel(geometry=Point(0, 0)).to_geojson_model(),
                TestModel(geometry=Point(1, 1)).to_geojson_model(),
            ]

        print(test.model_dump_json(indent=2))
        # RESULT:
        # {
        #   "type": "FeatureCollection",
        #   "features": [
        #     {
        #       "type": "Feature",
        #       "geometry": {
        #         "type": "Point",
        #         "coordinates": [
        #           0.0,
        #           0.0
        #         ]
        #       },
        #       "properties": {
        #         "name": "Hello World",
        #         "answer": 42
        #       }
        #     },
        #     {
        #       "type": "Feature",
        #       "geometry": {
        #         "type": "Point",
        #         "coordinates": [
        #           1.0,
        #           1.0
        #         ]
        #       },
        #       "properties": {
        #         "name": "Hello World",
        #         "answer": 42
        #       }
        #     }
        #   ]
        # }
    """

    type: typing.Literal["FeatureCollection"] = "FeatureCollection"
    features: typing.List[S]

    def to_feature_models(self) -> typing.List[FeatureBaseModel]:
        """Convert the GeoJSON Feature Collection to a list of FeatureBaseModel
        (or better: its sub-classes) objects."""
        return [feature.to_feature_model() for feature in self.features]
    
    @classmethod
    def from_feature_models(
            cls,
            features: typing.List[FeatureBaseModel]
        ) -> GeoJsonFeatureCollectionBaseModel:
        """Convert a list of FeatureBaseModel objects to a GeoJSON Feature Collection."""
        # Get the annotation from the features field
        features_field = cls.model_fields["features"]
        if isclass(features_field.annotation):
            if not all(isinstance(f, features_field.annotation.ParentDataModel) for f in features):
                raise ValueError(f"All features must be of type {features_field.annotation}")
        else:
            requested_types = typing.get_args(features_field.annotation)
            if not all(isinstance(f, tuple(t.ParentDataModel for t in requested_types)) for f in features):
                raise ValueError(
                    f"All features must be of type {','.join([str(t) for t in requested_types])}"
                )
        return cls(features=[typing.cast(S, f.to_geojson_model()) for f in features])
