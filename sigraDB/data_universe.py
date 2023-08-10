import os


class data_universe:
    """
    A data universe contains a number of dataspaces,
    A universe is a folder/container for all the dataspaces which are file/containers.
    This is the first proof of concept yet usable release!

    Author: Adham Hashibon and the Contrbuters of the DDMD@UCL Team
    """
    def __init__(self, universe_root):
        # If the universe_name does not contain any path separators, it's assumed to be a local folder name
        if os.path.sep not in universe_root:
            universe = os.path.join(os.getcwd(), universe_root) # define a local folder path!

        self.universe_root = universe_root
        self.data_spaces = []

        # Check if the folder exists
        if os.path.isdir(self.universe_root):
            # Iterate through the folder and find all data spaces (now simply .ttl files)
            for filename in os.listdir(self.universe_root):
                if filename.endswith(".ttl"):
                    self.data_spaces.append(os.path.join(self.universe_root, filename)) # the full path!
        else:
            # If the folder doesn't exist, create it and an empty .ttl file
            #TODO: the initial file should hold some metadata including when it was created, by whome, etc.
            # we could add a comment that is passed to the class or other data as well. Of course one needs to import
            # the proper simphony modules too.
            os.makedirs(self.universe_root)
            empty_data_space_path = os.path.join(self.universe_root, "meta_universe.ttl") # the meta includes the
            # metadata about the universe, including later a list of files, and some indices...
            open(empty_data_space_path, 'w').close()
            self.data_spaces.append(empty_data_space_path)

    def __iter__(self):
        # Return an iterator to all the dataspaces (now .ttl files) in the universe (now a folder)
        return iter(self.data_spaces)
