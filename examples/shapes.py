"""
Simple example showing some animated shapes
"""
import math
import pyglet
from pyglet import shapes
from pyglet.gl import glViewport
from pyglet.window import key


class Camera:
    def __init__(self, x=0.0, y=0.0, zoom=1.0):
        self.x = x
        self.y = y
        self.zoom = zoom

class ShapesDemo(pyglet.window.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "Shapes")
        self.time = 0
        self.batch = pyglet.graphics.Batch()

        # Camera controls
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.left_cam = Camera(0, 0, 1.0)
        self.right_cam = Camera(150, -50, 1.0)

        self.circle = shapes.Circle(360, 240, 75, color=(255, 225, 255, 127), batch=self.batch)

        # Rectangle with center as anchor
        self.square = shapes.BorderedRectangle(360, 240, 100, 100, border=5, color=(55, 55, 255),
                                               border_color=(25, 25, 25), batch=self.batch)
        self.square.anchor_position = 50, 50

        # Large transparent rectangle
        self.rectangle = shapes.Rectangle(100, 190, 500, 100, color=(255, 22, 20, 64), batch=self.batch)

        self.line = shapes.Line(0, 0, 0, 480, thickness=4, color=(200, 20, 20), batch=self.batch)

        self.triangle = shapes.Triangle(10, 10, 190, 10, 100, 150, color=(55, 255, 255, 175), batch=self.batch)

        septagon_step = math.pi * 2 / 7
        self.fading_septagon = shapes.Polygon(
            *[[50 + 40 * math.sin(i * septagon_step), 200 + 40 * math.cos(i * septagon_step)] for i in range(7)],
            batch=self.batch,
        )

        self.arc = shapes.Arc(50, 300, radius=40, segments=25, angle=270.0, color=(255, 255, 255), batch=self.batch)

        self.star = shapes.Star(600, 375, 50, 30, 5, color=(255, 255, 0), batch=self.batch)

        self.ellipse = shapes.Ellipse(650, 150, a=50, b=30, color=(55, 255, 55), batch=self.batch)

        self.sector = shapes.Sector(125, 400, 60, angle=0.45 * 360, color=(55, 255, 55), batch=self.batch)

        self.polygon = shapes.Polygon([400, 100], [500, 10], [600, 100], [550, 175], [450, 150], batch=self.batch)

        self.box = shapes.Box(60, 40, 200, 100, thickness=2, color=(244, 55, 55), batch=self.batch)

        coordinates = [[450, 400], [475, 450], [525, 450], [550, 400]]
        self.multiLine = shapes.MultiLine(*coordinates, closed=True, batch=self.batch)
        self.divider = shapes.Line(self.width // 2, 0, self.width // 2, self.height, thickness=2, color=(255, 255, 255))

    def _apply_camera(self, cam):
        """Temporarily apply a camera transform to the window view."""
        orig_view = self.view
        view_matrix = orig_view.translate((-cam.x * cam.zoom, -cam.y * cam.zoom, 0))
        view_matrix = view_matrix.scale((cam.zoom, cam.zoom, 1))
        self.view = view_matrix
        return orig_view

    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        # Use framebuffer size for correct viewport on HiDPI/Retina
        try:
            fb_w, fb_h = self.get_framebuffer_size()
        except AttributeError:
            fb_w, fb_h = self.get_size()

        # Left half (left_cam)
        glViewport(0, 0, fb_w // 2, fb_h)
        orig = self._apply_camera(self.left_cam)
        self.batch.draw()
        self.view = orig  # restore

        # Right half (right_cam)
        glViewport(fb_w // 2, 0, fb_w - fb_w // 2, fb_h)
        orig = self._apply_camera(self.right_cam)
        self.batch.draw()
        self.view = orig  # restore

        # Reset to full window and draw the divider line
        glViewport(0, 0, fb_w, fb_h)
        self.divider.x = self.width // 2
        self.divider.x2 = self.width // 2
        self.divider.y = 0
        self.divider.y2 = self.height
        self.divider.draw()
        FPS.draw()

    def update(self, delta_time):
        """Animate the shapes"""
        self.time += delta_time
        self.square.rotation = self.time * 15
        self.rectangle.y = 200 + math.sin(self.time) * 190
        self.circle.radius = 75 + math.sin(self.time * 1.17) * 25
        self.triangle.rotation = self.time * 15

        self.line.x = 360 + math.sin(self.time * 0.81) * 360
        self.line.x2 = 360 + math.sin(self.time * 1.34) * 360

        self.arc.rotation = self.time * 30

        self.fading_septagon.opacity = int(255 * (0.5 + (0.5 * math.cos(self.time))))

        self.star.rotation = self.time * 50
        self.polygon.rotation = self.time * 45

        self.ellipse.b = abs(math.sin(self.time) * 100)
        self.sector.angle = (self.time * 30) % 360.0

        self.multiLine.rotation = self.time * -15

        self.multiLine.rotation = self.time * -15

        # Camera controls
        speed = 200
        zoom_rate = 1.2  # multiplicative per second

        # Left camera: arrows + Q/E for zoom
        if self.keys[key.LEFT]:
            self.left_cam.x -= speed * delta_time
        if self.keys[key.RIGHT]:
            self.left_cam.x += speed * delta_time
        if self.keys[key.DOWN]:
            self.left_cam.y -= speed * delta_time
        if self.keys[key.UP]:
            self.left_cam.y += speed * delta_time
        if self.keys[key.Q]:
            self.left_cam.zoom *= (zoom_rate ** delta_time)
        if self.keys[key.E]:
            self.left_cam.zoom /= (zoom_rate ** delta_time)
        self.left_cam.zoom = max(0.2, min(4.0, self.left_cam.zoom))

        # Right camera: WASD + U/O for zoom
        if self.keys[key.A]:
            self.right_cam.x -= speed * delta_time
        if self.keys[key.D]:
            self.right_cam.x += speed * delta_time
        if self.keys[key.S]:
            self.right_cam.y -= speed * delta_time
        if self.keys[key.W]:
            self.right_cam.y += speed * delta_time
        if self.keys[key.U]:
            self.right_cam.zoom *= (zoom_rate ** delta_time)
        if self.keys[key.O]:
            self.right_cam.zoom /= (zoom_rate ** delta_time)
        self.right_cam.zoom = max(0.2, min(4.0, self.right_cam.zoom))

if __name__ == "__main__":
    demo = ShapesDemo(720, 480)
    FPS = pyglet.window.FPSDisplay(demo)
    pyglet.clock.schedule_interval(demo.update, 1/30)
    pyglet.app.run()
