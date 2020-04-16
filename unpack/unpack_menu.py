# !!! READ ME !!!
# This script will not work as is if running as the current git repo.
# Due to git LFS limits, the git repo does not include the GEDI hdf5 files or the GADM country files that are needed to run this.


# Other imports

import h5py, numpy as np, pandas as pd, geopandas as gpd

from geopandas.tools import sjoin

from shapely.geometry import Point

import os

 

# Top level dir

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

idir = os.path.join(THIS_FOLDER, 'GEDI_files')

# List files (full paths)

h5files = []

for dirpath, subdirs, files in os.walk(idir):

    for x in files:

        if x.endswith(".h5"):

            h5files.append(os.path.join(dirpath, x))

 

# Temporary code!!

# h5files = h5files[483:]
 

# GEDI beams

beams = [u'BEAM0000', u'BEAM0001', u'BEAM0010', u'BEAM0011', u'BEAM0101', u'BEAM0110', u'BEAM1000', u'BEAM1011']

#[u'METADATA']

 

beamkeysgeo = ['lon_lowestmode','lat_lowestmode','elev_lowestmode']

beamkeys = ['shot_number','rh100','fhd_normal','cover','pai','l2b_quality_flag']

 

# maybe add num_detectedmodes (number of detected modes in return waveform)

# and pavd_z (Plant Area Volume Density profile)

# and cover_z

# and solar zenith angle

 

painames = ['pai_' + str(z) for z in range(5,155,5)]

dfnames = ['X','Y','Z','shotNum','rh100','fhd_norm','cover','pai', 'l2b_QF'] + painames

 

# Read in zone shapefile

col_inshp = os.path.join(THIS_FOLDER, 'shapefiles_COL/gadm36_COL_0.shp')
bol_inshp = os.path.join(THIS_FOLDER, 'shapefiles_BOL/gadm36_BOL_0.shp')
bra_inshp = os.path.join(THIS_FOLDER, 'shapefiles_BRA/gadm36_BRA_0.shp')
chl_inshp = os.path.join(THIS_FOLDER, 'shapefiles_CHL/gadm36_CHL_0.shp')
ecu_inshp = os.path.join(THIS_FOLDER, 'shapefiles_ECU/gadm36_ECU_0.shp')
guy_inshp = os.path.join(THIS_FOLDER, 'shapefiles_GUY/gadm36_GUY_0.shp')
pry_inshp = os.path.join(THIS_FOLDER, 'shapefiles_PRY/gadm36_PRY_0.shp')
per_inshp = os.path.join(THIS_FOLDER, 'shapefiles_PER/gadm36_PER_0.shp')
sur_inshp = os.path.join(THIS_FOLDER, 'shapefiles_SUR/gadm36_SUR_0.shp')
ury_inshp = os.path.join(THIS_FOLDER, 'shapefiles_URY/gadm36_URY_0.shp')
ven_inshp = os.path.join(THIS_FOLDER, 'shapefiles_VEN/gadm36_VEN_0.shp')
arg_inshp = os.path.join(THIS_FOLDER, 'shapefiles_ARG/gadm36_ARG_0.shp')



col = gpd.read_file(col_inshp)
bol = gpd.read_file(bol_inshp)
bra = gpd.read_file(bra_inshp)
chl = gpd.read_file(chl_inshp)
ecu = gpd.read_file(ecu_inshp)
guy = gpd.read_file(guy_inshp)
pry = gpd.read_file(pry_inshp)
per = gpd.read_file(per_inshp)
sur = gpd.read_file(sur_inshp)
ury = gpd.read_file(ury_inshp)
ven = gpd.read_file(ven_inshp)
arg = gpd.read_file(arg_inshp)


field = 'GID_0'

col = col[col[field]=='COL']
bol = bol[bol[field]=='BOL']
bra = bra[bra[field]=='BRA']
chl = chl[chl[field]=='CHL']
ecu = ecu[ecu[field]=='ECU']
guy = guy[guy[field]=='GUY']
pry = pry[pry[field]=='PRY']
per = per[per[field]=='PER']
sur = sur[sur[field]=='SUR']
ury = ury[ury[field]=='URY']
ven = ven[ven[field]=='VEN']
arg = arg[arg[field]=='ARG']

# col, bol, bra, chl, ecu, guy, pry, per, sur, ury, ven
all_zshp = [arg]

print("Shapefiles are prepared")


# Loop through each country
for country in range(len(all_zshp)):
    zshp = all_zshp[country]

    print("{} has started unpacking".format(country))

    # Loop through files and process

    for h5f in h5files:

        beamdflist = []

        for i in beams:

            # Check that file is valid then read dataset to object

            try:

                f = h5py.File(h5f, 'r')

                f.close()

                #list(f.keys())

            except IOError:

                with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                    tf.write('IOError error in file ' + h5f + ', beam ' + i + '\n')

                continue

            with h5py.File(h5f, 'r') as f:

                # Read beam to object, skip if bad

                try:

                    dset = f[i]

                except KeyError:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('Key error in file ' + h5f + ', beam ' + i + '\n')

                    continue

               

                # Check for geobeamkeys

                dlist = []

                for j in beamkeysgeo:

                    try:

                        xx = dset['geolocation'][j]

                        dlist.append(np.array(xx))

                    except KeyError:

                        with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                            tf.write('Key error in file ' + h5f + ', beam ' + i + '\n')

                        continue

                for j in beamkeys:

                    try:

                        yy = dset[j]

                        dlist.append(np.array(yy))

                    except KeyError:

                        with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                            tf.write('Key error in file ' + h5f + ', beam ' + i + '\n')

                        continue

                if len(dlist) == 0:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('No datasets in file ' + h5f + ', beam ' + i + '\n')

                    continue

                ddf = np.stack(dlist, axis=1)

     

                # Check for pai_z

                try:

                    zz = dset['pai_z']

                    ddf = np.hstack([ddf, zz])

                except KeyError:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('Key error in file ' + h5f + ', beam ' + i + '\n')

                    continue

     

                # Check dimension of ddf (in case pai_z has missing columns)

                if ddf.shape[1] < 39:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('Missing columns in ' + h5f + ', beam ' + i + '\n')

                    continue

     

                # Convert to dataframe

                ddf = pd.DataFrame(ddf, columns=dfnames)

                # Check if df is empty

                if ddf.shape[0] < 1:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('No datasets in ' + h5f + ', beam ' + i + '\n')

                    continue

     

                # Check if there are any good footprints

                ddf = ddf.loc[ddf.l2b_QF==1]

                if ddf.shape[0] < 1:

                    with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                        tf.write('No quality footprints in ' + h5f + ', beam ' + i + '\n')

                    continue

     

                # Add column for beam id

                ddf['beam'] = ddf.shape[0]*[i]

     

                # Append datafrmaes to list

                beamdflist.append(ddf)

               

        # Concatenate beam dataframes

        if len(beamdflist) > 0:

            ddf = pd.concat(beamdflist)

        else:

            with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                tf.write('No beams to concatenate in ' + h5f + '\n')

            continue

       

        # Convert to geodataframe

        geometry = [Point(xy) for xy in zip(ddf.X, ddf.Y)]

        ddf = ddf.drop(['X', 'Y'], axis=1)

        crs = {'init': 'epsg:4326'}

        gdf = gpd.GeoDataFrame(ddf, crs=crs, geometry=geometry) 

        # Get intersections with zone

        gdf.crs = zshp.crs

        ix = sjoin(gdf, zshp, how='inner')

        if ix.shape[0] >= 2:

            # opath = '/unpacked_files/files/'

            # ofile = opath + os.path.basename(h5f).strip('.h5') + '_qc.shp'

            ix.to_file(os.path.join(THIS_FOLDER, 'unpacked_{}/test.shp'.format(country)))

        else:

            with open(os.path.join(THIS_FOLDER, 'unpacked_{}/errors.txt'.format(country)), 'a') as tf:

                tf.write('No points in zone for file ' + h5f + '\n')

    print("{} is done unpacking!".format(country))
    print("---------------------------")
