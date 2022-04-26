#Import the required modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

#Load the wards dataset from the data_files folder
wards = gpd.read_file('data_files/Electoral_Wards.shp')
wards.crs

# The shapefiles have the area provided in hectares, this can be verified by printing the header
print(wards.head(0))

#transform the GeoDataFrame to UTM Zone 30, and assign the output to a new variable, wards_itm.
#wards_proj = wards.to_crs(epsg=32630)
#wards_proj.crs

#Convert hectares to square metres
for i, row in wards.iterrows():  # iterate over each row in the GeoDataFrame
    wards.loc[i, 'Area_Ward'] = row['HECTARES'] * 10000  # Calculate each ward's area in square metres and assign toa  new column, Area

print(wards.head())

# load the Green space shapefiles
GreenSpace = gpd.read_file('data_files/OS_Green_Space.shp')

# Ensure projection is the same as that of the wards
GreenSpace.crs = wards.crs

print(GreenSpace.crs == wards.crs)

#Calculate area green space in each ward
for i, row in GreenSpace.iterrows():  # iterate over each row in the GeoDataFrame
    GreenSpace.loc[i, 'Area_GS'] = row['geometry'].area  # Calculate area in m2 and assign to a new column, Area

print(GreenSpace.head())

GreenClip = gpd.clip(GreenSpace, wards) # Clip Green Space shapefile to London area

# Calculate area of green space in each ward
clipped = [] # initialize an empty list
for ward in wards['NAME'].unique():
    tmp_clip = gpd.clip(GreenClip, wards[wards['NAME'] == ward]) # Clip the GS polygons to each electoral ward
    for i, row in tmp_clip.iterrows():
        tmp_clip.loc[i, 'NAME'] = ward
        tmp_clip.loc[i, 'Ward_area'] = 'Area_Ward'
        tmp_clip.loc[i, 'GS_Area'] = row['geometry'].area # Calculate total GS in each ward, assign to each row
        # tmp_clip.loc[i, 'GS_Sum'] = (['GS_Area']).groupby(['NAME'])['GS_Area'].sum()
        #tmp_clip.loc[i, 'Ward_Area'] = row[wards[wards['Area_Ward']]]

    clipped.append(tmp_clip)

clipped_gdf = gpd.GeoDataFrame(pd.concat(clipped))

GS_SUM = (clipped_gdf.groupby(['NAME'])['GS_Area'].sum())

#for i, row in clipped_gdf.iterrows():  # iterate over each row in the GeoDataFrame
#    clipped_gdf.loc[i, 'GS_Sum'] = GS_SUM

print(clipped_gdf)


# Output green space percenatge to a map