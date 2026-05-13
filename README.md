# Flatpak Meta Installer

A GTK4/Libadwaita application for batch installing, updating, and removing Flatpak applications based on a structured configuration file.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![GTK](https://img.shields.io/badge/GTK-4.0-green?logo=gnome&logoColor=white)
![Flatpak](https://img.shields.io/badge/Flatpak-Supported-blue)

## Features

- **Batch Operations** — Install, update, or remove groups of Flatpak applications in one click.
- **Organized Sections** — Applications are grouped into categories (e.g. Development, Gaming, Media) via a simple JSON config.
- **Selective Installation** — Choose which sections to act on using checkboxes; expand each section to review individual apps.
- **Live Output** — A built-in terminal view displays real-time output from Flatpak commands.
- **Update All** — Quickly update every installed Flatpak with a single button.
- **Native Look & Feel** — Built with GTK4 and Libadwaita for a modern GNOME-native experience.

## Screenshots

*Coming soon*

## Prerequisites

- **Python 3.10+**
- **GTK 4.0** and **Libadwaita 1**
- **Flatpak** (with the [Flathub](https://flathub.org/setup) remote configured)
- **PyGObject** (Python GObject Introspection bindings)

## Installation

### 1. Install System Dependencies

#### Debian / Ubuntu / Kali

```bash
sudo apt install python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 flatpak
```

#### Fedora

```bash
sudo dnf install python3 python3-gobject gtk4 libadwaita flatpak
```

#### Arch Linux

```bash
sudo pacman -S python python-gobject gtk4 libadwaita flatpak
```

### 2. Set Up Flathub (if not already configured)

```bash
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

### 3. Clone the Repository

```bash
git clone https://github.com/your-username/flatpak-meta-installer.git
cd flatpak-meta-installer
```

### 4. Run the Application

```bash
python3 main.py
```

No virtual environment or `pip install` is required — all dependencies are system packages.

## Configuration

Applications are defined in `config.json` at the project root. The file uses a simple structure where each key is a section name and its value is a list of Flatpak application IDs:

```json
{
  "Development": [
    "org.gnome.Builder",
    "com.visualstudio.code"
  ],
  "Gaming": [
    "com.valvesoftware.Steam",
    "net.lutris.Lutris"
  ],
  "Media": [
    "org.videolan.VLC",
    "com.spotify.Client"
  ],
  "Communication": [
    "com.discordapp.Discord",
    "org.telegram.desktop"
  ]
}
```

To customize, simply edit `config.json` and add or remove sections and application IDs as needed. You can find application IDs on [Flathub](https://flathub.org) — they are shown on each application's page.

## Usage

1. **Launch** the application with `python3 main.py`.
2. **Select sections** by ticking the checkboxes next to each category. Expand a section to see which apps it contains.
3. **Click an action button**:
   - **Install Selected** — Installs all Flatpaks in the checked sections.
   - **Update Selected** — Updates all Flatpaks in the checked sections.
   - **Remove Selected** — Uninstalls all Flatpaks in the checked sections.
   - **Update All Flatpaks** — Updates every installed Flatpak (ignores selection).
4. **Monitor progress** in the terminal output pane at the bottom of the window.
