import json, re, html, urllib.parse

import rdflib
from rdflib import Graph, Literal, Namespace, RDF, URIRef, FOAF, SDO, SKOS, DC


path_to_files = 'C:/Users/MSI-NB/PycharmProjects/firstProject/JSON DMP Files/'
dmp_file_ids = [112581]

for file_id in dmp_file_ids:
    file_name = str(file_id) + '.json'
    with open(path_to_files + file_name) as file:
        data = json.load(file)
        dmp = data[0][0]

# Define namespaces
fdo = Namespace("https://fairdmp.online/eco-system/")
dmp_ns = Namespace("https://fairdmp.online/dmp/vu/")
fip = Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")

graph = rdflib.Graph()
# Extract and add section data
plan_contents = dmp.get('plan_content', [])
for plan in plan_contents:
    sections = plan.get('sections', [])
    for section in sections:
        section_number = int( section.get('number')-1)
        section_node = URIRef(dmp_ns + str(file_id) + "/section/" + str(section_number))

        questions = section.get('questions', [])
        for question in questions:
                question_number = question.get('number')
                answer = question.get('answer')
                question_node = URIRef(dmp_ns + str(file_id) + "/section/" + str(section_number) + "/question/" + str(question_number))

                if section_number == 0:
                    if question_number == 4:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 5:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 6:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 7:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 8:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                if section_number == 4:
                    if question_number == 2:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F4))
                    if question_number == 3:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F4))
                    if question_number == 6:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F4))
                    if question_number == 7:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F4))
                    if question_number == 8:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 9:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F1))
                    if question_number == 10:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["A1.2"]))
                    if question_number == 11:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["A1.2"]))
                    if question_number == 13:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["R1.1"]))
                if section_number == 5:
                    if question_number == 1:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["R1.2"]))
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["F2"]))
                    if question_number == 2:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["R1.3"]))
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip.F2))
                    if question_number == 3:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["R1.2"]))
                if section_number == 6:
                    if question_number == 3:
                        graph.add((question_node, fdo["questionRefersToPrincipal"], fip["A1.2"]))
    

# Serialize the graph to TTL format
graph.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/DMP1_Linking_To_FIP.ttl', format='turtle')