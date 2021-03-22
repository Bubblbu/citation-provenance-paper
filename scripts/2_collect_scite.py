"""Scite collection script

Based on a seed file (`data/raw_data/pubmed/seed.csv`) with DOIs this script
will collect four datasets from Scite:

1. The metadata for the seed articles
2. *Only* the incoming citations for those seed articles
3. The metadata for those incoming articles that cite the seed articles are
4. *All* citations for the seed-citing articles

Each file will *NOT* be collected if it already exists on disk. Make sure to
remove files if re-collection is required. All files will be saved in 
`data/raw_data/scite/`
"""

import os
from pathlib import Path
from typing import List

import pandas as pd
from dotenv import load_dotenv, find_dotenv

from pyscite.scite import Scite


# Data directories
data_dir = Path("../data")

raw_dir = data_dir / "raw_data"
pubmed_dir = raw_dir / "pubmed"
scite_dir = raw_dir / "scite"


def collect_citations(scite: Scite, dois: List, f: Path, only_incoming: bool) -> None:
    if not f.exists():
        scite.citations(dois, f)
    else:
        print("{f} already exists. Skipping.")


def collect_metadata(scite: Scite, dois: List, f: Path) -> None:
    if not f.exists():
        scite.papers(dois, f)
    else:
        print("{f} already exists. Skipping.")


if __name__ == "__main__":
    # Setup Scite client
    load_dotenv(find_dotenv())

    SCITE_KEY = os.getenv("SCITE_KEY")
    TOOL = os.getenv("TOOL")
    EMAIL = os.getenv("EMAIL")

    scite = Scite(SCITE_KEY)

    # Load seed DOI file
    seed_f = pubmed_dir / "1000_doi_sample.csv"
    seed_dois = pd.read_csv(seed_f)
    seed_dois = seed_dois.doi.tolist()

    #################
    # SEED ARTICLES #
    #################

    # Collect metadata for seed articles if not existing already
    print("=== Collecting metadata for seed articles")
    seed_metadata_f = scite_dir / "seed_papers.jsonl"
    collect_metadata(scite, seed_dois, seed_metadata_f)

    # Collect incoming citations for seed articles
    print("=== Collecting incoming citations for seed articles")
    seed_citations_f = scite_dir / "seed_incoming_citations.jsonl"
    collect_citations(scite, seed_dois, seed_citations_f, True)

    #####################
    # INCOMING ARTICLES #
    #####################

    # Load incoming DOIs
    seed_cites_f = scite_dir / "seed_incoming_citations.jsonl"
    seed_incoming_citations = pd.read_json(seed_cites_f, orient="records", lines=True)
    incoming_dois = seed_incoming_citations.source.unique().tolist()

    # Collect metadata for seed articles if not existing already
    print("=== Collecting metadata incoming articles")
    incoming_metadata_f = scite_dir / "incoming_papers.jsonl"
    collect_metadata(scite, incoming_dois, incoming_metadata_f)

    # Collect incoming citations for seed articles
    print("=== Collecting all citations for incoming articles")
    incoming_citations_f = scite_dir / "incoming_citations.jsonl"
    collect_citations(scite, incoming_dois, incoming_citations_f, False)
