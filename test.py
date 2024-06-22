import typing
from pydantic import Field
from shapely import Point

from pydantic_shapely import FeatureBaseModel, GeometryField


class PointModel(FeatureBaseModel):
    geometry: typing.Annotated[
        Point,
        GeometryField(),
        Field(),
    ]

print(PointModel)