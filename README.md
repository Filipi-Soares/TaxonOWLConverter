# GBIF Taxonomy to OWL Converter

## Overview

This Python program fetches taxonomic classification information for a list of species from the Global Biodiversity Information Facility (GBIF) API and generates an Ontology Web Language (OWL) representation of the taxonomy. It is designed to handle multiple species, ensuring that higher taxonomic levels are represented only once, even if they are shared across species.

## Requirements

- Python 3.x
- `requests` library

To install the required requests library, run:

`pip install requests`

## Usage

Start by defining a list of scientific names for the species you're interested in. For example:

```python
species_names = [
    "Apis mellifera",
    "Bos taurus",
    "Panthera leo"
]

Execute the program. It will iterate over each species name, fetch its taxonomic data from the GBIF API, and accumulate the unique taxonomic levels.
