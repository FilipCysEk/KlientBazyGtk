from gi.repository import Gtk

class ErrorClass(Exception):
    def __init__(self, type, exceprtionMessage, description, extraAdminDescription = None):
        '''

        :param exceprtionMessage:
        :param description:
        :param extraAdminDescription:
        :param type: type of error; 0 - no critical; 1 - critical;
        '''
        self.exceptionMessage = exceprtionMessage
        self.description = description
        self.extraAdminDescription = extraAdminDescription
        self.type = type

    def __str__(self):
        return self.exceptionMessage

    def message(self):
        return self.exceptionMessage

    def getDescription(self):
        return self.description

    def getExtraAdmin(self):
        return self.extraAdminDescription

class ErrorPrompt:
    def __init__(self, ErrorClasses):
        message = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, ErrorClasses.message())
        message.format_secondary_text(ErrorClasses.getDescription())
        print("ERROR")
        print(ErrorClasses.message())
        print(ErrorClasses.getDescription())
        print(ErrorClasses.getExtraAdmin())

        if message.run() == Gtk.ResponseType.OK:
            if ErrorClasses.type == 1:
                exit(1)

        message.destroy()