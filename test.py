import typing

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from pydantic import Field
from shapely import Point

from pydantic_shapely import FeatureBaseModel, GeometryField


class PointModel(FeatureBaseModel):
    geometry: Annotated[
        Point,
        GeometryField(),
        Field(),
    ]

print(PointModel)