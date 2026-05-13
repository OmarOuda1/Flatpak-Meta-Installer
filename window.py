import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
import json
import os
from flatpak_manager import FlatpakManager

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Flatpak Meta Installer")
        self.set_default_size(800, 600)
        
        self.flatpak_manager = FlatpakManager(self.on_output, self.on_finished)
        self.section_checks = {} # To keep track of checkboxes
        self.config_data = {}
        
        self._build_ui()
        self._load_config()

    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # HeaderBar
        header = Adw.HeaderBar()
        main_box.append(header)
        
        # Paned for split view
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        paned.set_vexpand(True)
        main_box.append(paned)
        
        # Top: Preferences Page for sections
        self.prefs_page = Adw.PreferencesPage()
        scrolled_prefs = Gtk.ScrolledWindow()
        scrolled_prefs.set_child(self.prefs_page)
        paned.set_start_child(scrolled_prefs)
        
        # Bottom: Terminal and Actions
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        bottom_box.set_margin_top(12)
        bottom_box.set_margin_bottom(12)
        bottom_box.set_margin_start(12)
        bottom_box.set_margin_end(12)
        
        # Actions
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        action_box.set_halign(Gtk.Align.CENTER)
        
        btn_install = Gtk.Button(label="Install Selected")
        btn_install.add_css_class("suggested-action")
        btn_install.connect("clicked", self.on_install_clicked)
        
        btn_update = Gtk.Button(label="Update Selected")
        btn_update.connect("clicked", self.on_update_clicked)
        
        btn_remove = Gtk.Button(label="Remove Selected")
        btn_remove.add_css_class("destructive-action")
        btn_remove.connect("clicked", self.on_remove_clicked)

        btn_update_all = Gtk.Button(label="Update All Flatpaks")
        btn_update_all.connect("clicked", self.on_update_all_clicked)
        
        action_box.append(btn_install)
        action_box.append(btn_update)
        action_box.append(btn_remove)
        action_box.append(btn_update_all)
        bottom_box.append(action_box)
        
        # Terminal TextView
        self.text_buffer = Gtk.TextBuffer()
        self.text_view = Gtk.TextView(buffer=self.text_buffer)
        self.text_view.set_editable(False)
        self.text_view.set_monospace(True)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_left_margin(6)
        self.text_view.set_right_margin(6)
        self.text_view.set_top_margin(6)
        self.text_view.set_bottom_margin(6)
        # Using a card style to make it look nicer
        self.text_view.add_css_class("card")
        
        scrolled_text = Gtk.ScrolledWindow()
        scrolled_text.set_child(self.text_view)
        scrolled_text.set_vexpand(True)
        # Add a border to the scrolled window
        scrolled_text.add_css_class("view")
        bottom_box.append(scrolled_text)
        
        paned.set_end_child(bottom_box)
        paned.set_position(350)

        # Buttons state list to disable during run
        self.action_buttons = [btn_install, btn_update, btn_remove, btn_update_all]

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(config_path, "r") as f:
                self.config_data = json.load(f)
                
            group = Adw.PreferencesGroup(title="Available Sections")
            self.prefs_page.add(group)
            
            for section, apps in self.config_data.items():
                row = Adw.ExpanderRow(title=section, subtitle=f"{len(apps)} applications")
                
                check = Gtk.CheckButton()
                check.set_valign(Gtk.Align.CENTER)
                row.add_prefix(check)
                self.section_checks[section] = check
                
                for app in apps:
                    app_row = Adw.ActionRow(title=app)
                    row.add_row(app_row)
                    
                group.add(row)
                
        except Exception as e:
            self.on_output(f"Error loading config.json: {e}\n")

    def get_selected_apps(self):
        apps = []
        for section, check in self.section_checks.items():
            if check.get_active():
                apps.extend(self.config_data.get(section, []))
        return apps

    def set_buttons_sensitive(self, sensitive):
        for btn in self.action_buttons:
            btn.set_sensitive(sensitive)

    def on_install_clicked(self, btn):
        apps = self.get_selected_apps()
        if apps:
            self.set_buttons_sensitive(False)
            self.text_buffer.set_text("")
            self.flatpak_manager.execute("install", apps)
        else:
            self.on_output("No sections selected for installation.\n")

    def on_update_clicked(self, btn):
        apps = self.get_selected_apps()
        if apps:
            self.set_buttons_sensitive(False)
            self.text_buffer.set_text("")
            self.flatpak_manager.execute("update", apps)
        else:
            self.on_output("No sections selected for update.\n")

    def on_remove_clicked(self, btn):
        apps = self.get_selected_apps()
        if apps:
            self.set_buttons_sensitive(False)
            self.text_buffer.set_text("")
            self.flatpak_manager.execute("uninstall", apps)
        else:
            self.on_output("No sections selected for removal.\n")

    def on_update_all_clicked(self, btn):
        self.set_buttons_sensitive(False)
        self.text_buffer.set_text("")
        self.flatpak_manager.execute("update", [])

    def on_output(self, line):
        end_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert(end_iter, line)
        # Scroll to bottom
        mark = self.text_buffer.create_mark(None, self.text_buffer.get_end_iter(), False)
        self.text_view.scroll_to_mark(mark, 0.0, True, 0.0, 1.0)

    def on_finished(self, returncode):
        self.set_buttons_sensitive(True)
        if returncode == 0:
            self.on_output("\nOperation completed successfully.\n")
        else:
            self.on_output(f"\nOperation failed with return code {returncode}.\n")
