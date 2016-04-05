from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

import cv2
from PIL import Image, ImageTk

from vision_utils.camera_service import CameraService

if __name__ == '__main__':

    root = Tk()
    main_panel = PanedWindow()
    main_panel.pack()
    open_cv_camera = cv2.VideoCapture(0)
    open_cv_camera.set(3, 1600)
    open_cv_camera.set(4, 1200)
    camera = CameraService(open_cv_camera,cv2)
    assert(open_cv_camera.isOpened())

    img = Image.open('test_with_islands.jpg')
    width, height = img.size
    left_panel = PanedWindow(main_panel, orient=VERTICAL)
    main_panel.add(left_panel)
    canvas = Canvas(left_panel, width=width, height=height)
    left_panel.add(canvas)
    canvas.image = ImageTk.PhotoImage(img)
    canvas.create_image(0,0,image=canvas.image, anchor='nw')

    right_panel = PanedWindow(main_panel, orient=VERTICAL)
    main_panel.add(right_panel)

    info = ScrolledText(right_panel)
    info.config(state=DISABLED)
    right_panel.add(info)

    def picture_callback():
        global img, config
        img = camera.get_frame()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_rgb)
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(0,0,image=canvas.image, anchor='nw')
        config = ConfigParser()
        config['map'] = {}
        show_map()


    picture_button = Button(left_panel, text='Take a photo!', command=picture_callback)
    left_panel.add(picture_button)

    class FilePanel:
        def __init__(self, panel):
            self.panel = panel

        def write(self, string):
            self.panel.config(state=NORMAL)
            self.panel.insert(END, string)
            self.panel.config(state=DISABLED)

        def reset(self):
            self.panel.config(state=NORMAL)
            self.panel.delete(1.0, END)
            self.panel.config(state=DISABLED)

    filepanel = FilePanel(info)
    config = ConfigParser()
    config['map'] = {}
    kindclicked = None

    def kind_click(event):
        x,y = event.x, event.y
        global kindclicked
        register(x,y, kindclicked)
        canvas.unbind('<Button-1>')

    def button_clicked(kind):
        global kindclicked
        kindclicked = kind
        canvas.bind('<Button-1>', kind_click)

    def show_map():
        filepanel.reset()
        config.write(filepanel)

    def register(x, y, kind):
        config['map'][kind] = '({0},{1})'.format(x,y)
        show_map()

    def top_left_scale_button_callback():
        button_clicked('top left')

    def bottom_right_scale_button_callback():
        button_clicked('bottom right')

    def triangle_green_button_callback():
        button_clicked('green triangle')

    def square_green_button_callback():
        button_clicked('green square')

    def pentagon_green_button_callback():
        button_clicked('green pentagon')

    def circle_green_button_callback():
        button_clicked('green circle')

    def triangle_blue_button_callback():
        button_clicked('blue triangle')

    def square_blue_button_callback():
        button_clicked('blue square')

    def pentagon_blue_button_callback():
        button_clicked('blue pentagon')

    def circle_blue_button_callback():
        button_clicked('blue circle')

    def triangle_yellow_button_callback():
        button_clicked('yellow triangle')

    def square_yellow_button_callback():
        button_clicked('yellow square')

    def pentagon_yellow_button_callback():
        button_clicked('yellow pentagon')

    def circle_yellow_button_callback():
        button_clicked('yellow circle')

    def triangle_red_button_callback():
        button_clicked('red triangle')

    def square_red_button_callback():
        button_clicked('red square')

    def pentagon_red_button_callback():
        button_clicked('red pentagon')

    def circle_red_button_callback():
        button_clicked('red circle')

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
        global img
        filename = filedialog.asksaveasfilename()
        with open(filename + '.txt', 'w') as file_txt:
            config.write(file_txt)
            file_txt.close()
        cv2.imwrite( filename + '.jpg', img)


    def remove_callback():
        global kindclicked
        if(kindclicked is not None):
            config.remove_option('map', kindclicked)
        show_map()

    remove_button = Button(right_panel, text='Remove', command=remove_callback)
    right_panel.add(remove_button)
    save_button = Button(right_panel, text='Save', command=save_callback)

    right_panel.add(save_button)
    show_map()
    root.mainloop()

