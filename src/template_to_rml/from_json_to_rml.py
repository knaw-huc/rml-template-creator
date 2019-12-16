# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import re
import sys
import json

class MappingToRML:

    def __init__(self, mappingfile, outputfile, rawcollectionuri, dataset):
        self.mappingfile = mappingfile
        self.rawcollectionuri = rawcollectionuri
        self.dataset = dataset
        self.output = open(outputfile, "w", encoding='utf-8')

    def makeRML(self):
        mapping_dict = {}
        with open(self.mappingfile) as json_input:
            mapping_dict = json.load(json_input)
        self.mapping = mapping_dict.get('mapping', {})
        self.sheet_ids = mapping_dict.get('ids', {})
        self.links = self.doLinks(mapping_dict.get('links', {}))
        self.names_titles = mapping_dict.get('names_titles',{})
        self.combine = mapping_dict.get('combine',{})
        self.result = {}
        self.result['@context'] = {
                "rr": "http://www.w3.org/ns/r2rml#",
                "rml": "http://semweb.mmlab.be/ns/rml#",
                "tim": "http://timbuctoo.huygens.knaw.nl/mapping#"
                }
        self.result['@graph'] = []
        self.doSheets()

    def doLinks(self, links):
        result = {}
        for key in links.keys():
            sheet,column = re.split(r'\.', key, 1)
            if sheet in result:
                target_sh,target_col = re.split(r'\.', links[key], 1)
                result[sheet][column] = { target_sh: target_col }
            else:
                result[sheet] = {}
                target_sh,target_col = re.split(r'\.', links[key], 1)
                result[sheet][column] = { target_sh: target_col }
        return result

    def doCombine(self, this_sheet, combine):
        object_maps = []
        for key in combine.keys():
            # it seems, combining fields only works wenn using datatype 'person-name'
            object_maps.append({ "rr:objectMap": {
                "rr:column": key,
                "rr:datatype": {
                  "@id": "http://timbuctoo.huygens.knaw.nl/static/v5/datatype/person-name"
                },
                "rr:termType": {
                  "@id": "rr:Literal"
                }
              }
            })
            new_combine = {"tim:name":key}
            expression = combine[key]['join'].join(combine[key]['fields'])
            expression = r'"{\"components\":['
            first = True
            components = []
            for field in combine[key]['fields']:
                components.append({ "type": '"{}"'.format(field.upper()),
                                    "value": '"Json:stringify(v.{})"'.format(field) })
                if first:
                    first = False
                else:
                    expression = expression + ','
                expression = expression + r'{\"type\":\"' + field.upper() + r'\",\"value\":" + '
                expression = expression + " Json:stringify(v." + field + r') + "}'
            expression = expression + r']}"'
            new_combine["tim:expression"] = expression
            this_sheet.append(new_combine)
        return object_maps

    def doSheets(self):
        teller = 0
        for sheet in self.mapping.keys():
            combine = self.combine.get(sheet,{})
            this_sheet = {}
            self.resource = "http://timbuctoo.huygens.knaw.nl/v5/data/{0}/{1}/".format(self.dataset,sheet)
            this_sheet['@id'] = self.resource
            teller += 1
            this_sheet['rml:logicalSource'] = {
                    "rml:source" : {
                        "tim:rawCollectionUri" : {
                            "@id" : self.rawcollectionuri + "{}".format(teller)
                            },
                        "tim:customField": []
                        }
                    }
            
            this_sheet['rr:subjectMap'] = {}
            this_sheet['rr:subjectMap']['rr:template'] = self.resource + "{" + self.sheet_ids.get(sheet,"persistent_id") + "}"
            this_sheet['rr:subjectMap']['rr:class'] =  { "@id": self.resource }
            this_sheet['rr:predicateObjectMap'] = []

            if combine:
                object_maps = self.doCombine(this_sheet['rml:logicalSource']['rml:source']['tim:customField'], combine)
                for obj_map in object_maps:
                    this_sheet['rr:predicateObjectMap'].append(obj_map)

            for column in self.mapping[sheet].keys():
                if column in self.names_titles.get(sheet,{}):
                    this_sheet['rr:predicateObjectMap'].append(self.do_make_title_col(sheet, column))
                this_sheet['rr:predicateObjectMap'].append(self.do_column(sheet, column))
            self.result['@graph'].append(this_sheet)
    
        self.output.write(json.dumps(self.result, sort_keys=False, indent=2))
        self.output.close()

    def do_column(self, sheet, column):
        result = {}
        result['rr:predicate'] = {
                "@id": "http://schema.org/" + column
                }
        if sheet in self.links:
            if column in self.links[sheet]:
                tar_sh = list(self.links[sheet][column].keys())[0]
                tar_col = self.links[sheet][column][tar_sh]
                result['rr:objectMap'] = {}
                result['rr:objectMap']['rr:parentTriplesMap'] = {
                        "@id": self.resource.replace(sheet, tar_sh)
                        }
                result['rr:objectMap']['rr:joinCondition'] = {
                        "rr:child": column,
                        "rr:parent": tar_col
                        }
                return result
        result['rr:objectMap'] = {
                "rr:column": column,
                "rr:datatype": {
                    "@id": "http://www.w3.org/2001/XMLSchema#string"
                    },
                "rr:termType": {
                    "@id": "rr:Literal"
                    }
                }
        return result

    def do_make_title_col(self, sheet, column):
        result = {}
        result['rr:predicate'] = {
                "@id": "http://schema.org/name"
                }
        result['rr:objectMap'] = {
                "rr:column": column,
                "rr:datatype": {
                    "@id": "http://www.w3.org/2001/XMLSchema#string"
                    },
                "rr:termType": {
                    "@id": "rr:Literal"
                    }
                }
        return result

# end class MappingToRML


def stderr(text):
    sys.stderr.write("{}\n".format(text))
 
def arguments():
    ap = argparse.ArgumentParser(description='Read mappingfile to make an rml-file')
    ap.add_argument('-o', '--outputfile',
                    help="outputfile",
                    default = "rml_mapping.json")
    ap.add_argument('-m', '--mappingfile',
                    help="mappingfile (default = mapping.json)",
                    default = "mapping.json")
    ap.add_argument('-d', '--dataset',
                    help="dataset (default = test_sheet)",
                    default = "test_sheet")
    ap.add_argument('-r', '--rawcollectionuri',
                    help="rawcollectionuri")
    args = vars(ap.parse_args())
    return args

def start():
    stderr("started at: {}".format(datetime.today().strftime("%H:%M:%S")))

def end():
    stderr("stopped at: {}".format(datetime.today().strftime("%H:%M:%S")))
 
if __name__ == "__main__":
    start()
    args = arguments()
    mappingfile = args['mappingfile']
    outputfile = args['outputfile']
    rawcollectionuri= args['rawcollectionuri']
    dataset = args['dataset']

    mtr = MappingToRML(mappingfile, outputfile, rawcollectionuri, dataset)
    mtr.makeRML()

    end()

