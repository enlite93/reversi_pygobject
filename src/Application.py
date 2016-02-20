#!/usr/bin/env python3

try:
    import gi
    gi.require_version('Gtk', '3.0')
except ImportError:
    raise('Cannot import "gi" repository')

try:
    from gi.repository import Gtk
except ImportError:
    raise('Cannot import "Gtk" framework')

import random
import Screen
# import Leaderboard


class Application(Gtk.Window):

    """
    Main window of game.
    """

    def __init__(self):
        """
        Initialize Application Window
        """
        Gtk.Window.__init__(self)

        # Default properties
        self.set_title("reversi")
        self.set_border_width(10)
        self.set_resizable(False)

        # Default events
        self.connect('delete-event', Gtk.main_quit)

        # Create Title bar
        header = Gtk.HeaderBar(title='Reversi 0.1',
                               subtitle="TDT University - Spring 2016",
                               show_close_button=True)
        self.set_titlebar(header)

        # Create main container
        self.hcontainer = Gtk.HBox(spacing=10)
        self.add(self.hcontainer)

        # Create drawing area
        self.screen = Screen.Screen(self.matrix)
        self.connect('button-press-event', self.__on_mouse_pressed)
        self.hcontainer.pack_start(self.screen, True, True, 0)

        # Create right panel
        vbox_panel = Gtk.VBox()
        self.__init_panel(vbox_panel)
        self.hcontainer.pack_end(vbox_panel, False, False, 0)

        # Display Application Window
        self.show_all()

    def __init_panel(self, widget):
        """Initialize right panel

        :widget: container
        :returns: none

        """
        # Create panel labels

        lbl_information = Gtk.Label()
        lbl_information.set_markup("<b>Information</b>")

        lbl_score = Gtk.Label()
        lbl_score.set_markup("<b>Score</b>")

        lbl_setting = Gtk.Label()
        lbl_setting.set_markup('<b>Setting</b>')

        lbl_time = Gtk.Label(halign=Gtk.Align.START)
        lbl_time.set_label("Time")

        lbl_turn = Gtk.Label(halign=Gtk.Align.START)
        lbl_turn.set_label("Turn")

        lbl_score_player = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_player.set_label(self.player_label)

        lbl_score_computer = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_computer.set_label(self.computer_label)

        lbl_showhint = Gtk.Label(halign=Gtk.Align.START)
        lbl_showhint.set_label('Show hint')

        lbl_showmove = Gtk.Label(halign=Gtk.Align.START)
        lbl_showmove.set_label('Show move')

        lbl_time_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_time_count.set_label(repr(self.timer))

        lbl_turn_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_turn_count.set_label(repr(self.turn))

        lbl_score_player_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_score_player_count.set_label(repr(self.player_score))

        lbl_score_computer_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_score_computer_count.set_label(repr(self.computer_score))

        # Create buttons
        self.btn_start = Gtk.Button()
        self.btn_start.set_label("Start Game")
        self.btn_start.set_size_request(-1, 50)
        self.btn_start.connect('clicked', self.__on_button_start_clicked)

        self.btn_hiscore = Gtk.Button()
        self.btn_hiscore.set_label("High Scores")
        self.btn_hiscore.set_size_request(-1, 50)
        self.btn_hiscore.connect('clicked', self.__on_button_hiscore_clicked)

        self.btn_quit = Gtk.Button()
        self.btn_quit.set_size_request(-1, 50)
        self.btn_quit.set_label("Quit")
        self.btn_quit.connect('clicked', self.__on_button_quit_clicked)

        self.switch_hint = Gtk.Switch(valign=Gtk.Align.END)
        self.switch_hint.connect('notify::active',
                                 self.__on_switch_hint_activated)

        self.switch_show_moves = Gtk.Switch(valign=Gtk.Align.END)
        self.switch_show_moves.set_active(True)
        self.switch_show_moves.connect('notify::active',
                                       self.__on_switch_show_move_activated)

        # Right panel listbox
        panel_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        widget.add(panel_listbox)

        # Sysinfo Label
        row = Gtk.ListBoxRow()
        row.add(lbl_information)
        panel_listbox.add(row)

        # Timer row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_time, True, True, 0)
        hbox.pack_start(lbl_time_count, True, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Turn row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_turn)
        hbox.add(lbl_turn_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Blank Row
        row = Gtk.ListBoxRow()
        lbl_blank = Gtk.Label()
        lbl_blank.set_label("")
        row.add(lbl_blank)
        panel_listbox.add(row)

        # Score Row
        row = Gtk.ListBoxRow()
        row.add(lbl_score)
        panel_listbox.add(row)

        # Player's score row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_score_player)
        hbox.add(lbl_score_player_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Computer's score row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_score_computer)
        hbox.add(lbl_score_computer_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Blank row
        row = Gtk.ListBoxRow()
        lbl_blank = Gtk.Label()
        lbl_blank.set_label("")
        row.add(lbl_blank)
        panel_listbox.add(row)

        # Setting row
        row = Gtk.ListBoxRow()
        row.add(lbl_setting)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_showhint, True, True, 0)
        hbox.pack_start(self.switch_hint, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_showmove, True, True, 0)
        hbox.pack_start(self.switch_show_moves, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Add buttons to the bottom
        widget.pack_end(self.btn_quit, False, True, 0)
        widget.pack_end(self.btn_hiscore, False, True, 0)
        widget.pack_end(self.btn_start, False, True, 0)

    def __on_button_start_clicked(self, button):
        """Start game and change the label to "restart",
        "High Scores" label to "Pause"

        :button: button
        :return: none
        """
        self.turn = random.randint(1, 2)
        button.set_label('Restart')
        self.btn_hiscore.set_label('Pause')
        pass

    def __on_mouse_pressed(self, widget, event):
        """Handle mouse click on drawing area

        :widget: Gtk.DrawingArea
        :event: mouse click
        :returns: none

        """
        row, col = self.get_position_in_matrix(int(event.x), int(event.y))
        print('Mouse clicked on', col, row)

        # if self.turn == 1 and self.is_valid_move(row, col):
        # TODO recheck
        if self.is_valid_move(row, col):
            self.matrix[row][col] = self.turn
            widget.queue_draw()
            self.turn_switch()

    def __on_button_hiscore_clicked(self, button, args=""):
        """Show the leaderboard and receive new high score (if any).

        :button: button
        :args: current score and time
        :returns: none

        """
        # leaderboard = Leaderboard.Leaderboard(args)
        # leaderboard.show_all()

        pass

    def __on_button_quit_clicked(self, button, args=""):
        """Show the quit confirmation dialog.

        :button: button
        :args: TODO
        :returns: none
        """
        dialog = Gtk.MessageDialog(parent=self)
        dialog.set_markup("<b><big>Do you want to quit?</big></b>")
        dialog.format_secondary_text("We will wait for you!")
        dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
        dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

        dialog.add_button("Not now", Gtk.ResponseType.CANCEL)
        dialog.add_button("I said quit!", Gtk.ResponseType.OK)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            Gtk.main_quit(self)
        else:
            pass

        dialog.destroy()

    def __on_button_restart_clicked(self, button):
        pass

    def __on_switch_hint_activated(self, switch, args=""):
        """Show hints.

        :switch: switch
        :args: TODO
        :returns: none
        """
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show hint\" was turned", state)

    def __on_switch_show_move_activated(self, switch, args=""):
        """Show moves.

        :switch: switch
        :args: TODO
        :returns: none
        """
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show moves\" was turned", state)

    def is_valid_move(self, x, y):
        """Check if the movement in current position is a valid move

        :x: matrix row
        :y: matrix column
        :returns: True if is a valid move, false otherwise


        """
        if self.matrix[x][y] != 0:
            return False

        if x >= 0 and y >= 0:
            return True

        return False

    def get_position_in_matrix(self, position_x, position_y):
        """Determine the current pair of x, y position is in which cell of
           matrix

        :position_x: x position in pixel
        :position_y: y position in pixel
        :returns: position x, y of matrix, (-1, -1) if out-of-bound
        """
        if (position_x < self.screen.cell_size) \
           or (position_x > self.screen.size - self.screen.cell_size) \
           or (position_y < self.screen.cell_size) \
           or (position_y > self.screen.size - self.screen.cell_size):
            return -1, -1

        for row in range(8):
            if (row + 2) * self.screen.cell_size > position_y:
                break

        for col in range(8):
            if (col + 2) * self.screen.cell_size > position_x:
                break

        return row, col

    def turn_switch(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

    timer = 0.00
    turn = 0
    player_label = "Player"
    player_score = 0
    computer_label = "Computer"
    computer_score = 0

    matrix = [[0 for col in range(8)] for row in range(8)]
    matrix[3][4] = 1
    matrix[4][3] = 1
    matrix[3][3] = 2
    matrix[4][4] = 2

application = Application()
Gtk.main()
