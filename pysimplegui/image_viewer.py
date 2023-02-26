import PySimpleGUI as sg
from PIL import Image
import os
import shutil

sg.theme("DarkAmber")
size = (400, 300)

file_list_column=[
    [
    sg.Text('Image Folder'),
    sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
    sg.FolderBrowse(button_text="Browse")
    ],
    [
    sg.Listbox(values=[], enable_events=True, size=(45, 20), key="-FILE LIST-")
    ]
]
image_viewer_column = [
    [sg.Text(text="choose an image on the left list", justification="top")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")]
]
layout = [
    [
    sg.Column(file_list_column),
    sg.VSeparator(),
    sg.Column(image_viewer_column, element_justification="center")
    ]
]

window = sg.Window("Image Viewer", layout)
try:
    if "temp" not in os.listdir(os.curdir):
        os.mkdir('temp')
except OSError:
    pass

while True:
    event, values = window.read()
    if event == "-FOLDER-":
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)
        except OSError:
            file_list = []
        filenames = [
            f 
            for f in file_list 
            if os.path.isfile(os.path.join(folder, f)) 
            and f.lower().endswith((".png", '.jpg', '.jpeg', '.gif'))
        ]
        window['-FILE LIST-'].update(filenames)
    elif event == '-FILE LIST-':
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            with Image.open(filename) as image:
                image.thumbnail(size=size)
                image.save("./temp/temp_img.png")
            window['-IMAGE-'].update(filename="./temp/temp_img.png")
        except:
            window['-TOUT-'].Update('FILE CANT BE OPENEND OR EXISTS')
    if event == sg.WIN_CLOSED or event == 'Exit':
        try:
            shutil.rmtree('temp')
        except OSError:
            pass
        break

window.close()