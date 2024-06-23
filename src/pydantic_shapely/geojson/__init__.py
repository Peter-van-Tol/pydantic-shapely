from __future__ import annotations

import typing
from inspect import isclass

from pydantic import create_model

from pydantic_shapely import FeatureBaseModel, GeometryField

from .feature import GeoJsonFeatureBaseModel
from .geometry import MAPPING, MAPPING_2D, MAPPING_3D


def create_geojson_datamodel(
    feature_cls: "FeatureBaseModel",
    geometry_field: str,
) -> GeoJsonFeatureBaseModel[typing.Any]:
    """Creates a Pydantic model for the GeoJSON feature.

    Returns:
        Type: The Pydantic model for the GeoJSON feature.
    """
    geometry_field_info = feature_cls.model_fields[geometry_field]
    metadata = geometry_field_info.metadata
    # Check the behaviour for z-values
    z_values = "allow"
    for meta in metadata:
        if isinstance(meta, GeometryField):
            z_values = meta.z_values
            break
    # Select the correct mapping
    if z_values in ["strip", "forbidden"]:
        mapping = MAPPING_2D
    elif z_values == "required":
        mapping = MAPPING_3D
    else:
        mapping = MAPPING
    # Select the correct field_type
    if isclass(geometry_field_info.annotation):
        # NOTE: the field_type is always an Union. In case the annotation is a
        # class, the Union will be collapsed to the sole field type. At least
        # mypy is happy now.
        field_type = typing.Union[mapping[geometry_field_info.annotation]]
    else:
        field_type = typing.Union[
            tuple(
                mapping[arg] for arg in typing.get_args(geometry_field_info.annotation)
            )
        ]
    # Create the fields and the property model
    fields: typing.Dict[str, typing.Any] = {
        key: (value.annotation, value)
        for key, value in feature_cls.model_fields.items()
        if key != geometry_field
    }
    property_model = create_model(
        str(feature_cls.__name__) + "GeoJsonProperties",
        **fields,
    )
    # Create a model for the GeoJSON feature
    geo_json = create_model(
        feature_cls.__name__ + "GeoJsonFeature",
        __base__=GeoJsonFeatureBaseModel[field_type],
        __doc__=feature_cls.__doc__,
        properties=(property_model, ...),
    )
    return geo_json
