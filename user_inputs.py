import pyxel

class UserInputs:
    def __init__(self, app) -> None:
        self.APP = app

    def user_inputs(self) -> None:
        """
        Listen to user inputs
        """
        # Time controls
        if pyxel.btnr(pyxel.KEY_SPACE) and self.time_speed != 0:
            self.APP.time_speed_previous = self.APP.time_speed
            self.APP.frame_per_frame_previous = self.APP.frame_per_frame
            self.time_speed = 0
            self.frame_per_frame = 9999999
        elif pyxel.btnr(pyxel.KEY_SPACE):
            self.time_speed = self.time_speed_previous
            self.frame_per_frame = self.frame_per_frame_previous

        elif pyxel.btn(pyxel.KEY_1):
            self.time_speed = 0.1
            self.frame_per_frame = 1
        elif pyxel.btn(pyxel.KEY_2):
            self.time_speed = 0.5
            self.frame_per_frame = 2
        elif pyxel.btn(pyxel.KEY_3):
            self.time_speed = 1
            self.frame_per_frame = 5
        elif pyxel.btn(pyxel.KEY_4):
            self.time_speed = 2
            self.frame_per_frame = 10
        elif pyxel.btn(pyxel.KEY_5):
            self.time_speed = 4
            self.frame_per_frame = 20
        elif pyxel.btn(pyxel.KEY_6):
            self.time_speed = 10
            self.frame_per_frame = self.fps

        # Zoom
        if pyxel.btn(pyxel.KEY_PAGEUP) and self.zoom > 0.0:
            self.zoom -= 0.05 * self.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_PAGEDOWN) and self.zoom < 15.0:
            self.zoom += 0.05 / self.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_HOME):
            self.zoom = 1
            self.camera.x = 0
            self.camera.y = 0
            pyxel.camera()

        # Camera position
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.x -= int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.x += int(10 / self.zoom)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.y += int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_UP):
            self.camera.y -= int(10 / self.zoom)

        # Grid
        if pyxel.btnr(pyxel.KEY_G):
            self.draw_grid = not self.draw_grid
        