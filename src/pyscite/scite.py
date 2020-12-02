from pathlib import Path

import ndjson
import pandas as pd
import requests
from tqdm import tqdm


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

    def __api_get(self, url, doi, headers, params):
        # Execute query
        url = url.format(doi)
        r = self.session.get(url, headers=headers, params=params)

        # Check status code
        if r.status_code != 200:
            raise SciteException(f"HTTP Error ({r.status_code}): {r.text}")
        else:
            return r

    def get_doi(self, doi, citations="all", tallies=False, papers=False, df=False):
        """Retrieve data for one DOI

        Currently supported endpoints:

        - All
        - Incoming
        - Tallies
        """
        if citations not in self.endpoints:
            raise ValueError(
                f"Could not find '{citations}' in available endpoints. Try one of these: f{list(self.endpoints.values())}"
            )
        url = self.endpoints[citations]

        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        try:
            data = self.__api_get(url, doi, self.headers, params).json()
        except SciteException:
            raise

        # Add `papers` or `tallies` object depending on request
        if papers or tallies:
            result = [data["citations"]]
        else:
            return data["citations"]

        if papers:
            result.append(data["papers"])

        if tallies:
            result.append(data["tallies"])

        # Convert results to pandas dataframes if required
        if df:
            result[0] = pd.DataFrame.from_records(result[0])

            if papers:
                result[1] = pd.DataFrame.from_dict(result[1]).T
                result[1]["target"] = doi
                result[1].index = range(0, len(result[1]))

            if tallies:
                result[2] = pd.DataFrame.from_dict(result[2]).T
                result[2].index = range(0, len(result[2]))
                result[2].set_index("doi", inplace=True)

        return result

    def get_dois(
        self,
        dois,
        output,
        overwrite=False,
        citations="all",
        tallies=False,
        papers=False,
    ):
        # Verify correct function call
        if citations not in self.endpoints:
            raise ValueError(
                f"Could not find '{citations}' in available endpoints. Try one of these: f{list(self.endpoints.values())}"
            )

        if output is None:
            raise ValueError("'outfile' is missing. Please provide path.")

        # Setup outfile
        outfile = Path(output)
        if outfile.exists():
            if overwrite:
                outfile.write_text("")
            else:
                raise FileExistsError(
                    "Outfile already exists. Set 'overwrite' to True if you want to overwrite it."
                )

        # Set up API
        url = self.endpoints[citations]
        params = {"tallies": str(tallies).lower(), "papers": str(papers).lower()}

        with open(outfile, "a") as f:
            writer = ndjson.writer(f)
            for doi in tqdm(dois):
                # Get citations from Scite
                try:
                    result = self.__api_get(
                        url, doi, self.headers, params
                    )
                    result = result.json()['citations']
                    # print(len(result))
                except SciteException as e:
                    print(f"{doi} failed: {str(e)}")
                    continue

                # Write citation object as a line in jsonl
                for citation in result:
                    writer.writerow(citation)

    def citation_tally(self, doi):
        url = self.endpoints["tallies"]

        # list of dois is used
        if type(doi) is list:
            r = self.session.post(url, headers=self.headers, data=doi)
        else:
            r = self.session.get(url.format(doi), headers=self.headers)

        return r
