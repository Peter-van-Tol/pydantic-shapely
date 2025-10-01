import dataclasses
import typing
from inspect import isclass

import shapely
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from shapely.geometry.base import BaseGeometry

# Example WKT strings for different geometry types.
# Source: https://www.ibm.com/docs/en/i/7.4?topic=formats-well-known-text-wkt-format
EXAMPLES = {
    shapely.Point: "POINT(10 20)",
    shapely.LineString: "LINESTRING(10 10, 20 20, 21 30)",
    shapely.Polygon: "POLYGON((0 0, 0 40, 40 40, 40 0, 0 0))",
    shapely.MultiPoint: "MULTIPOINT((0 0), (10 20), (15 20), (30 30))",
    shapely.MultiLineString: "MULTILINESTRING((10 10, 20 20), (15 15, 30 15))",
    shapely.MultiPolygon: "MULTIPOLYGON("
    "((10 10, 10 20, 20 20, 20 15, 10 10)),"
    "((60 60, 70 70, 80 60, 60 60 ))"
    ")",
    shapely.GeometryCollection: "GEOMETRYCOLLECTION("
    "POINT (10 10), "
    "POINT (30 30), "
    "LINESTRING (15 15, 20 20)"
    ")",
}
EXAMPLES3D = {
    shapely.Point: "POINT Z (10 20 30)",
    shapely.LineString: "LINESTRING Z (10 10 30, 20 20 30, 21 30 30)",
    shapely.Polygon: "POLYGON Z ((0 0 30, 0 40 30, 40 40 30, 40 0 30, 0 0 30))",
    shapely.MultiPoint: "MULTIPOINT Z ((0 0 30), (10 20 30), (15 20 30), (30 30 30))",
    shapely.MultiLineString: "MULTILINESTRING Z ((10 10 30, 20 20 30), (15 15 30, 30 15 30))",
    shapely.MultiPolygon: "MULTIPOLYGON Z("
    "((10 10 30, 10 20 30, 20 20 30, 20 15 30, 10 10 30)),"
    "((60 60 30, 70 70 30, 80 60 30, 60 60 30))"
    ")",
    shapely.GeometryCollection: "GEOMETRYCOLLECTION("
    "POINT Z (10 10 30), "
    "POINT Z (30 30 30), "
    "LINESTRING Z (15 15 30, 20 20 30)"
    ")",
}

# The ZValues describe how the geometry handles z-values:
# - forbidden: the geometry must be strictly 2-dimensional. A ValueError will
#   raised when a shape with z-values is provided.
# - strip: the geometry may have z-values. These values will be stripped from
#   then geometry in the validation process. The resulting shape will be
#   2-dimensional in all cases.
# - allow: both 2- and 3-dimensional values are allowed. During the validation
#   process the data is not altered. This is the default behavior.
# - required: the geometry must be strictly 2-dimensional. A ValueError will
#   raised when a shape without z-values is provided.
ZValues = typing.Literal["required", "allow", "strip", "forbidden"]


@dataclasses.dataclass
class GeometryField:
    """
    Annotation for geometry fields in Pydantic models. Provides methods for
    validating and serializing geometry values.

    Attributes:
        __geometry_type__: Returns the geometry type associated with the field.

    Methods:
        validate: Validates the geometry value.
        serialize: Serializes the geometry value.
        __get_pydantic_core_schema__: Generates the core schema for the field.
        __get_pydantic_json_schema__: Generates the JSON schema for the field.
    """

    if typing.TYPE_CHECKING:
        # Type variable representing the geometry type.
        __geometry_type__: typing.Type[BaseGeometry]  # pragma: no cover

    z_values: ZValues = "allow"

    def _validate_z_values(self, value: BaseGeometry) -> BaseGeometry:

        if self.z_values == "forbid" and value.has_z:
            raise ValueError(
                "The supplied geometry has z-values. The field does not allow this."
            )
        if self.z_values == "required" and not value.has_z:
            raise ValueError(
                "The supplied geometry has no z-values. The field does require this."
            )
        if self.z_values == "strip":
            return shapely.force_2d(value)
        # Default behavior: return the data unmodified
        return value

    def validate(self, value) -> BaseGeometry:
        """
        Validates the input value and returns a validated geometry object.

        Args:
            value: The input value to be validated.

        Returns:
            A validated geometry object.

        Raises:
            ValueError: If the input value is not a valid WKT-string or if the
            supplied geometry is not of the expected type.
        """
        # - Test whether user supplied the geometry directly
        if isinstance(value, BaseGeometry):
            geometry = value
        # - convert a (WKT-) string to a object
        elif isinstance(value, str):
            try:
                geometry: BaseGeometry = shapely.from_wkt(value)
            except Exception as ex:
                raise ValueError("Supplied string is not a valid WKT-string") from ex
        # - last resort, pass the value to the constructor of shapely
        else:
            # - get the types that are supported by the field
            if isclass(self.__geometry_type__):
                supported_types = [self.__geometry_type__]
            else:
                supported_types = typing.get_args(self.__geometry_type__)
            # - for each type, check we can instantiate the geometry with the value
            #   from the field
            for t in supported_types:
                try:
                    geometry = t(value)
                    break
                except Exception:
                    pass
            else:
                raise ValueError(
                    f"Supplied value ({value}) cannot be converted to a valid geometry."
                )

        if isclass(self.__geometry_type__):
            # The geometry type is a class, check if the geometry is an instance of the class
            if isinstance(geometry, self.__geometry_type__):
                return self._validate_z_values(geometry)
            raise ValueError(
                f"Supplied geometry ({geometry.geom_type}) is not a "
                f"{self.__geometry_type__.__name__}."
            )
        else:
            # The geometry type is a Union, check if the geometry is an instance of any of the
            # classes
            supported_types = typing.get_args(self.__geometry_type__)
            if any(isinstance(geometry, t) for t in supported_types):
                return self._validate_z_values(geometry)
            raise ValueError(
                f"Supplied geometry ({geometry.geom_type}) is not one of the expected "
                f"types: {', '.join([t.__name__ for t in supported_types])}."
            )

    @staticmethod
    def serialize(value) -> str:
        """
        Serialize a Shapely geometry object to a Well-Known Text (WKT) string.

        Args:
            value: The Shapely geometry object to be serialized.

        Returns:
            A string representing the serialized Well-Known Text (WKT) representation
            of the geometry object.
        """
        return shapely.to_wkt(value)

    def __get_pydantic_core_schema__(
        self, source: typing.Type[typing.Any], _: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        if isclass(source):
            if not issubclass(source, BaseGeometry):
                raise TypeError(
                    "GeometryField annotation can only be applied to Shapely geometries."
                )
        else:
            requested_types = typing.get_args(source)
            if not all(issubclass(t, BaseGeometry) for t in requested_types):
                raise TypeError(
                    "GeometryField annotation can only be applied to Shapely geometries. All types "
                    "in the Union must be a Shapely geometry."
                )
        self.__geometry_type__ = source
        return core_schema.no_info_after_validator_function(
            self.validate,
            core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                self.serialize,
                info_arg=False,
                return_schema=core_schema.any_schema(),
            ),
        )

    def __get_pydantic_json_schema__(
        self, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> typing.Dict[str, typing.Any]:
        # Determine the example WKT string for the geometry type.
        examples = [""]
        if isclass(self.__geometry_type__):
            if self.z_values is "required":
                examples = [EXAMPLES3D.get(self.__geometry_type__, "POINT Z (0 0 0)")]
            else:
                examples = [EXAMPLES.get(self.__geometry_type__, "POINT (0 0)")]
        else:
            requested_types = typing.get_args(self.__geometry_type__)
            if self.z_values is "required":
                examples = [EXAMPLES3D[t] for t in requested_types if t in EXAMPLES3D]
            else:
                examples = [EXAMPLES[t] for t in requested_types if t in EXAMPLES]
        # Create the JSON schema for the geometry field.
        json_schema = handler(_core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema["type"] = "string"
        json_schema["examples"] = examples
        return json_schema
