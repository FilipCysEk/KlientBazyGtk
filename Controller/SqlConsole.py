import gi, re

gi.require_version('Gtk', '3.0')
# from gi.overrides import Gtk
from gi.repository import Gtk

from View.SqlConsoleView import *
from error import *


class SqlConsole:
    def __init__(self, window):
        try:
            self.selectedRow = None
            self.window = window
            self.table_name = None
            self.window.set_title("Konsola")
            self.view = SqlConsoleView(window)

            # Wyciąganie wszystkich danych z tej tabeli
            #self.tableContent = window.modelConnection.SelectAll(tableName)
            self.tableList()
            self.view.render()

            self.view.button_back.connect("clicked", self.backToTableList)
            self.view.button_run.connect("clicked", self.runSqlCommand)

        except ErrorClass as err:
            ErrorPrompt(err)

    def tableList(self, ):
        # Wyciąganie wszystkich danych z tej tabeli
        #self.tableContent = self.window.modelConnection.runSql("SELECT * from student")
        self.tableContent = []
        self.view.tableListRender(self.tableContent)

    def tableListRefresh(self):
        # Wyciąganie wszystkich danych z tej tabeli
        self.tableContent = self.window.modelConnection.SelectAll(self.table_name)
        self.view.tableListRefresh(self.tableContent)

    def backToTableList(self, widget=None):
        child = self.window.get_child()
        child.destroy()
        del self.view
        self.window.changeWindowContent("tableList")

    def runSqlCommand(self, widget):
        if len(self.view.entry.get_text()) > 10:
            try:
                self.tableContent = self.window.modelConnection.runSql(self.view.entry.get_text())
                self.view.tableListRefresh(self.tableContent)
            except ErrorClass as err:
                ErrorPrompt(err)