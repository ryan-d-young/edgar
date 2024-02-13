import requests
import time
from typing import Callable, Optional

from .constants import (
    USER_AGENT, LAST_PERIOD, REQUESTS_PER_SEC,
    BUFFER_MS, TIMEOUT_SEC, DEFAULT_TAX, DEFAULT_UNIT)


class Limiter(object):
    HISTORY = []

    @staticmethod
    def request(func: Callable):
        def wrapper(self, url: str):
            now = time.time()
            Limiter.HISTORY.append(now)
            if len(Limiter.HISTORY) > REQUESTS_PER_SEC:
                elapsed = now - Limiter.HISTORY[-REQUESTS_PER_SEC]
                if remaining := 1 - elapsed > 0:
                    time.sleep(remaining + BUFFER_MS/1000)
            return func(self, url)
        return wrapper


class Endpoint(object):
    def __init__(self):
        self._session = requests.Session()
        self._session.headers = {
            'Host': 'data.sec.gov',
            'User-Agent': USER_AGENT,
            'Accept-Encoding': 'gzip, deflate'}

    @property
    def session(self):
        return self._session

    @Limiter.request
    def _get(self, url: str):
        try:
            return self.session.get(url, timeout=TIMEOUT_SEC)
        except Exception as e:
            raise Exception("Error occurred making request...\n"
                            f"    {e.__class__.__name__}: {e}")

    def get_submissions(
            self,
            cik: str = '0000320193'
    ) -> requests.Response:
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        return self._get(url)

    def get_concept(
            self,
            cik: str = '0000320193',
            tag: str = 'Assets',
            taxonomy: str = DEFAULT_TAX
    ) -> requests.Response:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{tag}.json"
        return self._get(url)

    def get_facts(
            self,
            cik: str = '0000320193'
    ) -> requests.Response:
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        return self._get(url)

    def get_frame(
            self,
            tag: str = 'Assets',
            period: str = LAST_PERIOD,
            taxonomy: str = DEFAULT_TAX,
            unit: str = DEFAULT_UNIT,
    ) -> requests.Response:
        url = f"https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json"
        return self._get(url)
