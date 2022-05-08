# EGM722-Project

**Setup and Installation**

Clone or download the GitHub repository.

Install conda and create a conda environment using the environment file (.yml) found in the repository. This file contains a list of the dependencies that are required to run the code:
•	 Python 3.8.8
•	 Geopandas 0.9.0
•	 Cartopy 0.18.0
•	 Notebook 6.2.0
•	 Rasterio 1.2.0

The code is made up of two parts that run independently of each other.

All required files for analysis can be found in the data_files folder.

**Step-by-step guide**

The steps outlined in this section correspond to the numbering found in the python code, preceded by a hash (#) symbol

**Part 1** - Automated classification and calculation of greenspace in London Electoral wards

1. Import the required modules. These are used to perform the operations and have already been listed in the setup and 
   installation section above

2. Load shapefiles and prepare for analysis. 
   
   1. Load datasets (wards and green_space), found in the data_files folder. 
   2. Green space shapefile converted to the same CRS as that of the wards (BNG, EPSG: 27700).
   3. Verification performed to check that both files have the same CRS, with an output displaying this as “CRS matches: True/False”.
   4. Green space shapefile (green_space) clipped to the study area (wards) to streamline the calculation. The clipped file is named green_clip.

3. Calculations 

   1. Calculate the area of each ward. This step will add a new column to the wards geodataframe named area_calc.
   2. As a means of knowing the program’s progress, and to verify that a new column has been added to the wards geodataframe can be displayed/hidden in the output by removing/adding the hash (#) before the line of code. 
   3. Calculate the area of green space in each ward and add a new column to the wards table named GS_Area. (This may take some time)
   4. Again, the updated geodataframe can be displayed by removing the # before the line of code 
   5. The calculated green space in each ward is summed and output to gs_sum. 
   6. gs_sum is combined with wards as a new table named joined. 
   7. The percentage of total area that is green space is then calculated and added to the joined table as a new column named gs_percent. 
   8. Check progress if necessary by removing # from line 
   9. Save the joined shapefile to the Output folder (optional)

5. Plot green space percentages on a map

4.1. Save the map in the Output folder (select suitable file name)

**Part 2** - Automated calculation and mapping of greenspace changes in London Electoral wards between 2011 and 2018.

1. Import the required modules. These are used to perform the operations and have already been listed in the setup and 
   installation section above. 

2. Load shapefiles and prepare for analysis.

   1. Load datasets (wards, gs_2011 and gs_2018), found in the data_files folder. 
   2. gs_2011 and gs_2018 converted to the same CRS as that of the wards (BNG, EPSG: 27700). 
   3. Verification performed to check that all files have the same CRS, with an output displaying this as “2011/2018 CRS matches: True/False”. 
   4. Green space shapefiles (gs_2011 and gs_2018) clipped to the study area (wards) to streamline the calculation. The clipped files are named gs_2011_clip and gs_2018_clip.

3. Calculations

   1. Calculate the area of each ward. This step will add a new column to the wards geodataframe named area_calc. 
   2. As a means of checking the codes’s progress, and to verify that a new column has been added to the wards geodataframe can be displayed/hidden in the output by removing/adding the hash (#) before the line of code. 
   3. Calculate the area of green space in each ward for both data sets and add a new column to the wards table named 2011_GS_Area and 2018_GS_Area. (This may take some time)
   4. Again, the updated geodataframe can be displayed by removing the # before the line of code.
   5. The calculated green space in each ward is summed and output to variables gs_2011_sum and gs_2018_sum. 
   6. gs_2011_sum and gs_2018_sum are combined with wards as a new table named joined. 
   7. The change in percentage of total area that is green space is then calculated and added to the joined table as a column named gs_change. 
   8. Check progress if necessary by removing # from line.
   9. Save the joined shapefile to the Output folder (optional).

4. Plot green space percentages on a map 

   1. Set the UTM zone that corresponds to the crs set in section 2
   2. 


4.8. Save the map in the Output folder (select suitable file name)

**Troubleshooting**

CRS issues
If using the code with data not included in the package, check that EPSG is correct for the study area and uses metres for a unit. See https://epsg.io/. Check that the coordinate reference system (CRS) for all files matches. 

Modules/Dependancies
Ensure that the environment created in conda with the Environment.yml file is active when running the code.

Long calculation times/Program appears frozen
Part 1 can take up to 25 minutes to compute, while part 2 can take up to 1h45m due to the very detailed and complex nature of the green space shape files derived from classification. 
