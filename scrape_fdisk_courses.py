from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import pandas as pd


def main():
    #load environment variables
    load_dotenv()

    #configure the browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    driver = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    try:
        print("Logging in")
        driver.get("https://app.fdisk.at/fdisk/module/vws/logins/logins.aspx")

        # Fill out form
        loginE = driver.find_element_by_id('login')
        loginE.clear()
        loginE.send_keys(os.environ.get("FDISK_USERNAME"))

        passwordE = driver.find_element_by_id('password')
        passwordE.clear()
        passwordE.send_keys(os.environ.get("FDISK_PASSWORD"))
        driver.find_element_by_id('Submit2').click()

        # Now Logged in and call site, which contains the table
        driver.get(
            f'https://app.fdisk.at/fdisk/module/kvw/karriere/AngemeldeteKurseLFKDOList.aspx?'
            'instanzennummer_person={instanzennummer}'
            '&ordnung=zuname%2Cvorname%2Ckursartenbez%2Ckursbeginn'
            '&orderType=ASC'
            '&search=1'
            '&anzeige_count=ALLE'.format(instanzennummer=os.environ.get("FDISK_INSTANZNUMMER")))

        print("Scraping table")

        table_kurse = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[1]')
        soup = BeautifulSoup(table_kurse.get_attribute('innerHTML'), 'html.parser')
        table = soup.select("table")[0]

        print("Preparing data")
        tabledata = pd.read_html(str(table))[0]

        #Remove unneded lines
        df = tabledata.iloc[:-5, 7:]
        df.drop(labels=[0, 2], axis=0, inplace=True)
        df.drop(labels=[7, 8, 10, 12, 14, 16, 18, 20, 21, 22, 23, 24, 25, 26, 27], axis=1, inplace=True)

        #Data Cleaning
        #Set Column Labels and remove them from the data
        df.columns = df.iloc[0:1].to_numpy()[0]
        df = df.iloc[1:]

        # Rename the couse title column name
        df.rename(columns={'Kursart (Kurzbez.)': 'Kursbez:'}, inplace=True)
        # Change the location name of the NÖ Feuerwehr- und Sicherheitszentrum to NÖFSZ
        df.loc[df['Ort'] == 'Tulln, NÖ Feuerwehr- und Sicherheitszentrum', 'Ort'] = 'NÖFSZ'

        df['Ort'] = df['Ort'].str.replace('Feuerwehrhaus', 'Fwh.', regex=False)
        df['Ort'] = df['Ort'].str.replace('Feuerwehr', 'Fw.', regex=False)

        # Just display the first- and lastname (remove rank and number)
        df['Name'] = df['Name'].apply(lambda x: x[:x.find(',')])

        # Remove lines where booking is already rejected by the system
        df.drop(df[(df['Teilnehmerstatus'] == 'Abgelehnt vom System') | (df['Teilnehmerstatus'] == 'Abgelehnt Veranstalter')].index, inplace=True)
        # Drop the end date column
        df.drop(labels='Kursende', axis=1, inplace=True)

        # Sorting by begin date
        df['sort'] = (pd.to_datetime(df['Kursbeginn'], format='%d.%m.%Y %H:%M'))
        df.sort_values(by=['sort'], inplace=True)
        df.drop(labels='sort', inplace=True, axis=1)

        print("Generating excel")
        df.to_excel('out.xlsx', index=False)

    except Exception as ex:
        print("There was an error. The program didn't succeed!")
        print(ex)
    finally:
        driver.close()

if __name__ == "__main__":
    main()
