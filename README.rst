================
pydantic-shapely
================


    Letting two great packages work together!


``pydantic-shapely`` is a Python package that allows you to use Shapely geometries as Pydantic
fields. This package is useful when you want to validate and serialize Shapely geometries using
Pydantic models. As an added bonus, you can also use the package to validate and serialize the
geometries in GeoJSON format, without the need of any additional code. The GeoJSON serialization
is based on the `GeoJSON specification <https://tools.ietf.org/html/rfc7946>`_.

Installation
------------

You can install the package using pip:

.. code-block:: shell

    pip install pydantic-shapely

Ofcourse, you can also install the package using `poetry <https://python-poetry.org/>`_ as 
package manager:

.. code-block:: shell

    poetry add pydantic-shapely

Basic usage
-----------

Normally, when you want to use Shapely geometries in Pydantic models, you would have
to set ``arbitrary_types_allowed`` to ``True`` in the Pydantic model. This is because
the Shapely geometries are not natively supported by Pydantic. 

With ``pydantic-shapely`` you can use Shapely geometries as Pydantic fields without
having to set ``arbitrary_types_allowed`` to ``True``. You only have to add the
``GeometryField`` as _additional_ annotation to the field in the Pydantic model.

.. code-block:: python

    import typing
    from pydantic import BaseModel
    from pydantic_shapely import GeometryField
    from shapely.geometry import Point

    class MyModel(BaseModel):
        point: typing.Annotation[Point, GeometryField(), Field(...)]

    model = MyModel(point=Point(0, 0))
    print(model.point)  # POINT (0 0)

With the ``GeometryField`` allows also to set the following parameters whether the geometry
should be 2- or 3-dimensional with the parameter ``z_values``. The following values are
allowed:

- ``forbidden``: the geometry must be strictly 2-dimensional. A ValueError will
  raised when a shape with z-values is provided.
- ``strip``: the geometry may have z-values. These values will be stripped from
  then geometry in the validation process. The resulting shape will be
  2-dimensional in all cases.
- ``allow`` (default): both 2- and 3-dimensional values are allowed. During the
  validation process the data is not altered. This is the default behavior.
- ``required``: the geometry must be strictly 2-dimensional. A ValueError will
  raised when a shape without z-values is provided.

GeoJSON serialization
---------------------
With ``pydantic-shapely`` you can also serialize the a Pydantic model with a Shapely geometry
to GeoJSON format. In order to add this functionality to your model, you have to inherit from
the ``FeatureBaseModel`` class. This class is a subclass of the Pydantic ``BaseModel`` class
and adds the following methods and attributes to the model:

- ``GeoJsonDataModel``: an attribute that contains the Pydantic GeoJSON model based on the 
  original model. This model is created when the subclass is created.
- ``to_geojson_model``: a method that returns the GeoJSON model of the model instance. To convert
  the GeoJSON model back to the original model, you can use the ``to_feature_model`` method on
  the GeoJSON model.
- ``model_dump_geojson``: a method that serializes the model to GeoJSON format.

Example usage of the GeoJSON serialization:

.. code-block:: python

    import typing
    from pydantic import BaseModel
    from pydantic_shapely import GeometryField, FeatureBaseModel
    from shapely.geometry import Point

    class MyModel(FeatureBaseModel):
        point: typing.Annotation[Point, GeometryField(), Field(...)]
        a: int = 42
        b: str = "Hello, World!"

    model = MyModel(point=Point(0, 0))
    print(model.model_dump_geojson())
    # {
    #     "type": "Feature",
    #     "geometry": {
    #         "type": "Point",
    #         "coordinates": [0.0, 0.0]
    #     },
    #     "properties": {
    #         "a": 42,
    #         "b": "Hello, World!"}
    # }

The GeoJSON serialization can also be used with FastApi. The following example shows how to
create a simple annotated API that returns a GeoJSON representation of a Shapely geometry:

.. code-block:: python

    import typing
    from fastapi import FastAPI
    from pydantic_shapely import FeatureBaseModel, GeometryField
    from shapely.geometry import Point

    app = FastAPI()

    class MyModel(FeatureBaseModel):
        point: typing.Annotation[Point, GeometryField(), Field(...)]

    @app.get("/point")
    def get_point() -> MyModel.GeoJsonDataModel:
        # Return a GeoJSON representation of a Shapely geometry.
        return MyModel(point=Point(0, 0)).to_geojson_model()

    @app.post("/point")
    def post_point(model: MyModel.GeoJsonDataModel) -> MyModel:
        # Convert the GeoJSON model back to the original model instance with the
        # `to_feature_model` method. The Shapely geometry will be returned as a
        # WKT-string in this case.
        return model.to_feature_model()

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)

Work in progress
----------------
This package is still in development. The following features are planned for the future:

- ``GeometryCollection`` is not yet supported.
- Adding more options for the ``GeometryField`` annotation. For example, the ability to
  set a bounding box for the geometry.
- Adding the CRS to the both ``GeometryField`` and the GeoJSON serialization. This functionality
  will automatically transform the geometries to the specified CRS.

Allthough the package is still in development, the current features are tested and ready
for use. The signature of the methods and classes will not change in the future. If you have
any suggestions or questions, feel free to open an issue on the 
`GitHub repository <https://github.com/Peter-van-Tol/pydantic-shapely>`_.
