from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

def fetch_gbif_data(scientific_name, retries=3):
    """Fetch taxonomic classification from GBIF API with retries."""
    url = f"https://api.gbif.org/v1/species/match?name={scientific_name.replace(' ', '%20')}"
    
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "scientificName" not in data:
                return None  # Handle missing data gracefully
            return data
        print(f"Retrying {scientific_name}... Attempt {attempt + 1}")
        time.sleep(2)  # Wait before retrying
    
    return None

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

@app.route('/')
def home():
    return "TaxonOWLConverter API is running!", 200

@app.route('/generate_owl', methods=['POST'])
def generate_owl_api():
    request_data = request.json
    print("Received request:", request_data)  # Debugging

    species_names = request_data.get("species", [])
    if not species_names:
        return jsonify({"error": "No species provided"}), 400  # Handle empty input

    taxa = {}
    for name in species_names:
        data = fetch_gbif_data(name)
        print(f"Fetched GBIF data for {name}:", data)  # Debugging

        if data:
            accumulate_taxa(data, taxa)
            validate_accepted_name(data, taxa)
    
    owl_data = generate_owl(taxa)
    print("Generated OWL:", owl_data)  # Debugging

    return jsonify({"owl": owl_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
