from bin.Window import Window
import lib.PySimpleGUI as gui

# Constant font properties
UI_THEME = "DarkGrey13"
FONT_FAMILY = "Helvetica"
TITLE_FONT = (FONT_FAMILY, 24)
HEADER_TWO_TEXT = (FONT_FAMILY, 16)
NORMAL_TEXT = (FONT_FAMILY, 10)

class MainMenu(Window):

    def __init__(self, controller, data):

        # Theme of the window set to default
        self.setTheme(UI_THEME)

        # Title of the window being created
        self.title = "Main Menu"

        # ------------- Create the Layout -------------
        #
        #                    HEADER
        #       --------------------------------
        #                     BODY
        #

        header = [
            [gui.Text(self.title, font=TITLE_FONT, pad=(350, 2), justification='center')],
            [gui.Text('_' * 100, pad=(100, 0))]
        ]

        body = []
        for option in data:
            body.append([
                gui.Button(option, size=(26, 2), pad=(65, 14), font=(FONT_FAMILY, 13)),
                gui.Text(data[option]['disc'], size=(60, 3), pad=(10, 12), font=NORMAL_TEXT)
                ])

        self.layout = [
            [gui.Column(header, size=(900, 75))],
            [gui.Column(body, size=(900, 400))]
        ]

        #
        # ------------------------------------------------

        super().__init__(controller, data)
        
        
    def _inLoop(self, event):

        # Passing events to the event handler in the Controller
        self.controller.menuEventHandler(event, self.getValues())


class DMXAddressCalculator(Window):

    def __init__(self, controller, data):
        self.title = "DMX Address Calculator"
        self.setTheme(UI_THEME)
        self.layout = [ [gui.Text(self.title)],
                        [gui.Button("Close")] ]
        super().__init__(controller, data)
        
    def _inLoop(self, event):
        self.controller.dmxCalculatorEventHandler(event, self.getValues())


class WVACalculator(Window):

    def __init__(self, controller, data):
        self.title = "WVA Calculator"
        self.setTheme(UI_THEME)

        # ------------- Create the Layout -------------
        #
        #                    HEADER
        #       --------------------------------
        #                     BODY
        #            C1   C2   C3   C4   C5               
        #
        #                    FOOTER
        #

        header = [
            [gui.Text(self.title, font=TITLE_FONT, pad=(325, 2), justification='center')],
            [gui.Text('_' * 100, pad=(105, 0), justification='center')]
        ]

        body = [
            [gui.Column([[
                gui.Column([[gui.Text('Watts: ', font=HEADER_TWO_TEXT), gui.Input(size=(13, 1), key='w')]], pad=(25, 20)),
                gui.Column([[gui.Text('=', font=TITLE_FONT)]], pad=(25, 0)),
                gui.Column([[gui.Text('Volts: ', font=HEADER_TWO_TEXT), gui.Input(size=(13, 1), key='v')]], pad=(25, 20)),
                gui.Column([[gui.Text('X', font=TITLE_FONT)]], pad=(25, 0)),
                gui.Column([[gui.Text('Amps: ', font=HEADER_TWO_TEXT), gui.Input(size=(13, 1), key='a')]], pad=(25, 20))
            ]], pad=(10, 35))],
            [gui.Column([[gui.Button('Calculate')]], pad=(410, 5))]
        ]
            

        footer = gui.Column([[gui.Button("Close")]], pad=(420, 5))

        self.layout = [
            [header],
            [body],
            [footer]
        ]
        
        #
        # ------------------------------------------------
          
        super().__init__(controller, data)
        
    def _inLoop(self, event):
        self.controller.wvaCalculatorEventHandler(event, self.getValues())


class RoscoGelDataSheetViewer(Window):

    def __init__(self, controller, data):
        self.title = "Rosco Gel Data Sheet Viewer"
        self.setTheme(UI_THEME)
        self.layout = [ [gui.Text(self.title)],
                        [gui.Button("Close")] ]
        super().__init__(controller, data)
        
    def _inLoop(self, event):
        self.controller.roscoViewerEventHandler(event, self.getValues())


class FixtureLibrary(Window):

    def __init__(self, controller, data):

        # Window Title
        self.title = "Fixture Library"

        # Window Theme
        self.setTheme(UI_THEME)

        # Window Layout
        self.layout = [ [gui.Text(self.title)],
                        [gui.Button("Save and Close")]]
        
        super().__init__(controller, data)
        
    # Anytime a user interacts with the window
    def _inLoop(self, event):
        self.controller.fixtureLibraryEventHandler(event, self.getValues())


class Settings(Window):

    def __init__(self, controller, data):
        self.title = "Settings"
        self.setTheme(UI_THEME)

        # ------------- Create the Layout -------------
        #
        #                    HEADER
        #       --------------------------------
        #
        #                     BODY
        #
        #                    FOOTER
        #

        header = [
            [gui.Text(self.title, font=TITLE_FONT, pad=(400, 2), justification='center')],
            [gui.Text('_' * 100, pad=(125, 0), justification='center')]
        ]

        body = gui.Column(
                [[gui.Text('Toolkit Mode: ')], [gui.Combo(['Designer', 'Electrican', 'Both'],
                                                    default_value=data['mode'],
                                                    key='mode')]],
                pad=(400, 25))

        footer = [gui.Button("Save and Close", pad=(400, 25))]

        
        self.layout = [
            [header],
            [body],
            [footer]
        ]

        #
        # ------------------------------------------------

        super().__init__(controller, data)
        
    def _inLoop(self, event):
        self.controller.settingsEventHandler(event, self.getValues())

