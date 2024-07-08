from __future__ import annotations

import typing

try:
    from typing import Annotated
except ImportError:
    # This import is required in Python 3.8
    from typing_extensions import Annotated  # type: ignore

from pydantic import BaseModel, Field, computed_field
from shapely import from_geojson

from pydantic_shapely.base import FeatureBaseModel
from pydantic_shapely.geojson.geometry import (  # GeometryCollection2D,; GeometryCollection3D,; GeometryCollection,
    LineString,
    LineString2D,
    LineString3D,
    MultiLineString,
    MultiLineString2D,
    MultiLineString3D,
    MultiPoint,
    MultiPoint2D,
    MultiPoint3D,
    MultiPolygon,
    MultiPolygon2D,
    MultiPolygon3D,
    Point,
    Point2D,
    Point3D,
    Polygon,
    Polygon2D,
    Polygon3D,
    bounding_box
)

S = typing.TypeVar(
    "S",
    Point2D,
    Point3D,
    Point,
    MultiPoint2D,
    MultiPoint3D,
    MultiPoint,
    LineString2D,
    LineString3D,
    LineString,
    MultiLineString2D,
    MultiLineString3D,
    MultiLineString,
    Polygon2D,
    Polygon3D,
    Polygon,
    MultiPolygon2D,
    MultiPolygon3D,
    MultiPolygon,
    # GeometryCollection2D,
    # GeometryCollection3D,
    # GeometryCollection,
)


class GeoJsonFeatureBaseModel(BaseModel, typing.Generic[S]):
    """Base class for GeoJSON point features."""

    type: typing.Literal["Feature"]
    geometry: S
    properties: BaseModel

    if typing.TYPE_CHECKING:
        # Here we provide annotations for the attributes of GeoJsonFeatureBaseModel.
        # These are populated by the __pydantic_init_subclass__ of the model on which
        # this model is based on, which is why this section is in a `TYPE_CHECKING` block.
        ParentDataModel: typing.ClassVar[  # pylint: disable=invalid-name
            Annotated[
                typing.Type["FeatureBaseModel"],
                Field(
                    default=...,
                    description="The parent Pydantic model from which this class has been derived.",
                ),
            ]
        ]

    def to_feature_model(self) -> FeatureBaseModel:
        """
        Converts the GeoJSON feature to the FeatureModel this class has been
        based off.
        """
        property_dict = {
            self.ParentDataModel.__geometry_field__: from_geojson(
                self.geometry.model_dump_json()
            ),
            **self.properties.model_dump(),
        }
        return self.ParentDataModel.model_validate(property_dict)


class FeatureBoundingBoxMixin(BaseModel):
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
        if 'bbox' in data:
            data.pop('bbox')
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
        return bounding_box(self.geometry.to_shapely())
