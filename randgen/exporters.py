import csv
import json
import xml.etree.ElementTree as ET

class DataExporter:

    def __init__(self, dataset):
        self.dataset = dataset
    
    def getDataset(self):
        return self.dataset
    
    def setDataset(self, dataset):
        self.dataset = dataset
    
    def getDatasetInfo(self):
        filename = self.dataset.getFilename()
        path = self.dataset.getPath()
        data = self.dataset.generateValues()
        headers = data[0]
        return (filename, path, data, headers)

    def export(self):
        pass

class CsvExporter(DataExporter):

    def export(self):
        filename, path, data, headers = self.getDatasetInfo()
        outFile = open(path + '/' + filename + '.csv', 'w', encoding='utf8')
        writer = csv.DictWriter(outFile, fieldnames=headers, lineterminator = '\n')
        writer.writeheader()
        for row in data[1:]:
            entry = {}
            for index, value in enumerate(row):
                entry.update({headers[index] : value})
            writer.writerow(entry)
        outFile.close()

class JsonExporter(DataExporter):

    def export(self):
        filename, path, data, headers = self.getDatasetInfo()
        result = []
        for row in data[1:]:
            entry = {}
            for index, value in enumerate(row):
                entry.update({headers[index] : value})
            result.append(entry)
        with open(path + '/' + filename + '.json', 'w') as outFile:
            json.dump(result, outFile, indent=4)

class XmlExporter(DataExporter):
    
    def export(self):
        filename, path, data, headers = self.getDatasetInfo()
        root = ET.Element('dataset')
        for row in data[1:]:
            entry = ET.Element('entry')
            root.append(entry)
            for index, value in enumerate(row):
                valueEntry = ET.SubElement(entry, headers[index])
                valueEntry.text = str(value)
        tree = ET.ElementTree(root)
        with open(path + '/' + filename + '.xml', 'wb') as outFile:
            tree.write(outFile)