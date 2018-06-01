import gi

gi.require_version('Gtk', '3.0')
# from gi.overrides import Gtk
from gi.repository import Gtk

from View.LoginView import *
from error import *


class Login:

    def __init__(self, window):
        try:
            self.view = LoginView()
            self.window = window
            self.poupup = PoupUpLoginWindow(window)
            if not (self.DialogWindowButtonSupport() == True):
                raise ErrorClass(1, "Nieznany", "Nieznany błąd",
                                 "Okienko dialogowe logowania zwóricło inną wartość, niż True")

            self.poupup.destroy()
            self.window.changeWindowContent("tableList")

        except ErrorClass as err:
            ErrorPrompt(err)

    def DialogWindowButtonSupport(self):
        while (1):
            response = self.poupup.run()

            if response == Gtk.ResponseType.CANCEL:
                exit(0)
            elif response == Gtk.ResponseType.OK:
                err = self.window.modelConnection.testConnection(self.poupup.rb1_input.get_text(),
                                                                 self.poupup.rb2_input.get_text(),
                                                                 self.poupup.rb4_input.get_text(),
                                                                 self.poupup.rb3_input.get_text())
                if err == True:
                    self.window.modelConnection.makeConnection(
                        self.poupup.rb1_input.get_text(), self.poupup.rb2_input.get_text(),
                        self.poupup.rb4_input.get_text(),
                        self.poupup.rb3_input.get_text())
                    return 1
                else:
                    self.poupup.connectionErrorMessage(err)
