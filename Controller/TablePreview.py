import gi, re

gi.require_version('Gtk', '3.0')
# from gi.overrides import Gtk
from gi.repository import Gtk

from View.TablePreviewView import *
from error import *


class TablePreview:
    def __init__(self, window, tableName):
        try:
            self.lockChange = False
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
            self.view.button_new_row.connect("clicked", self.newRow)

            select = self.view.tableListView.get_selection()
            select.connect("changed", self.deleteRow)

        except ErrorClass as err:
            ErrorPrompt(err)

    def tableList(self):
        # Wyciąganie wszystkich danych z tej tabeli
        self.tableContent = self.window.modelConnection.SelectAll(self.table_name)
        self.view.tableListRender(self.tableContent)

    def tableListRefresh(self):
        # Wyciąganie wszystkich danych z tej tabeli
        self.lockChange = True
        self.tableContent = self.window.modelConnection.SelectAll(self.table_name)
        self.view.tableListRefresh(self.tableContent)
        self.lockChange = False

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

    def deleteRow(self, selected):
        if self.lockChange == False:
            response = self.view.confirmDeleteRow()

            model, row = selected.get_selected()

            rowData = self.tableContent[1][model[row][0]]
            #print(rowData)
            #for row in model[row]:
                #print(row)
            #    rowData.append(row)

            if response == Gtk.ResponseType.YES:
                #print("QUESTION dialog closed by clicking YES button")
                self.window.modelConnection.deleteRow(self.table_name, rowData, self.tableContent[0])
                self.tableListRefresh()

    def newRow(self, widget):
        rowDialog = CreateNewRowDialog(self.window, self.tableContent[0], self.tableContent[2])

        #rowDialog.connect("close", rowDialog.closeWindow)
        data = rowDialog.valuesRow

        while(1):
            run = rowDialog.run()
            if run == Gtk.ResponseType.CANCEL:
                rowDialog.closeWindow()
                break
            elif run == Gtk.ResponseType.OK:

                colnames = []
                content = []
                empty = 0
                print(self.tableContent[2])

                typeError = False
                for i in range(len(data)):
                    if data[i][1].get_text() == '':
                        empty += 1
                    else:
                        content.append(data[i][1].get_text())
                        colnames.append(data[i][0])

                        temp = content[len(content) - 1]
                        pat = r".*"

                        if data[i][2] == 'DATE':
                            pat = r"^[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}$"
                        elif data[i][2] == 'DATETIME':
                            pat = r"^([0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}\s[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})|([0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}\s[0-9]{1,2}:[0-9]{1,2})$"
                        elif data[i][2] == 'NEWDECIMAL' or data[i][2] == 'FLOAT':
                            pat = r"^([0-9]+\.[0-9]+)|[0-9]+$"
                        elif data[i][2] == 'LONG':
                            pat = r"^[0-9]+$"


                        if re.match(pat, temp) == None:
                            rowDialog.createErrorMessage("W polu " + data[i][0] + " jest błąd!")
                            typeError = True

                        if data[i][2] == 'VAR_STRING' or data[i][2] == 'DATE' or data[i][2] == 'DATETIME':
                            content[len(content) - 1] = "'" + content[len(content) - 1] + "'"

                if typeError:
                    continue

                if empty == len(content):
                    rowDialog.createErrorMessage("Wszystkie pola są puste!!")
                    continue

                try:
                    if self.window.modelConnection.addRowToTable(self.table_name, colnames, content):
                        rowDialog.closeWindow()
                        self.tableListRefresh()
                        break
                except ErrorClass as err:
                    ErrorPrompt(err)

                #print(data)
