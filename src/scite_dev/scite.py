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

    def __init__(self, api_key=None):
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

    def __api_get(self, url, headers, params, papers, tallies, df):
        r = self.session.get(url, headers=headers, params=params)
        if r.status_code != 200:
            raise SciteException(f"Status code: {r.status_code}\n{r.text}")
        data = r.json()
        citation_object = data["citations"]
        if df:
            citation_object = pd.DataFrame.from_records(citation_object)

        result = [citation_object]

        if papers:
            papers_object = data["papers"]
            if df:
                papers_object = pd.DataFrame.from_dict(papers_object).T
            result.append(papers_object)

        if tallies:
            tallies_object = data["tallies"]
            if df:
                tallies_object = pd.DataFrame.from_dict(tallies_object).T
            result.append(tallies_object)

        return result

    def citations_incoming(self, doi, tallies=False, papers=False, df=False):
        url = self.endpoints["incoming"].format(doi)
        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        try:
            result = self.__api_get(url, self.headers, params, papers, tallies, df)
        except SciteException:
            raise

        return result

    def citations_all(self, doi, tallies=False, papers=False, df=False):
        url = self.endpoints["all"].format(doi)
        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        try:
            result = self.__api_get(url, self.headers, params, papers, tallies, df)
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
