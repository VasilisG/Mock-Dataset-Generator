from randgen.datafields import *

class DataFieldFactory:

    @classmethod
    def create(cls, key, values):
        lookup = {
            'cityfield' : CityField,
            'countryfield' : CountryField,
            'datefield' : DateField,
            'emailfield' : EmailField,
            'incrementfield' : IncrementField,
            'ipaddressfield' : IpAddressField,
            'namefield' : NameField,
            'numberfield' : NumberField,
            'stringfield' : StringField,
            'customfield' : CustomField
        }
        if key in lookup:
            return lookup[key](**values)
        else:
            raise ValueError('Wrong key for datafield entry: {}'.format(key))
