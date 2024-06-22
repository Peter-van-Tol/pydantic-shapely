import typing
from pydantic import BaseModel, Field

from shapely import from_geojson

from pydantic_shapely.geojson.geometry import (
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

from pydantic_shapely.base import FeatureBaseModel

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
            typing.Annotated[
                typing.Type["FeatureBaseModel"],
                Field(
                    default=...,
                    description="The parent Pydantic model from which this class has been derived.",
                ),
            ]
        ]

    def to_feature_model(self) -> "FeatureBaseModel":
        """
        Converts the GeoJSON feature to the FeatureModel this class has been
        based off.
        """
        property_dict = {
            self.ParentDataModel.__geometry_field__: 
                from_geojson(self.geometry.model_dump_json()),
            **self.properties.model_dump(),
        }
        return self.ParentDataModel.model_validate(property_dict)
