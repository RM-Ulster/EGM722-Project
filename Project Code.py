"""
Automated calculation and mapping of greenspace in London Electoral wards



"""

# 1 Import the required modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# 2 Load and prepare files for analysis

# 2.1 Load the datasets from the data_files folder
wards = gpd.read_file('data_files/Electoral_Wards.shp')
green_space = gpd.read_file('data_files/OS_Green_Space.shp')

# 2.2 Ensure CRS is the same for both files
wards = wards.to_crs(epsg=27700)
green_space = green_space.to_crs(epsg=27700)

print('CRS matches: ', (green_space.crs == wards.crs)) # Verify that CRS is the same for both

# 2.3 Convert ward area from hectares to m^2

for i, row in wards.iterrows(): # iterate over each row in the GeoDataFrame
    wards.loc[i, 'area_calc'] = row['geometry'].area

print(wards.head(10))

# 2.4 Clip Green Space shapefile to London area
green_clip = gpd.clip(green_space, wards)

ward_clip = wards[wards['NAME'] == 'ward']

# 3 Calculate area of green space in each ward

# 3.1
for ii, row in wards.iterrows():
    tmp_clip = gpd.clip(green_space, wards)
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[ii, 'GS_Area'] = tmp_clip['Area'].sum()
    tmp_clip['NAME'] = 'ward'
    wards.loc[ii, 'ward_name'] = row['NAME']

print(wards.head(10))

#print(wards.head(-1))

# 2.6 Sum area of green space in each ward

gs_sum = (wards.groupby(['NAME'])['GS_Area'].sum())
print(gs_sum)

joined = wards.set_index('NAME').join(gs_sum.rename('Total GS Area'))

gs_area = joined[joined['Total GS Area'] == 'total_gs_area']
area_ward = joined[joined['Area_Ward'] == 'area_ward']

for i, row in joined.iterrows():
    joined.loc[i, 'gs_percent'] = (row['Total GS Area'] / row['Area_Ward'])

print(joined.head(0))

'''
for ward in wards['NAME'].unique():
    tmp_clip = gpd.clip(green_clip, wards[wards['NAME'] == ward])
    for i, row in tmp_clip.iterrows():
        tmp_clip.loc[i, 'GS_Area'] = row['geometry'].area
        tmp_clip.loc[i, 'NAME'] = ward
        for ii, row in wards.iterrows():
            tmp_clip = gpd.clip(green_clip, wards[wards['NAME'] == ward])
            tmp_clip['Area'] = tmp_clip['geometry'].area
            wards.loc[ii, 'GS_Area'] = tmp_clip['Area'].sum()







        #tmp_clip.loc[i, 'GS_Area'] = row['geometry'].area # Calculate GS in each ward, assign to each row
        #tmp_clip.loc[i, 'GS_Sum'] = row['GS_Area'].groupby(['NAME'])['GS_Area'].sum() # Sum GS in each ward
        #tmp_clip.loc[i, 'GS_Sum'] = row['geometry'].area.groupby(['NAME'])['GS_Area'].sum()
'''
'''
    clipped.append(tmp_clip)

clipped_gdf = gpd.GeoDataFrame(pd.concat(clipped))
'''
"""
for i, row in clipped_gdf.iterrows():
    clipped_gdf.loc[i, 'GS_Sum'] = row['geometry'].area.groupby(['NAME'])['GS_Area'].sum() # Sum GS in each ward
"""
#print(clipped_gdf)

"""
# Output green space percentage to a map

plt.ion() # make the plotting interactive

# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# create a scale bar of length 20 km in the upper right corner of the map
def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)

# load the outline of London wards for a backdrop
outline = gpd.read_file('data_files/Electoral_Wards.shp')

myFig = plt.figure(figsize=(10, 10))  # create a figure of size 10x10 inches

myCRS = ccrs.UTM(29N) # create a Universal Transverse Mercator reference system to transform our data.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

myFig # re-display the figure here.
"""
