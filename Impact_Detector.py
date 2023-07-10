from rdflib import Graph,URIRef
from rdflib.plugins.sparql.processor import SPARQLResult
from pandas import DataFrame
from rdflib.plugins.sparql import prepareQuery


# Create a Graph object
graph = Graph()

# Import and parse the first TTL file
file_path1 = "ttl_files/DMP1_converted.ttl"
graph.parse(file_path1, format="turtle")

# Import and parse the second TTL file
file_path2 = "ttl_files/FIP_analysis_converted.ttl"
graph.parse(file_path2, format="turtle")
#Create the big graph
graph.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/NotWorking.ttl',
            format='turtle')
# extract the namespaces
dec_namespace = graph.namespace_manager.store.namespace("dec")
dec_URI = dec_namespace
final_analysis = set()

print("Please enter the question number would like to inspect. (ex. 1.1,2,4.2)")
input_question = input()
section_and_number = input_question.split(".")
question_section = section_and_number[0]
question_number = section_and_number[1]


question_node =("https://fairdmp.online/dmp/vu/112581/section/"+question_section+"/question/"+question_number)
print(question_node)
# SPARQL query to retrieve all entries related to the class
sparql_query = """
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
    # If it is required by legal team follow the edges
    if predicate == URIRef("https://fairdmp.online/eco-system/requiredBy") and row['object'] == URIRef("https://fairdmp.online/eco-system/VuLegalTeam"):
        final_analysis.add(str(f"The university legal team has impact on section {question_section} question {question_number}: \n"
                                    f"  Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                                        f"  The University Legal Team is the party that requires section {question_section} question {question_number} to be added to this template."))
    # If it is responsible for DMP question
    if predicate == URIRef("https://fairdmp.online/eco-system/isResponsibleForDMPQuestion"):
        final_analysis.add(str(f"{subject} has impact on {object_value}:\n"
              f"    {subject} is responsible for this DMP question."))
    # If it uses a template by RDM team
    if predicate == URIRef("https://fairdmp.online/eco-system/hasImpactOn"):
        final_analysis.add(str(f"{subject} has impact on section {question_section} question {question_number}: \n"
              f"    Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
              f"        {subject} is one of the parties that has an impact on the DMP template question {question_section}.{question_number}."))

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
                        final_analysis.add(str(f"The FIP {dec_URI} could be a reference when the researcher is updating section DMP {question_section} question {question_number}. \n"
                                                f"  Explanation: This DMP uses DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
                                                f"      Question {question_section}.{question_number} of DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3 is about FAIR principle {fip_principle}.\n"
                                                f"          In the FIP the question {fip_question} is about the same FAIR principle."
                                                f"              The answer of this question {fip_question} in the FIP is {fer_answer},This answer could be taken into consideration by the researcher."))


for element in set(final_analysis):
    print("•",element)
def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    """
    Export results from an rdflib SPARQL query into a `pandas.DataFrame`,
    using Python types. Got from https://github.com/RDFLib/rdflib/issues/1179.
    """
    return DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )

