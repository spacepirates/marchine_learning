import urllib
import json
import os

jsonstream = urllib.urlopen("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/?output=json.indented")
JSONObject = json.load(jsonstream)

sol_data = JSONObject['nodes'][2]
for x in range(0, len(sol_data)):
    dir_name = os.mkdir(sol_data['name'])

print(sol_data['name'])
solNameData = sol_data['name']

result = urllib.urlopen("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/" + solNameData + "?output=json.indented" )

imageJsonObject = json.load(result)

image_data = imageJsonObject['leaves']

for x in range(0, len(image_data)):
    var = image_data[x]
    image_string = var['name']
    if image_string.endswith(".IMG") and "_F" in image_string:
        url_result = urllib.urlretrieve("http://data1.jpl.nasa.gov/pds/imaging/msl/MSLHAZ_0XXX/DATA/" + solNameData + "/" + image_string + "/0/image[]?output=gif", dir_name/image_string[0:-4] + ".gif")
        print(url_result)
        print(image_string)
