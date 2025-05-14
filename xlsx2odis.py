import jinja2
import json
import polars
import sys

from typing import Dict, List, Optional


def help():
    """Displays a manual page for the script"""
    print("""Usage xlsx2odis.py [options]

Options:
    -h             Displays this help page and exit
    -b=BASE_URL    Specifies the root url, or BASE_URL, to locate outputs of
                   this script on the web. This is essentially the web accesible
                   address of DIRECTORY
    -i=FILE        Use FILE as the input Excel spreadsheet
    -o=DIRECTORY   Write output to DIRECTORY
    -s=SHEETNAME   Read SHEET_NAME from the FILE specified by -i
    """)


def kwdBuilder(instr: str) -> List[str]:
    """Helper function to turn multi-row text from an individual cell into a
    list of keywords"""
    kwd:List = []
    try:
        for kw in instr.split("\n"):
            if kw != "":
                kwd.append(kw)
    except AttributeError:
        pass
    return kwd


def getKeywords(row: Dict) -> List[str]:
    """Helper function to build a List of keywords from an XLSX spreadsheet
    row"""
    kwd = []
    for kw in kwdBuilder(row[26]):
        kwd.append(kw)
    for kw in kwdBuilder(row[20]):
        kwd.append(kw)
    for kw in kwdBuilder(row[27]):
        kwd.append(kw)
    return kwd


def getVariablesMeasured(row: Dict) -> List[str]:
    """Helper function to build a List of variables measured from an XLSX
    spreadsheet row"""
    varMeas = []
    for vm in kwdBuilder(row[25]):
        varMeas.append(vm)
    return varMeas


if __name__ == "__main__":
    baseurl: Optional[str] = None
    """The base URL to locate outputs on the web"""
    infil: Optional[str] = None
    """XLSX file to load data from"""
    outdir: Optional[str] = None
    """The directory to write output to"""
    sheet: Optional[str] = None
    """The sheet name to read from infil"""

    # Parse the input options
    for opt in sys.argv:
        if opt.split("=")[0] == "-h":
            help()
            exit()
        elif opt.split("=")[0] == "-b":
            baseurl = opt.split("=")[1]
            while baseurl[-1] == "/":
                baseurl = baseurl[:-1]
        elif opt.split("=")[0] == "-i":
            infil = opt.split("=")[1]
        elif opt.split("=")[0] == "-o":
            outdir = opt.split("=")[1]
        elif opt.split("=")[0] == "-s":
            sheet = opt.split("=")[1]

    # Handle errors on invocation
    if baseurl is None:
        raise Exception(
            "No base URL specified, please use the -b=BASE_URL option")
    if infil is None:
        raise Exception(
            "No input file specified, please use the -i=FILE option")
    if outdir is None:
        raise Exception(
            "No output directory is specified, please use the -o=DIRECTORY",
            " option")
    if sheet is None:
        raise Exception(
            "No sheet name to be read from the input file specified, "
            "please use the -s=SHEETNAME option")

    #
    # TODO: Add error checking on the existence on the input file and the
    # accessibility of the output directoryß
    #

    # Read the input file with Polars
    df: polars.DataFrame = polars.read_excel(source=infil, sheet_name=sheet)
    """This dataframe holds the data from the input Excel sheet"""

    # Set up the templating environment
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates/"))
    template = environment.get_template("odis.jsonld")
    template2 = environment.get_template("sitemap.xml")

    # Set up the array to hold the sitemap
    sitemap: List = []
    
    # Loop over the entries in the data
    for row in df.iter_rows():
        with open(f"{outdir}/{row[33]}.json", "w") as fil:
            fil.write(template.render(
                dsid=f"{baseurl}/{row[33]}.json",
                name=row[8],
                abstract=row[12],
                kwds=getKeywords(row),
                contentUrl=row[3],
                orgName=row[14],
                orgUrl=row[4],
                variableMeasured=getVariablesMeasured(row)))
            fil.close()
        sitemap.append({"url": f"{baseurl}/{row[33]}.json"})

    # Generate the sitemap
    with open(f"{outdir}/sitemap.xml", "w") as fil:
        fil.write(template2.render(sitemap=sitemap))
        fil.close()        
