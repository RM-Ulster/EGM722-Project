"""
Automated calculation and mapping of greenspace in London Electoral wards using OS data.

Data is outputted to thematic map in section 4.

This code was developed as a pilot for Project Code Part 2.
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

# i Load the datasets from the data_files folder
wards = gpd.read_file('data_files/Electoral_Wards.shp')
green_space = gpd.read_file('data_files/OS_Green_Space.shp')

# ii Ensure CRS is the same for both files
wards = wards.to_crs(epsg=27700)
green_space = green_space.to_crs(epsg=27700)

# iii Verify that CRS is the same for both
print('CRS matches: ', (green_space.crs == wards.crs))

# iv Clip Green Space shapefile to London area
green_clip = gpd.clip(green_space, wards)

# 3 Calculations

# i Calculate area of each ward

for i, row in wards.iterrows():
    wards.loc[i, 'area_calc'] = row['geometry'].area

# ii Show/hide table in output
print(wards.head(10))

# iii Calculate area of green space in each ward
ward_clip = wards[wards['NAME'] == 'ward']

for i, row in wards.iterrows():
    tmp_clip = gpd.clip(green_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, 'GS_Area'] = tmp_clip['Area'].sum()
    wards.loc[i, 'ward_name'] = row['NAME']

# iv Show/hide table in output
print(wards.head(10))

# v Sum area of green space in each ward
gs_sum = (wards.groupby(['NAME'])['GS_Area'].sum())
print(gs_sum)

# vi Join gs_sum to wards table
joined = wards.set_index('NAME').join(gs_sum.rename('Total GS Area'))

# vii Calculate percentage of green space in each ward
for i, row in joined.iterrows():
    joined.loc[i, 'gs_percent'] = ((row['Total GS Area'] / row['area_calc']) * 100)

# viii Show/hide table in output
print(joined.head(10))

# ix save shapefile with calculated columns
# joined.to_file("Output/joined.shp")

# 4 Output green space percentage to a map

def generate_handles(labels, colors, edge='k', alpha=0.5):
    """generate matplotlib handles to create a legend of the features we put in our map."""
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

plt.ion()

# i Set projection
myCRS = ccrs.UTM(29)

# ii Prepare map area
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# iii Add ward outlines
ward_outlines = ShapelyFeature(joined['geometry'], myCRS, edgecolor='darkgray', facecolor='none', linewidth=0.25)

ax.add_feature(ward_outlines)
county_handles = generate_handles([''], ['none'], edge='darkgray')

# iv Data bounds and colour scale
gs_plot = joined.plot(column='gs_percent', ax=ax, vmin=0, vmax=50, cmap='Greens',
                       legend=True, cax=cax, legend_kwds={'label': 'Green Space Percentage (%)'})


# v Legend
ax.legend(county_handles, ['Ward Boundaries'], fontsize=12, loc='lower right', framealpha=1)

# vi Copyright info
ax.text(0, 0, 'Contains National Statistics data © Crown copyright and database right (2015) \n '
                           'Contains Ordnance Survey data © Crown copyright and database right (2015)',
        verticalalignment='bottom',
        horizontalalignment='left',
        transform=ax.transAxes,
        fontsize=6)

# vii Title
ax.set_title('Publicly Accessible Green Space as a Proportion of Ward Area in Greater London',
             fontweight="bold")

# viii save the map
fig.savefig('Output/OS_Green_Space_Percent_b.png', dpi=300, bbox_inches='tight')