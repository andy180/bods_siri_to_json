#!/bin/env python
import requests
import zipfile
import xmltodict
import json
import xml.etree.ElementTree as ET
import jsonify
from io import BytesIO

def fetchUpdate(operatorList=['GNEL']):
    try:
        r = requests.get('https://data.bus-data.dft.gov.uk/avl/download/bulk_archive')
    except:
        print('Unable to obtain updated bulk archive from DfT.')
        return

    zipdata = BytesIO()
    zipdata.write(r.content)

    print('Extracting ZIP data...')
    ziphandler = zipfile.ZipFile(zipdata)
    siri = ziphandler.open('siri.xml')

    siriXml = siri.read().decode('utf-8')

    siriNode = ET.fromstring(siriXml)

    siriNs = 'http://www.siri.org.uk/siri'
    ns = {'siri': siriNs}

    activityLocal = []
    for op in operatorList:
        operatorFilter = ".='%s'" % op
        xpathSelector = [
            'siri:ServiceDelivery',
            'siri:VehicleMonitoringDelivery',
            'siri:VehicleActivity',
            'siri:MonitoredVehicleJourney',
            'siri:OperatorRef[%s]' % operatorFilter,
            '..',
            '..'
        ]

        activityNodes = siriNode.findall('./%s' % '/'.join(xpathSelector), namespaces=ns)
        for activity in activityNodes:
            activityDict = xmltodict.parse(ET.tostring(activity, encoding='utf8', method='xml', default_namespace=siriNs))
            activityLocal.append(activityDict)
    return activityLocal

if __name__ == "__main__":
    # List of operators to include, from the NOC tables
    nocTable = ['SDVN']

TheData=fetchUpdate(operatorList=nocTable)

print(json.dumps(TheData,indent=4, sort_keys=True))



