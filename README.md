# Content-based Citations

> Reproduction material for paper

- Code
- Instruction to reproduce
- Results presented in paper
- Additional materials presented in paper

## Requirements

TBA

## Instructions

All scripts required to run are located in `scripts`.

1. `1_query_pubmed.py` - Retrieves a list of DOIs based on Pubmed query saved in `data/raw_data/pubmed/query.txt`
2. `2_collect_scite.py` - Collects all required Scite data based on the seed DOIs saved in `data/raw_data/pubmed/seed.csv`
3. `3_process_scite.py` - Transforms and merges data from Scite and creates processed datasets in `data/processed/`

Data exploration and analysis is conducted in notebooks which can be found in `notebooks/`.