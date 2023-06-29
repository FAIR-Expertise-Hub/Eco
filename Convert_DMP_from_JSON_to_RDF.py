import json, re, html, urllib.parse
from rdflib import Graph, Literal, Namespace, RDF, URIRef, FOAF, SDO, SKOS, DC


#Different levels of things
#UseTemplate new relations, hasTemplate
#Template consists of DMP questions
rdf = RDF
sdo = SDO
dc = DC
# Specify the path to the JSON files
path_to_files = 'C:/Users/MSI-NB/PycharmProjects/firstProject/JSON DMP Files/'
dmp_file_ids = [112581]

# Create an RDF graph
graph = Graph()

# Define namespaces
fdo = Namespace("https://fairdmp.online/eco-system/")
dmp_ns = Namespace("https://fairdmp.online/dmp/vu/")

# Bind namespaces to prefixes



# remove the HTML tags that come from the JSON file
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)



# Iterate over the JSON files and convert to TTL triples
for file_id in dmp_file_ids:
    file_name = str(file_id) + '.json'
    with open(path_to_files + file_name) as file:
        data = json.load(file)
        dmp = data[0][0]

        # Extract and add template information
        file_node = URIRef(dmp_ns + str(file_id))
        template = dmp['template']
        template_title = template.get('title')
        template_id = template.get('id')
        if template_title:
            graph.add((file_node, fdo.usesDMPTemplate, Literal(template_title)))

        # Extract and add data contact information
        data_contact = dmp.get('data_contact')
        if data_contact:
            data_contact_name = data_contact.get('name')
            data_contact_email = data_contact.get('email')
            if data_contact_name:
                graph.add((fdo.DataContact, sdo.name, Literal(data_contact_name)))
            if data_contact_email:
                graph.add((fdo.DataContact, sdo.email, Literal(data_contact_email)))

        # Extract and add project funder information
        funder = dmp.get('funder')
        if funder:
            funder_name = funder.get('name')
            if funder_name:
                graph.add((file_node, sdo.funder, Literal(funder_name)))


        #Extract and add DMP description
        description = dmp.get('description')
        if description:
            graph.add((file_node, dc.description, Literal(description)))

    # Extract and add section data
    plan_contents = dmp.get('plan_content', [])
    for plan in plan_contents:
        sections = plan.get('sections', [])
        for section in sections:
            section_title = remove_html_tags(section.get('title'))
            section_number = section.get('number')
            section_node = URIRef(dmp_ns + str(file_id) + "/section/" + str(section_number))
            section_description = remove_html_tags(section.get('description'))


            if section_node:
                graph.add((section_node, rdf.type, fdo.Section))
                if section_title:
                    graph.add((section_node, dc.title, Literal(section_title)))
                # Add section number if it exists
                if section_number:
                    graph.add((section_node, sdo.identifier, Literal(section_number)))
                if section_description:
                    graph.add((section_node, dc.description, Literal(section_description)))

                # Extract and add section questions
                questions = section.get('questions', [])
                for question in questions:
                    question_text = remove_html_tags(question.get('text'))
                    question_number = question.get('number')
                    answer = (question.get('answer'))
                    if section_number == 1 and question_number == 4:
                        name_pattern = r"<p>(.+)</p>"
                        match = re.search(name_pattern, str(answer))
                        if match:
                            name = match.group(1)
                            graph.add((file_node, sdo.author, name))

                    if question_number and question_text:
                        question_node = URIRef(dmp_ns + str(file_id)+"/section/"+str(section_number)+ "/question/" + str(question_number))
                        graph.add((question_node, rdf.type, fdo.DataManagementPlanQuestion))
                        graph.add((question_node, dc.title, Literal(question_text)))
                        graph.add((section_node, fdo.consists_of, question_node))
                        # Add answer text if it exists
                        if answer:
                            answer_text = remove_html_tags(answer.get('text', ''))
                            graph.add((question_node, sdo.acceptedAnswer, Literal(answer_text)))

    # Serialize the graph to TTL format
    graph.serialize(destination='C:/Users/MSI-NB/PycharmProjects/firstProject/ttl_files/DMP1_converted.ttl', format='turtle')
