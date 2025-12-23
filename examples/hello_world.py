# import pyglet
# from pyglet.gl import *

# window = pyglet.window.Window()

# glEnable(GL_DEPTH_TEST)

# batch = pyglet.graphics.Batch()


# class DepthGroup(pyglet.graphics.Group):
#     def set_state(self):
#         glEnable(GL_DEPTH_TEST)
#         glDepthFunc(GL_LESS)
#         glEnable(GL_BLEND)
#         # glBlendFunc(self.blend_src, self.blend_dest)

#     def unset_state(self):
#         glDisable(GL_DEPTH_TEST)
#         glDisable(GL_BLEND)
# group = DepthGroup()

# label = pyglet.text.Label('Hello, world!',
#                           font_size=36,
#                           x=window.width // 2,
#                           y=window.height // 2,
#                           anchor_x='center',
#                           anchor_y='center',
#                           batch=batch,
#                           group=group,
#                           )
# # label.set_style('background_color', (150, 0, 0, 255))
# label.z = 1.0


# pyglet.resource.path = ['resources']
# pyglet.resource.reindex()
# image = pyglet.resource.image("pyglet.png")
# image.anchor_x = image.width // 2
# image.anchor_y = image.height // 2
# sprite = pyglet.sprite.Sprite(image, x=label.x, y=label.y,
#                               batch=batch,
#                               group=group,
# )
# sprite.opacity = 200
# sprite.z = 2.0  # In front of the label

# sprite1 = pyglet.sprite.Sprite(image, x=label.x, y=label.y-50,
#                               batch=batch,
#                               group=group,
# )
# sprite1.opacity = 200
# sprite1.z = -3.0  # In front of the previous sprite
# # sprite1.z = -2.0  # Below the previous sprite

# @window.event
# def on_draw():
#     window.clear()
#     batch.draw()
#     # label.draw()
#     # sprite.draw()


# pyglet.app.run()


import pyglet
# pyglet.options.debug_graphics_batch = True
from pyglet.gl import *

window = pyglet.window.Window()

glEnable(GL_DEPTH_TEST)

label = pyglet.text.Label('Hello, world!',
                          font_size=36,
                          x=window.width // 2,
                          y=window.height // 2,
                          anchor_x='center',
                          anchor_y='center')
label.set_style('background_color', (150, 0, 0, 255))
label.z = -1.0

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()

