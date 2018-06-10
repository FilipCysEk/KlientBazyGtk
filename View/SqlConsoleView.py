import gi, re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import datetime

class SqlConsoleView(Gtk.Window):
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


        #Przycisk powrotu
        self.button_back = Gtk.Button("<- Powrót")
        self.button_back.set_size_request(100, 20)
        self.fixed.put(self.button_back, 10, 10)

        #linia poleceń
        self.entry = Gtk.Entry()
        self.entry.set_size_request(450, 20)
        self.entry.set_text("SELECT * from test1 WHERE wzrost = 2.5 AND id %2 =0")
        self.fixed.put(self.entry, 10, 70)

        #Przycisk wykonywania
        # Przycisk usuwania tabeli
        self.button_run = Gtk.Button("Wykonaj")
        self.button_run.set_size_request(100, 20)
        self.button_run.override_background_color(0, Gdk.RGBA(0, 0.6, 0, 1))
        self.button_run.override_color(0, Gdk.RGBA(1, 1, 1, 1))
        self.fixed.put(self.button_run,
                       self.window.get_size()[0] - 40 - self.button_run.get_size_request()[0], 10)

        #Lista tabel
        self.tableListView.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)



        self.window.add(self.fixed)
        self.window.show_all()

    def tableListRefresh(self, objList):
        if self.tableListObj != None:

            self.tableListObj.clear()
            del self.tableListObj
            self.tableListObj = None
            self.tableListView.destroy()
            self.scroll.destroy()
            del self.tableListView
            self.tableListRender(objList)

            self.scroll = Gtk.ScrolledWindow()
            # self.fixed.put(self.tableListView, 10, 140)
            self.scroll.add(self.tableListView)
            self.scroll.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)
            self.fixed.put(self.scroll, 10, 130)
            self.window.show_all()
        else:
            self.tableListRender(objList)

            self.scroll = Gtk.ScrolledWindow()
            # self.fixed.put(self.tableListView, 10, 140)
            self.scroll.add(self.tableListView)
            self.scroll.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 200)
            self.fixed.put(self.scroll, 10, 130)

            self.window.show_all()


    def tableListRender(self, objList):
        print(objList)
        if len(objList) != 0:
            print("Cos")
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
        else:
            self.tableListView = Gtk.TreeView()