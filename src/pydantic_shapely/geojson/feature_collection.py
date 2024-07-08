from __future__ import annotations

import typing
from inspect import isclass

from pydantic import BaseModel, computed_field
from shapely.ops import unary_union

from pydantic_shapely.base import FeatureBaseModel

from .feature import GeoJsonFeatureBaseModel
from .geometry import bounding_box

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
        cls, features: typing.List[FeatureBaseModel]
    ) -> GeoJsonFeatureCollectionBaseModel:
        """Convert a list of FeatureBaseModel objects to a GeoJSON Feature Collection."""
        # Get the annotation from the features field
        features_field = cls.model_fields["features"]
        if isclass(features_field.annotation):
            if not all(
                isinstance(f, features_field.annotation.ParentDataModel)
                for f in features
            ):
                raise ValueError(
                    f"All features must be of type {features_field.annotation}"
                )
        else:
            requested_types = typing.get_args(features_field.annotation)
            if not all(
                isinstance(f, tuple(t.ParentDataModel for t in requested_types))
                for f in features
            ):
                raise ValueError(
                    f"All features must be of type {','.join([str(t) for t in requested_types])}"
                )
        return cls(features=[typing.cast(S, f.to_geojson_model()) for f in features])


class FeatureCollectionBoundingBoxMixin(BaseModel):
    """
    Mixin class for adding bounding box functionality to a Pydantic model.

    Attributes:
        bbox: The bounding box of the geometry.
    """

    def __init__(self, /, **data: typing.Any) -> None:
        # Remove the bbox field from the data. This is to allow the bbox to be part of the
        # input data (thus complying with the GeoJSON standard), but still using the computed
        # field to determine the bounding box. See also:
        #     https://github.com/pydantic/pydantic/discussions/7782
        if "bbox" in data:
            data.pop("bbox")
        super().__init__(**data)

    @computed_field
    @property
    def bbox(
        self,
    ) -> typing.Union[
        typing.Tuple[float, float, float, float],
        typing.Tuple[float, float, float, float, float, float],
    ]:
        """
        Determine the bounding box of a Shapely geometry. This function will
        either return a 2D or 3D bounding box, depending on the presence of z-values.

        Returns:
            tuple[]: The bounding box of the geometry. Either containing 4 (2D) or
            6 (3D) values.
        """
        return bounding_box(unary_union([geom.to_shapely() for geom in self.features]))
