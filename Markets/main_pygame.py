import pygame as pg
import sys
import win32api
import win32con
import win32gui
from app_settings import HEIGHT, WIDTH, BGCOLOR, FPS, BLACK

class AppGetInfo:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((HEIGHT, WIDTH))
        self.clock = pg.time.Clock()
        # Set window transparency color
        hwnd = pg.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*BGCOLOR), 100, win32con.LWA_COLORKEY)

    def run(self):
        self.running = True

        while self.running:
            self.dt = self.clock.tick(FPS) / 100
            self.events()
            self.update()
            self.draw()
        
        self.quit()
    
    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        pg.display.set_caption("Get Info App")
        self.screen.fill(BGCOLOR)
        pg.display.flip()
    
if __name__ == "__main__":
    app = AppGetInfo()
    app.run()