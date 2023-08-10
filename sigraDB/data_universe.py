import os

from filelock import FileLock
import time
from datetime import datetime
from pydantic import BaseModel

# not sure if all these are needed, if they are used in sigraDB any way!
from simphony_osp.namespaces import city, rdfschema, dcoretbox, simphony
from simphony_osp.namespaces import owl, foaf, emmo, domeo, dcterms, evmpo, eurosci, iof
from simphony_osp.namespaces import http_method

from simphony_osp.tools import semantic2dot, pretty_print
from simphony_osp.tools import search, export_file, import_file, pretty_print, search
from simphony_osp.tools.search import sparql

from simphony_osp.ontology import RESTRICTION_QUANTIFIER, RESTRICTION_TYPE, OntologyIndividual
from simphony_osp.ontology import COMPOSITION_OPERATOR, Composition, Restriction

from simphony_osp.ontology.relationship import OntologyRelationship
from simphony_osp.ontology.annotation import OntologyAnnotation

from simphony_osp.session import Session, core_session


class StampModel(BaseModel):
    time: str


class data_universe:
    """
    sigraDB is a lightweight open source graph-based database.
    ----------------------------------------------------------
    The sigraDB universe contains a number of dataspaces,

    In this implementation:
        A universe is a folder/container for all the dataspaces which are files/containers.
        This is the first proof of concept, yet usable release!
        It is based on RDFLIB and SimPhoNy-Future OSP.
    """

    def __init__(self, universe_root):
        """
        :param universe_root: the root of the data universe, containing the data spaces.
        lock: ensure no other process writes to the database at the same time.
        active: True if the dataspace is loaded, False otherwise.
        """

        self.lock = FileLock("universe.lock")
        self.universe_root = universe_root
        self.active = False
        self.initialised = False

    def initialise(self):
        """
        :return: True if initialised
        """

        self.data_spaces = []

        # If the universe root does not contain any path separators, it's assumed to be a local folder name
        if os.path.sep not in self.universe_root:
            universe = os.path.join(os.getcwd(), self.universe_root)  # define a local folder path!
        # Check if the folder exists
        if os.path.isdir(self.universe_root):
            # Iterate through the folder and find all data spaces (now simply .ttl files)
            for filename in os.listdir(self.universe_root):
                if filename.endswith(".ttl"):
                    self.data_spaces.append(os.path.join(self.universe_root, filename))  # the full path!
        else:
            # If the folder doesn't exist, create it and an empty .ttl file
            # TODO: the initial file should hold some metadata including when it was created, by whome, etc.
            # we could add a comment that is passed to the class or other data as well. Of course one needs to import
            # the proper simphony modules too.
            os.makedirs(self.universe_root)
            empty_data_space = os.path.join(self.universe_root, "meta_universe.ttl")  # the meta includes the
            # metadata about the universe, including later a list of files, and some indices...
            open(empty_data_space, 'w').close()
            self.data_spaces.append(empty_data_space)

        self.initialized = True
        return self.initialized

    def __iter__(self):
        # Return an iterator to all the dataspaces (now .ttl files) in the universe (now a folder)
        return iter(self.data_spaces)

    def _load_data_spaces_to_graph(self):
        """
        Create a new RDF graph to hold the data, meant for testing only, not user consumption

        :return:
        """
        graph = Graph()
        # Iterate over the .ttl files and parse them into the graph
        for data_space_path in self.data_spaces:
            graph.parse(data_space_path, format='ttl')
        # Return the graph or store it as needed
        return graph

    def activate(self):
        """
            Activate the data space
            in effect now it is loading it into the core session.
            TODO: separate to ABC and actual implementation
        """
        # Iterate over the data spaces and initialise them into the session (loading/importing)
        if not self.active:
            print("activating........")
            for data_space in self.data_spaces:
                import_file(data_space, all_triples=True)  # all triples needed to allow for extraneous dangling
                # ontology,
                # TODO: enhance built in treatment of such cases in OSP.
                # TODO: return stat on imported data spaces and success/warning etc.
        self.active = True

        self.size = len(core_session)

        return self.size

    # TODO: add something to do query and then return the result, this would be enough for today

    def _update_data_space_Graph(self, data_space, update_data):
        """
        # Acquire the global lock to prevent concurrent access hopefully!
        This is for testing only.
        """
        with self._lock:
            # Load the data space as a graph
            graph = Graph()
            graph.parse(data_space, format='ttl')

            # Perform updates on the graph (you'll need to specify the exact update process)
            # You could add, remove, or modify triples based on 'update_data'

            # Save the updated graph back to the file
            graph.serialize(destination=data_space, format='ttl')

    def update(self, data_space, update_data):
        """
        Take a proper data and use it to update an existing dataspace (file).
        """
        with self.lock:
            """
            check if the session is loaded, initialised, otherwise initialise, etc. 
            """
            if not self.initialised:
                self.initialise()
            if not self.active:
                self.activate()

            # perform the update operation (add, delete, create, etc, )
            # return status
            return self.size

    def sparql(self, the_query):
        """
        Method to update the data spaces with provenance (using Git)
        :return: query result

        TODO: ABC for query, then one which can take wither a sparql or other form (graphQL, or native) then we
        create another meta query which activates any of them as needed.

        """

        with self.lock:
            """
            this is stub
            result = sparql(query)
            """

            time_stamp = self.get_time()
            time.sleep(0) # useful to test the locking.
            res = self.sparql_query(the_query)
            """print(res)
            print(len(res))
            res1=str(res.serialize(format="txt").decode('utf-8'))"""

            result = {"query": the_query, "time stamp": time_stamp, "size": len(res), "res": res}
        return result

    def deactivate(self):
        # Acquire the lock to prevent concurrent access
        with self._lock:
            """
            Perform any necessary clean-up, such as closing open files or releasing resources
            
            call update if needed, check if a new version has somehow in the meantime been created, but normally we 
            would update the provenance data, who accesses, and what they did, 
            check the log is uptodaye. 
            
            clear data_spaces
            """

            self.data_spaces = []

    @staticmethod
    def get_time():
        current_time = datetime.now().isoformat()
        return {"time": current_time}

    def sparql_query(self, query):
        """
        This is the sigradb own sparql wrapper, which takes the simphony one (which itself is
        built on rdfllib at the moment) and adds a layer for more json/python friendly output.
        :param query:
        :return:
        """
        res = data_universe.unpack_result(sparql(query))

        return res


    @staticmethod
    def unpack_result(packed_result):
        result = []
        for row_number, row in enumerate(packed_result, 1):
            entry = {}
            if row:
                elements = ['s', 'p', 'o']
                for index, element in enumerate(row):
                    entry[elements[index]] = str(element)
                result.append(entry)
        return result
