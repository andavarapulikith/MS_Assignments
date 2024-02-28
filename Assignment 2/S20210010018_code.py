import pyglet
from pyglet import shapes as sh
import imageio
import numpy as np

win = pyglet.window.Window(fullscreen=True)
# Title
win.set_caption("Bouncing Ball Animation")  

# Orange border color
border_clr = (255, 165, 0)  
border_w = 15 

def draw_border():
    border_top = sh.Rectangle(0, win.height - border_w, win.width, border_w, color=border_clr)
    border_bottom = sh.Rectangle(0, 0, win.width, border_w, color=border_clr)
    border_left = sh.Rectangle(0, 0, border_w, win.height, color=border_clr)
    border_right = sh.Rectangle(win.width - border_w, 0, border_w, win.height, color=border_clr)
    
    border_top.draw()
    border_bottom.draw()
    border_left.draw()
    border_right.draw()

ball_img = pyglet.image.load('ball2.png')
ball_sprite = pyglet.sprite.Sprite(ball_img)

ball_sprite.x = border_w  
ball_sprite.y = win.height - ball_sprite.height - border_w  
vel_x = 10  
vel_y = -15 

lbl = pyglet.text.Label('Bouncing Ball Animation',
                        font_name='Arial',
                        font_size=36,
                        x=win.width//2, y=win.height - 50,
                        anchor_x='center', anchor_y='center',
                        color=(255,165,0,255))  

def update(dt):
    global vel_x, vel_y
    ball_sprite.x += vel_x
    ball_sprite.y += vel_y
    if ball_sprite.x + ball_sprite.width > win.width - border_w or ball_sprite.x < border_w:
        vel_x *= -1  
        if abs(vel_x) < 1: 
            vel_x = 1 if vel_x > 0 else -1
    if ball_sprite.y + ball_sprite.height > win.height - border_w or ball_sprite.y < border_w:
        vel_y *= -1 
        if abs(vel_y) < 1:  
            vel_y = 1 if vel_y > 0 else -1
    frames.append(pyglet.image.get_buffer_manager().get_color_buffer().get_image_data())

@win.event
def on_draw():
    win.clear()
    draw_border() 
    ball_sprite.draw()
    lbl.draw()  


animation_duration = 10

frames = []

pyglet.clock.schedule_interval(update, 1/120)

pyglet.app.run()


frames_np = [np.frombuffer(frame.get_data(), dtype=np.uint8).reshape(win.height, win.width, 4) for frame in frames]
frames_scaled = [(np.flipud(frame[:, :, :3]) / 255 * 255).astype(np.uint8) for frame in frames_np]


imageio.mimsave('S20210010018_ball_animation.gif', frames_scaled[::-1], fps=60)