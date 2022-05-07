# EGM722-Project
Automated classification and calculation of greenspace in London Electoral wards

The steps outlined in this document correspond to the numbering found in the python code, preceded by a hash (#) symbol

Part 1

1. Import the required modules. These are used to perform the operations and have already been listed in the setup and 
2. installation section above
3. Load shapefiles and prepare for analysis. 
2.1.	Load datasets (wards and green_space), found in the data_files folder. 
2.2.	Green space shapefile converted to the same CRS as that of the wards (BNG, EPSG: 27700). 
2.2.1.	 Verification performed to check that both files have the same CRS, with an output displaying this as “CRS matches: True/False”.
2.3.	Green space shapefile (green_space) clipped to the study area (wards) to streamline the calculation. The clipped file is named green_clip.
4. Calculations
3.1.	Calculate the area of each ward. This step will add a new column to the wards geodataframe named area_calc.
3.1.1.	 As a means of knowing the program’s progress, and to verify that a new column has been added to the wards geodataframe can be displayed/hidden in the output by removing/adding the hash (#) before the line of code.
3.2.	Calculate the area of green space areas in each ward and add a new column to the wards table named GS_Area. (This may take some time)
3.2.1.	 Again, the updated geodataframe can be displayed by removing the # before the line of code
3.3.	The calculated green space in each ward is summed and output to gs_sum.
3.4.	gs_sum is combined with wards as a new table named joined.
3.5.	The percentage of total area that is green space is then calculated and added to the joined table as a new column named gs_percent.
3.5.1.	 Check progress if necessary by removing # from line
3.6.	Save the joined shapefile to the Output folder (optional)
5. Plot green space percentages on a map
4.1.	Save the map in the Output folder
