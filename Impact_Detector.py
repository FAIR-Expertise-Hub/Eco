from rdflib import Graph,URIRef
from rdflib.plugins.sparql.processor import SPARQLResult
from pandas import DataFrame

# Create a Graph object
graph = Graph()


# Import and parse the first TTL file
file_path1 = "ttl_files/DMP1_converted.ttl"
graph.parse(file_path1, format="turtle")

# Import and parse the second TTL file
file_path2 = "ttl_files/FIP_analysis_converted.ttl"
graph.parse(file_path2, format="turtle")

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
    if row['predicate'] == URIRef("https://fairdmp.online/eco-system/requiredBy") and row['object'] == URIRef("https://fairdmp.online/eco-system/VuLegalTeam"):
        print(f"The university legal team has impact on section {question_section} question {question_number}: \n"
              f"Explanation: This DMP has DMP template: 1 - VU DMP template 2021 (NWO & ZonMW certified) v1.3, \n"
              f"The University Legal Team is the party that requires section {question_section} question {question_number} to be added to this template.")
    if row['predicate'] == URIRef("https://fairdmp.online/eco-system/hasImpactOn"):
        print(f"{subject} has impact on {object_value}")

def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    """
    Export results from an rdflib SPARQL query into a `pandas.DataFrame`,
    using Python types. Got from https://github.com/RDFLib/rdflib/issues/1179.
    """
    return DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in results),
        columns=[str(x) for x in results.vars],
    )

df = sparql_results_to_df(results)
