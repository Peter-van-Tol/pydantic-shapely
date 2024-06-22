"""
THIS FILE IS GENERATED AUTOMATICALLY. CHANGES IN THIS FILE WILL BE OVERWRITTEN
WHEN THE TEMPLATE IS APPLIED AGAIN.

This script will create all `nblink` files for the Jupyter Notebooks located
in the examples-folder. It will not overwrite nor delete any files. For a full
update of the examples, manual removal of the files on beforhand is required.

The output of this method is a list of entries which can be used in the file
`examples.rst`.
"""

import os

EXAMPLES_BASE = r"../../../examples/"

__location__ = os.path.dirname(__file__)
for file in os.listdir(os.path.join(__location__, EXAMPLES_BASE)):
    if file.endswith(".ipynb") and not os.path.exists(
        f'./{file.replace(".ipynb", "nblink")}'
    ):
        with open(
            os.path.join(__location__, file.replace(".ipynb", ".nblink")), "w"
        ) as nblink_file:
            nblink_file.write(
                f'{{\n    "path": "{os.path.join(EXAMPLES_BASE, file)}"\n}}'
            )
    print(f'   {file.split(".")[0]} <examples/{file.split(".")[0]}>')
