# FDISK Course Scraper which can write to [BlaulichtSMS](https://blaulichtsms.net) Blackboard

[![Status: In development](https://img.shields.io/badge/STATUS-IN_DEVELOPMENT-red.svg)](https://shields.io/)
[![DISCLAIMER: This project is not using official APIs](https://img.shields.io/badge/DISCLAIMER-This_project_is_not_using_official_APIs-red.svg)](https://shields.io/)
[![Python version: >= 3.7](https://img.shields.io/badge/python->=3.7-blue.svg)](https://shields.io/)

This scraper is used to get the courses from [FDISK](app.fdisk.at), which is among other things used to book courses for firefighters in multiple states of austria.
It gets exported as an excel in the following format:

| Name               | Kursbez. | Kursbeginn | Ort    | Teilnehmerstatus       |
|--------------------|----------|------------|--------|------------------------|
| Mustermann Max     | TE10     | 31.12.2021 | NÖFSZ  | Teilnehmerliste        |
| Mustermann Franz   | GFÜ      | 31.11.2021 | Fw XYZ | Kandidatenliste        |
| Mustermann Melissa | BD       | 31.10.2021 | NÖFSZ  | Warteliste             |
| Mustermann Klaus   | SD20     | 31.10.2021 | NÖFSZ  | Abgelehnt Veranstalter |
| Mustermann Heinz   | FÜ20     | 31.10.2021 | NÖFSZ  | Abgelehnt vom System   |

The Blackboard will be displayed in the following format

| Name                 | Kursbez. | Kursbeginn     | Ort       | Teilnehmerstatus           |
|----------------------|----------|----------------|-----------|----------------------------|
| **Mustermann Max**   | **TE10** | **31.12.2021** | **NÖFSZ** | **Teilnehmerliste**        |
| Mustermann Franz     | GFÜ      | 31.11.2021     | Fw XYZ    | Kandidatenliste            |
| *Mustermann Melissa* | *BD*     | *31.10.2021*   | *NÖFSZ*   | *Warteliste*               |
| ~~Mustermann Klaus~~ | ~~SD20~~ | ~~31.10.2021~~ | ~~NÖFSZ~~ | ~~Abgelehnt Veranstalter~~ |
| ~~Mustermann Heinz~~ | ~~FÜ20~~ | ~~31.10.2021~~ | ~~NÖFSZ~~ | ~~Abgelehnt vom System~~   |

Update 21.12.2021 12:21

### Required Packages

* selenium
* pandas
* beautifulsoup4
* python-dotenv
* openpyxl
* html5lib
* tabulate
* lxml
* requests

## Setup

* Install dependencies with pip ```pip install -r requirements.txt```
* create an `.env` file with your credentials like in `example.env`
* With flags in the `config/flags.py` you can choose
  * if the table gets written into an xlsx file
  * if the table gets written into the BlaulichtSMS Blackboard.
  * if the courses of the past should get removed
  * if declined courses should get removed

## Run

### Run once

* Execute the `__main__.py` with Python 3

### With cronjob

1. Clone this github repository to a folder (e.g. ```~/Programs/```)
2. Add it to crontabs for repeatly update
   * ```crontab -e``` 
   * Append to file ```* * * * * python3 ~/Programs/fire_brigade_mining/src/main.py >> ~/Programs/fire_brigade_mining/output.log 2>&1```
3. Check output.log for output