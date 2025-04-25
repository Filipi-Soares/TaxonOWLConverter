# Taxonomy OWLizer

## Overview

This script fetches taxonomic classification data for given species names from the GBIF API and generates an OWL ontology representation of the taxonomy. It ensures that only accepted scientific names are included in the OWL representation, ignoring synonyms.

## Requirements

- Python 3.x
- `requests` library

## Functions

### `fetch_gbif_data(scientific_name)`

Fetches taxonomic classification from the GBIF API for a given scientific name.

- Parameters: `scientific_name` (str) - The scientific name of the species.
- Returns: `dict` - The JSON response from the API containing taxonomic data, or None if the request fails.

Example:

```python
data = fetch_gbif_data("Apis mellifera")
```

### `fetch_synonyms(species_key)`

Fetches synonyms for a given species key from the GBIF API.

Parameters:

`species_key (int)`: The unique key identifying the species in the GBIF database.

Returns:

`list`: A list of dictionaries, each representing a synonym of the species, or an empty list if the request fails.

Example:

```python
synonyms = fetch_synonyms(1341976)
```

### `accumulate_taxa(data, taxa)`

Accumulates unique taxa and their relationships from the provided taxonomic data into the taxa dictionary.

Parameters:
- `data` (dict): The taxonomic data for a species.
- `taxa` (dict): A dictionary to store unique taxa and their relationships.

### `validate_accepted_name(data, taxa)`

Ensures that only the accepted scientific name is included in the taxa dictionary by validating against synonyms.
Parameters:

  
### `generate_owl(taxa)`
Generates an OWL representation from the accumulated taxa.

Parameters: taxa (dict) - A dictionary containing unique taxonomic information.
Returns: A string containing the OWL representation of the taxonomy.

### Usage

1. Define a list of species names you want to include in the ontology.

```python
species_names = [
    "Apis mellifera",
    "Bos taurus",
    "Capra aegagrus hircus",
    "Ovis aries",
    "Sus",
    "Prochilodus cearensis",
    "Prochilodus scrofa",
    "Prochilodus margravii",
    "Semaprochilodus insignis",
    "Semaprochilodus taeniurus",
    "Colossoma mitrei",
    "Arapaima gigas",
    "Tilapia"
]
```
2. Iterate through the list of species names, fetch their taxonomic data, accumulate the taxa, and validate accepted names.

```python
taxa = {}
for name in species_names:
    data = fetch_gbif_data(name)
    if data:
        accumulate_taxa(data, taxa)
        validate_accepted_name(data, taxa)
```

3. Generate the OWL representation from the accumulated taxa.

```python
owl_data = generate_owl(taxa)
print(owl_data)
```

The program generates an OWL representation of the accumulated taxonomy, ensuring that each taxonomic level is included only once, and prints it to the console.

## Citation
Soares, F. M. (2024). Taxonomy OWLizer. Zenodo. [https://doi.org/10.5281/zenodo.14984136](https://doi.org/10.5281/zenodo.14984136)






