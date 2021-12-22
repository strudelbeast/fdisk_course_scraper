from dotenv import load_dotenv
import os

from blaulichtsms import authcache
import blaulichtsms.auth
import blaulichtsms.blackboard
from fdisk.fdisk_scraper import fetch_fdisk_table
from config import flags
from datetime import datetime, timedelta

# load environment variables
load_dotenv()

result = fetch_fdisk_table()

if flags.WRITE_FDISK_TABLE_TO_BLAULICHTSMS_BLACKBOARD:
    if result is None:
        raise Exception("No Fdisk data")

    login_request = blaulichtsms.auth.LoginRequest(os.environ.get("BLAULICHTSMS_CUSTOMER_ID"),
                                                   os.environ.get("BLAULICHTSMS_USERNAME"),
                                                   os.environ.get("BLAULICHTSMS_PASSWORD"))
    token_cache = blaulichtsms.auth.login(login_request)
    if token_cache is None:
        raise Exception("Login to BlaulichtSMS not successfully")

    succeeded = blaulichtsms.blackboard \
        .update_blackboard(token_cache.token,
                           os.environ.get("BLAULICHTSMS_CUSTOMER_ID"),
                           result)
    if succeeded:
        expire_time = datetime.now() + timedelta(hours=24)
        authcache.cache_token(token_cache.customerId, token_cache.username, token_cache.token, expire_time)
        print(datetime.now().strftime("[%d-%b-%Y %H:%M:%S]"), "Successfully updated blackboard")
