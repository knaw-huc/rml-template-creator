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
        self.stderr("started at: {}".format(datetime.today().strftime("%H:%M:%S")))

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

    def tearDown(self):
        self.stderr("stopped at: {}".format(datetime.today().strftime("%H:%M:%S")))

    def stderr(self, text):
        sys.stderr.write("{}\n".format(text))

 
if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()

