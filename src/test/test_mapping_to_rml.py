# -*- coding: utf-8 -*-
from datetime import datetime
import json
import os
import re
import sys
import unittest
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from template_to_rml.from_json_to_rml import MappingToRML
import tracemalloc

class TestMakeRML(unittest.TestCase):
    def setUp(self):
        pass

    def test_make_rml(self):
        mappingfile = 'test_input_mapping.json'
        outputfile = 'this_test_rml.json'
        rawcollectionuri= 'https://data.huygens.knaw.nl/rdf/datasets/u1234567890/test_sheet/rawData/be827d-af8ctest_sheet_xlsx/collections/'
        dataset = 'test_sheet'
        mtr = MappingToRML(mappingfile, outputfile, rawcollectionuri, dataset)
        mtr.makeRML()
        expected_resultfile = 'test_expected_rml.json'
        compare_file = open(expected_resultfile)
        generated_file = open(outputfile)
        expected_rml = json.load(compare_file)
        generated_rml = json.load(generated_file)
        self.assertEqual(generated_rml, expected_rml)
        compare_file.close()
        generated_file.close()
        os.remove(outputfile)

    def test_make_rml_with_link(self):
        self.maxDiff = None
        mappingfile = 'test_mapping_with_link.json'
        outputfile = 'this_test_rml_with_link.json'
        rawcollectionuri= 'https://data.huygens.knaw.nl/rdf/datasets/u1234567890/test_sheet/rawData/be827d-af8ctest_sheet_xlsx/collections/'
        dataset = 'test_sheet'
        mtr = MappingToRML(mappingfile, outputfile, rawcollectionuri, dataset)
        mtr.makeRML()
        expected_resultfile = 'test_expected_rml_with_link.json'
        compare_file = open(expected_resultfile)
        generated_file = open(outputfile)
        expected_rml = json.load(compare_file)
        generated_rml = json.load(generated_file)
        self.assertEqual(generated_rml, expected_rml)
        compare_file.close()
        generated_file.close()
        os.remove(outputfile)

    def test_make_rml_with_names(self):
        self.maxDiff = None
        mappingfile = 'test_input_mapping_with_names.json'
        outputfile = 'this_test_rml_with_names.json'
        rawcollectionuri= 'https://data.huygens.knaw.nl/rdf/datasets/u1234567890/test_sheet/rawData/be827d-af8ctest_sheet_xlsx/collections/'
        dataset = 'test_sheet'
        mtr = MappingToRML(mappingfile, outputfile, rawcollectionuri, dataset)
        mtr.makeRML()
        expected_resultfile = 'test_expected_rml_with_titles.json'
        compare_file = open(expected_resultfile)
        generated_file = open(outputfile)
        expected_rml = json.load(compare_file)
        generated_rml = json.load(generated_file)
        self.assertEqual(generated_rml, expected_rml)
        compare_file.close()
        generated_file.close()
        os.remove(outputfile)

    def test_combine(self):
        outputfile = 'this_test_combine.json'
        mtr = MappingToRML(None, outputfile, "", "")
        sheet = []
        combine = {
                    "birthDate": {
                        "join": "-",
                        "fields": [ "birth_year", "birth_month", "birth_day"]
                    }
                }
        result = mtr.doCombine(sheet, combine)
        expected_result= [{'rr:objectMap': {'rr:column': 'birthDate', 'rr:datatype': {'@id': 'http://timbuctoo.huygens.knaw.nl/static/v5/datatype/person-name'}, 'rr:termType': {'@id': 'rr:Literal'}}}]
        self.assertEqual(result, expected_result)
        expected_sheet = [{'tim:name': 'birthDate', 'tim:expression': '"{\\"components\\":[{\\"type\\":\\"BIRTH_YEAR\\",\\"value\\":" +  Json:stringify(v.birth_year) + "},{\\"type\\":\\"BIRTH_MONTH\\",\\"value\\":" +  Json:stringify(v.birth_month) + "},{\\"type\\":\\"BIRTH_DAY\\",\\"value\\":" +  Json:stringify(v.birth_day) + "}]}"'}]
        self.assertEqual(sheet, expected_sheet)
        mtr.output.close()
        os.remove(outputfile)

    def tearDown(self):
        pass

def stderr(text):
    sys.stderr.write("{}\n".format(text))

 
if __name__ == "__main__":
    stderr("started at: {}".format(datetime.today().strftime("%H:%M:%S")))
    tracemalloc.start()
    unittest.main()
    stderr("stopped at: {}".format(datetime.today().strftime("%H:%M:%S")))

