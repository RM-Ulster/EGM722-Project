"""
Automated calculation and mapping of greenspace in London Electoral wards using OS data

Percentage of total area that is greenspace in each ward is calculated in section 2

Data is outputted to thematic map in section 3
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
green_space = gpd.read_file('data_files/OS_Green_Space.shp')

# 2.2 Ensure CRS is the same for both files
wards = wards.to_crs(epsg=27700)
green_space = green_space.to_crs(epsg=27700)

# 2.2.1 Verify that CRS is the same for both
print('CRS matches: ', (green_space.crs == wards.crs))

# 2.3 Clip Green Space shapefile to London area
green_clip = gpd.clip(green_space, wards)

# 3 Calculations

# 3.1 Calculate area of each ward

for i, row in wards.iterrows():
    wards.loc[i, 'area_calc'] = row['geometry'].area

# 3.1.1 Show/hide table in output
print(wards.head(10))

# 3.2 Calculate area of green space in each ward
ward_clip = wards[wards['NAME'] == 'ward']

for i, row in wards.iterrows():
    tmp_clip = gpd.clip(green_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, 'GS_Area'] = tmp_clip['Area'].sum()
    wards.loc[i, 'ward_name'] = row['NAME']

# 3.2.1 Show/hide table in output
print(wards.head(10))

# 3.3 Sum area of green space in each ward
gs_sum = (wards.groupby(['NAME'])['GS_Area'].sum())
print(gs_sum)

# 3.4 Join gs_sum to wards table
joined = wards.set_index('NAME').join(gs_sum.rename('Total GS Area'))

# 3.5 Calculate percentage of green space in each ward
for i, row in joined.iterrows():
    joined.loc[i, 'gs_percent'] = ((row['Total GS Area'] / row['area_calc']) * 100)

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

gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-0.3, -0.15, 0, 0.15, 0.3],
                         ylocs=[51, 51.1, 51.2, 51.3, 51.4])
gridlines.right_labels = True
gridlines.bottom_labels = True

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

gs_plot = joined.plot(column='gs_percent', ax=ax, vmin=0, vmax=50, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Green Space Percentage (%)'})

ward_outlines = ShapelyFeature(joined['geometry'], myCRS, edgecolor='y', facecolor='none', linewidth=0.25)

ax.add_feature(ward_outlines)
county_handles = generate_handles([''], ['none'], edge='y')

ax.legend(county_handles, ['Ward Boundaries'], fontsize=12, loc='upper left', framealpha=1)

'''
copyright_info = generate_handles([''], ['none'])

ax.legend(copyright_info, 'Contains National Statistics data © Crown copyright and database right (2015) \n '
                           'Contains Ordnance Survey data © Crown copyright and database right (2015)',
                            fontsize=6, loc='lower right', framealpha=1)
'''
ax.text(0, 0, 'Contains National Statistics data © Crown copyright and database right (2015) \n '
                           'Contains Ordnance Survey data © Crown copyright and database right (2015)',
        verticalalignment ='bottom',
        horizontalalignment ='left',
        transform = ax.transAxes,
        fontsize = 5)

# 4.1 save the figure
fig.savefig('Output/sample_map.png', dpi=300, bbox_inches='tight')