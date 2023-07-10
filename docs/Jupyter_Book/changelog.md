# Changelog

## April-2023  Versión 0.0.3
  * *relative_dose_1d* is added to [PyPi](https://pypi.org/)

## May-2023 Version 0.1.0
  * It is now possible to perform unit transformation for distance using a multiplication factor, and to move the origin of coordinate system.

## May-2023 Version 0.1.2
  * New web page documentation, following [PEP 287 – reStructuredText Docstring Format](https://peps.python.org/pep-0287/) and [napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon)

## May-2023 Version 0.1.3
* [Interpolation error](https://github.com/LuisOlivaresJ/relative_dose_1d/issues/1) solved.

## Jul-2023 Version 0.1.4 - 0.1.5
* Two new functions, [build_from_array_and_step](Tools_module_label) to add physical positions, and [plot](GUI_tool_module_label) to show a GUI. 
* [New GUI_tool module](GUI_tool_module_label).
* Now it is possible to change tolerance parameter for gamma evaluation.
* Pass rate, total and evaluated points are now displayed on the GUI.
* gamma_1d function returns the number of evaluated points.