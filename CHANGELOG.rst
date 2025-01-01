=========
Changelog
=========


Version 1.0.0a4
===============

- Unpinned `pydantic` package version;

Version 1.0.0a3
===============

- BUGFIX: Removed ``numpy`` as a dependency. This was causing issues with the installation of the
  package, since it was pinned to strictly. The dependency is not required, as ``shapely`` already
  has a dependency on ``numpy``.;
- BUGFIX: When using the ``GeometryField`` it is now possible to instantiate the field with a the
  default ``shapely`` constructor. I.e. a ``MultiPolygon`` can be instantiated with a list of
  ``Polygon`` objects; 

Version 1.0.0a2
===============

- FEATURE: Added support for Shapely ``GeometryCollection`` geometries;
- FEATURE: Added support for GeoJSon feature collections model that represents
  a GeoJSON feature collection and serialize it to a GeoJSON feature collection;
- REFACTOR: Changed the GeoJSON geometry models from TypeAlias to sub classes of the corresponding
  base-models. This gives a better documentation in the API. This has no effects on the functionality
  of the package.
- BUGFIX: Changed ``wkt.dumps`` and ``wkt.loads`` to respectively ``shapely.to_wkt`` and 
  ``shapely.wkt.loads``;
- BUGFIX: Fixed a bug where the class property ``ParentDataModel`` was not being set when the 
  a sub-class of ``GeoJsonFeatureBaseModel`` was created. This prohibited the correct
  serialization of the Feature Collection;

Version 1.0.0a1
===============

- Updated metadata for correct rendering on PyPI;


Version 1.0.0a0
===============

- Initial version;
- Support for annotated geometry fields for all Pydantic geometries, except for ``GeometryCollection``;
- Support for converting a FeatureModel (i.e. a Pydantic model with a geometry field) to a GeoJSON Feature;
