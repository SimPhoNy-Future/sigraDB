from sigraDB import data_universe

sigraDB = data_universe('data_universe_name')
for data_space in sigraDB:
    print(data_space)

# Load the data spaces (.ttl files) into an RDF graph
graph = sigraDB.load_data_spaces_to_graph()

# Now you can work with the RDF graph using rdflib or other tools.
# For example, you might print out all the triples in the graph:
for subject, predicate, object in graph:
    print(subject, predicate, object)

# Or you could run a SPARQL query against the graph:
query_result = graph.query("""
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object.
    }
""")
for row in query_result:
    print(row)


sigraDB.load_data_spaces_to_session()
