import gi
gi.require_version('Gtk', '3.0')
from gi.overrides import Gtk
from gi.repository import Gtk


from View.LoginView import *
from Controller.Login import *
from Controller.TableList import *
from Controller.TablePreview import *
from Model.MainModel import *
from Controller.SqlConsole import *



class MainClass(Gtk.Window):
    def __init__(self):
        self.modelConnection = MainModel()
        Gtk.Window.__init__(self, title="Klient bazy danych mysql")
        self.connect("destroy", Gtk.main_quit)
        self.controller = Login(self)

    def __del__(self):
        try:
            self.modelConnection.closeConnection()
        except ErrorClass:
            pass

    def changeWindowContent(self, content, date = None):
        if content == "tableList":
            self.controller = TableList(self)

        elif content == "tablePreview":
            if date == None or len(date) == 0:
                raise ErrorClass(1, "Błąd krytyczny", "Nie udało się załadować podglądu tabeli", "Nieprzekazano nazwy tabeli")
            self.controller = TablePreview(self, date)
        elif content == "console":
            self.controller = SqlConsole(self)
        else:
            raise ErrorClass(1, "Błąd krytyczny", "Nie wiem co się stało, nie potrafię stworzyć kolejnego okna",
                             "Nie odnaleziono kontrollera!!!!")




main = MainClass()
Gtk.main()
'''
window = Gtk.Window(title="Hello World")
window.show()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
'''