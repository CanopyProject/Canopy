# this file is an example of how to access the data in the test.shp for the tech demo

import os

import geopandas as gpd

# to access the file that holds the data

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# edit this line of code to the new path from your file, currently grabs from Colombia only
# only need to edit the part in 'unpacked_COL/test.shp' to the path you'd take to get to the test.shp file
# keep the THIS_FOLDER part
fp = os.path.join(THIS_FOLDER, 'unpacked_0/test.shp')

data = gpd.read_file(fp)


# available column names: 'shot_number','rh100','fhd_normal','cover','pai','l2b_QF'

# rh100 = "Height above ground of the received waveform signal start", assuming just = height
# fhd_normal = "Foliage height diversity index calculated by vertical foliage profile normalized by total plant area index"
# cover = "Total canopy cover, defined as the percent of the ground covered by the vertical projection of canopy material"

# assuming current most useful col for clustering is cover and pai
# assuming current most useful col for stat. func. is rh100 and l2b_quality_flag


# to read everything in a column (in this case, pai) to an array and use (print) the array

for index, row in data.iterrows():
	pai_array = row['pai']
	print("PAI at index {0} is: {1:f}".format(index, pai_array))

