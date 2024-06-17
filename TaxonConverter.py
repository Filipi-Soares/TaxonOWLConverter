import requests

def fetch_gbif_data(scientific_name):
    """Fetch taxonomic classification from GBIF API."""
    url = f"https://api.gbif.org/v1/species/match?name={scientific_name.replace(' ', '%20')}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def fetch_synonyms(species_key):
    """Fetch synonyms for a given species key from GBIF API."""
    url = f"https://api.gbif.org/v1/species/{species_key}/synonyms"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def accumulate_taxa(data, taxa):
    """Accumulate unique taxa and their relationships."""
    keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    for key in keys:
        if key in data and data[key] is not None:
            key_id = str(data[key + 'Key'])
            if key_id not in taxa:
                taxa[key_id] = {
                    "name": data[key],
                    "rank": key,
                    "parentKey": str(data.get(f"{keys[keys.index(key)-1]}Key", "1")) if key != 'kingdom' else None
                }

def validate_accepted_name(data, taxa):
    """Ensure that only the accepted name is included in the taxa."""
    if 'speciesKey' in data:
        synonyms = fetch_synonyms(data['speciesKey'])
        for synonym in synonyms:
            if 'acceptedKey' in synonym and synonym['acceptedKey'] == data['speciesKey']:
                # Ensure that the accepted name is in the taxa dictionary
                accepted_key_id = str(data['speciesKey'])
                if accepted_key_id not in taxa:
                    taxa[accepted_key_id] = {
                        "name": data['scientificName'],
                        "rank": 'species',
                        "parentKey": str(data['genusKey'])
                    }

def generate_owl(taxa):
    """Generate OWL representation from accumulated taxa."""
    base_url = "https://www.gbif.org/species/"
    owl_parts = ["""<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:owl="http://www.w3.org/2002/07/owl#">"""]

    for key, taxon in taxa.items():
        parent = f'\n        <rdfs:subClassOf rdf:resource="{base_url}{taxon["parentKey"]}"/>' if taxon["parentKey"] else ""
        owl_parts.append(f"""    <owl:Class rdf:about="{base_url}{key}">
        <rdfs:label xml:lang="lat">{taxon["name"]}</rdfs:label>{parent}
    </owl:Class>""")

    owl_parts.append("</rdf:RDF>")
    return "\n".join(owl_parts)

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

taxa = {}
for name in species_names:
    data = fetch_gbif_data(name)
    if data:
        accumulate_taxa(data, taxa)
        validate_accepted_name(data, taxa)

owl_data = generate_owl(taxa)
print(owl_data)




