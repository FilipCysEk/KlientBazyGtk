import gi, re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import datetime

class TablePreviewView(Gtk.Window):
    def __init__(self, window = Gtk.Window):
        #Gtk.Window.__init__(parent)
        self.window = window
        #self.window.set_size_request(500, 600)
        self.window.set_border_width(10)
        self.tableListObj = None

    def render(self):

        #Rysujemy okno
        self.window.show()
        self.fixed = Gtk.Fixed()
        self.scroll = Gtk.ScrolledWindow()


        #Przycisk usuwania tabeli
        self.button_delete_table = Gtk.Button("Usuń tabele")
        self.button_delete_table.set_size_request(100, 20)
        self.button_delete_table.override_background_color(0, Gdk.RGBA(1, 0, 0, 1))
        self.button_delete_table.override_color(0, Gdk.RGBA(1, 1, 1, 1))
        self.fixed.put(self.button_delete_table, self.window.get_size()[0] - 40 - self.button_delete_table.get_size_request()[0], 10)

        #Przycisk powrotu
        self.button_back = Gtk.Button("<- Powrót")
        self.button_back.set_size_request(100, 20)
        self.fixed.put(self.button_back, 10, 10)

        #przcisk nowego wiersza
        self.button_new_row = Gtk.Button("Nowy wiersz")
        self.button_new_row.set_size_request(100, 20)
        self.fixed.put(self.button_new_row, self.window.get_size()[0] - 60 - self.button_delete_table.get_size_request()[0]
                       - self.button_new_row.get_size_request()[0], 10)

        #Przycisk usuwania
        self.button_delete_row = Gtk.Button("Usuń wiersz")
        self.button_delete_row.set_size_request(100, 20)
        self.button_delete_row.override_background_color(0, Gdk.RGBA(1, 0, 0, 1))
        self.button_delete_row.override_color(0, Gdk.RGBA(1, 1, 1, 1))
        self.fixed.put(self.button_delete_row, 10, self.window.get_size()[1]-60)

        #Lista tabel
        #self.tableListView.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)

        #self.fixed.put(self.tableListView, 10, 70)
        self.scroll.add(self.tableListView)
        self.scroll.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)
        self.fixed.put(self.scroll, 10, 70)

        self.window.add(self.fixed)
        self.window.show_all()

    def tableListRefresh(self, objList):
        self.tableListObj.clear()
        #self.tableListView.destroy()
        self.tableListRender(objList)
        #self.scroll.add(self.tableListView)
        self.window.show_all()


    def tableListRender(self, objList):
        colnames = objList[0]
        result = objList[1]
        dataTypes = objList[2]

        coltypes = [int]
        result1 = []
        colnum = 0

        for i in range(len(result)):
            result1.append([row for row in result[i]])

        for type in dataTypes:
            if type == 'LONG':
                coltypes = coltypes + [int]
            elif type == 'FLOAT':
                coltypes = coltypes + [float]
            elif type == 'DOUBLE':
                coltypes = coltypes + [float]
            elif type == 'VAR_STRING':
                coltypes = coltypes + [str]
            elif type == 'BLOB':
                coltypes = coltypes + [str]
            elif type == 'NEWDECIMAL':
                coltypes = coltypes + [float]
            elif type == 'DATE':
                coltypes = coltypes + [str]

                for i in range(len(result)):
                    result1[i][colnum] = str(result1[i][colnum])
            elif type == 'DATETIME':
                coltypes = coltypes + [str]

                for i in range(len(result)):
                    result1[i][colnum] = str(result1[i][colnum])

            colnum += 1
        '''
        if len(result) == 0:
            coltypes = [str] * len(colnames)
        else:
            coltypes = [type(result[0][0])]
            if type(result[0][0]) == type(None):
                coltypes = [str]

            for i in range(1, len(result[0])):
                temp = type(result[0][i])
                if temp == type(None):
                    temp = str
                coltypes = coltypes + [temp]
        '''
        #print(coltypes)
        i = 0

        if self.tableListObj == None:
            self.tableListObj = Gtk.ListStore(*coltypes)

        for row in result1:
            row = [i] + row
            i += 1
            self.tableListObj.append(row)

        self.tableListView = Gtk.TreeView(self.tableListObj)

        #print(colnames)
        colnames = ("nr",) + colnames

        for i, col_title in enumerate(colnames):
            renderer = Gtk.CellRendererText()

            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            column.set_sort_column_id(i)

            self.tableListView.append_column(column)

    def deleteTableDialog(self):
        message = Gtk.Dialog("Napewno?", self.window, Gtk.DialogFlags.MODAL,
                             (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                              Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        message.set_default_size(300, 90)

        box = message.get_content_area()
        label = Gtk.Label("Czy na pewno chcesz usunąć tą tabelę?")
        box.pack_start(label, True, True, 0)
        message.add(box)
        message.show_all()
        answer = message.run()

        message.destroy()
        return answer

    def confirmDeleteRow(self):
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.YES_NO, "Czy napewno chcesz usunąć wiersz?")
        #dialog.format_secondary_text("And this is the secondary text that explains things.")
        temp = dialog.run()
        dialog.destroy()
        return temp

class CreateNewRowDialog(Gtk.Dialog):
    def __init__(self, parent, colnames, coltypes):
        Gtk.Dialog.__init__(self, "Dodaj nowy wiersz", parent, Gtk.DialogFlags.MODAL,
                                  (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                   Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))



        #self.set_default_size(300, 400)

        # Tworzenie tabeli
        self.row_num = 2
        self.table = Gtk.Grid(column_spacing=20, row_spacing=15, margin_bottom=15, margin_top=15, margin_left=15,
                              margin_right=15)

        # Tworzenie przewijanej przestrzeni
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(500, 375)

        # pierwszy wiersz
        #self.addToTable([Gtk.Label("Nazwa kolumny"), Gtk.Label("Typ"), Gtk.Label("Rozmiar")])

        # tablica zmiennych
        self.valuesRow = []

        # Tworzenie listy pól
        for i in range(len(colnames)):
            label = Gtk.Label(colnames[i])
            self.table.attach(label, 0, self.row_num, 1, 1)

            entry = Gtk.Entry()
            self.table.attach(entry, 1, self.row_num, 1, 1)

            label = Gtk.Label(coltypes[i])
            self.table.attach(label, 2, self.row_num, 1, 1)

            self.valuesRow.append((colnames[i], entry, coltypes[i]))
            #print([colnames[i], entry, coltypes[i]])

            self.row_num += 1

        # rysowanie

        self.area = self.get_content_area()
        scroll.add(self.table)
        self.area.add(scroll)
        self.show_all()

    def createErrorMessage(self, error):
        message = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                    "Błąd dodawania wiersza")
        message.format_secondary_text(str(error))
        message.run()

        message.destroy()

    def closeWindow(self, widget = None):
        self.destroy()