import requests

response = requests.post('https://lpdaacsvc.cr.usgs.gov/appeears/api/login', auth=('nau_canopy_project', 'T2j%m7Y#lx'))
token_response = response.json()
print(token_response)
print("\n")

params = {'limit': 2, 'offset': 2}
response = requests.get(
    'https://lpdaacsvc.cr.usgs.gov/appeears/api/product',
    params=params)
product_response = response.json()
print(product_response)
print("\n")

params2 = '''{
  "task_type": "point",
  "task_name": "Point Example",
  "params":
  {
    "dates": [
    {
      "startDate": "01-01-2015",
      "endDate": "12-31-2016"
    }],
    "layers": [
    {
      "layer": "LST_Day_1km",
      "product": "MOD11A2.006"
    },
    {
      "layer": "LST_Night_1km",
      "product": "MOD11A2.006"
    },
    {
      "layer": "_500m_16_days_NDVI",
      "product": "MYD13A1.006"
    }],
    "coordinates": [
    {
      "latitude": 44.97766115516424,
      "longitude": -93.26824955642223,
      "id": "Minneapolis",
      "category": "Urban"
    },
    {
      "latitude": 44.950103770941496,
      "longitude": -93.09091188758612,
      "id": "St. Paul",
      "category": "Urban"
    },
    {
      "latitude": 45.31713876128197,
      "longitude": -93.26879900693893,
      "id": "North",
      "category": "Rural"
    },
    {
      "latitude": 44.523559615015984,
      "longitude": -93.26367196440697,
      "id": "South",
      "category": "Rural"
    }]
  }
}'''


response = requests.get(
    'https://lpdaacsvc.cr.usgs.gov/appeears/api/product',
    params=params2)
product_response = response.json()
print(product_response)
