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
from excel_to_template.make_excel_mapping import MakeBaseMapping

class TestMakeMapping(unittest.TestCase):
    def setUp(self):
        self.stderr("start")
        self.stderr(datetime.today().strftime("%H:%M:%S"))

    def test_mapping(self):
        inputfile = "test_sheet.xlsx"
        comparefile = "test_sheet_mapping.json"
        resultfile = "test_mapping.json"
        mbm = MakeBaseMapping(inputfile, resultfile)
        mbm.make_mapping()
        test_mapping_file = open(resultfile, 'r')
        test_mapping = json.load(test_mapping_file)
        compare_file = open(comparefile)
        compare_mapping = json.load(compare_file)
        self.assertEqual(test_mapping, compare_mapping)
        test_mapping_file.close()
        compare_file.close()
        os.remove(resultfile)

    def tearDown(self):
        self.stderr(datetime.today().strftime("%H:%M:%S"))
        self.stderr("einde")

    def stderr(self, text):
        sys.stderr.write("{}\n".format(text))

if __name__ == "__main__":
    
    unittest.main()

