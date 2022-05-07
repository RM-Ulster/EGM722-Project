"""
Automated calculation and mapping of greenspace changes in London Electoral wards between 2011 and 2018.

Data is outputted to thematic map in section 4.

This code can be applied across another study area and time frame to calculate changes in land cover
- The troubleshooting guide in the read me provides assistance with adapting it.



"""

# 1 Import the required modules
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

# 2 Load and prepare files for analysis

# 2.1 Load the datasets from the data_files folder
wards = gpd.read_file('data_files/Electoral_Wards.shp')
gs_2011 = gpd.read_file('data_files/2011_gs_simplified.shp')
gs_2018 = gpd.read_file('data_files/2018_gs_simplified.shp')

# 2.2 Ensure CRS is the same for all files
wards = wards.to_crs(epsg=27700)
gs_2011 = gs_2011.to_crs(epsg=27700)
gs_2018 = gs_2018.to_crs(epsg=27700)

# 2.2.1 Verify that CRS is the same for all files
print('2011 CRS matches wards: ', (gs_2011.crs == wards.crs))
print('2018 CRS matches wards: ', (gs_2018.crs == wards.crs))

# 2.3 Clip Green Space shapefiles to London area
gs_2011_clip = gpd.clip(gs_2011, wards)
gs_2018_clip = gpd.clip(gs_2018, wards)

# 3 Calculations

# 3.1 Calculate area of each ward

for i, row in wards.iterrows():
    wards.loc[i, 'area_calc'] = row['geometry'].area

# 3.1.1 Show/hide table in output
#print(wards.head(10))

# 3.2 Calculate area of green space in each ward for both 2011 and 2018

for i, row in wards.iterrows():
    tmp_clip = gpd.clip(gs_2011_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, '2011_GS_Area'] = tmp_clip['Area'].sum()
    tmp_clip = gpd.clip(gs_2018_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, '2018_GS_Area'] = tmp_clip['Area'].sum()
    wards.loc[i, 'ward_name'] = row['NAME']

# 3.2.1 Show/hide table in output
print(wards.head(10))

# 3.3 Sum area of green space in each ward
gs_2011_sum = (wards.groupby(['NAME'])['2011_GS_Area'].sum())
print(gs_2011_sum)
gs_2018_sum = (wards.groupby(['NAME'])['2018_GS_Area'].sum())
print(gs_2018_sum)

# 3.4 Join 'gs_sum' to 'wards' table to create a new table named 'joined'
joined = wards.set_index('NAME').join[gs_2011_sum.rename('2011_GS_Sum'), gs_2018_sum.rename('2018_GS_Sum')]

# 3.5 Calculate percentage of green space in each ward
for i, row in joined.iterrows():
    joined.loc[i, '2011_gs_perc'] = ((row['2011_GS_Sum'] / row['area_calc']) * 100)
    joined.loc[i, '2018_gs_perc'] = ((row['2018_GS_Sum'] / row['area_calc']) * 100)
    joined.loc[i, 'gs_change'] = (row['2018_gs_perc'] - row['2011_gs_perc'])

# 3.5.1 Show/hide table in output
print(joined.head(10))

# 3.6 save shapefile with calculated columns
# joined.to_file("Output/joined.shp")

# 4 Output green space percentage to a map

plt.ion() # make the plotting interactive

'''
generate matplotlib handles to create a legend of the features we put in our map.

Original code by Bob McNabb at: 
https://github.com/iamdonovan/egm722/blob/week3/Week3/Practical3.ipynb
'''

def generate_handles(labels, colors, edge='k', alpha=0.5):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

myCRS = ccrs.UTM(29)

fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

gs_plot = joined.plot(column='gs_change', ax=ax, vmin=-25, vmax=25, cmap='RdGn',
                       legend=True, cax=cax, legend_kwds={'label': 'Green Space Percentage Change (2011-2018) (%)'})

ward_outlines = ShapelyFeature(joined['geometry'], myCRS, edgecolor='y', facecolor='none', linewidth=0.25)

ax.add_feature(ward_outlines)
county_handles = generate_handles([''], ['none'], edge='y')

ax.legend(county_handles, ['Ward Boundaries'], fontsize=12, loc='upper left', framealpha=1)

ax.text(0, 0, 'Contains National Statistics data © Crown copyright and database right (2015) \n '
                           'Contains Ordnance Survey data © Crown copyright and database right (2015)',
        verticalalignment='bottom',
        horizontalalignment='left',
        transform=ax.transAxes,
        fontsize=5)

ax.set_title('Publicly Accessible Green Space as a Proportion of Ward Area in Greater London',
             fontweight="bold")

# 4.1 save the figure
fig.savefig('Output/Green_Space_Change.png', dpi=300, bbox_inches='tight')