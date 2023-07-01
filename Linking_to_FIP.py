import json, re, html, urllib.parse
from rdflib import Graph, Literal, Namespace, RDF, URIRef, FOAF, SDO, SKOS, DC

g = Graph()
#Instance level:
#A question in a DMP can use a specific FER in a specific FIP

#FAIR Principles that are corralated to the DMP
# F1,F2,F4,A1.2,R1.1,R1.2.

#Related Fair Enabling Resources

# Define namespaces
fdo = Namespace("https://fairdmp.online/eco-system/")
dmp_ns = Namespace("https://fairdmp.online/dmp/vu/")
fip = Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")



#fip.["FAIR-Enabling Resource"]
#fip.["Identifier service"]
#fip.["declares planned use of"]
#fdo.requiredBy

# The relation property declares planned use of might not be the ideal property for ouy situation, some other candidate relations are
# : fdo"achieved_by" fdo"required_by" fip"declares use of"

#FAIR principles and their fair enabling artifacts
g.add((fip.F1, fip["declares planned use of"], fip["Identifier service"]))
g.add((fip.F2, fip["declares planned use of"], fip["Metadata schema"]))
g.add((fip.F4, fip["declares planned use of"], fip["Metadata-data linking schema"]))
g.add((fip["A1.2"], fip["declares planned use of"], fip["Authentication and authorization service"]))
g.add((fip["R1.1"], fip["declares planned use of"], fip["Data usage license"]))
g.add((fip["R1.2"], fip["declares planned use of"], fip["Provenance model"]))


g.add((fip["Identifier service"], RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fip["Metadata schema"], RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fip["Metadata-data linking schema"], RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fip["Authentication and authorization service"], RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fip["Data usage license"], RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fip["Provenance model"], RDF.type, fip["FAIR-Enabling-Resource"]))




