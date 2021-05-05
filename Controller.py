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
        
        # TODO DMX Calc Functionality
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()

    def wvaCalculatorEventHandler(self, event, data):
        
        # Exit on user exit
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()
        
        # Calculate Button
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
        
        # Exit on user exit
        if event == None:
            self.currentWindow.close()
        if event == "Close":
            self.currentWindow.close()
            self.openMainMenu()
        
        # Load image per input upon button press
        if event == 'Lookup':
            fileName = f"{data['gel']}.jpg"
            bio = io.BytesIO()

            # Check if file is already downloaded
            if not os.path.exists(fileName):
            
                # If image downloads successfuly
                if downloadImage(f"https://us.rosco.com/sites/default/files/content/filters//{data['gel_type'][0]}/{data['gel']}.jpg"):
                    
                    imageToMemory(fileName, 600, 600, bio)
                    # Update image view with image downloaded
                    self.currentWindow.window['img'].update(data=bio.getvalue())

                # Error if not success
                else:
                    self.view.gui.popup_error("Please try another gel, that one didn't work!", title='Error')

            else:

                imageToMemory(fileName, 600, 600, bio)
                # Update image view with image downloaded
                self.currentWindow.window['img'].update(data=bio.getvalue())

    def fixtureLibraryEventHandler(self, event, data):

        # Model key
        mKey = 'FIXTURE_LIBRARY'

        # Saves fixture data regardless of data being updated
        def saveFixture():
            for key in data.keys():

                # Extract selected fixture from data
                if key == 'selected_fixture':
                    selectedFixture = data['selected_fixture'][0]

                # TODO Proccess Name Fixture Name Changes
                elif key == 'name':
                    None

                # Update model with data to save
                else:
                    # Handle t/f Listboxes
                    if isinstance(data[key], list):
                        if data[key][0] == 'True':
                            self.model.set(True, mKey, selectedFixture, key)
                        else:
                            self.model.set(False, mKey, selectedFixture, key)
                    else:
                        self.model.set(data[key], mKey, selectedFixture, key)

        
        # Fixture model
        fixtureData = self.model.get(mKey)
        
        # Exit on user exit, without saving
        if event == None:
            self.currentWindow.close()
        
        # Save and return to the menu
        if event == "Save and Close":
            self.currentWindow.close()
            saveFixture()
            self.openMainMenu()

        # Save only
        if event == "Save":
            saveFixture()
        
        # User selected a fixture from the list
        if event == "selected_fixture":
            selectedFixture = data['selected_fixture'][0]

            # If the dataColumn is hidden, unhide it
            if not self.currentWindow.window['dataColumn'].visible:
                self.currentWindow.window['dataColumn'].update(visible=True)

            # Set data in the dataColumn
            self.currentWindow.window['name'].update(selectedFixture)
            self.currentWindow.window['lamp_type'].update(fixtureData[selectedFixture]['lamp_type'])
            self.currentWindow.window['fixture_type'].update(fixtureData[selectedFixture]['fixture_type'])
            self.currentWindow.window['degree_min'].update(fixtureData[selectedFixture]['degree_min'])
            self.currentWindow.window['degree_max'].update(fixtureData[selectedFixture]['degree_max'])
            self.currentWindow.window['wattage'].update(fixtureData[selectedFixture]['wattage'])
            self.currentWindow.window['volts'].update(fixtureData[selectedFixture]['volts'])
            self.currentWindow.window['amperage'].update(fixtureData[selectedFixture]['amperage'])
            self.currentWindow.window['addresses'].update(fixtureData[selectedFixture]['addresses'])
            
            # Handle bool values in data set
            if fixtureData[selectedFixture]['3-pin-data']:
                self.currentWindow.window['3-pin-data'].update(set_to_index=0)
            else:
                self.currentWindow.window['3-pin-data'].update(set_to_index=1)

            if fixtureData[selectedFixture]['5-pin-data']:
                self.currentWindow.window['5-pin-data'].update(set_to_index=0)
            else:
                self.currentWindow.window['5-pin-data'].update(set_to_index=1)


    def settingsEventHandler(self, event, data):

        # Model key
        mKey = 'SETTINGS'
        
        # Exit on user exit, without saving
        if event == None:
            self.currentWindow.close()

        # Save and return to the menu
        if event == "Save and Close":
            self.currentWindow.close()
            self.model.set(data['mode'], mKey, 'mode')
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

    def openFixtureLibrary(self):

        # Opens the fixture library window with the fixture library from the model
        # Only passes in the fixture names for list creation
        fixtureData = self.model.get('FIXTURE_LIBRARY').keys()
        self.currentWindow = self.view.FixtureLibrary(self, fixtureData)
        self.currentWindow.open()

    def openRoscoGelDataSheetViewer(self):

        # Opens the rosco data sheet veiwer window
        # Passes in supported gel types
        supportedGels = self.model.get('SUPPORTED_GELS')
        self.currentWindow = self.view.RoscoGelDataSheetViewer(self, supportedGels)
        self.currentWindow.open()


# Start the program
if __name__ == '__main__':
    lxtoolkit = Controller()
    lxtoolkit.core()