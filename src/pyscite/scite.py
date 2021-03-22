from pathlib import Path

import ndjson
import requests
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm


class SciteException(Exception):
    pass


class Scite:
    """Simple Scite API client.

    Currently two endpoints are implemented:

    - "incoming": provides overviews for citing articles for a select DOI
    - "all": returns both citing and cited articles for a select DOI
    """

    def __init__(self, api_key=None, ratelimit=(1, 1)):
        self.endpoints = {
            "incoming": "https://api.scite.ai/citations/citing/{}",
            "all": "https://api.scite.ai/citations/all/{}",
            "papers": "https://api.scite.ai/papers/{}",
            "tallies": "https://api.scite.ai/tallies/{}",
        }
        self.session = requests.session()

        self._api_get = sleep_and_retry
        self._api_get = limits(calls=ratelimit[0], period=ratelimit[1])

        if api_key:
            self.headers = {"Authorization": f"Bearer {api_key}"}
        else:
            self.headers = None

    def __api_get(self, url, doi, headers, params=None):
        # Execute query
        url = url.format(doi)
        r = self.session.get(url, headers=headers, params=params)

        # Check status code
        if r.status_code != 200:
            raise SciteException(f"HTTP Error ({r.status_code}): {r.text}")
        else:
            return r

    def doi(
        self, doi, only_incoming="all", citations=True, tallies=False, papers=False
    ):
        """Retrieve data for one DOI"""
        # Set up API
        if only_incoming:
            url = self.endpoints["incoming"]
        else:
            url = self.endpoints["all"]

        params = {
            "citations": str(citations).lower(),
            "tallies": str(tallies).lower(),
            "papers": str(papers).lower(),
        }

        try:
            data = self.__api_get(url, doi, self.headers, params).json()
        except SciteException:
            raise

        # Add `papers` or `tallies` object depending on request
        return data

    def citations(self, dois, output, overwrite=False, only_incoming=False):
        # Set up API
        if only_incoming:
            url = self.endpoints["incoming"]
        else:
            url = self.endpoints["all"]

        params = {"tallies": False, "papers": False}

        if output is None:
            raise ValueError("'outfile' is missing. Please provide path.")

        # Setup outfile
        outfile = Path(output)
        if outfile.exists():
            if overwrite:
                outfile.write_text("")
            else:
                raise FileExistsError(
                    "Outfile already exists. Set 'overwrite' "
                    "to True if you want to overwrite it."
                )

        with open(outfile, "a") as f:
            writer = ndjson.writer(f)
            for doi in tqdm(dois):
                # Get citations from Scite
                try:
                    result = self.__api_get(url, doi, self.headers, params)
                    result = result.json()["citations"]
                    # print(len(result))
                except SciteException as e:
                    print(f"{doi} failed: {str(e)}")
                    continue

                # Write citation object as a line in jsonl
                for citation in result:
                    writer.writerow(citation)

    def related_papers(self, dois, output, overwrite=False, only_incoming=False):
        # Set up API
        if only_incoming:
            url = self.endpoints["incoming"]
        else:
            url = self.endpoints["all"]

        params = {"papers": True, "tallies": False, "citations": False}

        if output is None:
            raise ValueError("'outfile' is missing. Please provide path.")

        # Setup outfile
        outfile = Path(output)
        if outfile.exists():
            if overwrite:
                outfile.write_text("")
            else:
                raise FileExistsError(
                    "Outfile already exists. Set 'overwrite' "
                    "to True if you want to overwrite it."
                )

        base = outfile.parent
        name = outfile.name
        log = Path(base / (name.split(".")[0] + "_log"))

        with open(log, "w") as logf:
            with open(outfile, "a") as f:
                writer = ndjson.writer(f)
                for doi in tqdm(dois):
                    # Get citations from Scite
                    try:
                        result = self.__api_get(url, doi, self.headers, params)
                    except SciteException as e:
                        logf.write(f"{doi} | {str(e)}\n")
                        continue

                    result = result.json()["papers"]
                    # Write citation object as a line in jsonl
                    for v in result.values():
                        writer.writerow(v)

    def papers(self, dois, output, overwrite=False, citations="all"):
        # Set up API
        url = self.endpoints["papers"]
        if type(dois) is not list:
            dois = [dois]

        if output is None:
            raise ValueError("'outfile' is missing. Please provide path.")

        # Setup outfile
        outfile = Path(output)
        if outfile.exists():
            if overwrite:
                outfile.write_text("")
            else:
                raise FileExistsError(
                    "Outfile already exists. Set 'overwrite' "
                    "to True if you want to overwrite it."
                )

        base = outfile.parent
        name = outfile.name
        log = Path(base / (name.split(".")[0] + "_log"))

        with open(log, "w") as logf:
            with open(outfile, "a") as f:
                writer = ndjson.writer(f)
                for doi in tqdm(dois):
                    # Get citations from Scite
                    try:
                        result = self.__api_get(url, doi, self.headers)
                    except SciteException as e:
                        logf.write(f"{doi} | {str(e)}\n")
                        continue

                    result = result.json()

                    # Write citation object as a line in jsonl
                    writer.writerow(result)

    def tallies(self, doi):
        url = self.endpoints["tallies"]

        # list of dois is used
        if type(doi) is list:
            r = self.session.post(url, headers=self.headers, data=doi)
        else:
            r = self.session.get(url.format(doi), headers=self.headers)

        return r
