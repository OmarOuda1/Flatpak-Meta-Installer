import subprocess
import threading
from gi.repository import GLib

class FlatpakManager:
    def __init__(self, output_callback, finished_callback):
        """
        output_callback: function taking a string (a line of output)
        finished_callback: function taking an integer (return code)
        """
        self.output_callback = output_callback
        self.finished_callback = finished_callback
        self.process = None
        self._cancel_requested = False

    def _run_command(self, cmd):
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Read output line by line
            for line in self.process.stdout:
                if self._cancel_requested:
                    self.process.terminate()
                    break
                GLib.idle_add(self.output_callback, line)

            self.process.wait()
            returncode = self.process.returncode
        except Exception as e:
            GLib.idle_add(self.output_callback, f"Error starting process: {e}\n")
            returncode = 1

        GLib.idle_add(self.finished_callback, returncode)

    def execute(self, action, app_ids):
        """
        action: 'install', 'update', or 'uninstall'
        app_ids: list of flatpak app IDs
        """
        self._cancel_requested = False

        if not app_ids and action != 'update':
            GLib.idle_add(self.output_callback, "No applications selected.\n")
            GLib.idle_add(self.finished_callback, 0)
            return

        cmd = ["flatpak", action, "--user", "--assumeyes", "--noninteractive"]
        
        # When installing, specify flathub to avoid interactive prompt for remote
        if action == "install":
            cmd.append("flathub")
            
        cmd.extend(app_ids)
        
        GLib.idle_add(self.output_callback, f"Running: {' '.join(cmd)}\n")
        
        thread = threading.Thread(target=self._run_command, args=(cmd,))
        thread.daemon = True
        thread.start()

    def cancel(self):
        self._cancel_requested = True
