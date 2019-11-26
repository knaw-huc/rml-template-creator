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
        self.mapping = mapping_dict['mapping']
        self.sheet_ids = mapping_dict['ids']

        # mapping_dict['names_titles']
    
        self.result = {}
        self.result['@context'] = {
                "rr": "http://www.w3.org/ns/r2rml#",
                "rml": "http://semweb.mmlab.be/ns/rml#",
                "tim": "http://timbuctoo.huygens.knaw.nl/mapping#"
                }
        self.result['@graph'] = []
        self.doSheets()

    def doSheets(self):
        teller = 0
        for sheet in self.mapping.keys():
            this_sheet = {}
            resource = "http://timbuctoo.huygens.knaw.nl/v5/data/{0}/{1}/".format(self.dataset,sheet)
            this_sheet['@id'] = resource
    
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
            this_sheet['rr:subjectMap']['rr:template'] = resource + "{" + self.sheet_ids[sheet] + "}"
            this_sheet['rr:subjectMap']['rr:class'] =  { "@id": resource }
            this_sheet['rr:predicateObjectMap'] = []
    
            for column in self.mapping[sheet].keys():
                this_sheet['rr:predicateObjectMap'].append(self.do_column(column))
            self.result['@graph'].append(this_sheet)
    
        self.output.write(json.dumps(self.result, sort_keys=False, indent=2))
        self.output.close()

    def do_column(self, column):
        return {
          "rr:predicate": {
            "@id": "http://schema.org/" + column
          },
          "rr:objectMap": {
            "rr:column": column,
            "rr:datatype": {
              "@id": "http://www.w3.org/2001/XMLSchema#string"
            },
            "rr:termType": {
              "@id": "rr:Literal"
            }
          }
        }

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

