import csv
import os

import randgen.utils as utils

class Importer:

    def __init__(self, filename, fetchBy, delimiter=','):
        self.filename = filename
        self.fetchBy = fetchBy
        self.delimiter = delimiter
        self.data = None
    
    @property
    def filename(self):
        return self.filename
    
    @property
    def delimiter(self):
        return self.delimiter
    
    @filename.setter
    def filename(self, filename):
        self.filename = filename
    
    @delimiter.setter
    def delimiter(self, delimiter):
        self.delimiter = delimiter
    
    def importData(self):
        if not utils.isValidFile(self.filename, '.csv'):
            return None
        with open(self.filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            if self.fetchBy == 0:
                data = []
                for row in csv_reader:
                    data.append(row)
                data = tuple(zip(*data))
            if self.fetchBy == 1:
                rowData = []
                headers = []
                rowIndex = 0
                for row in csv_reader:
                    if rowIndex == 0:
                        headers = row
                    else:
                        rowData.append(row)
                    rowIndex += 1
                rowData = list(zip(*rowData))
                data = dict((header, rowElem) for header, rowElem in zip(headers, rowData))
            return data