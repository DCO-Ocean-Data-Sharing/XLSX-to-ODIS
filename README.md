# DCO-ODS XLSX to ODIS

Python script to take an XLSX spreadsheet prepared by the Decade Coordination Office for Ocean Data Sharing of metadata from Decade Actions and publish it the Ocean Data Information System federation

- Author: [@adamml](https://github.com/adamml) for the [Decade Coordination Office for Ocean Data Sharing](https://oceandatasharing-dco.org/)

## Dependencies
- fastexcel==0.14.0
- Jinja2==3.1.6
- polars=1.29.0

## Running the script

```shell
python xlsx2odis.py -h

python xlsx2odis.py -b=BASE_URL -i=INPUT_FILE -o=OUT_DIR -s=INPUT_SHEET
```

Where:

- `-b` specifies the base URL used to locate the output files on the web. Essentially, this is the web accessible location of the directory the script will write to and given by the `-o` option.
- `-h` prints a manual or help page and exits the script with no further action taken.
- `-i` specifies the XLSX file to use as an input to the script. The column structure expected in the XLSX file is detailed [here](XLSXSPEC.md).
- `-o` specifies the output directory or folder to write the results of the script to.
- `-s` specifies the sheet name within the input file given by `-i` where the content expected by the script is stored.

## Ouputs

1. One JSON-LD file per spreadsheet row
2. One sitemap.xml file

## Acknowledgement

The work of the Decade Coordination Office for Ocean Data Sharing is supported by [Fondation Engie](https://fondation-engie.com).