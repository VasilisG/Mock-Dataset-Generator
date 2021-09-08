import csv
import datetime
import random
import string
import sys

from randgen.importers import Importer

class AbstractField:

    def __init__(self, name='datafield'):
        self.name = name
        self.numItems = 0
        self.id = self.__class__.__name__.lower() + '_' + str(id(self))
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def setNumItems(self, numItems):
        self.numItems = numItems
    
    def generateValue(self):
        pass
    
    def jsonify(self):
        return {
            self.id : {
                'name' : self.name
            }
        }
        
    def generateValues(self):
        result = [self.name]
        for _ in range(self.numItems):
            value = self.generateValue()
            result.append(value)
        return result

class CityField(AbstractField):

    def __init__(self, name, country=None):
        super().__init__(name)
        self.country = country
        self.cities = self.fetchCities()
    
    def getCountry(self):
        return self.country
    
    def setCountry(self, country):
        self.country = country
    
    def getCities(self):
        return self.cities
    
    def fetchCities(self):
        cities = {}
        with open('csv/cities.csv', 'r', encoding='utf-8') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for index, row in enumerate(csvReader):
                if index > 0:
                    if cities.get(row[1]) == None:
                        cities[row[1]] = [row[0]]
                    else:
                        cities[row[1]].append(row[0])
        return cities
    
    def generateValue(self):
        randomCity = None
        if self.country == None:
            listOfCities = random.choice(list(self.cities.values()))
        else:
            if self.cities.get(self.country) != None:
                listOfCities = self.cities[self.country]
            else:
                return ''
        randomCity = random.choice(listOfCities)
        return randomCity
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['country'] = self.country
        return result

class CountryField(AbstractField):

    def __init__(self, name, abbr=False):
        super().__init__(name)
        self.abbr = abbr
        self.countries = self.fetchCountries()
    
    def getAbbr(self):
        return self.abbr
    
    def setAbbr(self, abbr):
        self.abbr = abbr
    
    def getCountries(self):
        return self.countries
    
    def fetchCountries(self):
        countries = []
        with open('csv\countries.csv', 'r') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for index, row in enumerate(csvReader):
                if index > 0:
                    countries.append([row[0], row[3]])
        return countries
    
    def generateValue(self):
        country = random.choice(self.countries)
        return country[0] if self.abbr else country[1]

    def jsonify(self):
        result = super().jsonify()
        result[self.id]['abbr'] = self.abbr
        return result

class DateField(AbstractField):

    LOWER_YEAR = 1900
    UPPER_YEAR = 2080

    def __init__(self, name, dateFormat='%m-%d-%Y', fromYear=None, fromMonth=1, fromDay=1, toYear=None, toMonth=1, toDay=1, addTime=True):
        super().__init__(name)
        self.dateFormat = dateFormat
        self.fromYear = fromYear
        self.fromMonth = fromMonth
        self.fromDay = fromDay
        self.toYear = toYear
        self.toMonth = toMonth
        self.toDay = toDay
        self.addTime = addTime
    
    def getDateFormat(self):
        return self.dateFormat
    
    def setDateFormat(self, dateFormat):
        self.dateFormat = dateFormat
    
    def getFromYear(self):
        return self.fromYear if self.fromYear != None and self.fromYear > 0 else self.LOWER_YEAR
    
    def setFromYear(self, fromYear):
        self.fromYear = fromYear
    
    def getFromMonth(self):
        return self.fromMonth
    
    def setFromMonth(self, fromMonth):
        self.fromMonth = fromMonth
    
    def getFromDay(self):
        return self.fromDay
    
    def setFromDay(self, fromDay):
        self.fromDay = fromDay
    
    def getToYear(self):
        return self.toYear if self.toYear != None and self.toYear > 0 else self.UPPER_YEAR
    
    def setToYear(self, toYear):
        self.toYear = toYear
    
    def getToMonth(self):
        return self.toMonth
    
    def setToMonth(self, toMonth):
        self.toMonth = toMonth
    
    def getToDay(self):
        return self.toDay
    
    def setToDay(self, toDay):
        self.toDay = toDay
    
    def getMonth(self, month):
        return month if month >= 1 and month <= 12 else 1
    
    def getDay(self, day):
        return day if day >= 1 and day <= 31 else 1

    def generateValue(self):
        cleanFromYear = self.getFromYear()
        cleanToYear = self.getToYear()
        fromMonth = self.getMonth(self.fromMonth)
        fromDay = self.getDay(self.fromDay)
        toMonth = self.getMonth(self.toMonth)
        toDay = self.getMonth(self.toDay)
        if self.addTime:
            hour = random.randint(0,23)
            minute = random.randint(0,59)
            second = random.randint(0,59)
            startDate = datetime.datetime(cleanFromYear, fromMonth, fromDay, hour, minute, second)
            endDate = datetime.datetime(cleanToYear, toMonth, toDay, hour, minute, second)
        else:
            startDate = datetime.date(cleanFromYear, fromMonth, fromDay)
            endDate = datetime.date(cleanToYear, toMonth, toDay)

        if endDate < startDate:
            endDate, startDate = startDate, endDate

        diff = endDate - startDate
        randDays = random.randrange(diff.days)
        randomDate = startDate + datetime.timedelta(randDays)
        randomDate = randomDate.strftime(self.dateFormat)

        return str(randomDate)
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['dateFormat'] = self.dateFormat
        result[self.id]['fromYear'] = self.fromYear
        result[self.id]['fromMonth'] = self.fromMonth
        result[self.id]['fromDay'] = self.fromDay
        result[self.id]['toYear'] = self.toYear
        result[self.id]['toMonth'] = self.toMonth
        result[self.id]['toDay'] = self.toDay
        result[self.id]['addTime'] = self.addTime
        return result

class EmailField(AbstractField):

    LOCAL_PARTS = [
        'johndoe',
        'janedoe',
        'johnsmith',
        'janesmith'
    ]

    DOMAINS = [
        'test.com',
        'example.com'
    ]

    def __init__(self, name, unique=True):
        super().__init__(name)
        self.currentIndex = 0
        self.unique = unique
    
    def getUnique(self):
        return self.unique
    
    def setUnique(self, unique):
        self.unique = unique
    
    def generateValue(self):
        self.currentIndex += 1
        if self.unique:
            return random.choice(self.LOCAL_PARTS) + str(self.currentIndex) + '@' + random.choice(self.DOMAINS)
        else:
            return random.choice(self.LOCAL_PARTS) + '@' + random.choice(self.DOMAINS)
    
    def jsonify(self):
        return {
            self.getId() : {
                'name' : self.name,
                'unique' : self.unique
            }
        }

class IncrementField(AbstractField):

    def __init__(self, name, startValue=0):
        super().__init__(name)
        self.startValue = startValue
        self.currentIndex = self.startValue
    
    def getStartingValue(self):
        return self.startValue
    
    def setStartingValue(self, startValue):
        self.startValue = startValue
    
    def generateValue(self):
        self.currentIndex += 1
        return self.currentIndex
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['startValue'] = self.startValue
        return result

class IpAddressField(AbstractField):
    
    IPv_4 = 0
    IPv_6 = 1
    IP_BOTH = 2

    def __init__(self, name, type=IP_BOTH):
        super().__init__(name)
        self.name = name
        self.type = type
    
    def getType(self):
        return self.type
    
    def setType(self, type):
        self.type = type
    
    def generateIPv4(self):
        return ":".join(['{}'.format(random.randint(0,255)) for _ in range(4)])
    
    def generateIPv6(self):
        return ":".join(["%x" % random.randint(0,65535) for _ in range(8)])
    
    def generateIP(self, type):
          if type == self.IPv_4:
            return self.generateIPv4()
          elif type == self.IPv_6:
            return self.generateIPv6()
    
    def generateValue(self):
        if self.type == self.IP_BOTH:
            addrType = random.randint(self.IPv_4, self.IPv_6)
            return self.generateIP(addrType)
        else:
            return self.generateIP(self.type)

    def jsonify(self):
        result = super().jsonify()
        result[self.id]['type'] = self.type
        return result

class NameField(AbstractField):

    NAMES = [
        'JOHN DOE',
        'JANE DOE',
        'JOHN SMITH',
        'JANE SMITH'
    ]

    def generateValue(self):
        return random.choice(self.NAMES)
    
    def jsonify(self):
        return super().jsonify()

class NumberField(AbstractField):

    def __init__(self, name, type="int", lowerBound=None, upperBound=None, continuous=True, discretValues=None, precision=2, symbolPrefix='', symbolSuffix=''):
        super().__init__(name)
        self.type = type
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.continuous = continuous
        self.discretValues = discretValues
        self.precision = precision
        self.symbolPrefix = symbolPrefix
        self.symbolSuffix = symbolSuffix
    
    def getLowerBound(self):
        return self.lowerBound
    
    def setLowerBound(self, lowerBound):
        self.lowerBound = lowerBound
    
    def getUpperBound(self):
        return self.upperBound
    
    def setUpperBound(self, upperBound):
        self.upperBound = upperBound
    
    def getContinuous(self):
        return self.continuous
    
    def setContinuous(self, continuous):
        self.continuous = continuous
    
    def getDiscretValues(self):
        return self.discretValues

    def setDiscretValues(self, discretValues):
        self.discretValues = discretValues
    
    def getPrecision(self):
        return self.precision
    
    def setPrecision(self, precision):
        self.precision = precision
    
    def getSymbolPrefix(self):
        return self.symbolPrefix
    
    def setSymbolPrefix(self, symbolPrefix):
        self.symbolPrefix = symbolPrefix
    
    def getSymbolSuffix(self):
        return self.symbolSuffix
    
    def setSymbolSuffix(self, symbolSuffix):
        self.symbolSuffix = symbolSuffix
    
    def validDiscretValues(self):
        for value in self.discretValues:
            if not isinstance(value, int) and not isinstance(value, float):
                return False
        return True

    def getNumber(self, lower, upper):
        if self.type == "int":
            return str(random.randint(lower, upper))
        elif self.type == "float":
            formatter = '{:.' + '{}'.format(self.precision) + 'f}'
            floatNumber = round(random.uniform(lower, upper), self.precision)
            return formatter.format(floatNumber)
    
    def getPrefixSymbol(self):
        return self.symbolPrefix + ' ' if self.symbolPrefix.strip() != '' else ''
    
    def getSuffixSymbol(self):
        return ' ' + self.symbolSuffix if self.symbolSuffix.strip() != '' else ''
     
    def generateValue(self):
        prefix = self.getPrefixSymbol()
        suffix = self.getSuffixSymbol()
        if self.continuous:
            lower = 0
            upper = 0
            if self.lowerBound == None and self.upperBound == None:
                if self.type == "int":
                    lower = -sys.maxsize + 1
                    upper = sys.maxsize
                elif self.type == "float":
                    lower = float("-inf")
                    upper = float("inf")
            elif self.lowerBound != None and self.upperBound == None:
                lower = self.lowerBound
                if self.type == "int":
                    upper = sys.maxsize
                elif self.type == "float":
                    upper = float("inf")
            elif self.lowerBound == None and self.upperBound != None:
                upper = self.upperBound
                if self.type == "int":
                    lower = -sys.maxsize + 1
                elif self.type == "float":
                    lower = float("-inf")
            else:
                lower = self.lowerBound
                upper = self.upperBound
            
            return prefix + self.getNumber(lower, upper) + suffix

        else:
            if self.discretValues == None or not len(self.discretValues):
                return None
            else:
                if self.validDiscretValues():
                    return prefix + str(random.choice(self.discretValues)) + suffix
                else:
                    return None
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['type'] = self.type
        result[self.id]['lowerBound'] = self.lowerBound
        result[self.id]['upperBound'] = self.upperBound
        result[self.id]['continuous'] = self.continuous
        result[self.id]['discretValues'] = self.discretValues
        result[self.id]['precision'] = self.precision
        result[self.id]['symbolPrefix'] = self.symbolPrefix
        result[self.id]['symbolSuffix'] = self.symbolSuffix
        return result

class StringField(AbstractField):

    def __init__(self, name, length=10, strCount=1, charset=None, case=None, includeDigits=False, strSep=' '):
        super().__init__(name)
        self.length = length
        self.strCount = strCount
        self.charset = charset
        self.case = case
        self.includeDigits = includeDigits
        self.strSep = strSep
    
    def getLength(self):
        return self.length
    
    def setLength(self, length):
        self.length = length
    
    def getStrCount(self):
        return self.strCount
    
    def setStrCount(self, strCount):
        self.strCount = strCount
    
    def getCharset(self):
        return self.charset
    
    def setCharset(self, charset):
        self.charset = charset
    
    def getCase(self):
        return self.case
    
    def setCase(self, case):
        self.case = case
    
    def getIncludeDigits(self):
        return self.includeDigits
    
    def setIncludeDigits(self, includeDigits):
        self.includeDigits = includeDigits
    
    def getStrSep(self):
        return self.strSep
    
    def setStrSep(self, strSep):
        self.strSep = strSep
    
    def getFinalCharset(self):
        if self.charset != None:
            return self.charset
        else:
            finalCharset = ''
            if self.case == None:
                finalCharset = string.ascii_letters
            elif self.case == 'upper':
                finalCharset = string.ascii_uppercase
            elif self.case == 'lower':
                finalCharset = string.ascii_lowercase
            else:
                return None
            if self.includeDigits:
                finalCharset += string.digits
            return finalCharset

    
    def getString(self, charset):
        return "".join(random.choice(charset) for _ in range(self.length))

    def generateValue(self):
        if self.strCount < 1:
            return None
        else:
            finalValue = []
            charset = self.getFinalCharset()
            for _ in range(self.strCount):
                finalValue.append(self.getString(charset))
            return self.strSep.join(finalValue)
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['length'] = self.length
        result[self.id]['strCount'] = self.strCount
        result[self.id]['charset'] = self.charset
        result[self.id]['case'] = self.case
        result[self.id]['includeDigits'] = self.includeDigits
        result[self.id]['strSep'] = self.strSep
        return result

class CustomField(AbstractField):
    
    COLUMN_INDEX = 0
    COLUMN_NAME = 1

    def __init__(self, name, filePath='\\', columnIndex=0, columnName=None, fetchBy=COLUMN_INDEX, unique=False, delimiter=','):
        super().__init__(name)
        self.filePath = filePath
        self.columnIndex = columnIndex
        self.columnName = columnName
        self.fetchBy = fetchBy
        self.unique = unique
        self.delimiter = delimiter
        self.data = self.getData()
        self.dups = []
    
    def getFilePath(self):
        return self.filePath
    
    def setFilePath(self, filePath):
        self.filePath = filePath
    
    def getColumnIndex(self):
        return self.columnIndex
    
    def setColumnIndex(self, columnIndex):
        self.columnIndex = columnIndex
    
    def getColumnName(self):
        return self.columnName
    
    def setColumnName(self, columnName):
        self.columnName = columnName
    
    def getFetchBy(self):
        return self.fetchBy
    
    def setFetchBy(self, fetchBy):
        self.fetchBy = fetchBy
    
    def getUnique(self):
        return self.unique

    def setUnique(self, unique):
        self.unique = unique
    
    def getDelimiter(self):
        return self.delimiter
    
    def setDelimiter(self, delimiter):
        self.delimiter = delimiter
    
    def getData(self):
        importer = Importer(self.filePath, self.fetchBy, self.delimiter)
        self.data = importer.importData()
        return self.data
    
    def getValue(self):
        value = None
        if self.fetchBy == self.COLUMN_INDEX:
            value = random.choice(self.data[self.columnIndex])
        elif self.fetchBy == self.COLUMN_NAME and not self.columnName is None:
            value = random.choice(self.data[self.columnName])
        return value

    def generateValue(self):
        if self.unique:
            if len(self.data) < self.numItems:
                raise ValueError('Data amount is smaller than number of unique entries required ({} data - {} unique entries required)'.format(len(self.data), self.numItems))
            else:
                while True:
                    value = self.getValue()
                    if not value in self.dups:
                        self.dups.append(value)
                        return value
        else:
            return self.getValue()
    
    def jsonify(self):
        result = super().jsonify()
        result[self.id]['filePath'] = self.filePath
        result[self.id]['columnIndex'] = self.columnIndex
        result[self.id]['columnName'] = self.columnName
        result[self.id]['fetchBy'] = self.fetchBy
        result[self.id]['unique'] = self.unique
        return result