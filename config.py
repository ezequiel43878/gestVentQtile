##### IMPORTS #####
import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

##### DEFINING SOME VARIABLES #####
mod = "mod4"
myTerm = "terminator"
myConfig = "/home/ezequel/.config/qtile/config.py"

##### KEYBINDINGS #####
keys = [
         ### The essentials
         Key(
             [mod], "Return",
             lazy.spawn(myTerm)
             ),
         Key(
             [mod], "d",
             lazy.spawn("dmenu_run -p 'Buscar: '")
             ),
         Key(
             [mod], "Tab",
             lazy.next_layout() 
             ),
         Key(
             [mod], "q",
             lazy.window.kill()
             ),
         Key(
             [mod, "shift"], "r",
             lazy.restart() 
             ),
         Key(
             [mod, "shift"], "q",
             lazy.shutdown()
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0)                       # Keyboard focus to screen(0)
             ),
         Key([mod], "e",
             lazy.to_screen(1)                       # Keyboard focus to screen(1)
             ),
         Key([mod], "r",
             lazy.to_screen(2)                       # Keyboard focus to screen(2)
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen()                      # Move monitor focus to next screen
             ),
         Key([mod], "comma",
             lazy.prev_screen()                      # Move monitor focus to prev screen
             ),
         ### Window controls
         Key([mod], "i",
             lazy.layout.up()                       # Move up a section in bsp
             ),
         Key([mod], "k",
             lazy.layout.down()                     # Move down a section in bsp
             ),
         Key(
             [mod], "l",
             lazy.layout.right()                    # Move right a section in bsp                      
             ),
         Key(
             [mod], "j",
             lazy.layout.left()                      # Move left a section in bsp
             ),
         ### Hacer flotante la ventana
         Key(
             [mod, "shift"], "f",
             lazy.window.toggle_floating()           # Toggle floating
             ),
         Key(
             [mod, "shift"], "Print",
             lazy.spawn('gnome-screenshot -i')
             ),
]

##### Named GROUPS #####
workspaces = [
    {"name": "Term", "key": "1", "matches": [Match(wm_class=myTerm)]},
    {"name": "WWW", "key": "2", "matches": [Match(wm_class='brave-browser')]},
    {"name": "Dev", "key": "3", "matches": [Match(wm_class='subl')]},
    {"name": "Tel", "key": "4", "matches": [Match(wm_class='telegram-desktop')]},
    {"name": "Apps", "key": "5", "matches": [Match(wm_class='gimp'),Match(wm_class='teamviewer')]},
    {"name": "Music", "key": "6", "matches": [Match(wm_class='spotify')]},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.append(Key([mod], workspace["key"], lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"], lazy.window.togroup(workspace["name"])))   

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {
        "border_width": 3,
        "margin": 4,
        "border_focus": "b30000",
        "border_normal": "1D2330",
}

##### THE LAYOUTS #####
layouts = [
    layout.Bsp(**layout_theme),
    layout.Max(**layout_theme),
]

##### COLORS #####
colors = [["#282a36", "#282a36"], # panel background
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#cc0000", "#cc0000"], # border line color for other tab and odd widgets rs
          ["#330000", "#330000"], # color for the even widgets cst
          ["#00b33c", "#00b33c"]] # window name   tmb

##### PROMPT #####
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

##### WIDGETS #####
def init_widgets_list():
    widgets_list = [
               widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 1,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = colors[2],
                        inactive = colors[2],
                        rounded = False,
                        highlight_color = colors[1],
                        highlight_method = "line",
                        this_current_screen_border = colors[3],
                        this_screen_border = colors [4],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.Prompt(
                        prompt=prompt,
                        font="Ubuntu Mono",
                        padding=10,
                        foreground = colors[3],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.WindowName(
                        foreground = colors[6],
                        background = colors[0],
                        padding = 0
                        ),
               widget.Net(
                        format = "{down} ↓↑ {up}",
                        background = colors[5],
                        foreground = colors[2],
                        interface = "wlp16s0",
                        padding = 10
                        ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.KeyboardLayout(
                        background = colors[4],
                        foreground = colors[2],
                        configured_keyboards = ["es", "bd probhat"],
                        update_interval = 1,
                        padding = 10
                       ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.CPU(
                       background = colors[5],
                       foreground = colors[2],
                       padding = 10
                       ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.TextBox(
                       text=" Vol:",
                       foreground=colors[2],
                       background=colors[4],
                       padding = 0
                       ),
               widget.Volume(
                        foreground = colors[2],
                        background = colors[4],
                        padding = 10
                        ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.CurrentLayoutIcon(
                        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                        foreground = colors[0],
                        background = colors[5],
                        padding = 0,
                        scale=0.7
                        ),
               widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[5],
                        padding = 10
                        ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.Clock(
                        foreground = colors[2],
                        background = colors[4],
                        format = "%H:%M:%S %p",
                        padding = 10
                        ),
               widget.Spacer(length = 2, background = colors[0]),
               widget.Clock(
                        foreground = colors[2],
                        background = colors[5],
                        format = "%d %b ,%Y",
                        padding = 10
                        ),
               widget.Systray(
                        background = colors[0],
                        padding = 5
                        ),
              ]
    return widgets_list

##### SCREENS ##### (TRIPLE MONITOR SETUP)

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

##### DRAG FLOATING WINDOWS #####
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

##### FLOATING WINDOWS #####
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

##### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

autostar = [
	"feh --bg-max /home/ezequiel/.config/qtile/fondo.jpg",
	#"compton --config /home/ezequiel/.config/compton/compton.conf &",
        "picom &",
]

for x in autostar:
    os .system(x)

wmname = "LG3D"
