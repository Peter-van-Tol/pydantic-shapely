.. |CI-status-badge| image:: https://img.shields.io/github/actions/workflow/status/Peter-van-Tol/pydantic-shapely/pytest.yml?branch=main&logo=github&label=CI
   :target: https://github.com/Peter-van-Tol/pydantic-shapely/actions 
.. |version-badge| image:: https://img.shields.io/pypi/v/pydantic-shapely.svg
   :target: https://pypi.org/project/pydantic-shapely/
.. |downloads-badge| image:: https://static.pepy.tech/badge/pydantic-shapely/month
   :target: https://pepy.tech/project/pydantic-shapely
.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/pydantic-shapely.svg
   :target: https://github.com/Peter-van-Tol/pydantic-shapely
.. |license-badge| image:: https://img.shields.io/github/license/Peter-van-Tol/pydantic-shapely.svg
   :target: https://github.com/Peter-van-Tol/pydantic-shapely/blob/main/LICENSE

|CI-status-badge| |version-badge| |downloads-badge| |pyversions-badge| |license-badge|

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
to GeoJSON format. 

GeoJSON features
~~~~~~~~~~~~~~~~

In order to add this functionality to your model, you have to inherit from the ``FeatureBaseModel``
class. This class is a subclass of the Pydantic ``BaseModel`` class and adds the following methods
and attributes to the model:

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

    class MyModel(FeatureBaseModel, geometry_field="point"):
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
    from pydantic import Field
    from pydantic_shapely import FeatureBaseModel, GeometryField
    from shapely.geometry import Point

    app = FastAPI()

    class MyModel(FeatureBaseModel, geometry_field="point"):
        point: typing.Annotated[Point, GeometryField(), Field(...)]

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


GeoJSON feature collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on the ``GeoJsonDataModel``, a feature collection can be easily created by using the
``FeatureCollectionBaseModel`` class. This class is a subclass of the Pydantic ``BaseModel``
class and adds the following methods and attributes to the model:

- ``from_feature_models``: a class method that creates a feature collection from a list of features.
  The list of features is validated before the feature collection is created. The validation
  ensures that all features are of the correct type.
- ``to_feature_models``: a method that returns a list of feature models from the feature collection.

Example usage of the feature collection:

.. code-block:: python

    import typing
    from shapely import Point

    from pydantic_shapely import FeatureBaseModel, GeometryField
    from pydantic_shapely.geojson import GeoJsonFeatureCollectionBaseModel


    class TestModel(FeatureBaseModel):
        """Test class for a feature which supports GeoJSON serialization."""

        geometry: typing.Annotated[Point, GeometryField()]
        name: str = "Hello World"
        answer: int = 42


    TestFeatureCollection = GeoJsonFeatureCollectionBaseModel[TestModel.GeoJsonDataModel]

    # Method 1: Create a feature collection from a list of features.
    test = TestFeatureCollection(
        features=[
            TestModel(geometry=Point(0, 0)).to_geojson_model(),
            TestModel(geometry=Point(1, 1)).to_geojson_model(),
        ]
    )
    # Method 2: Create a feature collection from a list features using the `from_feature_models`
    # class method.
    test = TestFeatureCollection.from_feature_models(
        [
            TestModel(geometry=Point(0, 0)),
            TestModel(geometry=Point(1, 1)),
        ]
    )

    # Print the resluting GeoJSON feature collection.
    print(test.model_dump_json(indent=2))
    # RESULT:
    # {
    #   "type": "FeatureCollection",
    #   "features": [
    #     {
    #       "type": "Feature",
    #       "geometry": {
    #         "type": "Point",
    #         "coordinates": [
    #           0.0,
    #           0.0
    #         ]
    #       },
    #       "properties": {
    #         "name": "Hello World",
    #         "answer": 42
    #       }
    #     },
    #     {
    #       "type": "Feature",
    #       "geometry": {
    #         "type": "Point",
    #         "coordinates": [
    #           1.0,
    #           1.0
    #         ]
    #       },
    #       "properties": {
    #         "name": "Hello World",
    #         "answer": 42
    #       }
    #     }
    #   ]
    # }

The GeoJSON serialization can also be used with FastApi. The following example shows how to
create a simple annotated API that returns a GeoJSON Feature Collection:

.. code-block:: python

    import typing
    from fastapi import FastAPI
    from pydantic import Field
    from pydantic_shapely import FeatureBaseModel, GeometryField
    from pydantic_shapely.geojson import GeoJsonFeatureCollectionBaseModel
    from shapely.geometry import Point

    app = FastAPI()

    class MyModel(FeatureBaseModel, geometry_field="point"):
        point: typing.Annotated[Point, GeometryField(), Field(...)]
        name: str = "Hello World"
        answer: int = 42

    
    # NOTE: Sub-classing the GeoJsonFeatureCollectionBaseModel gives a cleaner description
    # in the API documentation.
    class MyModelFeatureCollection(GeoJsonFeatureCollectionBaseModel[MyModel.GeoJsonDataModel]):
        ...

    
    @app.get("/points")
    def get_points() -> MyModelFeatureCollection:
        # Return a GeoJSON representation of a Shapely geometry.
        return MyModelFeatureCollection.from_feature_models(
            [
                MyModel(point=Point(0, 0)).to_geojson_model(),
                MyModel(point=Point(1, 1)).to_geojson_model(),
            ]
        )

    @app.post("/points")
    def post_points(model: MyModelFeatureCollection) -> typing.List[MyModel]:
        # Convert the GeoJSON model back to the original model instance with the
        # `to_feature_model` method. The Shapely geometry will be returned as a
        # WKT-string in this case.
        return model.to_feature_models()

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)

Optional fields specified in RFC 7946
-------------------------------------

The GeoJSON specification allows for optional fields in the GeoJSON feature. These fields are
``id``, ``crs``, and ``bbox``. The ``id`` field is a string or number that uniquely identifies
the feature. The ``crs`` field is an object that specifies the coordinate reference system of the
feature. The ``bbox`` field is an array of numbers that specifies the bounding box of the feature.

id field
~~~~~~~~

This field is not implemented yet.

crs field
~~~~~~~~~

This field is not implemented yet.

bbox field
~~~~~~~~~~

The ``bbox`` field is an array of numbers that specifies the bounding box of the feature. The array
has either 4 elements in case of a 2-dimensional geometry or 6 elements in case of a 3-dimensional
geometry. The elements of the array are in the order ``[minx, miny, maxx, maxy]`` for 2-dimensional
geometries and ``[minx, miny, minz, maxx, maxy, maxz]`` for 3-dimensional geometries.

The ``bbox`` can be added to the GeoJSON feature in two ways:

- By adding the ``bbox`` parameter to the ``FeatureBaseModel`` class. This parameter is a string
  with the allowed values ``ignore`` and ``export``. The default value is ``ignore``. When the
  value is set to ``export``, the bounding box of the feature will be added to the GeoJSON
  representation of the feature. For example:

    .. code-block:: python
    
        import typing
        from pydantic import Field
        from pydantic_shapely import FeatureBaseModel, GeometryField
        from shapely.geometry import Point
    
        class MyModel(FeatureBaseModel, geometry_field="point", bbox="export"):
            point: typing.Annotated[Point, GeometryField(), Field(...)]
            name: str = "Hello World"
            answer: int = 42
    
        model = MyModel(point=Point(0, 0))
        print(model.model_dump_geojson())
        # {
        #     "type": "Feature",
        #     "geometry": {
        #         "type": "Point",
        #         "coordinates": [0.0, 0.0]
        #     },
        #     "properties": {
        #         "name": "Hello World",
        #         "answer": 42
        #     },
        #     "bbox": [0.0, 0.0, 0.0, 0.0]
        # }

- By inhereting from both the ``FeatureModel.GeoJsonDataModel`` and the ``FeatureBoundingBoxMixin``
  classes. This method is especially useful when you want to add the bounding box to certain API
  endpoints.  
  
  .. code-block:: python

      import typing
      from fastapi import FastAPI
      from pydantic import Field
      from pydantic_shapely import FeatureBaseModel, GeometryField
      from pydantic_shapely.geojson import FeatureBoundingBoxMixin
      from shapely.geometry import Point

      app = FastAPI()

      class MyModel(FeatureBaseModel, geometry_field="point"):
          point: typing.Annotated[Point, GeometryField(), Field(...)]

      
      class MyModelFeatur(MyModel.GeoJsonDataModel, FeatureBoundingBoxMixin):
          ...

      @app.get("/point")
      def get_point() -> MyModelFeatur:
          # Return a GeoJSON representation of a Shapely geometry.
          return MyModel(point=Point(0, 0)).to_geojson_model()

      @app.post("/point")
      def post_point(model: MyModelFeatur) -> MyModel:
          # Convert the GeoJSON model back to the original model instance with the
          # `to_feature_model` method. The Shapely geometry will be returned as a
          # WKT-string in this case.
          return model.to_feature_model()

      if __name__ == "__main__":
          import uvicorn
          uvicorn.run(app, host="0.0.0.0", port=8000)

For the ``FeatureCollectionBaseModel`` the ``bbox`` parameter can *only* be added to the
class by using the ``FeatureClassBoundingBoxMixin`` class. The example belows adds the ``bbox``
to the feature collection, but the individual features do not have a bounding box.

.. code-block:: python

    import typing
    from pydantic_shapely import FeatureBaseModel, GeometryField
    from pydantic_shapely.geojson import GeoJsonFeatureCollectionBaseModel, FeatureClassBoundingBoxMixin
    from shapely.geometry import Point

    class MyModel(FeatureBaseModel, geometry_field="point"):
        point: typing.Annotated[Point, GeometryField()]
        name: str = "Hello World"
        answer: int = 42
    
    class MyModelFeatureCollection(
        GeoJsonFeatureCollectionBaseModel[MyModel.GeoJsonDataModel],
        FeatureClassBoundingBoxMixin
    ):
        ...

In all cases, the bounding box is calculated based on the geometry of the feature(s). The bounding
box will be therefore always up-to-date with the geometry of the feature(s), even if the GeoJson
feature(s) are updated after conversion between the model and the GeoJSON representation.

Work in progress
----------------
This package is still in development. The following features are planned for the future:

- Adding more options for the ``GeometryField`` annotation. For example, the ability to
  set a bounding box for the geometry.
- Adding the CRS to the both ``GeometryField`` and the GeoJSON serialization. This functionality
  will automatically transform the geometries to the specified CRS.

Allthough the package is still in development, the current features are tested and ready
for use. The signature of the methods and classes will not change in the future. If you have
any suggestions or questions, feel free to open an issue on the 
`GitHub repository <https://github.com/Peter-van-Tol/pydantic-shapely>`_.
