"""Process data from scite and rearrange to project structure

This script processes the four files collected from Scite with the
previous script (`scripts/2_collect_scite.py`) and processes and
combines the files into a new structure:

1. `contexts.csv` - a file containing metadata for each article in the dataset
2. `traces.csv` - contains the basic citational traces of
3. `citation_patterns.csv` - patterns that Scite provides for each citation
"""
