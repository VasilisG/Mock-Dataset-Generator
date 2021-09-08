import os

from randgen.datafields import *
from randgen.datafieldfactory import DataFieldFactory
from randgen.exporters import *
from randgen.exporterfactory import *
import randgen.utils as utils

class Dataset:
    
    def __init__(self, n, title, filename, path, type):
        self.n = n
        self.title = title
        self.filename = filename
        self.path = path
        self.type = type
        self.datafields = []
    
    def getN(self):
        return self.n
    
    def setN(self, n):
        self.n = n
    
    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def getFilename(self):
        return self.filename
    
    def setFilename(self, filename):
        self.filename = filename
    
    def getPath(self):
        return self.path
    
    def setPath(self, path):
        self.path = path
    
    def getType(self):
        return self.type
    
    def setType(self, type):
        self.type = type
    
    def addDatafield(self, datafield):
        self.datafields.append(datafield)
    
    def removeDatafield(self, datafield):
        self.datafields.remove(datafield)
    
    def getDatafields(self):
        return self.datafields

    def generateValues(self):
        result = []
        for field in self.datafields:
            field.setNumItems(self.n)
            result.append(field.generateValues())
        return list(zip(*result))
    
    def exportData(self):
        dataExporter = ExporterFactory.create(self)
        dataExporter.export()
    
    def jsonify(self):
        datasetKey = 'dataset_{unique_id}'.format(unique_id=str(id(self)))
        result = {
            datasetKey : {
                'info' : {
                    'n' : self.n,
                    'title' : self.title,
                    'filename' : self.filename,
                    'path' : self.path,
                    'type' : self.type
                },
                'datafields' : []
            }
        }
        for datafield in self.datafields:
            result[datasetKey]['datafields'].append(datafield.jsonify())
        return result

class DatasetManager:

    def __init__(self):
        self.datasets = []
    
    def addDataset(self, dataset):
        self.datasets.append(dataset)
    
    def removeDataset(self, dataset):
        self.datasets.remove(dataset)
    
    def getDatasets(self):
        return self.datasets
    
    def isJsonFile(self, filename):
        _, fileExtension = os.path.splitext(filename)
        return fileExtension == '.json'

    def saveToFile(self, filename):
        if not utils.isValidFile(filename, '.json'):
            return False
        result = {}
        for dataset in self.datasets:
            result.update(dataset.jsonify())
        with open(filename, 'w') as saveFile:
            json.dump(result, saveFile, indent=4)
        return True
    
    def importFile(self, filename):
        if not self.isJsonFile(filename):
            return False
        with open(filename, 'r') as inFile:
            content = json.load(inFile)
            self.datasets = []
            for _, datasetValues in content.items():
                dataset = Dataset(**datasetValues['info'])
                datafields = datasetValues['datafields']
                importDataField = None
                for datafield in datafields:
                    for fieldKey, values in datafield.items():
                        key = fieldKey.split('_')[0]
                        importDataField = DataFieldFactory.create(key, values)
                    if not importDataField is None:
                        dataset.addDatafield(importDataField)
                self.addDataset(dataset)