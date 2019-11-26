# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import re
import sys
import xlrd 
import json
import os


class MakeBaseMapping:

    def __init__(self, inputfilename, mappingfile):
        self.inputfile = inputfilename
        self.mappingfile = mappingfile

    def make_mapping(self):
        headers,ids = self.read_sheets()
        mapping = { 'mapping': headers }
        mapping['ids'] = ids
        mapping['links'] = {}
        mapping['combine'] = {}
        with open(self.mappingfile,"w", encoding='utf-8') as outputfile:
            outputfile.write(json.dumps(mapping, sort_keys=False, indent=4))

    def read_sheets(self):
        headers = {}
        ids = {}
        with xlrd.open_workbook(self.inputfile) as wb:
            for sheetnum in range(0, wb.nsheets):
                res_headers,res_idcol = self.xls_sheet(wb.sheet_by_index(sheetnum))
                sheetname = wb.sheet_by_index(sheetnum).name 
                headers[sheetname] = res_headers
                ids[sheetname] = res_idcol
        return headers,ids

    def xls_sheet(self, sheet, headerrownum=0):
        headers = {}
        rownum = headerrownum
        coltitles = []
        for colnum in range(sheet.ncols):
            cell_type_no = sheet.cell_type(rownum,colnum)
            if cell_type_no==2:
                cell_type = "number"
            elif cell_type_no==3:
                cell_type = "date"
            elif cell_type_no==4:
                cell_type = "boolean"
            else:
                cell_type = "string"
            coltitle = ''
            if sheet.cell_value(headerrownum, colnum) != '':
                coltitle = re.sub(r'[ -/]+','-',sheet.cell_value(headerrownum,colnum)).strip('-')
            else:
                coltitle = 'empty{0}'.format(colnum)
            headers[coltitle] = [cell_type]
            coltitles.append(coltitle)
        for coltitle in coltitles:
            headers[coltitle] = []
        for rownum in range(1, sheet.nrows):
            for colnum in range(sheet.ncols):
                cell_type_no = sheet.cell_type(rownum,colnum)
                if cell_type_no==2:
                    cell_type = "number"
                elif cell_type_no==3:
                    cell_type = "date"
                elif cell_type_no==4:
                    cell_type = "boolean"
                elif cell_type_no==0:
                    cell_type = "empty"
                else:
                    cell_type = "string"
                if cell_type!="empty":
                    if not cell_type in headers[coltitles[colnum]]:
                        headers[coltitles[colnum]].append(cell_type)
        res = {}
        for key in headers.keys():
            if len(headers[key])==1:
                res[key] = headers[key][0]
            else:
                res[key] = "string"
        return res,coltitles[0]

def stderr(text):
    sys.stderr.write("{}\n".format(text))

 
def arguments():
    ap = argparse.ArgumentParser(description='Read lines from excelfile to make a standard mappingfile')
    ap.add_argument('-i', '--inputfile',
                    help="inputfile",
                    default = "20191011_manuscripts_mastersheet_CURRENT.xlsx")
    ap.add_argument('-m', '--mappingfile',
                    help="mappingfile (default = mapping.json)",
                    default = "mapping.json")
    ap.add_argument('-r', '--headerrow',
                    help="headerrow; 0=row 1 (default = 0)",
                    default = 0)
    args = vars(ap.parse_args())
    return args

 
if __name__ == "__main__":
    stderr("start")
    stderr(datetime.today().strftime("%H:%M:%S"))

    args = arguments()
    inputfile = args['inputfile']
    mappingfile = args['mappingfile']
    headerrow = int(args['headerrow'])

    base_mapping = MakeBaseMapping(inputfile, mappingfile)
    base_mapping.make_mapping()

    stderr(datetime.today().strftime("%H:%M:%S"))
    stderr("einde")


