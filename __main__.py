from dotenv import load_dotenv
import os

import blaulichtsms.auth
import blaulichtsms.blackboard
from fdisk.fdisk_scraper import fetch_fdisk_table

WRITE_FDISK_TABLE_TO_FILE = True
WRITE_FDISK_TABLE_TO_BLAULICHTSMS_BLACKBOARD = False

# load environment variables
load_dotenv()

result = fetch_fdisk_table(WRITE_FDISK_TABLE_TO_FILE)

if WRITE_FDISK_TABLE_TO_BLAULICHTSMS_BLACKBOARD:
    if result is None:
        raise Exception("No Fdisk data")

    login_request = blaulichtsms.auth.LoginRequest(os.environ.get("BLAULICHTSMS_CUSTOMER_ID"),
                                   os.environ.get("BLAULICHTSMS_USERNAME"),
                                   os.environ.get("BLAULICHTSMS_PASSWORD"))
    token = blaulichtsms.auth.login(login_request)
    if token is None:
         raise Exception("Login to Blaulichtsms not successfully")

    blaulichtsms.blackboard.update_blackboard(token,
                                              os.environ.get("BLAULICHTSMS_CUSTOMER_ID"),
                                              result)
    print("Successfully updated blackboard")

