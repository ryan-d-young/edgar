import datetime
from requests import Response

from .constants import DFMT


def _parse_submissions(response: Response) -> list[dict]:
    response = response.json()
    filings = response['filings']['recent']
    res = []

    for ix in range(len(filings['form'])):
        if (filings['form'][ix] == '10-K') or (filings['form'][ix] == '10-Q'):
            submission = {
                'form': filings['form'][ix],
                'accession_number': filings['accessionNumber'][ix],
                'filing_date': datetime.datetime.strptime(filings['filingDate'][ix], DFMT).date(),
                'report_date': datetime.datetime.strptime(filings['reportDate'][ix], DFMT).date(),
                'file_number': filings['fileNumber'][ix],
                'film_number': filings['filmNumber'][ix],
                'primary_document': filings['primaryDocument'][ix],
                'is_xbrl': bool(filings['isXBRL'][ix])}
            res.append(submission)

    return res


def _parse_concept(response: Response) -> list[dict]:
    response = response.json()
    res = []

    for unit in response['unitz'].keys():
        for record in response['units'][unit]:
            concept = {
                'unit': unit,
                'fiscal_year': record['fy'],
                'fiscal_quarter': record['fp'],
                'form': record['form'],
                'value': record['val'],
                'accession_number': record['accn']}
            res.append(concept)

    return res


def _parse_facts(response: Response) -> list[dict]:
    response = response.json()
    res = []

    for taxonomy in response['facts'].keys():
        for line_item in response['facts'][taxonomy].keys():
            facts = response['facts'][taxonomy][line_item]
            units = facts['units']
            for unit, records in units.items():
                for record in records:
                    fact = {
                        'taxonomy': taxonomy,
                        'line_item': line_item,
                        'unit': unit,
                        'label': facts['label'],
                        'description': facts['description'],
                        'end': datetime.datetime.strptime(record['end'], DFMT).date(),
                        'accession_number': record['accn'],
                        'fiscal_year': record['fy'],
                        'fiscal_period': record['fp'],
                        'form': record['form'],
                        'filed': record['filed']}
                    res.append(fact)

    return res


def _parse_frame(response: Response) -> list[dict]:
    response = response.json()
    res = []

    for record in response['data']:
        frame = {
            'taxonomy': response['taxonomy'],
            'line_item': response['tag'],
            'frame': response['ccp'],
            'unit': response['uom'],
            'label': response['label'],
            'description': response['description'],
            'accession_number': record['accn'],
            'cik': record['cik'],
            'entity_name': record['entityName'],
            'location': record['loc'],
            'end': datetime.datetime.strptime(record['end'], DFMT).date(),
            'value': record['val']}
        res.append(frame)

    return res


def parse_response(response: Response):
    url = response.url.split('/')
    try:
        if "submissions" in url:
            return _parse_submissions(response)
        elif "companyconcept" in url:
            return _parse_concept(response)
        elif "companyfacts" in url:
            return _parse_facts(response)
        elif "frames" in url:
            return _parse_frame(response)
        raise ValueError("Unrecognized response format"
                         f"url: {response.url}")
    except Exception as e:
        raise Exception("Error occurred during parsing...\n"
                        f"    {e.__class__.__name__}: {e}")
