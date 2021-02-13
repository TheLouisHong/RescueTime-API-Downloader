# RescueTime API Downloader

## Features
* Download Hourly Activity From RescueTime API In Monthly CSV Chunks
* Merge Monthly CSV Into merged.csv

## Requirement

Project created with Python 3.

Install `pandas`, for csv merging
```
pip3 install pandas
```

Install `python-dateutil`, for iterating over months.
```
pip3 install python-dateutil
```

## Usage
1. Create and generate your RescueTime API Key here: https://www.rescuetime.com/anapi/manage
2. Run rescuetime_downloader.py
```
python rescuetime_downloader.py download your_API_KEY 2020-1-1 2020-3-1
```
3. Merge monthly CSV
```
python rescuetime_downloader.py merge
```


## Code
* Download:
    * Generate the url using `iterate_rescuetimeapi_url_hourly_bymonth_csv`, 
    * Loop over that generator and download each using `download_rescuetime_file_hourly_bymonth_csv`
* Merge:
    * Use glob to find all files matching the name `{rescuetime_hourly_bymonth *.csv}`, merge with pandas, then output into "merged.csv"


## Updates
* Added support for hourly interval monthly chunk download. Strictly just for me use case. 
    - New intervals and chunk size can be easily added, pull request are welcome.