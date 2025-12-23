import pyglet

# Show pyglet version information
print('Pyglet version:', pyglet.version)

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world!',
                          font_size=36,
                          x=window.width // 2,
                          y=window.height // 2,
                          anchor_x='center',
                          anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.F11:
        # Prefer native macOS fullscreen; if unavailable or unstable,
        # fall back to a borderless fake fullscreen.
        def _toggle(dt):
            if hasattr(window, 'toggle_native_fullscreen'):
                try:
                    window.toggle_native_fullscreen()
                    return
                except Exception:
                    pass

            # Fake fullscreen fallback: cover the screen without capture
            display = pyglet.display.get_display()
            screen = display.get_default_screen()
            if not getattr(window, '_fake_fullscreen', False):
                window._windowed_size = (window.width, window.height)
                window._windowed_location = window.get_location()
                window.set_exclusive_keyboard(True)
                window.set_size(screen.width, screen.height)
                window.set_location(screen.x, screen.y)
                window._fake_fullscreen = True
            else:
                window.set_exclusive_keyboard(False)
                if getattr(window, '_windowed_size', None):
                    window.set_size(*window._windowed_size)
                if getattr(window, '_windowed_location', None):
                    window.set_location(*window._windowed_location)
                window._fake_fullscreen = False
        pyglet.clock.schedule_once(_toggle, 0)


pyglet.app.run()
