import re
from rdflib import Graph, Literal, Namespace, RDF, URIRef, FOAF, SDO, SKOS, DC
fip = Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")
fdo = Namespace("https://fairdmp.online/eco-system/")

g = Graph()
def extract_properties(trig_file):
    with open(trig_file, 'r') as file:
        content = file.read()

    # Use regular expression to find the assertions and extract the properties
    pattern = r':assertion\s*{(.*?)\s*}'
    assertions = re.findall(pattern, content, flags=re.DOTALL)

    properties = []
    for assertion in assertions:
        refers_to_question = None
        declares_current_use_of = None

        # Find the refers-to-question property
        refers_to_question_match = re.search(r':declaration\s+fip:refers-to-question\s+fip:(\S+)', assertion)
        if refers_to_question_match:
            refers_to_question = refers_to_question_match.group(1)

        # Find the declares-current-use-of property
        declares_current_use_of_match = re.search(r':declaration\s+fip:declares-current-use-of\s+<(\S+)>', assertion)
        if declares_current_use_of_match:
            declares_current_use_of = declares_current_use_of_match.group(1)

        # Append properties if both refers-to-question and declares-current-use-of are found in the same assertion
        if refers_to_question and declares_current_use_of:
            properties.append({
                'refers_to_question': refers_to_question,
                'declares_current_use_of': declares_current_use_of
            })

    return properties

# Example usage
trig_file = 'FIP/CMIP6_data_FIP.trig'  # Replace with your actual trig file name
extracted_properties = extract_properties(trig_file)

# Print the extracted properties
for prop in extracted_properties:
    g.add((Literal(prop['refers_to_question']), fdo.canHaveAnswer, Literal(prop['declares_current_use_of'])))
    #print('Refers to question:', prop['refers_to_question'])
    #print('Declares current use of:', prop['declares_current_use_of'])
    #print(g9
g.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/FIP_analysis_converted.ttl', format='turtle')