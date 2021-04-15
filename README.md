## Install requirements:
`pip install -r requirements.txt`

## Usage
Two options exist for R and Python users.

Firstly the pure Python option:
```
$ python3 geoinsight_download.py -h

usage: geoinsight_download.py [-h] [--start_date START_DATE] [--location_name LOCATION_NAME] [--location_id LOCATION_ID]

Download movement range maps data from Facebook Data for Good

optional arguments:
  -h, --help            show this help message and exit
  --start_date START_DATE
                        Date of earliest days data to import. Must be in format: YYYY-MM-DD (default = 2020-02-21)
  --location_name LOCATION_NAME
                        Name of location to download data for (default = Addis Ababa)
  --location_id LOCATION_ID
                        ID of location to download data for (default = 642750926308152)
```

Secondly, the R interface using `reticulate`:
```
$ Rscript run.R <start_date> <location_name> <location_id>
```
These command line args must follow the same format as described in the python documentation (above). If there are spaces in the name of the location it must be encapsulated by quotation marks.
