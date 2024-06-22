.. _examples:

========
Examples
========

These are examples for application of **pydantic-shapely**.

.. note::
    Examples can be added by creating `Jupyter Notebook`_ files in the ``\examples`` directory in
    the root of the repository. These notebooks are thus placed outside the tree of the documenation.
    Therefore a link should be created using ``.nblink``-files. These are placed in the ``\src\examples```
    directory within ``docs\src`` source. Also the created example should be added to the toctree
    below.

    Notebooks with no outputs are automatically executed during the documentation build process.
    If, however, there is at least one output cell present, the notebook is not evaluated and
    included as is. More information on modifying this standard behavior can be found on
    `nbsphinx documenation on executing notebooks`_.


.. toctree::
   :maxdepth: 2

   Skeleton <examples/skeleton>


.. _Jupyter Notebook: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _nbsphinx documenation on executing notebooks: https://nbsphinx.readthedocs.io/en/0.8.9/executing-notebooks.html
