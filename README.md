# [WIP] Citational Engagement

> Reproduction material for paper

Paper abstract:

*Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract Abstract*

---

This repository contains:

- Links to additional material
- Results and outputs presented in the paper
- Data collection and analysis code
- Instruction to reproduce

## The paper and other resources

- Provide link to data.
- Provide link to preprint.
- Provide link to published version.

## Reproduction

### Requirements

- Python v3.x.x
- Poetry v1.x.x

### Instructions

All scripts required to run are located in `scripts`.

1. `1_query_pubmed.py` - Retrieves a list of DOIs based on Pubmed query saved in `data/raw_data/pubmed/query.txt`
2. `2_collect_scite.py` - Collects all required Scite data based on the seed DOIs saved in `data/raw_data/pubmed/seed.csv`
3. `3_process_scite.py` - Transforms and merges data from Scite and creates processed datasets in `data/processed/`

Data exploration and analysis is conducted in notebooks which can be found in `notebooks/`.