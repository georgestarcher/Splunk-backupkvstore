import requests
import json 
import csv
from ConfigParser import SafeConfigParser
import sys, getopt
import os

__author__ = "george@georgestarcher.com (George Starcher)"

def loadConfig(filename):

    global splunk_server
    global splunk_server_port
    global splunk_server_verify
    global backupFolder

    parser = SafeConfigParser()
    parser.read(filename)

    splunk_server = parser.get('splunk', 'splunk_server')
    splunk_server_port = parser.get('splunk', 'splunk_server_port')
    splunk_server_verify = parser.getboolean('splunk', 'splunk_server_verify')
    backupFolder = parser.get('splunk', 'backup_folder')

def getKVStoreData(url):

    url = url.replace('config','data')
    splunk_url = ''.join([url,'/?output_mode=json'])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(splunk_url,auth=(splunk_user,splunk_password),verify=splunk_server_verify,headers=headers)
    return json.loads(r.text)

def getKVStoreCollections():

    splunk_url = ''.join(['https://',splunk_server,':',splunk_server_port,'/servicesNS/-/-//storage/collections/config/?output_mode=json'])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(splunk_url,auth=(splunk_user,splunk_password),verify=splunk_server_verify,headers=headers)
    return json.loads(r.text) 

def outputCollectionDataToFile(name,data):

    outFile = "data_"+name+".bak" 
    json.dump(data,open(os.path.join(backupFolder,outFile),"wt"))

def outputCollectionDefToFile(name,data):

    outFile = "def_"+name+".bak"
    json.dump(data,open(os.path.join(backupFolder,outFile),"wt"))

if __name__ == "__main__":

    config_file = 'kvstore.conf'
    template = 'template.csv'
    app = ''
    collection = ''
    argv = sys.argv[1:]

    global splunk_user  
    global splunk_password 

    try:
        loadConfig(config_file)
    except Exception, e:
        print "Config File Error: %s" % e
        sys.exit(2)

    splunk_user = raw_input('enter Splunk user:')
    splunk_password = raw_input('enter Splunk password:')

    outputCollections = []

    collections=getKVStoreCollections()

    for collection in collections.get('entry'):
        collectionName = collection.get('name')        
        url = collection.get('id')
        collectionData = getKVStoreData(url)
        outputCollectionDefToFile(collectionName, collection)
        outputCollectionDataToFile(collectionName,collectionData)

