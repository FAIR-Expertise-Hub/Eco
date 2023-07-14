import rdflib.namespace
from rdflib.namespace import  FOAF, RDF, RDFS, SDO, URIRef
from rdflib import Literal


fdo = rdflib.Namespace("https://fairdmp.online/eco-system/")
#dmp_ns = rdflib.Namespace("https://fairdmp.online/dmp/vu/")
fip = rdflib.Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")
sdo = SDO
rdf = RDF
rdfs = RDFS

g = rdflib.Graph()


g.bind("fip", fip)
g.bind("fdo", fdo)
#g.bind("dmp", dmp_ns)

#Instance level

#Vrije is of type Uni
#VuTemplate1.7 is of DMPTemplate.
#VuTemplate1.7 consists_of Sections.
#Sections consists_of TemplateQuestions.
#TemplateQuestions hasTitle questionitself.
#TemplateQuestions of type DMPQuestions
#DMP quesitons of type Questions
vu_template = URIRef("https://fairdmp.online/dmp/vu/VU-DMP-template-2021-NWO-ZonMW-certified-v1.3")


g.add((fdo.VrijeUniversiteitAmsterdam, RDF.type, SDO.CollegeOrUniversity))
g.add((fdo.TemplateQuestions, rdf.type, fdo.DataManagementPlanQuestion))
g.add((fdo.DataManagementPlanQuestion, RDF.type, SDO.Question))
g.add((vu_template, RDF.type, fdo.DataManagementPlanTemplate))
g.add((vu_template, fdo.consistsOf, fdo.TemplateSection))
g.add((fdo.TemplateSection, fdo.consistsOf, fdo.TemplateQuestions))
g.add((fdo.DataSteward, rdf.type, FOAF.Person))
g.add((fdo.RDMSupport, fdo.consistsOf, fdo.DataSteward))
g.add((fdo.VrijeUniversiteitAmsterdam, fdo.providesDMPTemplate, vu_template))
g.add((fdo.VuLegalTeam, rdf.type, fdo.UniversityLegalTeam))
g.add((fdo.DataManagementPlan, RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fdo.RDMPlatform, rdf.type, fip["FAIR-Enabling-Resource"]))
g.add((sdo.GovernmentOffice, fdo.hasImpactOn, fdo.UniversityLegalTeam))
g.add((sdo.GovernmentOffice, fdo.hasImpactOn, fdo.RDMPlatform))




g.add((fdo.UniversityResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))
g.add((fdo.FacultyResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))
g.add((fdo.DepartmentResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))



g.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/General_Instances.ttl',
            format='turtle')

