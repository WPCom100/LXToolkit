import lib.PySimpleGUI as gui


class Window:
    
    title = ""
    layout = []
    __returnValues = []

    def __init__(self, controller, data):

        # Create the window based on passed in parameters
        self.window = gui.Window(f"Lighting Toolkit: {self.title}", self.layout)

        # Windows are not open by default on instantiation
        self.__isOpen = False
        self.controller = controller
        
        # Checks if data was passed in, ignores if not
        if data is not None:
            self.data = data

    # Initalize loop to keep window open and waiting for events
    def open(self):

        self.__isOpen = True
        
        while self.__isOpen:
            event, self.__returnValues = self.window.read()
            self._inLoop(event)

            # Close the window on force exit
            if event == gui.WINDOW_CLOSED:
                break
        

    # Returns any values from user input of the window
    def getValues(self):
        return self.__returnValues

    # Returns t/f if window is open
    def isOpen(self):
        return self.__isOpen

    # Gracefully closes window
    def close(self):

        if self.__isOpen == True:
            self.__isOpen = False
            self.window.close()

    # Contains inner-loop functions in children
    # Should be overrided and used to make callbacks to the controller
    def _inLoop(self, event):
        pass

    #  Set the theme of the window. Should be called before calling
    #  gui for layout elements.
    def setTheme(self, theme):
        gui.theme(theme)