# FDISK Course Scraper

This scraper is used to get the courses from [FDISK](app.fdisk.at), which is used to book courses for the lower austrian firefighters.
It gets exported in the following format:

lastname firstname | course short label | course start time | location | status

### Required Packages

* selenium
* pandas
* beautifulsoup4
* python-dotenv
* openpyxl

## Run

Execute the `scrape_fdisk_courses.py` with Python 3