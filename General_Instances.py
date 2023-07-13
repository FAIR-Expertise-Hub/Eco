import rdflib.namespace
from rdflib.namespace import  FOAF, RDF, RDFS, SDO
from rdflib import Literal


fdo = rdflib.Namespace("https://fairdmp.online/eco-system/")
sdo = SDO
rdf = RDF
rdfs = RDFS
dmp_ns = rdflib.Namespace("https://fairdmp.online/dmp/vu/")
fip = rdflib.Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")




g = rdflib.Graph()


g.bind("fip", fip)
g.bind("fdo", fdo)
g.bind("dmp", dmp_ns)

#Instance level

#Vrije is of type Uni
#VuTemplate1.7 is of DMPTemplate.
#VuTemplate1.7 consists_of Sections.
#Sections consists_of TemplateQuestions.
#TemplateQuestions hasTitle questionitself.
#TemplateQuestions of type DMPQuestions
#DMP quesitons of type Questions


g.add((fdo.VrijeUniversiteitAmsterdam, RDF.type, SDO.CollegeOrUniversity))
g.add((fdo.TemplateQuestions, rdf.type, fdo.DataManagementPlanQuestion))
g.add((fdo.DataManagementPlanQuestion, RDF.type, SDO.Question))
g.add((Literal("1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3"), RDF.type, fdo.DataManagementPlanTemplate))
g.add((Literal("1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3"), fdo.consistsOf, fdo.TemplateSection))
g.add((fdo.TemplateSection, fdo.consistsOf, fdo.TemplateQuestions))
g.add((fdo.DataSteward, rdf.type, FOAF.Person))
g.add((fdo.RDMSupport, fdo.consistsOf, fdo.DataSteward))
g.add((fdo.VrijeUniversiteitAmsterdam, fdo.providesDMPTemplate, fdo.VuTemplate17))
g.add((fdo.VuLegalTeam, rdf.type, fdo.UniversityLegalTeam))
g.add((fdo.DataManagementPlan, RDF.type, fip["FAIR-Enabling-Resource"]))
g.add((fdo.RDMPlatform, rdf.type, fip["FAIR-Enabling-Resource"]))


g.add((fdo.UniversityResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))
g.add((fdo.FacultyResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))
g.add((fdo.DepartmentResearchDataManagement, rdfs.subClassOf, fdo.RDMSupport))



g.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/General_Instances.ttl',
            format='turtle')


