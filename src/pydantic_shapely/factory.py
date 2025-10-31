import typing

from inspect import isclass

from pydantic import BaseModel, Field
from shapely.geometry.base import BaseGeometry

from pydantic_shapely.geojson import create_geojson_datamodel


def create_geojson_feature_class(
    model: typing.Type[BaseModel],
    /,
    geometry_field_name: str = "geometry",
    # include_bbox: bool = False,
) -> typing.Type[BaseModel]:
    
    # Check whether the geometry field exists in the class
    if geometry_field_name not in model.model_fields:
        raise ValueError(
            f"Field '{geometry_field_name}' not found in class '{model.__name__}'."
        )
    
    # Create the GeoJSON data model
    geometry_field = model.model_fields[geometry_field_name]
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
    return create_geojson_datamodel(model, geometry_field)
