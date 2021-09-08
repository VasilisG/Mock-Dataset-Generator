from randgen.exporters import *

class ExporterFactory:
    
    @classmethod
    def create(cls, dataset):
        datasetType = dataset.getType()
        lookup = {
            'csv' : CsvExporter,
            'json' : JsonExporter,
            'xml' : XmlExporter
        }
        if datasetType in lookup:
            return lookup[datasetType](dataset)
        else:
            raise ValueError('Invalid export type: {}'.format(datasetType))