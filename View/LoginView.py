import gi
gi.require_version('Gtk', '3.0')
#from gi.overrides import Gtk
from gi.repository import Gtk
#from gi.repository import GObject

#from gi.overrides import Gtk

class LoginView:

    def __init__(self):
        #self.view =
        pass


class PoupUpLoginWindow(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Zaloguj się do bazy", parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        ))


        self.connect("destroy", Gtk.main_quit)

        self.set_default_size(400, 150)
        self.set_border_width(20)


        #main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box = Gtk.ListBox()
        main_box.set_selection_mode(Gtk.SelectionMode.NONE)

        row_1 = Gtk.ListBoxRow()
        row_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_1.add(row_box1)

        rb1_label = Gtk.Label("Podaj nazwę użytkownika:")
        self.rb1_input = Gtk.Entry()
        self.rb1_input.set_placeholder_text("Nazwa użytkownika")
        self.rb1_input.set_size_request(10, 1)

        row_box1.pack_start(rb1_label, True, True, 0)
        row_box1.pack_start(self.rb1_input, False, True, 0)
        main_box.add(row_1)

        row_2 = Gtk.ListBoxRow()
        row_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_2.add(row_box2)

        rb2_label = Gtk.Label("Podaj hosta:")
        self.rb2_input = Gtk.Entry()
        self.rb2_input.set_placeholder_text("localhost")
        self.rb2_input.set_size_request(10, 1)

        row_box2.pack_start(rb2_label, True, True, 0)
        row_box2.pack_start(self.rb2_input, False, True, 0)
        main_box.add(row_2)

        row_3 = Gtk.ListBoxRow()
        row_box3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_3.add(row_box3)

        rb3_label = Gtk.Label("Podaj nazwę bazy danych:")
        self.rb3_input = Gtk.Entry()
        self.rb3_input.set_placeholder_text("baza")
        self.rb3_input.set_size_request(10, 1)

        row_box3.pack_start(rb3_label, True, True, 0)
        row_box3.pack_start(self.rb3_input, False, True, 0)
        main_box.add(row_3)

        row_4 = Gtk.ListBoxRow()
        row_box4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_4.add(row_box4)

        rb4_label = Gtk.Label("Podaj hasło:")
        self.rb4_input = Gtk.Entry()
        self.rb4_input.set_placeholder_text("Hasło")
        self.rb4_input.set_size_request(10, 1)
        self.rb4_input.set_visibility(False)

        row_box4.pack_start(rb4_label, True, True, 0)
        row_box4.pack_start(self.rb4_input, False, True, 0)
        main_box.add(row_4)

        self.rb1_input.set_text("ktos")
        self.rb2_input.set_text("localhost")
        self.rb3_input.set_text("ktos")

        area = self.get_content_area()
        area.add(main_box)

        self.show_all()

    def connectionErrorMessage(self, error):
        message = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Błąd łączenia z bazą danych")
        message.format_secondary_text(str(error))
        message.run()

        message.destroy()