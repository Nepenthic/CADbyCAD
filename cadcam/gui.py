import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

from .model import Profile, Extrusion, Revolution
from .cam import generate_gcode


class MainWindow(tk.Tk):
    """Minimal graphical interface for CADbyCAD."""

    def __init__(self) -> None:
        super().__init__()
        self.title("CADbyCAD")
        self.profile: Profile | None = None

        self._create_menu()
        self._create_toolbar()
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", lambda e: self._draw_profile())

    # --- UI setup helpers -------------------------------------------------
    def _create_menu(self) -> None:
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_profile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def _create_toolbar(self) -> None:
        bar = tk.Frame(self, bd=1, relief=tk.RAISED)
        tk.Button(bar, text="G-code", command=self.generate_gcode).pack(side=tk.LEFT)
        tk.Button(bar, text="Extrude", command=self.extrude).pack(side=tk.LEFT)
        tk.Button(bar, text="Revolve", command=self.revolve).pack(side=tk.LEFT)
        tk.Button(bar, text="Transform", command=self.transform).pack(side=tk.LEFT)
        bar.pack(side=tk.TOP, fill=tk.X)

    # --- File handling ----------------------------------------------------
    def open_profile(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            self.profile = Profile.from_csv(path)
            self.title(f"CADbyCAD - {path}")
            self._draw_profile()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    # --- Drawing ----------------------------------------------------------
    def _draw_profile(self) -> None:
        self.canvas.delete("all")
        if not self.profile:
            return
        pts = self.profile.points
        if not pts:
            return
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x or 1.0
        height = max_y - min_y or 1.0
        pad = 20
        cw = max(1, self.canvas.winfo_width() - 2 * pad)
        ch = max(1, self.canvas.winfo_height() - 2 * pad)
        def tr(x: float, y: float) -> tuple[float, float]:
            sx = pad + (x - min_x) / width * cw
            sy = pad + (max_y - y) / height * ch
            return sx, sy
        for i in range(len(pts)):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % len(pts)]
            sx1, sy1 = tr(x1, y1)
            sx2, sy2 = tr(x2, y2)
            self.canvas.create_line(sx1, sy1, sx2, sy2)

    # --- Actions ----------------------------------------------------------
    def generate_gcode(self) -> None:
        if not self.profile:
            messagebox.showinfo("Info", "Load a profile first")
            return
        depth = simpledialog.askfloat("Cut depth", "Depth:", initialvalue=1.0)
        feed = simpledialog.askfloat("Feedrate", "Feedrate:", initialvalue=1000.0)
        passes = simpledialog.askinteger("Passes", "Depth passes:", initialvalue=1)
        if None in (depth, feed, passes):
            return
        code = generate_gcode(self.profile, depth=depth, feedrate=feed, passes=passes)
        path = filedialog.asksaveasfilename(defaultextension=".gcode")
        if path:
            with open(path, "w") as f:
                f.write(code)
            messagebox.showinfo("Saved", f"G-code written to {path}")

    def extrude(self) -> None:
        if not self.profile:
            messagebox.showinfo("Info", "Load a profile first")
            return
        height = simpledialog.askfloat("Extrusion height", "Height:", initialvalue=1.0)
        if height is None:
            return
        stl = Extrusion(self.profile, height).to_stl()
        path = filedialog.asksaveasfilename(defaultextension=".stl")
        if path:
            with open(path, "w") as f:
                f.write(stl)
            messagebox.showinfo("Saved", f"STL written to {path}")

    def revolve(self) -> None:
        if not self.profile:
            messagebox.showinfo("Info", "Load a profile first")
            return
        seg = simpledialog.askinteger("Segments", "Revolution segments:", initialvalue=36)
        if seg is None:
            return
        stl = Revolution(self.profile, segments=seg).to_stl()
        path = filedialog.asksaveasfilename(defaultextension=".stl")
        if path:
            with open(path, "w") as f:
                f.write(stl)
            messagebox.showinfo("Saved", f"STL written to {path}")

    def transform(self) -> None:
        if not self.profile:
            messagebox.showinfo("Info", "Load a profile first")
            return
        dx = simpledialog.askfloat("Translate X", "DX:", initialvalue=0.0)
        dy = simpledialog.askfloat("Translate Y", "DY:", initialvalue=0.0)
        sx = simpledialog.askfloat("Scale X", "SX:", initialvalue=1.0)
        sy = simpledialog.askfloat("Scale Y", "SY:", initialvalue=1.0)
        ang = simpledialog.askfloat("Rotate", "Angle (deg):", initialvalue=0.0)
        if None in (dx, dy, sx, sy, ang):
            return
        self.profile = (self.profile
                        .translated(dx, dy)
                        .scaled(sx, sy)
                        .rotated(ang))
        self._draw_profile()


def run() -> None:
    MainWindow().mainloop()
