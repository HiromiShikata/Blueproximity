#!/usr/bin/env python
# coding: utf-8

# system includes
import os
import sys

# blueproximity
SW_VERSION = '1.2.5'
'''
Add security to your desktop by automatically locking and unlocking
the screen when you and your phone leave/enter the desk.
Think of a proximity detector for your mobile phone via bluetooth.
requires external bluetooth util hcitool to run
(which makes it unix only at this time)
Needed python extensions:
    ConfigObj (python-configobj)
    PyGTK (python-gtk2, python-glade2)
    Bluetooth (python-bluez)

Copyright by Lars Friedrichs <larsfriedrichs@gmx.de>
this source is licensed under the GPL.
I'm a big fan of talkback about how it performs!
I'm also open to feature requests and notes on programming issues,
I am no python master at all...
'''

APP_NAME = "blueproximity"

# This value gives us the base directory for language files and icons.
# Set this value to './' for svn version
# or to '/usr/share/blueproximity/' for packaged version
dist_path = './'


# now the imports from external packages
try:
    import gobject
except:
    print(_("The program cannot import the module gobject."))
    print(_("Please make sure the GObject bindings for python are installed."))
    print(_("e.g. with Ubuntu Linux, type"))
    print(_(" sudo apt-get install python-gobject"))
    sys.exit(1)
try:
    from configobj import ConfigObj
    from validate import Validator
except:
    print(_("The program cannot import the module ConfigObj or Validator."))
    print(_("Please make sure the ConfigObject package for python is installed."))
    print(_("e.g. with Ubuntu Linux, type"))
    print(_(" sudo apt-get install python-configobj"))
    sys.exit(1)
try:
    import pygtk
    pygtk.require("2.0")
    import gtk
except:
    print(_("The program cannot import the module pygtk."))
    print(_("Please make sure the GTK2 bindings for python are installed."))
    print(_("e.g. with Ubuntu Linux, type"))
    print(_(" sudo apt-get install python-gtk2"))
    sys.exit(1)
try:
    import gtk.glade
except:
    print(_("The program cannot import the module glade."))
    print(_("Please make sure the Glade2 bindings for python are installed."))
    print(_("e.g. with Ubuntu Linux, type"))
    print(_(" sudo apt-get install python-glade2"))
    sys.exit(1)


# Setup config file specs and defaults
# This is the ConfigObj's syntax
conf_specs = [
    'device_mac=string(max=17,default="")',
    'device_channel=integer(1,30,default=7)',
    'lock_distance=integer(0,127,default=7)',
    'lock_duration=integer(0,120,default=6)',
    'unlock_distance=integer(0,127,default=4)',
    'unlock_duration=integer(0,120,default=1)',
    'lock_command=string(default=''gnome-screensaver-command -l'')',
    'unlock_command=string(default=''gnome-screensaver-command -d'')',
    'proximity_command=string(default=''gnome-screensaver-command -p'')',
    'proximity_interval=integer(5,600,default=60)',
    'buffer_size=integer(1,255,default=1)',
    'log_to_syslog=boolean(default=True)',
    'log_syslog_facility=string(default=''local7'')',
    'log_to_file=boolean(default=False)',
    'log_filelog_filename=string(default=''' + os.getenv('HOME') + '/blueproximity.log'')'
]


# The icon used at normal operation and in the info dialog.
icon_base = 'blueproximity_base.svg'
# The icon used at distances greater than the unlock distance.
icon_att = 'blueproximity_attention.svg'
# The icon used if no proximity is detected.
icon_away = 'blueproximity_nocon.svg'
# The icon used during connection processes and with connection errors.
icon_con = 'blueproximity_error.svg'
# The icon shown if we are in pause mode.
icon_pause = 'blueproximity_pause.svg'
