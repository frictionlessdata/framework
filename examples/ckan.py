import requests
from pprint import pprint
from jsontableschema import Table
from goodtables import Inspector, preset

@preset('ckan')
def ckan_preset(source, **options):
    errors = []
    tables = []
    url = '%s/api/3/action/package_search' % source
    data = requests.get(url).json()
    for package in data['result']['results']:
        for resource in package['resources']:
            if not resource['url'].endswith('.csv'):
                continue
            table = Table(resource['url'])
            extra = {
                'dataset': package['title'],
                'resource': resource['name'],
                'publisher': package['organization']['name']
            }
            tables.append({
                'table': table,
                'extra': extra,
            })
    return errors, tables

inspector = Inspector(custom_presets=[ckan_preset])
report = inspector.inspect('http://data.surrey.ca', preset='ckan')
pprint(report)
