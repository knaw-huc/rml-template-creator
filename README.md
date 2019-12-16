# rml-template-creator

Two script are provided to make it a bit simpler to create a rml-template for an xlsx file:
- `make_excel_mapping.py` (in `src/excel_to_template`)
- `from_json_to_rml.py` (in `src/template_to_rml`)

## generate a simple mapping

`usage: make_excel_mapping.py [-h] [-i INPUTFILE] [-m MAPPINGFILE] [-r HEADERROW]`

The input file (`-i`) should be an xlsx-file. 

The mapping file (`-m`) is the simple mapping made from the xlsx in the form of a `json` file. Make sure the extention is actually `.json`!

The headerrow is optional, the first row is presumed to be the header row, but it can be adjusted if it's on another row. The script presumes the data rows start below the header row!

There should always be a header row! if your xlsx has no header row, add it first before trying this script!

## Adjusting the mapping

As an example we take an xlsx containing two tabs:
* tab Persons, with columns PE-ID, Name, Birthplace
* tab Places, with columns, PL-ID, Placename
This will result in a json file like:
```
    {
        "mapping": {
            "Persons": {
                "PE-ID": "number",
                "Name": "string",
                "Birthplace": "number"
            },
            "Places": {
                "PL-ID": "number",
                "Placename": "string"
            }
        },
        "ids": {
            "Persons": "PE-ID",
            "Places": "PL-ID"
        },
        "names_titles": {},
        "links": {},
        "combine": {}
    }
```
'ids' indicates the column of each table which is the unique identifier.

`names_title` indicates the column of each table which is to be used as this recordtypes `schema:name`.

`links` gives you the posibility to make links between columns, both on the same tab and between tabs.
Example:
```
      "links": {
        "Persons.Birthplace": "Places.PL-ID"
      },
```
links the column Birthplace on tab Persons to the column PL_ID on tab Places. In the endresult, after uploading to timbuctoo, column Birthplace will show a link to the Places table.

`combine` gives you the possibility to combine several columns to a single column.
Example:
```
    "combine": {
	"Persons": {
	    "birthDate": {
		"fields": [ "birth_year", "birth_month", "birth_day"]
	    }
	}
    }
```
combines `birth_year`, `birth_month`, `birth_day` to a new field `birthDate` (in the same order as in the array after `"fields"`).

## generate an rml-mapping

After adjusting the mapping file you can generate an rml-mapping:

`usage: from_json_to_rml.py [-h] [-o OUTPUTFILE] [-m MAPPINGFILE] [-d DATASET] [-r RAWCOLLECTIONURI]`

The output (`-o`) is a json-ld file; the mapping file (`-m`) is what you made in the previous step.

`-d` is the name you gave your dataset (xlsx) uploading it to timbuctoo.

`-r` is the (generated) uri the dataset got after uploading it to timbuctoo. Find out what it is using graphQL (see timbuctoo documentation).

With  a `curl` command you can upload your json-ld. The amount of data will determine  how long it takes before you see the result.
