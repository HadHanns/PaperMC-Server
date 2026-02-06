import os
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext

def _resolve_server_dir() -> str:
    """Return the directory containing the real PaperMC server files."""
    candidates: list[str | os.PathLike[str] | None] = [
        os.environ.get("PAPERMC_SERVER_DIR"),
        Path.home() / "Documents" / "Server Minecraft",
        Path(__file__).resolve().parent,
    ]

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser().resolve()
        if (path / "start.sh").exists():
            return str(path)
    return str(Path(__file__).resolve().parent)

SERVER_DIR = _resolve_server_dir()
START_SCRIPT = os.path.join(SERVER_DIR, "start.sh")
BACKUP_SCRIPT = os.path.join(SERVER_DIR, "backup.sh")


class ServerGUI:
    """Minecraft-themed desktop UI to manage the PaperMC server."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("⛏ PaperMC Server Control")
        self.root.configure(bg="#8B5A3C")  # Dirt brown background
        self.root.minsize(850, 620)
        self.proc: subprocess.Popen | None = None
        self.output_thread: threading.Thread | None = None
        self.animation_id = None
        self.block_buttons: dict[str, dict] = {}
        self.auto_backup_proc: subprocess.Popen | None = None
        self.auto_backup_thread: threading.Thread | None = None

        self._build_ui()
        self._update_status("Server idle")
        self._start_animations()

    def _build_ui(self):
        # Main container with grass texture
        main_container = tk.Frame(self.root, bg="#7CBD6B", bd=6, relief="ridge")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header dengan ASCII borders dan decorations
        header = tk.Frame(main_container, bg="#2b2b2b", bd=5, relief="ridge")
        header.pack(fill="x", padx=8, pady=8)
        
        # Top border decoration
        top_border = tk.Label(
            header,
            text="╔═══════════════════════════════════════════════════════╗",
            font=("Courier New", 10, "bold"),
            fg="#55ff55",
            bg="#2b2b2b"
        )
        top_border.pack()
        
        # Title with decorations
        title = tk.Label(
            header,
            text="🌿 ⛏ PAPERMC SERVER CONTROL ⛏ 🌿",
            font=("Courier New", 18, "bold"),
            fg="#55ff55",
            bg="#2b2b2b",
            pady=8
        )
        title.pack()
        
        # Subtitle with gems
        subtitle = tk.Label(
            header,
            text="💎 Java Edition + Bedrock Edition Support 💎",
            font=("Courier New", 10),
            fg="#5DADE2",
            bg="#2b2b2b",
            pady=4
        )
        subtitle.pack()
        
        # Bottom border decoration
        bottom_border = tk.Label(
            header,
            text="╚═══════════════════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            fg="#55ff55",
            bg="#2b2b2b"
        )
        bottom_border.pack()

        # Control buttons dengan decorative frame
        btn_container = tk.Frame(main_container, bg="#9C7853", bd=4, relief="ridge")
        btn_container.pack(fill="x", padx=8, pady=8)
        
        # Button border decoration
        btn_top = tk.Label(
            btn_container,
            text="╔═══════════════════════════════════════════════════════╗",
            font=("Courier New", 9, "bold"),
            fg="#FFD700",
            bg="#9C7853"
        )
        btn_top.pack()
        
        btn_frame = tk.Frame(btn_container, bg="#9C7853")
        btn_frame.pack(padx=12, pady=8)
        
        inner_frame = tk.Frame(btn_frame, bg="#9C7853")
        inner_frame.pack()

        # Custom block buttons for better color control
        self.start_btn = self._create_block_button(
            inner_frame,
            key="start",
            text="🌿 ▶ START SERVER 🌿",
            base_color="#1E7F3E",
            hover_color="#2FB356",
            command=self.start_server,
            enabled=True,
        )

        self.stop_btn = self._create_block_button(
            inner_frame,
            key="stop",
            text="🔥 ■ STOP SERVER 🔥",
            base_color="#8B0000",
            hover_color="#C62828",
            command=self.stop_server,
            enabled=False,
        )

        self.auto_backup_btn = self._create_block_button(
            inner_frame,
            key="backup",
            text="⏱ START AUTO BACKUP",
            base_color="#B8860B",
            hover_color="#DAA520",
            command=self.toggle_auto_backup,
            enabled=True,
        )
        
        # Button bottom border
        btn_bottom = tk.Label(
            btn_container,
            text="╚═══════════════════════════════════════════════════════╝",
            font=("Courier New", 9, "bold"),
            fg="#FFD700",
            bg="#9C7853"
        )
        btn_bottom.pack()

        # Status display with visual indicators
        status_container = tk.Frame(main_container, bg="#7F7F7F", bd=4, relief="ridge")
        status_container.pack(fill="x", padx=8, pady=8)
        
        status_frame = tk.Frame(status_container, bg="#7F7F7F")
        status_frame.pack(padx=12, pady=10)
        
        # Status label with hearts
        status_row = tk.Frame(status_frame, bg="#7F7F7F")
        status_row.pack()
        
        tk.Label(
            status_row,
            text="⚡ STATUS:",
            font=("Courier New", 12, "bold"),
            fg="#FFD700",
            bg="#7F7F7F"
        ).pack(side="left", padx=(0, 12))
        
        self.status_var = tk.StringVar(value="Server idle")
        self.status_label = tk.Label(
            status_row,
            textvariable=self.status_var,
            font=("Courier New", 12, "bold"),
            fg="#FFFFFF",
            bg="#555555",
            padx=20,
            pady=6,
            bd=3,
            relief="sunken"
        )
        self.status_label.pack(side="left", padx=(0, 12))
        
        # Hearts indicator
        self.hearts_var = tk.StringVar(value="❤️❤️❤️")
        self.hearts_label = tk.Label(
            status_row,
            textvariable=self.hearts_var,
            font=("Courier New", 14),
            bg="#7F7F7F"
        )
        self.hearts_label.pack(side="left")

        # Console log with decorative borders
        log_container = tk.Frame(main_container, bg="#2b2b2b", bd=5, relief="ridge")
        log_container.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Console top border
        log_top = tk.Label(
            log_container,
            text="╔═══════════════════ SERVER CONSOLE ═══════════════════╗",
            font=("Courier New", 10, "bold"),
            fg="#55ff55",
            bg="#2b2b2b"
        )
        log_top.pack()
        
        # Console header with torch decoration
        log_header = tk.Label(
            log_container,
            text="🔥 Live Output from PaperMC Server 🔥",
            font=("Courier New", 10),
            fg="#FFA500",
            bg="#2b2b2b",
            pady=4
        )
        log_header.pack()

        self.log_box = scrolledtext.ScrolledText(
            log_container,
            height=16,
            state="disabled",
            bg="#0a0a0a",
            fg="#FFFFFF",
            insertbackground="#55ff55",
            font=("Courier New", 10),
            bd=0,
            padx=10,
            pady=10,
            wrap="word"
        )
        self.log_box.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Backup log header & panel
        backup_header = tk.Label(
            log_container,
            text="💾 Backup Log 💾",
            font=("Courier New", 10, "bold"),
            fg="#FFD700",
            bg="#2b2b2b",
            pady=4
        )
        backup_header.pack()

        self.backup_log_box = scrolledtext.ScrolledText(
            log_container,
            height=6,
            state="disabled",
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFD700",
            font=("Courier New", 10),
            bd=0,
            padx=10,
            pady=6,
            wrap="word"
        )
        self.backup_log_box.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        
        # Console bottom border with grass decoration
        log_bottom = tk.Label(
            log_container,
            text="╚═══════════════════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            fg="#55ff55",
            bg="#2b2b2b"
        )
        log_bottom.pack()
        
        # Footer decoration
        footer = tk.Frame(main_container, bg="#7CBD6B")
        footer.pack(fill="x", padx=8, pady=8)
        
        footer_text = tk.Label(
            footer,
            text="🌱🌱 ⚒️ Powered by PaperMC ⚒️ 🌱🌱",
            font=("Courier New", 10, "bold"),
            fg="#2b2b2b",
            bg="#7CBD6B",
            pady=6
        )
        footer_text.pack()

    def _append_log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _append_backup_log(self, text: str):
        self.backup_log_box.configure(state="normal")
        self.backup_log_box.insert("end", text)
        self.backup_log_box.see("end")
        self.backup_log_box.configure(state="disabled")

    def _update_status(self, text: str):
        self.status_var.set(text)
        lowered = text.lower()
        if "running" in lowered or "done" in lowered:
            self.status_label.configure(bg="#50C878", fg="#000000")  # Emerald green
            self.hearts_var.set("❤️❤️❤️")
        elif "starting" in lowered:
            self.status_label.configure(bg="#FFD700", fg="#000000")  # Gold
            self.hearts_var.set("💛💛💛")
        elif "stopping" in lowered:
            self.status_label.configure(bg="#FFA500", fg="#000000")  # Orange
            self.hearts_var.set("🧡🧡🧡")
        elif "error" in lowered or "fail" in lowered:
            self.status_label.configure(bg="#CC0000", fg="#FFFFFF")  # Redstone red
            self.hearts_var.set("💔💔💔")
        else:
            self.status_label.configure(bg="#555555", fg="#FFFFFF")  # Gray (idle)
            self.hearts_var.set("🤍🤍🤍")

    def _create_block_button(self, parent, key, text, base_color, hover_color, command, enabled=True):
        wrapper = tk.Frame(parent, bg="#1f1f1f", bd=3, relief="ridge")
        wrapper.pack(side="left", padx=8)

        block = tk.Frame(
            wrapper,
            bg=base_color,
            bd=0,
            relief="flat",
        )
        block.pack(fill="both", expand=True)

        label = tk.Label(
            block,
            text=text,
            font=("Courier New", 11, "bold"),
            fg="#FFFFFF",
            bg=base_color,
            padx=24,
            pady=10,
        )
        label.pack()

        self.block_buttons[key] = {
            "wrapper": wrapper,
            "block": block,
            "label": label,
            "base": base_color,
            "hover": hover_color,
            "enabled": enabled,
            "command": command,
        }

        for widget in (block, label):
            widget.bind("<Enter>", lambda e, k=key: self._on_block_hover(k, True))
            widget.bind("<Leave>", lambda e, k=key: self._on_block_hover(k, False))
            widget.bind("<Button-1>", lambda e, k=key: self._handle_block_button_click(k))

        if not enabled:
            self._set_block_button_enabled(key, False)

        return label

    def _handle_block_button_click(self, key):
        data = self.block_buttons.get(key)
        if not data or not data["enabled"]:
            return
        data["command"]()

    def _on_block_hover(self, key, entering):
        data = self.block_buttons.get(key)
        if not data or not data["enabled"]:
            return
        color = data["hover"] if entering else data["base"]
        data["block"].configure(bg=color)
        data["label"].configure(bg=color)

    def _set_block_button_enabled(self, key, enabled):
        data = self.block_buttons.get(key)
        if not data:
            return
        data["enabled"] = enabled
        block = data["block"]
        label = data["label"]
        if enabled:
            block.configure(bg=data["base"])
            label.configure(bg=data["base"], fg="#FFFFFF")
        else:
            block.configure(bg="#3b3b3b")
            label.configure(bg="#555555", fg="#9e9e9e")

    def _set_block_button_text(self, key, text):
        data = self.block_buttons.get(key)
        if data:
            data["label"].configure(text=text)

    def _start_animations(self):
        """Start subtle animations for visual feedback"""
        self._animate_hearts()
    
    def _animate_hearts(self):
        """Subtle pulse animation for hearts when server is running"""
        if self.proc and self.proc.poll() is None:
            current = self.hearts_var.get()
            if current == "❤️❤️❤️":
                self.hearts_var.set("❤️ ❤️ ❤️")
            else:
                self.hearts_var.set("❤️❤️❤️")
        self.animation_id = self.root.after(1000, self._animate_hearts)

    def start_server(self):
        if self.proc and self.proc.poll() is None:
            messagebox.showinfo("Server", "Server is already running.")
            return

        if not os.path.isfile(START_SCRIPT):
            messagebox.showerror("Error", "start.sh not found.")
            return

        self._append_log("\n=== Starting server ===\n")
        try:
            self.proc = subprocess.Popen(
                ["/bin/bash", "-lc", "./start.sh"],
                cwd=SERVER_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            messagebox.showerror("Error", f"Failed to start server: {exc}")
            return

        self._set_block_button_enabled("start", False)
        self._set_block_button_enabled("stop", True)
        self._update_status("Server starting...")

        self.output_thread = threading.Thread(target=self._stream_output, daemon=True)
        self.output_thread.start()
        self.root.after(1000, self._poll_process)

    def _stream_output(self):
        assert self.proc and self.proc.stdout is not None
        for line in self.proc.stdout:
            self._append_log(line)

    def _poll_process(self):
        if self.proc and self.proc.poll() is None:
            self.root.after(1000, self._poll_process)
            return

        if self.proc:
            self._append_log("\n=== Server exited ===\n")
        self.proc = None
        self._set_block_button_enabled("start", True)
        self._set_block_button_enabled("stop", False)
        self._update_status("Server idle")

    def stop_server(self):
        if not self.proc:
            messagebox.showinfo("Server", "Server is not running.")
            return

        if self.proc.stdin:
            try:
                self.proc.stdin.write("stop\n")
                self.proc.stdin.flush()
                self._append_log("\n=== Sent stop command ===\n")
            except BrokenPipeError:
                self._append_log("\n=== Unable to send stop command ===\n")
        self._update_status("Stopping server...")

    def toggle_auto_backup(self):
        script_path = os.path.join(SERVER_DIR, "auto_backup.sh")
        if self.auto_backup_proc and self.auto_backup_proc.poll() is None:
            self._append_backup_log("\n=== Stopping auto backup ===\n")
            self.auto_backup_proc.terminate()
            return

        if not os.path.isfile(script_path):
            messagebox.showerror("Error", "auto_backup.sh not found.")
            return

        self._append_backup_log("\n=== Starting auto backup (every 60 minutes) ===\n")
        try:
            self.auto_backup_proc = subprocess.Popen(
                ["/bin/bash", "-lc", "./auto_backup.sh 60"],
                cwd=SERVER_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        except FileNotFoundError as exc:
            self.auto_backup_proc = None
            messagebox.showerror("Error", f"Failed to start auto backup: {exc}")
            return

        self._set_block_button_text("backup", "⏹ STOP AUTO BACKUP")
        threading.Thread(target=self._stream_auto_backup_output, daemon=True).start()
        self._poll_auto_backup()

    def _stream_auto_backup_output(self):
        assert self.auto_backup_proc and self.auto_backup_proc.stdout is not None
        for line in self.auto_backup_proc.stdout:
            self._append_backup_log(line)
        self.root.after(0, self._auto_backup_finished)

    def _poll_auto_backup(self):
        if self.auto_backup_proc and self.auto_backup_proc.poll() is None:
            self.root.after(1000, self._poll_auto_backup)
        elif self.auto_backup_proc:
            self._auto_backup_finished()

    def _auto_backup_finished(self):
        if not self.auto_backup_proc:
            return
        code = self.auto_backup_proc.poll()
        self.auto_backup_proc = None
        self._set_block_button_text("backup", "⏱ START AUTO BACKUP")
        if code == 0:
            self._append_backup_log("\n=== Auto backup stopped ===\n")
        else:
            self._append_backup_log(f"\n=== Auto backup exited with code {code} ===\n")


def main():
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
