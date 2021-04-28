import bin.View as View
from bin.Model import Model
from lib.LXMath import *

class Controller:

    def __init__(self):
        self.view = View
        self.model = Model()

    def core(self):
        
        # Open main menu by default
        self.openMainMenu()

    # --------------- Event Handlers ---------------
    #
    #   View's callback function, in order to 
    #     proccess users interactions/events
    #
    
    def menuEventHandler(self, event, data):

        if event == None: # Exit on window close
            self.currentWindow.close()

        else:  # Open requested window using the event name as the class name to instantiate

            # Save menu selection and remove white space from event name, thus now matching the class in the view
            menuSelection = event.replace(" ", "")

            self.currentWindow.close()
            eval(f"self.open{menuSelection}()")

    def dmxCalculatorEventHandler(self, event, data):
        
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()

    def wvaCalculatorEventHandler(self, event, data):
        
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()
        if event == "Calculate":

            # If at least one field is blank
            if data['w'] == '' or data['v'] == '' or data['a'] == '':

                # Not all fields can be blank
                if not (data['w'] == '' and data['v'] == '' and data['a'] == ''):

                    # Two fields can not be blank
                    total: float = data['w'] + data['v'] + data['a']
                    if not (total == data['w'] or total == data['v'] or total == data['a']):

                        # If all checks are met, run calculation
                        result, solvedFor = powerCalculator(w=data['w'], v=data['v'], a=data['a'])
                        # And Display to the user in the appropriate input field
                        self.currentWindow.window[solvedFor].update(result)

                    # Error cases will popup to user
                    else:
                        self.view.gui.popup_error("Only one field can be left blank!", title='Error')
                else:
                    self.view.gui.popup_error("Fill out the formula first!", title='Error')
            else:
                self.view.gui.popup_error("At least one field must be blank!", title='Error')

    def roscoViewerEventHandler(self, event, data):
        
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()

    def fixtureLibraryEventHandler(self, event, data):
        
        if event == None:
            self.currentWindow.close()
        if event == "Save and Close":
            self.currentWindow.close()
            self.openMainMenu()


    def settingsEventHandler(self, event, data):
        
        if event == None:
            self.currentWindow.close()
        if event == "Save and Close":
            self.currentWindow.close()
            self.model.updateSettings('mode', data['mode'])
            self.openMainMenu()

    # ------------------------------------------------

    def openMainMenu(self):

        menuOptions = self.model.get('MENU_OPTIONS')
        # TODO Add menu options filter
        # Open the window and pass in menu options from model
        self.currentWindow = self.view.MainMenu(self, menuOptions)
        self.currentWindow.open()

    def openSettings(self):

        # Opens the settings window with settings from the model
        settingsData = self.model.get('SETTINGS')
        self.currentWindow = self.view.Settings(self, settingsData)
        self.currentWindow.open()

    def openWVACalculator(self):

        # Opens the WVA Calculator window
        self.currentWindow = self.view.WVACalculator(self, None)
        self.currentWindow.open()

# Start the program
if __name__ == '__main__':
    lxtoolkit = Controller()
    lxtoolkit.core()