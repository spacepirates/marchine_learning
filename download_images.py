import urllib
import json
import os


jsonstream = urllib.urlopen("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/?output=json.indented")
JSONObject = json.load(jsonstream)

sol_data = JSONObject['nodes']
for x in range(0, len(sol_data)):
    solNameData = sol_data[x]
    sol_name = solNameData['name']
    dir_name = "images/" + sol_name

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        result = urllib.urlopen("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/" + sol_name + "?output=json.indented" )
        imageJsonObject = json.load(result)
        image_data = imageJsonObject['leaves']
        for x in range(0, len(image_data)):
            var = image_data[x]
            image_string = var['name']
            
            if image_string.endswith(".IMG") and "_F" in image_string:
                url_result = urllib.urlretrieve("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/" + sol_name + "/" + image_string + "/0/image[]?output=gif", dir_name + "/" + image_string[0:-4] + ".gif")

