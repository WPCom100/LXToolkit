import json

class Model:

    __PATHS = {
        'SETTINGS': "settings.json",
        'MENU_OPTIONS': "model/menu_options.json",
        'FIXTURE_LIBRARY': "model/fixture_library.json",
        'SUPPORTED_GELS' : "model/supported_gel_types.json"
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

        # Set sub paths, ignoring the root path if paths were passed in
        if len(paths) > 1:
            subPaths = tuple(path for path in paths
                            if not path == rootPath)
        else:
            subPaths = None

        # Get requested json file / root path
        result = self.__model[rootPath]

        # If a subpath was provided, move down the tree to the requested location
        if not subPaths is None:
            for subPath in subPaths:
                result = result[subPath]

        return result

    def set(self, value, *paths: str):

        # Set root path
        rootPath = paths[0]

        # If subpaths were passed, set sub paths ignoring the root path
        if len(paths) > 1:

            # The model with new information for updateing, the working model
            workingModel = self.get(rootPath)

            subPaths = tuple(path for path in paths
                            if not path == rootPath)

            # Position of final subpath, also known as the key of the updated value
            lastSubPath = len(subPaths) - 1
            
            # For each subpath, traverse the model accordingly, excluding the final key value
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

    def rename(self, newKey: str, *paths: str):

        # Set root path
        rootPath = paths[0]

        # If subpaths were passed, set sub paths ignoring the root path
        if len(paths) > 1:

            # Model refrence used to traverse the model
            workingModel = self.get(rootPath)

            subPaths = tuple(path for path in paths
                            if not path == rootPath)

            # Position of final subpath, also known as the key to be renamed
            lastSubPath = len(subPaths) - 1

            # For each subpath, traverse the model accordingly, excluding the final key value
            for subPath in subPaths:
                if not subPath == subPaths[lastSubPath]:
                    workingModel = workingModel[subPath]

            # Rename the key value
            workingModel[newKey] = workingModel.pop(subPaths[lastSubPath])

        # Otherwise rename the entire model
        else:
            self.__model[newKey] = self.__model.pop(rootPath)

        # Update JSON files with updated model values
        self.__updateModel(self.__model)


    # Parse and store provided json file in model
    def __readJsonFile(self, path):

        with open(path, 'r') as file:
            return json.load(file)

    # Updates provided json file with the model provided
    def __updateModel(self, model):

        #TODO Update only model that is changed

        for path in self.__PATHS:
            with open(self.__PATHS[path], 'w') as file:
                json.dump(model[path], file)

