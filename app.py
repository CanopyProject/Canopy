from flask import Flask, request, render_template, request
from flask_mail import Mail
from flask_mail import Message
import geopandas as gpd
import zipfile as zpf
import glob
import os

# call statistic functions
import StatisticFunctions

# call generate csv file
import output

import csv
app = Flask(__name__, template_folder = 'templates')

# mail_settings = {
#     "MAIL_SERVER": 'smtp.gmail.com',
#     "MAIL_PORT": 465,
#     "MAIL_USE_TLS": False,
#     "MAIL_USE_SSL": True,
#     "MAIL_USERNAME": os.environ['email'],
#     "MAIL_PASSWORD": os.environ['password']
# }

# app.config.update(mail_settings)
# mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

# Takes in shapefile, tests validity
@app.route("/success.html/", methods = ["GET", "POST"] )
def readShapefile():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    geomValid = True
    countryVal = request.form["country"]
    functionList = request.form.getlist("function")
    if request.method == "POST":
        if request.files["shapefileInput"].filename == "":
            if countryVal == "0":
                return render_template("",204)
            else:
                selectedCountry = request.form["country"]
                fp = os.path.join(THIS_FOLDER, 'unpack')
                os.chdir(fp)
                if selectedCountry == "ARG":
                    currentShapefile = glob.glob("*_ARG_shp")
                    folder = "unpack/unpacked_11"
                elif selectedCountry == "BOL":
                    currentShapefile = glob.glob("*_BOL_shp")
                    folder = "unpack/unpacked_1"
                elif selectedCountry == "BRA":
                    currentShapefile = glob.glob("*_BRA_shp")
                    folder = "unpack/unpacked_2"
                elif selectedCountry == "CHL":
                    currentShapefile = glob.glob("*_CHL_shp")
                    folder = "unpack/unpacked_3"
                elif selectedCountry == "COL":
                    currentShapefile = glob.glob("*_COL_shp")
                    folder = "unpack/unpacked_0"
                elif selectedCountry == "ECU":
                    currentShapefile = glob.glob("*_ECU_shp")
                    folder = "unpack/unpacked_4"
                elif selectedCountry == "GUY":
                    currentShapefile = glob.glob("*_GUY_shp")
                    folder = "unpack/unpacked_5"
                elif selectedCountry == "PRY":
                    currentShapefile = glob.glob("*_PRY_shp")
                    folder = "unpack/unpacked_6"
                elif selectedCountry == "PER":
                    currentShapefile = glob.glob("*_PER_shp")
                    folder = "unpack/unpacked_7"
                elif selectedCountry == "SUR":
                    currentShapefile = glob.glob("*_SUR_shp")
                    folder = "unpack/unpacked_8"
                elif selectedCountry == "URY":
                    currentShapefile = glob.glob("*_URY_shp")
                    folder = "unpack/unpacked_9"
                elif selectedCountry == "VEN":
                    currentShapefile = glob.glob("*_VEN_shp")
                    folder = "unpack/unpacked_10"
                os.chdir(THIS_FOLDER)
        else:
            # Take in file string
            currentShapefile = request.files["shapefileInput"]

            # Change directory to temporary folder
            fp = os.path.join(THIS_FOLDER, 'shapefiles/temporary')
            os.chdir(fp)

            # Save zip file to current directory
            currentShapefile.save(currentShapefile.filename)

            # Extract zip file in order to access .shp file
            ZIP = zpf.ZipFile(currentShapefile)
            ZIP.extractall(fp)

            # Search for files that have string .shp
            gpdfile = glob.glob("*.shp")[0]

            # Read in file with geopandas
            # read_file returns GeoDataFrame which contains a GeoSeries
            readfile = gpd.read_file(gpdfile)

            # Test validity of the shapefile
            # geometry is the GeoSeries of GeoDataFrame
            # GeoSeries has is_valid which returns dtype('bool')
            # Take first element of series (True or False)
            if not (readfile.geometry.is_valid[0]):
                geomValid = False
            os.chdir(THIS_FOLDER)
            os.chdir(THIS_FOLDER)
        # Send <<currentShapefile>> (selected variable) to Monsoon here
        # Demo stats functions here also
        Area=100

        #list store the result
        result = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        fp0 = os.path.join(THIS_FOLDER, folder)
        fp = os.path.join(fp0, 'test.shp')

        data = gpd.read_file(fp)
        height_array = []
        ObList = []
        for index, row in data.iterrows():
            height_array.append(row['rh100'])
            ObList.append(row['l2b_QF'])

        if "1" in functionList:
            result[0] = StatisticFunctions.NumberofObservations(ObList)
            output.writeCSV(result)
        if "3" in functionList:
            result[2] = StatisticFunctions.DensityofObservations(ObList,Area)
            output.writeCSV(result)
        if "4" in functionList:
            result[3] = StatisticFunctions.StandardDeviationOfDensityOfObservations(ObList)
            output.writeCSV(result)
        if "5" in functionList:
            result[4] = StatisticFunctions.MeanVegetationHeight(height_array)
            output.writeCSV(result)
        if "6" in functionList:
            result[5] = StatisticFunctions.StandardDeviationOfVegetationHeight(height_array)
            output.writeCSV(result)
        if "7" in functionList:
            result[6] = StatisticFunctions.DataQuality(ObList)
            output.writeCSV(result)


        # emailReceiver = request.form["emailInput"]
        # message = Message("Test",
        #         sender = "naucanopyproject@gmail.com",
        #         recipients = [emailReceiver])
        # with app.open_resource("static\\bg.jpg") as fp:
        #     message.attach("static\\bg.jpg", "img/png", fp.read())
        # mail.send(message)

    # Must return something
    # Return ( '', 204 ) makes sure the website does not change pages
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
