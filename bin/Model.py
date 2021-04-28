import json

class Model:

    __PATHS = {
        'SETTINGS': "settings.json",
        'MENU_OPTIONS': "model/menu_options.json",
        'FIXTURE_LIBRARY': "model/fixture_library.json"
    }
    
    def __init__(self):
        
        self.__model = {}

        # Parse and store all dependent json files in model
        for path in self.__PATHS:
            self.__model.update({
               path : self.__readJsonFile(self.__PATHS[path])
                })

    # Returns requested value as dict from the model based on argument path
    def get(self, *paths: str):
        
        # Set root path
        rootPath = paths[0]

        # Set sub paths, ignoring the root path
        subPaths = tuple(path for path in paths
                           if not path == rootPath)

        # Get requested json file / root path
        result = self.__model[rootPath]

        # If a subpath was provided, move down the tree to the requested location
        if not all(subPaths):
            for subPath in subPaths:
                result = result[subPath]

        return result

    # Update a {key, value} pair in the SETTINGS model
    def updateSettings(self, key, value):
        self.__model['SETTINGS'][key] = value
        self.__updateModel(self.__model)

    # def set(self, value, *paths: str):

    #     # The model with new information for updateing, the working model
    #     workingModel = {}

    #     # Set root path
    #     rootPath = paths[0]
    #     workingModel[rootPath] = {}

    #     # Set sub paths, ignoring the root path
    #     subPaths = tuple(path for path in paths
    #                        if not path == rootPath)
        
    #     strPaths = f"[\'{rootPath}\']"
    #     for subPath in subPaths:
    #         strSubPaths = strSubPaths + f"[\'{subPath}\']"

    #     eval(f"workingModel{strSubPaths} = {}")


    #     self.__updateModel(self.__model)


    # Parse and store provided json file in model
    def __readJsonFile(self, path):

        with open(path, 'r') as file:
            return json.load(file)

    # Updates provided json file with the model provided
    def __updateModel(self, model):

        for path in self.__PATHS:
            with open(self.__PATHS[path], 'w') as file:
                return json.dump(model[path], file)

