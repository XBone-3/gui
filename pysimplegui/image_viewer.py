import PySimpleGUI as sg
import os

sg.theme("DarkAmber")

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
    [sg.Text("choose an image on the left list")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")]
]
layout = [
    [
    sg.Column(file_list_column),
    sg.VSeparator(),
    sg.Column(image_viewer_column)
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "-FOLDER-":
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)
        except:
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
            window['-IMAGE-'].update(filename=filename)
        except:
            window['-TOUT-'].Update('FILE CANT BE OPENEND OR EXISTS')
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()