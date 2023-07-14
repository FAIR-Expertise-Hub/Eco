from rdflib import Graph, URIRef,Namespace
from rdflib.plugins.sparql.processor import SPARQLResult
from rdflib.plugins.sparql import prepareQuery


# Create a Graph object
graph = Graph()
fdo = Namespace("https://fairdmp.online/eco-system/")
fip = Namespace("https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/")

# Import and parse the first TTL file
file_path1 = "ttl_files/DMP112581_converted.ttl"
graph.parse(file_path1, format="turtle")

# Import and parse the second TTL file
file_path2 = "ttl_files/FIP_analysis_converted.ttl"
graph.parse(file_path2, format="turtle")

#Import and parse the third file
file_path3 = "ttl_files/Classes.ttl"
graph.parse(file_path3, format="turtle")

#Import and parse the fourth file
file_path4 = "ttl_files/General_Instances.ttl"
graph.parse(file_path4, format="turtle")

# extract the namespaces
dec_namespace = graph.namespace_manager.store.namespace("dec")
dec_URI = dec_namespace
dmp_namespace = graph.namespace_manager.store.namespace("dmp_file")
dmp_URI = dmp_namespace



#Printing relatons from this set
final_analysis = set()


# Get the community and add the impact of it on questions
community = set()
com_query = prepareQuery("""
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
        FILTER (?predicate = <https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/declared-by>)
    }
""")
resultscom = graph.query(com_query)
for row in resultscom:
    object_ = row["object"]
    community.add(object_)

# Get questions
all_questions = set()
community_name = community.pop()
question_query = prepareQuery("""
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
        FILTER (?object = <https://fairdmp.online/eco-system/DataManagementPlanQuestion>)
    }
""")
results22 = graph.query(question_query)
for row in results22:
    question = row["subject"]
    all_questions.add(question)
#Add impact relation for community on question
for question in all_questions:
    if 'section/5' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))
    if 'section/4/question/8' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))
    if 'section/4/question/9' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))
    if 'section/4/question/3' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))
    if 'section/0/question/4' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))
    if 'section/0/question/5' in str(question):
        graph.add((URIRef(community_name),fdo.hasImpactOn,URIRef(question)))


# Get Input question number and section
print("Please enter the question number you would like to inspect. (ex. 1.1, 0.4, 4.2)")
input_question = input()
section_and_number = input_question.split(".")
question_section = section_and_number[0]
question_number = section_and_number[1]


question_node =(dmp_URI+"/section/"+question_section+"/question/"+question_number)
print(question_node)
# SPARQL query to retrieve all entries related to the class
sparql_query =  """
SELECT ?subject ?predicate ?object
WHERE {
  ?subject ?predicate ?object .
  FILTER (CONTAINS(STR(?subject), "%s") || CONTAINS(STR(?object), "%s"))
}
""" % (question_node, question_node)

results = graph.query(sparql_query)

for row in results:
    subject = row['subject']
    predicate = row['predicate']
    object_value = row['object']
    #If it has a suggested answer:
    if predicate == URIRef("https://fairdmp.online/eco-system/recommendedAnswer"):
        final_analysis.add(str(f"The suggested response for the {subject} is: {object_value}"))
    # If it is required by legal team follow the edges
    if predicate == URIRef("https://fairdmp.online/eco-system/requiredBy") and row['object'] == URIRef("https://fairdmp.online/eco-system/VuLegalTeam"):
        final_analysis.add(str(f"The university legal team has direct impact on section {question_section} question {question_number}: \n"
                               f"       Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                               f"           The University Legal Team is the party that requires section {question_section} question {question_number} to be added to this template."))
    # If it is responsible for DMP question
    if predicate == URIRef("https://fairdmp.online/eco-system/isResponsibleForDMPQuestion"):
        final_analysis.add(str(f"{subject} has direct impact on {object_value}:\n"
                               f"       Explanation: {subject} is responsible for this DMP question."))
    # If it uses a template by RDM team
    if "http://purl.org/" not in str(subject)  and predicate == URIRef("https://fairdmp.online/eco-system/hasImpactOn") and ("https://fairdmp.online/dmp/vu/112581/section/") in str(object_value):
        final_analysis.add(str(f"{subject} has direct impact on section {question_section} question {question_number}: \n"
                               f"       Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                               f"              {subject} is one of the parties that has a direct impact on the answer of the DMP template question {question_section}.{question_number}."))
    #add the Community
    if "http://purl.org/" in str(subject)  and predicate == URIRef("https://fairdmp.online/eco-system/hasImpactOn") and ("https://fairdmp.online/dmp/vu/112581/section/") in str(object_value):
        final_analysis.add(str(f"{subject} has direct impact on section {question_section} question {question_number}: \n"
                               f"       Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                               f"              {subject} is a community. Community one of the parties that has a direct impact on the answer of the DMP template question {question_section}.{question_number}."))

    # It could be a reference
    if predicate == URIRef("https://fairdmp.online/eco-system/questionRefersToPrincipal"): #subject becomes the dmp question object becomes the principle
        #print(f"test debug_ {subject},{predicate},{object_value} this is the first cycle")
        #first object is fair principle
        sparql_query2 = prepareQuery("""
            SELECT ?subject ?predicate ?object
            WHERE {
                ?subject ?predicate ?object .
                FILTER (?predicate = <https://peta-pico.github.io/FAIR-nanopubs/fip/index-en.html#https://w3id.org/fair/fip/terms/refers-to-principle>)
            }
        """)
        results2 = graph.query(sparql_query2)
        for i in results2:
            fip_question = i['subject']
            refers_to_principle = i['predicate']
            fip_principle = i['object']
            # connect fair to fip object values are the principles
            if object_value == fip_principle:
                # subject_loop becomes fip question object_loop becomes the fip principle.
                # print(f"{subject_loop} between, {predicate_loop} between, {object_value_loop} this is the first loop cycle")
                sparql_query3 = prepareQuery("""
                    SELECT ?subject ?predicate ?object
                    WHERE {
                        ?subject ?predicate ?object .
                        FILTER (?predicate = <https://fairdmp.online/eco-system/canHaveAnswer>)
                    }
                """)
                results3 = graph.query(sparql_query3)
                for j in results3:
                    fip_question = j['subject']
                    canHaveAnswer = j['predicate']
                    fer_answer = j['object']
                    # Connect fip question to the respective answer
                    if object_value == fip_principle and ((fip_question.split("/")[-1]).split("-")[2]) == (fip_principle.split("/")[-1]):
                        # subject_loop2 becomes question fip:question and object_loop_2 becomes fer
                        # print(f"{subject_loop_2},{predicate_loop_2},{object_value_loop_2} this is the loop 2 cycle")
                        final_analysis.add(str( f"The FIP {dec_URI} could be a reference when the researcher is updating section DMP {question_section} question {question_number}. \n"
                                                f"      Explanation: This DMP uses DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                                                f"          Question {question_section}.{question_number} of this template is about FAIR principle {fip_principle}.\n"
                                                f"              In the given FIP the question {fip_question} is about the same FAIR principle.\n"
                                                f"                  The answer of this question {fip_question} in the FIP is {fer_answer}.\n"
                                                f"                      This answer could be taken into consideration by the researcher."))





graph.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ScriptsForKG/EcoSystem_Graph.ttl',
            format='turtle')


for element in set(final_analysis):
    print("•",element)
