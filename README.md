# edgar

Provides programmatic access to the SEC's Edgar API via the command-line, or within your Python project. Queries are made using company tickers rather than the SEC's CIK identifier.

# Install
It is recommended to use Rye, e.g.,

1. Clone: `git clone https://github.com/ryan-d-young/edgar.git`
2. Set up venv: `cd edgar/src/edgar && rye sync`
3. Set user agent* environment variable: `export $EDGAR_USER_AGENT="<COMPANY NAME> <E-MAIL>"`
4. (Optional) Refresh mappings: `cd .. && python -m edgar.map_tickers`

*Per the SEC's guidelines, declaring your user agent in this format is essential in order to use the API. 

# Usage
The following maps Edgar endpoints to package functionality:

| Endpoint | Command-line* | Python |
| -------- | ------------ | ------ |
| /submissions/ | `edgar submissions --args <TICKER>` | `Endpoint.get_submissions(<TICKER>)` |
| /xbrl/companyconcept/ | `edgar concept --args <TICKER> <TAG>` | `Endpoint.get_concept(<TICKER>, <TAG>)` |
| /xbrl/companyfacts/ | `edgar facts --args <TICKER>` | `Endpoint.get_facts(<TICKER>)` |
| /xbrl/frames/ | `edgar frame --args <TAG> <PERIOD>` | `Endpoint.get_frame(<TAG>, <PERIOD>)` |

You may also specify `--output <DEST>` for a json dump of the return. The workflow in mind is to leverage OS scripting languages to automate data gathering. As all API responses are parsed as lists of flat dictionaries, integration with a columnar database would be trivial.

*Assumes edgar is installed globally. If not, set your working directory to one level above the module and prefix any of the above commands with `python -m` as in the example below. 

*For more information on the API itself: https://www.sec.gov/edgar/sec-api-documentation*
