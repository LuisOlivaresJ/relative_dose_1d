# Quality control tests for new versions or post installation acceptance

Test based on International Forum of Medical Device Regulators working group guidelines (IMDRF)

## Main window

Open and run GUI_tool.py. 
Expected outputs:

    * A main GUI window should be displayed with a demo data.

Change interpolation to 0 and apply. The demo data consist of eleven points, representing a dose gradient of 10%/mm, evenly spaced by 1 mm. Since consecutive points have a difference of 10%, gamma analysis results can be easy verified.

    * For a given position, if the dose difference equals or is close to 6%, gamma should be 2.
    * From the plot, count the number of gamma points lower than 1, then divide it to 11. Verifiy the pass rate, evaluated and total points outputs.

On a command window with a python interpreter, write 

>>> from relative_dose_1d import GUI

    * A main GUI window should be displayed.

Click on ```Load a text file```. Go to .\relative_dose_1d\src\relative_dose_1d\test_data and open "6X_measured_profile_ptw.mcc"

    A profile should be showed.

Again, click on ```Load a text file```. Open the file "6X_Beam_Configuration_Eclipse.data". Change Threshold to 50%. The results should be 

    * Pass rate: 100%
    * Total points: 31.0
    * Evaluated points: 15.5