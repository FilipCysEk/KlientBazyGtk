import gi, re

gi.require_version('Gtk', '3.0')
# from gi.overrides import Gtk
from gi.repository import Gtk

from View.TableListView import *
from error import *

class TableList:
    def __init__(self, window = Gtk.Window):
        try:
            self.window = window
            self.view = TableListView(self.window)
            self.tableList()
            self.view.render()

            #self.window.changeWindowContent("TableList")
            self.view.button_new_table.connect("clicked", self.createTable)
            self.view.button_sql_console.connect("clicked", self.goToConsole)
            select = self.view.tableListView.get_selection()
            select.connect("changed", self.goToTablePreview)

        except ErrorClass as err:
            ErrorPrompt(err)

    def tableList(self):
        objList = self.window.modelConnection.getTableList()
        self.view.tableListRender(objList)

    def tableListRefresh(self):
        objList = self.window.modelConnection.getTableList()
        self.view.tableListRefresh(objList)

    def createTable(self, button):
        dialogWindow = CreateTableWindow(self.window)
        #dialogWindow.connect("destroy", dialogWindow.closeWindow)
        while(1):
            response = dialogWindow.run()

            if response == Gtk.ResponseType.CANCEL:
                dialogWindow.destroy()
                break

            elif response == Gtk.ResponseType.OK:
                if len(dialogWindow.name) == 0:
                    dialogWindow.createTableErrorMessage("Błąd wprowadzanych danych")
                else:
                    if len(dialogWindow.tableName.get_text()) == 0:
                        dialogWindow.createTableErrorMessage("Błąd nazwy tabeli")
                        continue

                    tableTypes = []
                    err = 0
                    empty = 0

                    for i in range(len(dialogWindow.name)):
                        temp_combo1 = dialogWindow.type[i].get_active()

                        if temp_combo1 == -1:
                            temp_combo = ''
                        else:
                            temp_combo = dialogWindow.type[i].get_model()
                            temp_combo = temp_combo[temp_combo1][0]

                        val = self.createTableCheckRow(dialogWindow.name[i].get_text(), temp_combo,
                                                       dialogWindow.size[i].get_text())

                        if val == -1:
                            empty += 1
                        elif val == 0:
                            err += 1
                        else:
                            tableTypes.append([dialogWindow.name[i].get_text(), temp_combo,
                                                       dialogWindow.size[i].get_text()])

                    if err > 0:
                        dialogWindow.createTableErrorMessage("Błąd wprowadzanych danych, sprawdź, czy wszystko jest dobrze")
                        continue

                    if empty == len(dialogWindow.name):
                        dialogWindow.createTableErrorMessage("Błąd wprowadzanych danych, chyba niewypełniłeś żadnej komórki")
                        continue

                    try:
                        if self.window.modelConnection.createTable(tableTypes, dialogWindow.tableName.get_text()):
                            self.tableListRefresh()
                            dialogWindow.destroy()
                            #print("Jest OK")
                            break

                    except ErrorClass as err:
                        ErrorPrompt(err)



    def createTableCheckRow(self, name, type, size):
        '''
        Function checking input entry, tats is good
        :param name: text to validation contains name
        :param type: text contains type
        :param size: text contains size of new column
        :return: 0 - error; 1 - row is good; -1 - row is empty;
        '''

        if len(name) == 0 and len(type) == 0 and len(size) == 0:
            return -1

        if len(name) == 0 or len(type) == 0:
            return 0

        if name.find(' ') != -1:
            print("Spacja w nazwie zmiennej")
            return 0

        if (type == 'DATE' or type == 'DATETIME'):
            if len(size) != 0:
                print("Podano coś w polu rozmiar w typie data lub datatime")
                return 0
        else:
            if type == 'DECIMAL':
                pat = r"^[0-9]+,[ ]*[0-9]+$"
                if re.match(pat, size) == None:
                    return 0
            elif type == 'VARCHAR':
                pat = r"^[0-9]+$"
                if re.match(pat, size) == None:
                    return 0
            else:
                pat = r"^[0-9]*$"
                if re.match(pat, size) == None:
                    return 0

    def goToTablePreview(self, selection):
        model, row = selection.get_selected()
        #print(model[row][0])

        child = self.window.get_child()
        child.destroy()
        del self.view
        self.window.changeWindowContent("tablePreview", model[row][0])

    def goToConsole(self, selection):

        child = self.window.get_child()
        child.destroy()
        del self.view
        self.window.changeWindowContent("console")

