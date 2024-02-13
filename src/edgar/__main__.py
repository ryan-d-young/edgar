import os
import json
from pathlib import Path
from pprint import pprint

from .cli import ARG_PARSER
from .endpoint import Endpoint
from .constants import MODNAME
from .map_tickers import sanitize_cik
from .parse import parse_response


with open(Path(os.getcwd()) / MODNAME / 'mappings' / 'ticker_to_cik_txt.json') as fp:
    MAP = json.load(fp)

endpoint = Endpoint()
namespace = ARG_PARSER.parse_args()
func = getattr(endpoint, f'get_{namespace.endpoint[0]}')

args = []
if namespace.args:
    if namespace.endpoint[0] in ['submissions', 'concept', 'facts']:
        ticker = namespace.args.pop(0)
        cik = MAP[ticker.lower()][0]
        args += [sanitize_cik(cik),]
    args += namespace.args

response = func(*args)

if response.status_code != 200:
    raise Exception(response.text)

processed = parse_response(response)
pprint(processed)

if namespace.output:
    with open(Path(namespace.output[0]), 'x') as fp:
        fp.write(result)
