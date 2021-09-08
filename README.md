# randgen

**randgen** is a mock dataset generator.

It allows you to easily create and populate datasets with random values from specific data fields.

## Data type support
The generator supports a wide range of data fields such as:

- Strings
- Numbers
- Dates
- Cities
- Countries
- Emails
- Increment IDs
- IP Addresses

or any other data format you wish by making custom fields.

## Export options
You can export your dataset in the following formats:
- csv
- json
- xml

## Dataset creation logic
A simple dataset creation would be like the following:
```
from randgen.datafields import *
from randgen.datasets import Dataset

incrementField = IncrementField('entity_id')
countryField = CountryField('country')
cityField = CityField('city')
ipAddressField = IpAddressField('ip_address')

dataset = Dataset(100, 'My Dataset', 'output_name', 'output_path', 'csv')

dataset.addDatafield(incrementField)
dataset.addDatafield(countryField)
dataset.addDatafield(cityField)
dataset.addDatafield(ipAddressField)

dataset.exportData()
```

This will produce a file called `output_name.csv` in `output_path`, whose content will be:
```
entity_id,country,city,ip_address
1,Slovakia,Harstad,18:159:28:137
2,Guinea,Marigot,119:22:174:98
3,Congo [Republic],Kroonstad,78d1:1828:3a9e:1e67:4ecf:fef6:eb21:a907
4,Zambia,Saint Peter Port,d7a6:75d6:5a9e:43ef:43be:fb35:fd77:fb8a
5,Jersey,Pago Pago,817d:42c4:1632:7549:7dfe:10cb:251d:19b9
6,Turkey,Oranjestad,2285:498f:3f95:889e:9f18:a059:90c0:6cbf
7,Bosnia and Herzegovina,Kawalu,db89:6273:10e1:ca81:276b:2319:8038:179d
8,Cambodia,Jamestown,6eb:f1ef:ffa8:2fe2:e3ab:d8a8:761c:6f6e
9,Croatia,Belmopan,119:226:90:210
10,Hungary,George Town,193:205:6:231
. 
.
.
```

In the code above, we create all data fields that we are interested in inserting in our dataset, then we create the dataset itself, which will consist of `100` entries, its filename will be `output_name`, its path will be `ouput_path` and it will be a `csv` file.

## Data fields

Below you can take a look at all the supported data fields in detail, along with the examples provided.

### 1) City Field
This field produces a random city from a list of cities found in `cities.csv`. It's parameters are:
- `name`: The name of the data field.
- `country`: An optional parameter which, if sets, forces the field to pick cities from the specific country.

Example:
```
from randgen.datafields import CityField

dataField = CityField('city')
```
Setting a country for the field:
```
dataField = CityField('city', 'Ireland')
```

### 2) Country Field
Gets a random country from a list of countries. It's parameters are:
- `name`: The name of the data field.
- `abbr`: An optional flag variable which, if set to `True`, will return a 2-digit code of the country.

Example:
```
from randgen.datafields import CountryField

dataField = CountryField('country')
```
Getting the country code:
```
dataField = CountryField('country', abbr=True)
```
### 3) Date Field

Gets a random date. It's parameters are:

- `name`: The name of the data field.
- `dateFormat`: The date format. By default it's `%m-%d-%Y`.
- `fromYear`: The starting year of the date.
- `fromMonth`: The starting month of the date.
- `fromDay`: The starting day of the date.
- `toYear`: The ending year of the date.
- `toMonth`: The ending month of the date.
- `toDay`: The ending day of the date.
- `addTime`: A flag variable that determines if time will be added in the end or not.

Example (*most of the parameters are skipped as they have default values as well):
```
dataField = DateField('date', fromYear=2000, toYear=2010)
```
This data field will generate dates from 2000 up to 2010.

### 4) Email Field

Gets a random email from a list of predefined emails. It's parameters are:

- `name`: The name of the data field.
- `unique`: It determines whether the emails that will be generated are unique without duplicates allowed.

Example:
```
dataField = EmailField('email')
```

### 5) Increment Field
Generates a series of incrementing IDs. It's parameters are:
- `name`: The name of the data field.
- `startValue`: The starting value of the field.

Example
```
dataField = IncrementField('increment_id', startValue=1000)
```
This will generate values from 1000 and higher (1001, 1002, ...).

### 6) IP Address Field
Generates a series of IPv4 or IPv6 addresses. It's parameters are:
- `name`: The name of the data field.
- `type`: The type of IP address. It's values are `IPv_4`, `IPv_6` and `IP_BOTH` (default value).

Example:
```
dataField = IpAddressField('ip_address')
dataField = IpAddressField('ipv4_address', IpAddressField.IPv_4)
dataField = IpAddressField('ipv6_address', IpAddressField.IPv_6)
```

### 6) Name Field
It generates a random name from a list of predefined names. It's parameters are:
- `name`: The name of the data field.
Example:
```
dataField = NameField('name')
```
### 7) Number Field
It will produce a random numeric values based on it's parameters:
- `name`: The name of the data field.
- `type`: It's type. It's either `int` or `float`.
- `lowerBound`: The lower bound of the domain.
- `upperBound`: The upper bound of the domain.
- `continuous`: A flag determining whether the values will be continuous or taken from the list of `discretValues`.
- `discretValues`: A list (or tuple) of values to be used as samples. `continuous` parameter must be set to `False` to use that.
- `precision`: The decimal precision, in case the number is float.
- `symbolPrefix`: Any symbols preceding the number.
- `symbolSuffix`: Any symbols after the number.

Example:
```
dataField = NumberField('number', type='int', lowerBound=0, upperBound=10000, continuous=True, symbolSuffix=' BTC')
```
Example output:
```
8058 BTC
1273 BTC
.
.
```
### 8) String Field
It generated random strings, based on it's parameters:
- `name`: The name of the field.
- `length`: The length of each string generated.
- `strCount`: The number of strings generated for each iteration.
- `charset`: The charset to be used.
- `case`: Can be `upper` for uppercase strings, `lower` for lowercase strings or `None` for both.
- `includeDigits`: A flag that determines if digits should be included.
- `strSep`: Sets the separator among different strings.

Example:
```
dataField = StringField('string', length=8, strCount=5, case='upper', strSep='-')
```
Example output:
```
ASDEDASA-EWQUIORE-ASDKLJFV-WERIUIUD-ASDIUWOI
```

### 9) CUSTOM FIELD
A custom field, created to allow the user to create his own field with his own values. The file to be uploaded must be in **csv** format. It's parameters are:
- `name`: The name of the field.
- `filePath`: The path of the `csv` file to be uploaded.
- `columnIndex`: The index of the column to get values from.
- `columnName`: The name of the header whose column values should be picked.
- `fetchBy`: Let's you decide whether you want to use `columnIndex` or `columnName`. It's values are `COLUMN_INDEX` and `COLUMN_NAME`. Use `COLUMN_INDEX` when your `csv` has no headers and `COLUMN_NAME` when it does.
- `unique`: A flag value on whether you want unique values of that field in your dataset or not.
- `delimiter`: The delimiter used in the `csv` in order to split the data of each row. Default is `,`.

Example:

Let's say that we have a file called `sample.csv` whose content structure is the following:
```
street,city,zip,state,beds,baths,sq__ft,type,sale_date,price,latitude,longitude
3526 HIGH ST,SACRAMENTO,95838,CA,2,1,836,Residential,Wed May 21 00:00:00 EDT 2008,59222,38.631913,-121.434879
51 OMAHA CT,SACRAMENTO,95823,CA,3,1,1167,Residential,Wed May 21 00:00:00 EDT 2008,68212,38.478902,-121.431028
2796 BRANCH ST,SACRAMENTO,95815,CA,2,1,796,Residential,Wed May 21 00:00:00 EDT 2008,68880,38.618305,-121.443839
2805 JANETTE WAY,SACRAMENTO,95815,CA,2,1,852,Residential,Wed May 21 00:00:00 EDT 2008,69307,38.616835,-121.439146
6001 MCMAHON DR,SACRAMENTO,95824,CA,2,1,797,Residential,Wed May 21 00:00:00 EDT 2008,81900,38.51947,-121.435768
```
Now, let's say that we want all the values of the `longitude` column in order to populate our dataset.

We will create a custom field like the following:
```
dataField = CustomField('longitude_field', filePath='sample.csv', columnName='longitude', fetchBy=CustomField.COLUMN_NAME)
```
That way, we are able to get only the values of `longitude` column.

## Datasets
Apart from creating datasets, you can also save and import any dataset you have created.

In order to save or import a dataset or a list of datasets, you can use the `DatasetManager` class.

### Saving datasets
```
from randgen.datafields import *
from randgen.datasets import Dataset, DatasetManager

incrementField = IncrementField('entity_id')
countryField = CountryField('country')
cityField = CityField('city')
ipAddressField = IpAddressField('ip_address')

dataset1 = Dataset(100, 'Dataset1', 'output_name_1', 'C:\Datasets\', 'csv')

dataset2 = Dataset(200, 'My Dataset2', 'output_name_2', 'C:\Datasets\', 'csv')

dataset1.addDatafield(incrementField)
dataset1.addDatafield(countryField)
dataset1.addDatafield(cityField)
dataset1.addDatafield(ipAddressField)

dataset2.addDatafield(incrementField)
dataset2.addDatafield(ipAddressField)

# Create a datasetManager and store all datasets there.
datasetManager = DatasetManager()
datasetManager.addDataset(dataset1)
datasetManager.addDataset(dataset2)

# Save them to location.
datasetManager.saveToFile('C:\Datasets\datasets.json')
```
This will create a `json` file containing all dataset information from above.

### Importing datasets

It's also fairly easy to import the datasets you already saved:
```
datasetManager = DatasetManager()
datasetManager.importFile('C:\Datasets\datasets.json)
```

# Note
This is an ongoing project. More features will be added to give more flexibility over data structure and format control.

Feel free to inform me for any issues, changes or features you'd like to see.