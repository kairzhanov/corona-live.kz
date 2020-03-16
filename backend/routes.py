import json
import scrape

from flask_restful import Resource
from datetime import datetime

class MainPage(Resource):
    def get(self):
        return {'Salem': 'Alem'}

class Stats(Resource):
  def get(self):
    #TODO: Add DB
    data = scrape.get_data_stats()
    #data.domestically_isolated
    #data.link
    res = {
        'domestically_isolated': data.domestically_isolated,
        'stationary_isolated': data.stationary_isolated,
        'dead': data.dead,
        'recovered': data.cured,
        'cases': data.infected,
    }
    return res

class News(Resource):
  def get(self):
    #TODO: Add DB
    data = scrape.get_data()

    res = [{
      'id': 0,
      'title': 'Bla bla title',
      'link': 'https://google.com',
      'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
      'cities': [{
          'id': 0,
          'name': 'Almaty',
          'cases': 7,
          'death': 0,
          'recovered': 0,
        },
        {
          'id': 1,
          'name': 'Nur-Sultan',
          'cases': 2,
          'death': 0,
          'recovered': 0,
        },
      ],
      'tags': [{
          'id': 355,
          'name': 'WTF tag name 1',
        },
        {
          'id': 134,
          'name': 'WTF tag name 2',
        },
      ],
      'type': 'news',
    },
  ]
    return json.dumps(res)

class Cities(Resource):
  def get(self):
    #TODO: Add scraper here and DB
    res = [
        {
        'id': 0,
        'name': 'Almaty',
        'cases': 7,
        'death': 0,
        'recovered': 0,
      },
      {
        'id': 1,
        'name': 'Nur-Sultan',
        'cases': 2,
        'death': 0,
        'recovered': 0,
      },
    ]
    return json.dumps(res)
