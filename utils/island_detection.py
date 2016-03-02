from tkinter import *
from PIL import Image, ImageTk
from tkinter.scrolledtext import ScrolledText


if __name__ == '__main__':

    root = Tk()
    main_panel = PanedWindow()
    main_panel.pack()

    img = Image.open('/home/adam/Projects/design3/base_station/mock_image.jpg')
    width, height = img.size
    canvas = Canvas(main_panel, width=width, height=height)
    main_panel.add(canvas)
    canvas.image = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=canvas.image, anchor='nw')

    right_panel = PanedWindow(main_panel, orient=VERTICAL)
    main_panel.add(right_panel)

    info = ScrolledText(right_panel)
    info.config(state=DISABLED)
    right_panel.add(info)


    def register(x, y, kind):
        info.config(state=NORMAL)
        info.insert(END, kind +' : ({0},{1})\n'.format(x,y))
        info.config(state=DISABLED)


    def top_left_click(event):
        x,y = event.x, event.y
        register(x,y,'top left')
        canvas.unbind('<Button-1>')

    def bottom_right_click(event):
        x,y = event.x, event.y
        register(x,y,'bottom right')
        canvas.unbind('<Button-1>')

    def top_left_scale_button_callback():
        canvas.bind('<Button-1>', top_left_click)

    def bottom_right_scale_button_callback():
        canvas.bind('<Button-1>', bottom_right_click)



    def triangle_green_click(event):
        x,y = event.x, event.y
        register(x,y,'green triangle')
        canvas.unbind('<Button-1>')


    def triangle_green_button_callback():
        canvas.bind('<Button-1>', triangle_green_click)

    def square_green_click(event):
        x,y = event.x, event.y
        register(x,y,'green square')
        canvas.unbind('<Button-1>')


    def square_green_button_callback():
        canvas.bind('<Button-1>', square_green_click)


    def pentagon_green_click(event):
        x,y = event.x, event.y
        register(x,y,'green pentagon')
        canvas.unbind('<Button-1>')


    def pentagon_green_button_callback():
        canvas.bind('<Button-1>', pentagon_green_click)


    def circle_green_click(event):
        x,y = event.x, event.y
        register(x,y,'green circle')
        canvas.unbind('<Button-1>')


    def circle_green_button_callback():
        canvas.bind('<Button-1>', circle_green_click)


    def triangle_blue_click(event):
        x,y = event.x, event.y
        register(x,y,'blue triangle')
        canvas.unbind('<Button-1>')


    def triangle_blue_button_callback():
        canvas.bind('<Button-1>', triangle_blue_click)

    def square_blue_click(event):
        x,y = event.x, event.y
        register(x,y,'blue square')
        canvas.unbind('<Button-1>')


    def square_blue_button_callback():
        canvas.bind('<Button-1>', square_blue_click)


    def pentagon_blue_click(event):
        x,y = event.x, event.y
        register(x,y,'blue pentagon')
        canvas.unbind('<Button-1>')


    def pentagon_blue_button_callback():
        canvas.bind('<Button-1>', pentagon_blue_click)


    def circle_blue_click(event):
        x,y = event.x, event.y
        register(x,y,'blue circle')
        canvas.unbind('<Button-1>')


    def circle_blue_button_callback():
        canvas.bind('<Button-1>', circle_blue_click)


    def triangle_yellow_click(event):
        x,y = event.x, event.y
        register(x,y,'yellow triangle')
        canvas.unbind('<Button-1>')


    def triangle_yellow_button_callback():
        canvas.bind('<Button-1>', triangle_yellow_click)

    def square_yellow_click(event):
        x,y = event.x, event.y
        register(x,y,'yellow square')
        canvas.unbind('<Button-1>')


    def square_yellow_button_callback():
        canvas.bind('<Button-1>', square_yellow_click)


    def pentagon_yellow_click(event):
        x,y = event.x, event.y
        register(x,y,'yellow pentagon')
        canvas.unbind('<Button-1>')


    def pentagon_yellow_button_callback():
        canvas.bind('<Button-1>', pentagon_yellow_click)


    def circle_yellow_click(event):
        x,y = event.x, event.y
        register(x,y,'yellow circle')
        canvas.unbind('<Button-1>')


    def circle_yellow_button_callback():
        canvas.bind('<Button-1>', circle_yellow_click)


    def triangle_red_click(event):
        x,y = event.x, event.y
        register(x,y,'red triangle')
        canvas.unbind('<Button-1>')


    def triangle_red_button_callback():
        canvas.bind('<Button-1>', triangle_red_click)

    def square_red_click(event):
        x,y = event.x, event.y
        register(x,y,'red square')
        canvas.unbind('<Button-1>')


    def square_red_button_callback():
        canvas.bind('<Button-1>', square_red_click)


    def pentagon_red_click(event):
        x,y = event.x, event.y
        register(x,y,'red pentagon')
        canvas.unbind('<Button-1>')


    def pentagon_red_button_callback():
        canvas.bind('<Button-1>', pentagon_red_click)


    def circle_red_click(event):
        x,y = event.x, event.y
        register(x,y,'red circle')
        canvas.unbind('<Button-1>')


    def circle_red_button_callback():
        canvas.bind('<Button-1>', circle_red_click)



    button_panel = PanedWindow(right_panel, orient=VERTICAL)
    right_panel.add(button_panel)


    top_left_scale_panel = PanedWindow(button_panel)
    button_panel.add(top_left_scale_panel)

    top_left_scale_button = Button(top_left_scale_panel, text='top left', command=top_left_scale_button_callback)
    top_left_scale_panel.add(top_left_scale_button)

    bottom_right_scale_panel = PanedWindow(button_panel)
    button_panel.add(bottom_right_scale_panel)

    bottom_right_scale_button = Button(bottom_right_scale_panel, text='bottom right', command=bottom_right_scale_button_callback)
    bottom_right_scale_panel.add(bottom_right_scale_button)

    islands_panel_button = PanedWindow(right_panel, orient=VERTICAL)
    right_panel.add(islands_panel_button)

    red_islands_panel_button = PanedWindow(islands_panel_button)
    islands_panel_button.add(red_islands_panel_button)

    triangle_red_island_button = Button(red_islands_panel_button, text='t-r', command=triangle_red_button_callback)
    square_red_island_button = Button(red_islands_panel_button, text='s-r', command=square_red_button_callback)
    pentagon_red_island_button = Button(red_islands_panel_button, text='p-r', command=pentagon_red_button_callback)
    circle_red_island_button = Button(red_islands_panel_button, text='c-r', command=circle_red_button_callback)

    red_islands_panel_button.add(triangle_red_island_button)
    red_islands_panel_button.add(square_red_island_button)
    red_islands_panel_button.add(pentagon_red_island_button)
    red_islands_panel_button.add(circle_red_island_button)



    green_islands_panel_button = PanedWindow(islands_panel_button)
    islands_panel_button.add(green_islands_panel_button)

    triangle_green_island_button = Button(green_islands_panel_button, text='t-g', command=triangle_green_button_callback)
    square_green_island_button = Button(green_islands_panel_button, text='s-g', command=square_green_button_callback)
    pentagon_green_island_button = Button(green_islands_panel_button, text='p-g', command=pentagon_green_button_callback)
    circle_green_island_button = Button(green_islands_panel_button, text='c-g', command=circle_green_button_callback)

    green_islands_panel_button.add(triangle_green_island_button)
    green_islands_panel_button.add(square_green_island_button)
    green_islands_panel_button.add(pentagon_green_island_button)
    green_islands_panel_button.add(circle_green_island_button)



    blue_islands_panel_button = PanedWindow(islands_panel_button)
    islands_panel_button.add(blue_islands_panel_button)

    triangle_blue_island_button = Button(blue_islands_panel_button, text='t-b', command=triangle_blue_button_callback)
    square_blue_island_button = Button(blue_islands_panel_button, text='s-b', command=square_blue_button_callback)
    pentagon_blue_island_button = Button(blue_islands_panel_button, text='p-b', command=pentagon_blue_button_callback)
    circle_blue_island_button = Button(blue_islands_panel_button, text='c-b', command=circle_blue_button_callback)

    blue_islands_panel_button.add(triangle_blue_island_button)
    blue_islands_panel_button.add(square_blue_island_button)
    blue_islands_panel_button.add(pentagon_blue_island_button)
    blue_islands_panel_button.add(circle_blue_island_button)


    yellow_islands_panel_button = PanedWindow(islands_panel_button)
    islands_panel_button.add(yellow_islands_panel_button)

    triangle_yellow_island_button = Button(yellow_islands_panel_button, text='t-y', command=triangle_yellow_button_callback)
    square_yellow_island_button = Button(yellow_islands_panel_button, text='s-y', command=square_yellow_button_callback)
    pentagon_yellow_island_button = Button(yellow_islands_panel_button, text='p-y', command=pentagon_yellow_button_callback)
    circle_yellow_island_button = Button(yellow_islands_panel_button, text='c-y', command=circle_yellow_button_callback)

    yellow_islands_panel_button.add(triangle_yellow_island_button)
    yellow_islands_panel_button.add(square_yellow_island_button)
    yellow_islands_panel_button.add(pentagon_yellow_island_button)
    yellow_islands_panel_button.add(circle_yellow_island_button)

    def save_callback():
        print(info.get(1.0, END))

    save_button = Button(right_panel, text='Save', command=save_callback)
    right_panel.add(save_button)
    root.mainloop()

