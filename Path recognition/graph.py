# img_viewer.py

import PySimpleGUI as sg
from pdi import prj
from PIL import Image
import PIL
#--------------------------------------------------------------------------
 #--6. Seccion grafica-----------------------------------------------
#--------------------------------------------------------------------------
# First the window layout 
def resize(name1,name2):
    base_width = 360
    image = Image.open(name1)
    width_percent = (base_width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(width_percent)))
    image = image.resize((base_width, hsize), PIL.Image.ANTIALIAS)
    image.save(name2)
    

file= 'rturn.mp4'
right_click_menu = ['Unused', ['&Recta',  '&Cruce', '&giro']]
file_list_column = [
    [
        sg.Text("Archivo a usar"),#Texto
    ],
    [
        sg.Button("OK"),
    ],
    [sg.ButtonMenu('opciones',  right_click_menu, key='-BMENU-')],

]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(size=(100, 100),key="-IMAGE-")],
    [sg.Text("Rutas")],
    [sg.Text(size=(40, 1), key="-TOUT2-")],
    [sg.Image(size=(100, 100),key="-IMAGE2-")],
    
]
image_viewer_column2 = [

]

# ----- Full layout -----
layout = [
    [
         
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.Column(image_viewer_column2),


    ]
]

window = sg.Window("Proyecto", layout,margins=(200, 100))
# Run the Event Loop
while True:
    event, values = window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    if event == "OK":
        prj(file)
        resize('first.png','first_r.png')
        resize('output.png', 'output_r.png')
        window["-TOUT-"].update('original')
        window["-IMAGE-"].update('first_r.png')
        window["-IMAGE2-"].update('output_r.png')
    if values["-BMENU-"] == 'Recta':
        file= 'recta.mp4'
    if values["-BMENU-"] == 'Cruce':
        file= 'many1.mp4'
    if values["-BMENU-"] == 'giro':
        file= 'rturn.mp4'
window.close()


