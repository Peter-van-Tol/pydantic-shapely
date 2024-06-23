import abc
import typing

from pydantic import BaseModel
from shapely.geometry.base import BaseGeometry


class GeometryBase(BaseModel, abc.ABC):
    """Base-class for GeoJSON geometries. This class should not be used directly,
    but is subclassed by the various geometry types. This class exists to provide
    a common interface for all GeoJSON geometries.
    """

    type: str = "LineString"
    coordinates: typing.Any

    @abc.abstractmethod
    def to_shapely(self) -> BaseGeometry:
        pass
