# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import re
import sys
import json

def stderr(text):
    sys.stderr.write("{}\n".format(text))

def end_prog(code=0):
    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")
    sys.exit(code)

 
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
    stderr("start")
    stderr(datetime.today().strftime("%H:%M:%S"))

def end():
    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")
 
if __name__ == "__main__":
    start()
    args = arguments()
    inputfile = args['mappingfile']
    outputfile = args['outputfile']
    rawcollectionuri= args['rawcollectionuri']
    dataset = args['dataset']

    output = open(outputfile, "w", encoding='utf-8')

    json_input = open(inputfile)
    mapping_dict = json.load(json_input)
    mapping = mapping_dict['mapping']

    result = {}
    result['@context'] = {
            "rr": "http://www.w3.org/ns/r2rml#",
            "rml": "http://semweb.mmlab.be/ns/rml#",
            "tim": "http://timbuctoo.huygens.knaw.nl/mapping#"
            }
    result['@graph'] = []

    teller = 0
    for sheet in mapping.keys():
        this_sheet = {}
        resource = "http://timbuctoo.huygens.knaw.nl/v5/data/{0}/{1}/".format(dataset,sheet)
        this_sheet['@id'] = resource

        teller += 1
        this_sheet['rml:logicalSource'] = {
                "rml:source" : {
                    "tim:rawCollectionUri" : {
                        "@id" : rawcollectionuri + "{}".format(teller)
                        },
                    "tim:customField": []
                    }
                }
        
        this_sheet['rr:subjectMap'] = {}
        this_sheet['rr:subjectMap']['rr:template'] = resource + "{persistant_id}"
        this_sheet['rr:subjectMap']['rr:class'] =  { "@id": resource }
        this_sheet['rr:predicateObjectMap'] = []

        for key in mapping[sheet].keys():
            this_key = {
              "rr:predicate": {
                "@id": "http://schema.org/" + key
              },
              "rr:objectMap": {
                "rr:column": key,
                "rr:datatype": {
                  "@id": "http://www.w3.org/2001/XMLSchema#string"
                },
                "rr:termType": {
                  "@id": "rr:Literal"
                }
              }
            }
            this_sheet['rr:predicateObjectMap'].append(this_key)
        result['@graph'].append(this_sheet)

    output.write(json.dumps(result, sort_keys=False, indent=2))
    output.close()

    end()


