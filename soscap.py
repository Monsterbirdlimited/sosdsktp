#!/usr/bin/env python

import gi
import os
import datetime
import time

gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, Gtk



class GTK_Main:
    def __init__(self):
        window = Gtk.Window()
        window.set_title("SOSCap")
        window.set_default_size(120, 50)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        hbox.set_border_width(10)
        hbox.pack_start(Gtk.Label(), False, False, 0)
        self.button = Gtk.Button(label ="Start")
        self.button.connect("clicked", self.start_stop)
        hbox.pack_start(self.button, False, False, 0)
        self.button2 = Gtk.Button(label ="Quit")
        self.button2.connect("clicked", self.exit)
        hbox.pack_start(self.button2, False, False, 0)
        hbox.add(Gtk.Label())
        window.show_all()

        # Set up the gstreamer pipeline
        self.player = Gst.parse_launch("pipewiresrc do-timestamp=True ! queue ! videoscale ! videoconvert ! vaapih264enc bitrate=6000 quality-level=1 ! h264parse ! mux. pulsesrc device=alsa_output.sink.monitor ! queue ! audioconvert ! audioresample ! lamemp3enc bitrate=320 ! matroskamux name=mux ! filesink location=/home/deck/Videos/SOSCap.mkv sync=true")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def rename(self, src):
        f_path = "/home/deck/Videos/SOSCap.mkv"
        t = os.path.getctime(f_path)
        t_str = time.ctime(t)
        t_obj = time.strptime(t_str)
        form_t = time.strftime("SOSCap_%Y-%m-%d %H:%M:%S", t_obj)
        form_t = form_t.replace(":", "꞉")
        os.rename(
            f_path, os.path.split(f_path)[0] + '/' + form_t + os.path.splitext(f_path)[1])


    def start_stop(self, w):
        if self.button.get_label() == "Start":
            self.button.set_label("Stop")
            self.player.set_state(Gst.State.PLAYING)
        else:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            #import rename
            #execfile('rename.py')
            self.rename(self)

    def exit(self, widget, data=None):
        Gtk.main_quit()
    

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            #import rename
            #execfile('rename.py')
            #rename()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        struct = message.get_structure()
        if not struct:
            return
        message_name = struct.get_name()





        
Gst.init(None)
GTK_Main()
Gtk.main()
