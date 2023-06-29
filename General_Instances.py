import rdflib.namespace
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XMLNS, XSD
fdo = rdflib.Namespace("https://fairdmp.online/eco-system/")
sdo = SDO
rdf = RDF
rdfs = RDFS
fip = rdflib.Namespace("https://w3id.org/fair/fip/latest/FAIR-Implementation-Community")
dmp_ns = rdflib.Namespace("https://fairdmp.online/dmp/vu/")


g = rdflib.Graph()

#Instance level

#Vrije is of type Uni
# VuTemplate1.7 is of DMPTemplate
#VuTemplate1.7 consists_of Sections
# Sections consists_of TemplateQuestions
# TemplateQuestions hasTitle questionitself.
# TemplateQuestions of type DMPQuestions
# DMP quesitons of type Questions


g.add((fdo.VrijeUniversiteitAmsterdam, RDF.type, SDO.CollegeorUniversity))
g.add((fdo.TemplateQuestions, rdf.type, rdfs.DataManagementPlanQuestion))
g.add((fdo.DataManagementPlanQuestion, RDF.type, SDO.Question))
g.add((fdo.VuTemplate17, RDF.type, fdo.DataManagementPlanTemplate))
g.add((fdo.VuTemplate17, fdo.consistsOf, fdo.Section))
g.add((fdo.Section, fdo.consistsOf, fdo.TemplateQuestions))
g.add((fdo.Shuai, rdf.type, sdo.Reasearcher))
g.add((fdo.VrijeUniversiteitAmsterdam, fdo.providesDMPTemplate, fdo.VuTemplate17))
g.add((fdo.ShuaisDMP, fdo.usesDMPTemplate, fdo.VuTemplate17))
g.add((fdo.ShuaisDMP, sdo.maintainer, fdo.Kees))
g.add((fdo.Kees, rdf.type, fdo.DataSteward))
g.add((fdo.DataSteward, rdf.type, FOAF.Person))
g.add((fdo.Shuai, sdo.employee, fdo.VrijeUniversiteitAmsterdam))
g.add((fdo.Kees, sdo.employee, fdo.VrijeUniversiteitAmsterdam))
g.add((fdo.Shuai, sdo.author, fdo.ShuaisDMP))
