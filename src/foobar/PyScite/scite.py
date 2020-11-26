import requests

import pandas as pd


class SciteException(Exception):
    pass


class Scite:
    """Simple Scite API client.

    Currently two endpoints are implemented:

    - "incoming": provides overviews for citing articles for a select DOI
    - "all": returns both citing and cited articles for a select DOI
    """

    def __init__(
        self,
        api_key=None,
    ):
        self.endpoints = {
            "incoming": "https://api.scite.ai/citations/citing/{}",
            "all": "https://api.scite.ai/citations/all/{}",
            "tallies": "https://api.scite.ai/tallies/",
        }
        self.session = requests.session()

        if api_key:
            self.headers = {"Authorization": f"Bearer {api_key}"}
        else:
            self.headers = None

    def __api_get(self, url, doi, headers, params, papers, tallies, df):
        # Execute query
        url = url.format(doi)
        r = self.session.get(url, headers=headers, params=params)

        # Check status code
        if r.status_code != 200:
            raise SciteException(f"HTTP Error ({r.status_code}): {r.text}")

        # Data
        data = r.json()

        citation_object = data["citations"]
        if df:
            citation_object = pd.DataFrame.from_records(citation_object)

        if papers or tallies:
            result = [citation_object]
        else:
            return citation_object

        if papers:
            papers_object = data["papers"]
            if df:
                papers_object = pd.DataFrame.from_dict(papers_object).T
                papers_object["target"] = doi
                papers_object.index = range(0, len(papers_object))
            result.append(papers_object)

        if tallies:
            tallies_object = data["tallies"]
            if df:
                tallies_object = pd.DataFrame.from_dict(tallies_object).T
                tallies_object.index = range(0, len(tallies_object))
                tallies_object.set_index("doi", inplace=True)
            result.append(tallies_object)

        return result

    def get_doi(self, doi, citations="all", tallies=False, papers=False, df=False):
        if citations not in self.endpoints:
            raise SciteException(f'"{citations}" is not in the available endpoints')
        url = self.endpoints[citations]

        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        try:
            result = self.__api_get(url, doi, self.headers, params, papers, tallies, df)
        except SciteException:
            raise

        return result

    def get_dois(self, dois, citations="all", tallies=False, papers=False, df=False):
        if citations not in self.endpoints:
            raise SciteException(f'"{citations}" is not in the available endpoints')
        url = self.endpoints[citations]

        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        # TODO

        try:
            result = self.__api_get(
                url, dois, self.headers, params, papers, tallies, df
            )
        except SciteException:
            raise

        return result

    def citation_tally(self, doi):
        url = self.endpoints["tallies"]

        # list of dois is used
        if type(doi) is list:
            r = self.session.post(url, headers=self.headers, data=doi)
        else:
            r = self.session.get(url.format(doi), headers=self.headers)

        return r
