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

    # TODO update settings to use new model set function
    # Update a {key, value} pair in the SETTINGS model
    def updateSettings(self, key, value):
        self.__model['SETTINGS'][key] = value
        self.__updateModel(self.__model)

    # TODO Check for none values in debug
    def set(self, value, *paths: str):

        # Set root path
        rootPath = paths[0]

        # The model with new information for updateing, the working model
        workingModel = self.get(rootPath)

        # If subpaths were passed, set sub paths ignoring the root path
        if not paths == None:
            subPaths = tuple(path for path in paths
                            if not path == rootPath)

            # Position of final subpath, also known as the key of the updated value
            lastSubPath = len(subPaths) - 1
            
            # For each subpath provided, traverse the model accordingly, excluding the final key value
            for subPath in subPaths:
                if not subPath == subPaths[lastSubPath]:
                    workingModel = workingModel[subPath]
            
            # Set the value requested
            workingModel[subPaths[lastSubPath]] = value
            
        # Otherwise set the entire model
        else:
            self.__model[rootPath] = value

        # Update JSON files with updated model values
        self.__updateModel(self.__model)


    # Parse and store provided json file in model
    def __readJsonFile(self, path):

        with open(path, 'r') as file:
            return json.load(file)

    # Updates provided json file with the model provided
    def __updateModel(self, model):

        for path in self.__PATHS:
            with open(self.__PATHS[path], 'w') as file:
                json.dump(model[path], file)

