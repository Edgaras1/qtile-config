from typing import List  # noqa: F401
import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal


mod = "mod4"    
terminal = "alacritty"#guess_terminal()

keys = [
    Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('term')),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),

    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),
    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    Key([mod], "h", lazy.layout.grow(), lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'),
    Key([mod], "l", lazy.layout.shrink(), lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'),


    Key([mod, "shift"], "m",lazy.window.toggle_fullscreen(),
        desc='Toggle fullscreen'
    ),

    Key([mod, "shift"], "space",lazy.layout.rotate(),lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'),

    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

#===== Workspaces config =====

group_names = [("WWW", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),]

groups = [ Group(name, **kwargs) for name, kwargs in group_names ]
for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

groups.append( ScratchPad("scratchpad", [DropDown("term", terminal, opacity=0.9)]))

#==== Layouts =====
layout_theme = {
    "border_width": 2,
    "margin": 0, #gaps
    "border_focus": "668bd7",
    "border_normal": "1D2330"
}

layouts = [
    layout.Max(),
    layout.MonadTall(**layout_theme),
    layout.Floating(),
    layout.Tile(),
    layout.TreeTab(
        font = "Ubuntu",
        fontsize = 10,
        sections = ["FIRST", "SECOND"],
        section_fontsize = 11,
        bg_color = "141414",
        active_bg = "90C435",
        active_fg = "000000",
        inactive_bg = "384323",
        inactive_fg = "a0a0a0",
        padding_y = 5,
        section_top = 10,
        panel_width = 320
    )
]

#===== Bar config =====

colors = [["#282c34", "#282c34"], # panel background
          ["#434758", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#8d62a9", "#8d62a9"], # border line color for other tab and odd widgets
          ["#668bd7", "#668bd7"], # color for the even widgets
          ["#e1acff", "#e1acff"]] # window name

widget_defaults = dict(
    font='Ubuntu Mono',
    fontsize=12,
    padding=2,

)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                # widget.Image(
                #     filename = "~/.config/qtile/icons/icon.png",
                #     mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('dmenu_run')}
                # ),
                widget.GroupBox( font = "Ubuntu Bold",
                    disable_drag = True,
                    fontsize = 9,
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[2],
                    inactive = colors[2],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "block",
                    this_current_screen_border = colors[1],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[0],
                    other_screen_border = colors[0],
                ),
                widget.Prompt(
                    font = "Ubuntu Mono",
                    padding = 10,
                    foreground = colors[3],
                    background = colors[1]
                ),
                widget.Sep(linewidth = 0,padding = 40),
                # widget.WindowName(
                #     foreground = colors[6],
                #     background = colors[0],
                #     padding = 0
                # ),
                widget.Spacer(),
                widget.KeyboardLayout(),
                widget.Systray(padding = 5),
                widget.Clock(format = "%H:%M"),
                # widget.Sep(linewidth = 0, padding = 10),

                # widget.Volume(
                #     foreground = colors[2],
                #     background = colors[5],
                #     padding = 5
                # ),
                widget.CurrentLayoutIcon(
                    custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                    padding = 0,
                    scale = 0.7
                ),
            ],
            24,
            background = colors[0]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
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

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
