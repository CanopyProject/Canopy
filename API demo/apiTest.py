import requests

key1 = ('task_type','point')
key2 = ('task_name', 'API Test')

dates = { 'startDate' : '01-01-2015' ,  "endDate": "12-31-2016"}
key4 = [('dates' , dates )]

layers = { "layer": "LST_Day_1km", "product": "MOD11A2.006" }
key5 = [('layers' , layers )]

coordnates = {"latitude": 44.950103770941496, "longitude": -93.09091188758612, "id": "St. Paul", "category": "Urban"}
key6 = [("coordinates" , coordnates)]

key3 =  {'params' : [key4, key5, key6]}

payload = [(key1 , key2, ('params', key4), ('params', key5), ('params', key6)  )]


raw_data = requests.post("https://lpdaacsvc.cr.usgs.gov/appeears/", auth=("nau_canopy_project", "T2j%m7Y#lx"), data=payload ) 

print(raw_data)
print(raw_data.text)


