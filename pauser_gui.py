import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

import pystray
from PIL import Image, ImageDraw


class PauserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kinect Media Pauser")
        self.root.geometry("450x250")
        self.process = None
        self.running = False
        self.tray_icon = None

        tk.Label(
            root,
            text="Kinect Media Controller",
            font=("Arial", 14, "bold"),
        ).pack(pady=20)

        self.start_btn = tk.Button(
            root,
            text="START",
            command=self.start_pauser,
            bg="green",
            fg="white",
            font=("Arial", 12),
            width=15,
        )
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(
            root,
            text="STOP",
            command=self.stop_pauser,
            bg="red",
            fg="white",
            font=("Arial", 12),
            width=15,
            state=tk.DISABLED,
        )
        self.stop_btn.pack(pady=10)

        self.status = tk.Label(root, text="Status: Stopped", font=("Arial", 10))
        self.status.pack(pady=10)

        threading.Thread(target=self.setup_tray, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_pauser(self):
        if self.running:
            return

        try:
            if getattr(sys, "frozen", False):
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))
            else:
                project_root = os.path.dirname(os.path.abspath(__file__))

            pauser_path = os.path.join(project_root, "pauser.py")
            python_path = os.path.join(project_root, ".venv", "Scripts", "python.exe")
            self.process = subprocess.Popen(
                [python_path, pauser_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status.config(text="Status: Running", fg="green")
        except Exception as error:
            messagebox.showerror("Error", f"Failed to start: {error}")

    def stop_pauser(self):
        if not self.running or not self.process:
            return

        try:
            self.process.terminate()
            self.process.wait(timeout=2)
        except Exception:
            try:
                self.process.kill()
            except Exception:
                pass

        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Status: Stopped", fg="red")

    def on_closing(self):
        self.root.withdraw()

    @staticmethod
    def create_tray_icon():
        image = Image.new("RGB", (64, 64), color=(0, 100, 200))
        ImageDraw.Draw(image).text((15, 20), "KP", fill=(255, 255, 255))
        return image

    def setup_tray(self):
        try:
            menu = pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Exit", self.exit_app),
            )
            self.tray_icon = pystray.Icon(
                "Kinect Pauser", self.create_tray_icon(), menu=menu
            )
            self.tray_icon.run()
        except Exception as error:
            print(f"Tray error: {error}")

    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        self.root.lift()

    def exit_app(self, icon=None, item=None):
        self.stop_pauser()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PauserGUI(root)
    root.mainloop()
