##### Step 1: Classify data


##### Step 2: Calculate % green space of each electoral ward

import numpy as np
import rasterio as rio
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterstats import zonal_stats

# open green space raster and read the data
with rio.open('data_files/LCM2015_Aggregate_100m.tif') as dataset:
    xmin, ymin, xmax, ymax = dataset.bounds
    crs = dataset.crs
    landcover = dataset.read(1)
    affine_tfm = dataset.transform

wards = gpd.read_file('data_files/London_Ward.shp').to_crs(crs)

#count (number of pixels) for each of the unique values in the array:

def count_unique(array, nodata=0):
    '''
    Count the unique elements of an array.

    :param array: Input array
    :param nodata: nodata value to ignore in the counting

    :returns count_dict: a dictionary of unique values and counts
    '''
    count_dict = {}
    for val in np.unique(array):
        if val == nodata:
            continue
        count_dict[str(val)] = np.count_nonzero(array == val)
    return count_dict

unique_landcover = count_unique(landcover)
print(unique_landcover)

##### Step 3: Calculate change from previous instance


##### Step 4: Output map showing GS changes







