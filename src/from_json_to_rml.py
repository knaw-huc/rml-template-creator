# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import re
import sys
import json


example = '''
{
  "@context": {
    "rr": "http://www.w3.org/ns/r2rml#",
    "rml": "http://semweb.mmlab.be/ns/rml#",
    "tim": "http://timbuctoo.huygens.knaw.nl/mapping#"
  },
  "@graph": [
    {
    "@id": "http://timbuctoo.com/mappings/bia/knaw/Persons",
      {
        "rr:predicate": {
          "@id": "http://schema.org/gender"
        },
        "rr:objectMap": {
          "rr:column": "gender",
          "rr:datatype": {
            "@id": "http://www.w3.org/2001/XMLSchema#string"
          },
          "rr:termType": {
            "@id": "rr:Literal"
          }
        }
      }
    }
  ]
}
'''

def stderr(text):
    sys.stderr.write("{}\n".format(text))

def end_prog(code=0):
    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")
    sys.exit(code)

 
def arguments():
    ap = argparse.ArgumentParser(description='Read headerline from excelfile make a standard mappingfile')
    ap.add_argument('-o', '--outputfile',
                    help="outputfile",
                    default = "rml_mapping.jsonnet")
    ap.add_argument('-m', '--mappingfile',
                    help="mappingfile (default = mapping.json)",
                    default = "mapping.json")
    args = vars(ap.parse_args())
    return args

 
if __name__ == "__main__":
    stderr("start")
    stderr(datetime.today().strftime("%H:%M:%S"))

    args = arguments()
    inputfile = args['mappingfile']
    outputfile = args['outputfile']

    mapping = {}
 
    output = open(outputfile, "w", encoding='utf-8')

    json_input = open(inputfile)
    mapping_dict = json.load(json_input)
    mapping = mapping_dict['mapping']
    
    header = '''
{
  "@context": {
    "rr": "http://www.w3.org/ns/r2rml#",
    "rml": "http://semweb.mmlab.be/ns/rml#",
    "tim": "http://timbuctoo.huygens.knaw.nl/mapping#"
  },
  "@graph": [
'''
    output.write(header)

    first = True
    for key in mapping['Mastersheet'].keys():
        if not first:
            output.write(',\n')
        first = False
        word = key
        example = {
          "rr:predicate": {
            "@id": "http://schema.org/" + word
          },
          "rr:objectMap": {
            "rr:column": word,
            "rr:datatype": {
              "@id": "http://www.w3.org/2001/XMLSchema#string"
            },
            "rr:termType": {
              "@id": "rr:Literal"
            }
          }
        }
        output.write(json.dumps(example, sort_keys=False, indent=2))

    footer = '''
  ]
}
'''
    output.write(footer)
    output.close()

    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")


