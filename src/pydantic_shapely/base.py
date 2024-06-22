from __future__ import annotations

from inspect import isclass
import json
import typing


from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo
from shapely import (
    Point,
    LineString,
    from_geojson,
    to_geojson
)
from shapely.geometry.base import BaseGeometry

# For static type checking, whilst preventing circular import
if typing.TYPE_CHECKING:
    from pydantic_shapely.geojson.feature import GeoJsonFeatureBaseModel


class FeatureBaseModel(BaseModel):
    """
    Represents a Pydantic model for a GeoJSON feature.

    Attributes:
        geometry: The geometry of the feature.

    Class Attributes:
        GeoJsonDataModel: The Pydantic model for the GeoJSON feature, used in FastApi.

    Methods:
        from_geojson_feature: Generates a model from a GeoJSON data model representation.
        as_geojson_feature: Generates a GeoJSON data model representation of the model.
        model_dump_geojson: Generates a GeoJSON representation of the model.
        model_validate_geojson: Validate the given JSON data against the Pydantic model.
    """
    __geometry_field__: typing.ClassVar[str] = "geometry"
        
    if typing.TYPE_CHECKING:
        # Here we provide annotations for the attributes of FeatureModel.
        # These are populated by the __pydantic_init_subclass__, which is why
        # this section is in a `TYPE_CHECKING` block.
        GeoJsonDataModel: typing.ClassVar[  # pylint: disable=invalid-name
            typing.Annotated[
                typing.Type,
                Field(
                    default=...,
                    description="The Pydantic model for the GeoJSON feature.",
                ),
            ]
        ]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        # Update the geometry field if it is defined in kwargs
        if "geometry_field" in kwargs:
            cls.__geometry_field__ = kwargs.pop("geometry_field")
        # Run init subclass from parent classes
        super().__init_subclass__(**kwargs)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        # Deferred import to prevent circular import
        from pydantic_shapely.geojson import create_geojson_datamodel
        # Run init subclass from parent classes
        super().__pydantic_init_subclass__(**kwargs)
        # Check whether the geometry field exists in the class
        if cls.__geometry_field__ not in cls.model_fields:
            raise ValueError(
                f"Field '{cls.__geometry_field__}' not found in class '{cls.__name__}'."
            )
        # Check whether the geometry field is a Shapely geometry
        geometry_field = cls.model_fields[cls.__geometry_field__]
        if isclass(geometry_field.annotation):
            if not issubclass(geometry_field.annotation, BaseGeometry):
                raise TypeError(
                    "GeometryField annotation can only be applied to Shapely geometries."
                )
        else:
            requested_types = typing.get_args(geometry_field.annotation)
            if not all(issubclass(t, BaseGeometry) for t in requested_types):
                raise TypeError(
                    "GeometryField annotation can only be applied to Shapely geometries. All types "
                    "in the Union must be a Shapely geometry."
                )
        # Create the GeoJsonDataModel
        cls.GeoJsonDataModel = create_geojson_datamodel(cls, cls.__geometry_field__)

    def to_geojson_model(self) -> "GeoJsonFeatureBaseModel":
        """
        Converts the GeoJSON feature to the FeatureModel this class has been
        based off.
        """
        # Cast the model to the GeoJsonDataModel
        return self.GeoJsonDataModel(
            type="Feature",
            geometry=json.loads(to_geojson(getattr(self, self.__geometry_field__))),
            properties=self.model_dump(exclude={"geometry"}),
        )
    
    def model_dump_geojson(self) -> str:
        """
        Dumps the model to a GeoJson string.
        """
        return self.to_geojson_model().model_dump_json()
