# FDISK Course Scraper

This scraper is used to get the courses from [FDISK](app.fdisk.at), which is used to book courses for the lower austrian firefighters.
It gets exported as an excel in the following format:

| lastname firstname | course short label | course start time | location          | status          |
|--------------------|--------------------|-------------------|-------------------|-----------------|
| Mustermann Max     | TE10               | 31.12.2021        | NÖFSZ             | Teilnehmerliste |
| Mustermann Franz   | BD                 | 31.11.2021        | FF XYZ            | Kandidatenliste |
| Mustermann Melissa | SD10               | 31.10.2021        | NÖFSZ             | Warteliste      |

### Required Packages

* selenium
* pandas
* beautifulsoup4
* python-dotenv
* openpyxl
* html5lib
* lxml

## Run

* create an `.env` file with your credantials like in `example.env`
* Execute the `scrape_fdisk_courses.py` with Python 3