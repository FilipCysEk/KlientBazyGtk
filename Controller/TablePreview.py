import gi, re

gi.require_version('Gtk', '3.0')
# from gi.overrides import Gtk
from gi.repository import Gtk

from View.TablePreviewView import *
from error import *


class TablePreview:
    def __init__(self, window, tableName):
        try:
            self.window = window
            self.table_name = tableName
            self.window.set_title(tableName)
            self.view = TablePreviewView(window)

            # Wyciąganie wszystkich danych z tej tabeli
            #self.tableContent = window.modelConnection.SelectAll(tableName)
            self.tableList()
            self.view.render()

            self.view.button_delete_table.connect("clicked", self.deleteTable)
            self.view.button_back.connect("clicked", self.backToTableList)

        except ErrorClass as err:
            ErrorPrompt(err)

    def tableList(self):
        # Wyciąganie wszystkich danych z tej tabeli
        self.tableContent = self.window.modelConnection.SelectAll(self.table_name)
        self.view.tableListRender(self.tableContent)

    def tableListRefresh(self):
        # Wyciąganie wszystkich danych z tej tabeli
        self.tableContent = self.window.modelConnection.SelectAll(self.table_name)
        self.view.tableListRefresh(self.tableContent)

    def deleteTable(self, widget):
        dialogWindow = self.view.deleteTableDialog()

        if dialogWindow == Gtk.ResponseType.OK:
            self.window.modelConnection.deleteTable(self.table_name)
            self.backToTableList()

    def backToTableList(self, widget=None):
        child = self.window.get_child()
        child.destroy()
        del self.view
        self.window.changeWindowContent("tableList")


