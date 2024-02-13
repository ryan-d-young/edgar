import json
import requests
from pathlib import Path

from .constants import TIMEOUT_SEC, USER_AGENT, MODNAME


def sanitize_cik(cik: int | str) -> str:
    cik = str(cik)
    cik = '0' * (10 - len(cik)) + cik
    return cik


def _fetch_raw_json_mapping() -> requests.Response:
    url = 'https://www.sec.gov/files/company_tickers.json'
    request = requests.get(
        url,
        headers={
            'Host': 'www.sec.gov',
            'User-Agent': USER_AGENT,
            'Accept-Encoding': 'gzip, deflate'},
        timeout=TIMEOUT_SEC)
    return request


def _fetch_raw_txt_mapping() -> requests.Response:
    url = 'https://www.sec.gov/include/ticker.txt'
    request = requests.get(
        url,
        headers={
            'Host': 'www.sec.gov',
            'User-Agent': USER_AGENT,
            'Accept-Encoding': 'gzip, deflate'},
        timeout=TIMEOUT_SEC)
    return request


def _load_raw_json_mapping(root: str) -> str:
    fp = Path(root) / 'mappings' / 'company_tickers.json'
    with open(fp) as file:
        file = file.read()
    return file


def _load_raw_txt_mapping(root: str) -> str:
    fp = Path(root) / MODNAME / 'mappings' / 'ticker.txt'
    with open(fp) as file:
        file = file.read()
    return file


def _load_json_mapping(root: str, index_on_cik: bool = True):
    fp = Path(root) / MODNAME / 'mappings'
    fp = fp / 'cik_to_ticker_json.json' if index_on_cik else fp / 'ticker_to_cik_json.json'
    if fp.exists():
        with open(fp) as file:
            file = file.read()
            res = json.loads(file)
    else:
        file = _load_raw_json_mapping(root)
        res = process_json_mapping(file, index_on_cik)
    return res


def _load_txt_mapping(root: str, index_on_cik: bool = True):
    fp = Path(root) / 'mappings'
    fp = fp / 'cik_to_ticker_txt.txt' if index_on_cik else fp / 'ticker_to_cik_txt.txt'
    if fp.exists():
        with open(fp) as file:
            file = file.read()
            res = json.loads(file)
    else:
        file = load_raw_txt_mapping(root)
        res = process_txt_mapping(file, index_on_cik)
    return res


def _save_json_mapping(mapping: dict, root: str, index_on_cik: bool = True):
    fp = Path(root) / MODNAME / 'mappings'
    fp = fp / 'cik_to_ticker_json.json' if index_on_cik else fp / 'ticker_to_cik_json.json'
    mapping = json.dumps(mapping)
    with open(fp, mode='w') as file:
        file.write(mapping)


def _save_txt_mapping(mapping: dict, root: str, index_on_cik: bool = True):
    fp = Path(root) / MODNAME / 'mappings'
    fp = fp / 'cik_to_ticker_txt.json' if index_on_cik else fp / 'ticker_to_cik_txt.json'
    mapping = json.dumps(mapping)
    with open(fp, mode='w') as file:
        file.write(mapping)


def _process_txt_mapping(raw: bytes, index_on_cik: bool = True) -> dict[str, list[str]]:
    res = {}
    pairs = raw.decode().split('\n')

    def cik_to_ticker(res: dict, pairs: list[str]) -> dict[str, list[str]]:
        for pair in pairs:
            ticker, cik = pair.split('\t')
            if cik not in res.keys():
                res[cik] = [ticker,]
            else:
                res[cik] += [ticker,]
        return res
    
    def ticker_to_cik(res: dict, pairs: list[str]) -> dict[str, list[str]]:
        for pair in pairs:
            ticker, cik = pair.split('\t')
            if ticker not in res.keys():
                res[ticker] = [cik,]
            else:
                res[ticker] += [cik,]
        return res
            
    return cik_to_ticker(res, pairs) if index_on_cik else ticker_to_cik(res, pairs)


def _process_json_mapping(raw: bytes, index_on_cik: bool = True) -> dict[str, dict[str, str]]:
    res = {}
    raw = json.loads(raw)
    
    def cik_to_ticker(res: dict, raw: dict) -> dict[str, dict[str, str]]:
        for record in raw.values():
            if record['cik_str'] not in res.keys():
                res[record['cik_str']] = {}
                res[record['cik_str']]['name'] = [record['title'],]
                res[record['cik_str']]['ticker'] = [record['ticker'],]
            else:
                res[record['cik_str']]['name'] += [record['title'],]
                res[record['cik_str']]['ticker'] += [record['ticker'],]
        return res
    
    def ticker_to_cik(res: dict, raw: dict) -> dict[str, dict[str, str]]:
        for record in raw.values():
            if record['ticker'] not in res.keys():
                res[record['ticker']] = {}
                res[record['ticker']]['name'] = [record['title'],]
                res[record['ticker']]['cik'] = [record['cik_str'],]
            else:
                res[record['ticker']]['name'] += [record['title'],]
                res[record['ticker']]['cik'] += [record['cik_str'],]
        return res
    
    return cik_to_ticker(res, raw) if index_on_cik else ticker_to_cik(res, raw)


def main():
    import os
    root = os.getcwd()
    
    json_mapping = _fetch_raw_json_mapping().content
    json_mapping_cik_ix = _process_json_mapping(json_mapping)
    json_mapping_ticker_ix = _process_json_mapping(json_mapping, index_on_cik=False)
    _save_json_mapping(json_mapping_cik_ix, root)
    _save_json_mapping(json_mapping_ticker_ix, root, index_on_cik=False)

    txt_mapping = _fetch_raw_txt_mapping().content
    txt_mapping_cik_ix = _process_txt_mapping(txt_mapping)
    txt_mapping_ticker_ix = _process_txt_mapping(txt_mapping, index_on_cik=False)
    _save_txt_mapping(txt_mapping_cik_ix, root)
    _save_txt_mapping(txt_mapping_ticker_ix, root, index_on_cik=False)


if __name__ == '__main__':
     main()
