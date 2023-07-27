#In charge of class level
import rdflib.namespace
from rdflib.namespace import  RDF, RDFS, SDO

fdo = rdflib.Namespace("https://fairdmp.online/eco-system/")
sdo = SDO
rdf = RDF
rdfs = RDFS
fip = rdflib.Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")

g = rdflib.Graph()


g.add((fdo.RDMPlatform, rdf.type, rdfs.Class))
g.add((fdo.RDMPlatform, rdfs.label, rdflib.Literal("RDMSoftware Systems, Data repositories, Data Management Platforms: Including the FIP Wizard,Yoda,Github etc..")))
g.add((fdo.RDMSupport, rdf.type, rdfs.Class))
g.add((fdo.RDMSupport, rdfs.label, rdflib.Literal("University Research Data Management, Department Research Data Management, Faculty Research Data Management")))
g.add((fdo.DepartmentResearchDataManagement, rdf.type, rdfs.Class))
g.add((fdo.DepartmentResearchDataManagement, rdfs.label, rdflib.Literal("DepartmentResearchDataManagement")))
g.add((fdo.FacultyResearchDataManagement, rdf.type, rdfs.Class))
g.add((fdo.FacultyResearchDataManagement, rdfs.label, rdflib.Literal("FacultyResearchDataManagement")))
g.add((fdo.UniversityResearchDataManagement, rdf.type, rdfs.Class))
g.add((fdo.UniversityResearchDataManagement, rdfs.label, rdflib.Literal("UniversityResearchDataManagement")))
g.add((fdo.UniversityLegalTeam, rdf.type, rdfs.Class))
g.add((fdo.UniversityLegalTeam, rdfs.label, rdflib.Literal("The team responsible of preparing the legal policies for a university")))
g.add((fdo.DataManagementPlan, rdf.type, rdfs.Class))
g.add((fdo.DataManagementPlan, rdfs.label, rdflib.Literal("Class repsresenting the Data Management Plans")))
g.add((fdo.DataManagementPlanQuestion, rdf.type, rdfs.Class))
g.add((fdo.DataManagementPlanQuestion, rdfs.label, rdflib.Literal("Data Management Plan Questions")))
g.add((fdo.DataManagementPlanTemplate, rdf.type, rdfs.Class))
g.add((fdo.DataManagementPlanTemplate, rdfs.label, rdflib.Literal("Class repsresenting the Data Management Plan Templates")))
g.add((fdo.DataSteward, rdf.type, rdfs.Class))
g.add((fdo.DataSteward, rdfs.label, rdflib.Literal("Data Steward")))
g.add((fdo.Section, rdf.type, rdfs.Class))
g.add((fdo.Section, rdfs.label, rdflib.Literal("Sections")))
g.add((fdo.TemplateQuestion, rdf.type, rdfs.Class))
g.add((fdo.TemplateQuestion, rdfs.label, rdflib.Literal("Questions located in a DMP template")))
g.add((fdo.TemplateSection, rdf.type, rdfs.Class))
g.add((fdo.TemplateSection, rdfs.label, rdflib.Literal("Sections located in a DMP template")))
g.add((fdo.DataContact, rdf.type, rdfs.Class))
g.add((fdo.DataContact, rdfs.label, rdflib.Literal("Person,or department responsible for data")))


g.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/Classes.ttl',
            format='turtle')



