import re
from rdflib import Graph, Literal, Namespace, RDF, URIRef, FOAF, SDO, SKOS, DC

fip = Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")
fdo = Namespace("https://fairdmp.online/eco-system/")

g = Graph()

# Bind the prefix to a namespace URI
g.bind("fip", fip)
g.bind("fdo", fdo)



def extract_fip_pubinfo(trig_file):
    with open(trig_file, 'r') as file:
        content = file.read()

    # Use regular expression to find the pubinfo
    pattern_pub = r':pubinfo\s*{(.*?)\s*}'
    pub = re.findall(pattern_pub, content, flags=re.DOTALL)

    # Find the FIP URI
    fip_uri = None
    for i in pub:
        fip_uri_match = re.findall(r'prov:wasDerivedFrom\s+<([^>]+)>', i)
        fip_uri = str(set(fip_uri_match))
        return fip_uri

def extract_properties(trig_file):
    with open(trig_file, 'r') as file:
        content = file.read()
    # Use regular expression to find the assertions
    pattern = r':assertion\s*{(.*?)\s*}'
    assertions = re.findall(pattern, content, flags=re.DOTALL)

    properties = []
    for assertion in assertions:
        # reset the variables
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
                'fip_questions': refers_to_question,
                'fair_enabling_resources': declares_current_use_of
            })

    return properties


# Load the FIP file
trig_file = 'FIP/CMIP6_data_FIP.trig'
extracted_properties = extract_properties(trig_file)
fip_uri = str(extract_fip_pubinfo(trig_file))[2:-2]
# Add namespace for the FIP
dec = Namespace(fip_uri)
g.bind("dec", dec)
# Print the extracted properties
for prop in extracted_properties:
    #Add declared FER
    g.add(((dec[(prop['fip_questions'])]), fip['declares-current-use-of'], URIRef(prop['fair_enabling_resources'])))
    #Add possible answer
    g.add(((fip[(prop['fip_questions'])]), fdo.canHaveAnswer, URIRef(prop['fair_enabling_resources'])))
    #Add related principle
    thePrinciple = (str(prop['fip_questions']).split('-'))[2]
    g.add(((fip[(prop['fip_questions'])]), fip["refers-to-question"], fip[thePrinciple]))

g.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/FIP_analysis_converted.ttl',
            format='turtle')
