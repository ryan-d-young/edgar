import os
import json
import dotenv
import datetime
from math import ceil


MODNAME = "edgar"
DFMT = "%Y-%m-%d"
USER_AGENT = os.environ['EDGAR_USER_AGENT']
DEFAULT_CIK = "0000320193"  # AAPL
DEFAULT_TAX = 'us-gaap'
DEFAULT_UNIT = 'USD'
REQUESTS_PER_SEC = 10
BUFFER_MS = 100
TIMEOUT_SEC = 5
TODAY = datetime.date.today()

if TODAY.month - 3 < 0:
    LAST_PERIOD = f"CY{TODAY.year - 1}Q4I"
else:
    LAST_PERIOD = f"CY{TODAY.year}Q{ceil(4 * (TODAY.month/12))}I"
