import rdflib.namespace
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
fdo = rdflib.Namespace("https://fairdmp.online/eco-system/")
sdo = SDO
rdf = RDF
rdfs = RDFS
fip = rdflib.Namespace("https://w3id.org/fair/fip/latest/FAIR-Implementation-Community")

#Instance level

#Vrije is of type Uni
# VuTemplate1.7 is of DMPTemplate
#VuTemplate1.7 consists_of Sections
# Sections consists_of TemplateQuestions
# TemplateQuestions hasTitle questionitself.
# TemplateQuestions of type DMPQuestions
# DMP quesitons of type Questions


g.add((fdo.Vrije, RDF.type, SDO.CollegeorUniversity))
