import json
import logging

import requests

ESRI_POINT = 'esriGeometryPoint'
ESRI_MULTIPOINT = 'esriGeometryMultipoint'
ESRI_POLYLINE = 'esriGeometryPolyline'
ESRI_POLYGON = 'esriGeometryPolygon'
ESRI_ENVELOPE = 'esriGeometryEnvelope'


def convert_rings(response):
  # convert geometry/rings to Polygon points for gmaps
  rings = response['features'][0]['geometry']['rings'][0]
  polycoords = []

  for coord in rings:
    polycoords.append({
      'lng': coord[0],
      'lat': coord[1]
    })
  response['features'][0]['geometry'] = polycoords
  return response


class GISUrbanHeatIndex:
  base_url = 'https://mapprod2.environment.nsw.gov.au/arcgis/rest/services/UHGC/UHGC/MapServer/0/query'

  def __init__(self):
    self.logger = logging.getLogger(GISUrbanHeatIndex.__name__)

  """
  Example params: 
  {
      'geometry': {"x" : 151.209900, "y" : -33.865143, "spatialReference" : {"wkid" : 4283}}
      'geometryType': GISUrbanHeatIndex.POINT',
      'outFields': '*',
      'inSR': 4283
  }
  """

  def retrieve_point(self, params, rformat='json'):
    params['f'] = rformat
    params['geometry'] = json.dumps(params['geometry'])
    params['outFields'] = 'UHI_16_m,SA1_MAIN16,SA1_7DIG16,SA2_MAIN16,SA2_5DIG16'
    params['inSR'] = '4283'

    self.logger.info("Creating request with params={}".format(params))

    request = requests.get(self.base_url, params=params)
    self.logger.info("URL: {}".format(request.url))

    if request.status_code == 200:
      response = request.json()
      response = convert_rings(response)
      return response

    self.logger.error("Error retrieving data from GIS API: {} - {}"
                      .format(request.status_code, request.content))


class GISGreenCover:
  base_url = 'https://mapprod2.environment.nsw.gov.au/arcgis/rest/services/UHGC/UHGC/MapServer/2/query'
  out_fields = [
    # 'LGA',
    # 'Region',
    # 'District',
    # 'LandType',
    # 'MB_Reclass',
    # 'MMB_Type',
    'FulArRatio',
    # 'AreaGrass',
    # 'AreaShrub',
    # 'ArTr03_10m',
    # 'ArTr10_15m',
    # 'ArTr15mPl',
    # 'ArAnyTree',
    # 'ArAnyVeg',
    # 'ArShrTree',
    # 'PerGrass',
    # 'PerShrub',
    # 'PerTr03_10',
    # 'PerTr10_15',
    # 'PerTr15mPl',
    # 'PerAnyTree',
    # 'PerShrTr',
    'PerAnyVeg',
    # 'PerNonVeg',
    # 'DataCover',
    # 'CompDataYN'
  ]

  def __init__(self):
    self.logger = logging.getLogger(GISGreenCover.__name__)

  def retrieve_point(self, params, rformat='json'):
    params['f'] = rformat
    params['geometry'] = json.dumps(params['geometry'])
    params['outFields'] = ",".join(self.out_fields)
    params['inSR'] = '4283'

    self.logger.info("Creating request with params={}".format(params))

    request = requests.get(self.base_url, params=params)
    self.logger.info("URL: {}".format(request.url))

    if request.status_code == 200:
      if request.status_code == 200:
        response = request.json()
        response = convert_rings(response)
        return response

    self.logger.error("Error retrieving data from GIS API: {} - {}"
                      .format(request.status_code, request.content))


def test_UHI():
  gis = GISUrbanHeatIndex()
  result = gis.retrieve_point(
      params={
        'geometry': {"x": 151.209900, "y": -33.865143},
        'geometryType': ESRI_POINT,
      })
  # print(result)
  for feature in result['features']:
    if feature.get('attributes') is not None:
      print(json.dumps(feature['attributes'], indent=2))


def test_GreenCover():
  gc = GISGreenCover()
  result = gc.retrieve_point(
      params={
        'geometry': {"x": 151.209900, "y": -33.865143},
        'geometryType': ESRI_POINT,
      })
  # print(result)
  for feature in result['features']:
    if feature.get('attributes') is not None:
      print(json.dumps(feature['attributes'], indent=2))


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  # test_UHI()
  test_GreenCover()
