import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TableListView(Gtk.Window):
    def __init__(self, window = Gtk.Window):
        #Gtk.Window.__init__(parent)
        self.window = window
        self.window.set_size_request(500, 600)
        #self.window.set_title("testowe")
        self.window.set_border_width(10)
        self.tableListObj = None

    '''
    def __del__(self):
        self.tableListObj.destroy()
        self.button_new_table.destroy()
        self.tableListView.destroy()
    '''

    def tableListRender(self, objList):
        if objList == None or len(objList) == 0:
            self.tableListObj = Gtk.Label("Nie ma żadnej tabeli")
        else:
            self.tableListObj = Gtk.ListStore(str)
            for row in objList:
                self.tableListObj.append([row[0]])

            self.tableListView = Gtk.TreeView(self.tableListObj)

            for i, col_title in enumerate(["Tabela"]):
                renderer = Gtk.CellRendererText()

                column = Gtk.TreeViewColumn(col_title, renderer, text=i)
                column.set_sort_column_id(i)

                self.tableListView.append_column(column)

    def tableListRefresh(self, objList):
        if objList == None or len(objList) == 0:
            if self.tableListObj != None:
                self.tableListObj.destroy()
            self.tableListObj = Gtk.Label("Nie ma żadnej tabeli")
        else:
            if self.tableListObj == Gtk.Label:
                self.tableListObj.destroy()
                self.tableListObj = Gtk.ListStore(str)

            self.tableListObj.clear()
            for row in objList:
                self.tableListObj.append([row[0]])

            self.tableListView = Gtk.TreeView(self.tableListObj)

            for i, col_title in enumerate(["Tabela"]):
                renderer = Gtk.CellRendererText()

                column = Gtk.TreeViewColumn(col_title, renderer, text=i)

                self.tableListView.append_column(column)

        self.window.show_all()

    def render(self):

        #Rysujemy okno
        self.window.show()
        self.fixed = Gtk.Fixed()

        #Zmieniamy tytuł
        self.window.set_title("Tabele")

        #Przycisk nowej tabeli
        self.button_new_table = Gtk.Button("Nowa tabela")
        self.button_new_table.set_size_request(100, 20)
        self.fixed.put(self.button_new_table, 10, 10)

        # Przycisk konsoli SQL
        self.button_sql_console = Gtk.Button("Konsola SQL")
        self.button_sql_console.set_size_request(100, 20)
        self.fixed.put(self.button_sql_console, 200, 10)

        #Lista tabel
        self.tableListView.set_size_request(self.window.get_size()[0] - 40, self.window.get_size()[1] - 150)

        self.fixed.put(self.tableListView, 10, 70)

        self.window.add(self.fixed)
        self.window.show_all()


class CreateTableWindow(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Stwórz nową tabelę", parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        ))

        #Tworzenie tabeli
        self.row_num = 2
        self.table = Gtk.Grid(column_spacing=20, row_spacing=15, margin_bottom=15, margin_top=15, margin_left=15, margin_right=15)
        #self.connect("destroy", Gtk.main_quit)
        #self.connect("destroy", self.closeWindow)

        #Tworzenie przewijanej przestrzeni
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(500, 375)

        #Nazwa tabeli
        #label = Gtk.Label("Nazwa tabeli:")
        self.tableName = Gtk.Entry()
        self.table.attach(Gtk.Label("Nazwa tabeli:"), 0, 0, 1, 1)
        self.table.attach(self.tableName, 1, 0, 2, 1)

        #pierwszy wiersz
        self.addToTable([Gtk.Label("Nazwa kolumny"), Gtk.Label("Typ"), Gtk.Label("Rozmiar")])


        #tablice zmiennych
        self.name = []
        self.type = []
        self.size = []

        #tworzenie comboboxa
        self.listOfType = Gtk.ListStore(str)
        self.listOfType.append(['INT'])
        self.listOfType.append(['VARCHAR'])
        self.listOfType.append(['TEXT'])
        self.listOfType.append(['FLOAT'])
        self.listOfType.append(['DOUBLE'])
        self.listOfType.append(['DECIMAL'])
        self.listOfType.append(['DATE'])
        self.listOfType.append(['DATETIME'])

        self.addNewTableColumn()

        buttonAddRow = Gtk.Button("Dodaj kolumne")
        buttonAddRow.set_margin_bottom(50)
        buttonAddRow.set_margin_top(20)
        buttonAddRow.set_margin_left(50)
        buttonAddRow.set_margin_right(50)

        buttonAddRow.connect("clicked", self.addNewTableColumnConnect)

        #rysowanie

        self.area = self.get_content_area()
        scroll.add(self.table)
        self.area.add(scroll)
        self.area.add(buttonAddRow)
        self.show_all()

    def addToTable(self, elements):
        '''
        Adding row in to table
        :param elements: elemnets of row
        :return:
        '''
        for i in range(len(elements)):
            self.table.attach(elements[i], i, self.row_num, 1, 1)
        self.row_num += 1

    def addNewTableColumn(self):
        entry = Gtk.Entry()
        entry.set_placeholder_text("Podaj nazwę")
        self.name.append(entry)

        combo = Gtk.ComboBox.new_with_model(self.listOfType)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        self.type.append(combo)

        entry2 = Gtk.Entry()
        entry2.set_placeholder_text("Rozmiar np 2")
        self.size.append(entry2)

        ix = len(self.name) - 1
        self.addToTable([self.name[ix], self.type[ix], self.size[ix]])
        self.show_all()

    def addNewTableColumnConnect(self, widget):
        self.addNewTableColumn()

    def createTableErrorMessage(self, error):
        message = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                    "Błąd tworzenia tabeli")
        message.format_secondary_text(str(error))
        message.run()

        message.destroy()

    def closeWindow(self, widget):
        self.destroy()


