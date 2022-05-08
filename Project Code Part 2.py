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

# i Load the datasets from the data_files folder
wards = gpd.read_file('data_files/Electoral_Wards.shp')
gs_2011 = gpd.read_file('data_files/2011_gs.shp')
gs_2018 = gpd.read_file('data_files/2018_gs.shp')

# ii Ensure CRS is the same for all files
wards = wards.to_crs(epsg=27700)
gs_2011 = gs_2011.to_crs(epsg=27700)
gs_2018 = gs_2018.to_crs(epsg=27700)

# iii Verify that CRS is the same for all files
print('2011 CRS matches wards: ', (gs_2011.crs == wards.crs))
print('2018 CRS matches wards: ', (gs_2018.crs == wards.crs))

# iv Clip Green Space shapefiles to London area
gs_2011_clip = gpd.clip(gs_2011, wards)
gs_2018_clip = gpd.clip(gs_2018, wards)

# 3 Calculations

# i Calculate area of each ward

for i, row in wards.iterrows():
    wards.loc[i, 'area_calc'] = row['geometry'].area

# ii Show/hide table in output
#print(wards.head(10))

# iii Calculate area of green space in each ward for both 2011 and 2018

for i, row in wards.iterrows():
    tmp_clip = gpd.clip(gs_2011_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, '2011_GS_Area'] = tmp_clip['Area'].sum()
    tmp_clip = gpd.clip(gs_2018_clip, row['geometry'])
    tmp_clip['Area'] = tmp_clip['geometry'].area
    wards.loc[i, '2018_GS_Area'] = tmp_clip['Area'].sum()
    wards.loc[i, 'ward_name'] = row['NAME']

# iv Show/hide table in output
print(wards.head(0))

# v Sum area of green space in each ward
gs_2011_sum = (wards.groupby(['NAME'])['2011_GS_Area'].sum())
print(gs_2011_sum)
gs_2018_sum = (wards.groupby(['NAME'])['2018_GS_Area'].sum())
print(gs_2018_sum)

# vi Join both green space sums to 'wards' table to create a new table named 'joined'
join_temp = wards.set_index('NAME').join(gs_2011_sum.rename('2011_GS_Sum'))
for i, row in join_temp.iterrows():
    join_temp.loc[i, 'NAME'] = row['ward_name']
joined = join_temp.set_index('NAME').join(gs_2018_sum.rename('2018_GS_Sum'))

# vii Calculate percentage of green space in each ward
for i, row in joined.iterrows():
    joined.loc[i, 'gs_perc_2011'] = ((row['2011_GS_Sum'] / row['area_calc']) * 100)
    joined.loc[i, 'gs_perc_2018'] = ((row['2018_GS_Sum'] / row['area_calc']) * 100)

for i, row in joined.iterrows():
    joined.loc[i, 'gs_change'] = (row['gs_perc_2018'] - row['gs_perc_2011'])

# viii Show/hide table in output
print(joined.head(10))

# ix save shapefile with calculated columns
# joined.to_file("Output/gs_2011_2018_diff.shp")

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

# vi Data bounds and colour scale
gs_plot = joined.plot(column='gs_change', ax=ax, vmin=-25, vmax=25, cmap='RdYlGn',
                       legend=True, cax=cax, legend_kwds={'label': 'Green Space Percentage Change (2011-2018) (%)'})

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
ax.set_title('Change In Proportion Of Area That Is Green Space (2011-2018)',
             fontweight="bold")

# viii save the map
fig.savefig('Output/Green_Space_Change.png', dpi=300, bbox_inches='tight')