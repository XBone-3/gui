import PySimpleGUI as sg

sg.theme("Dark")

layout = [
    [sg.Text("first line of text")],
    [sg.Text("second line of text"), sg.InputText()],
    [sg.Button('OK'), sg.Button('Cancel')]
]

window = sg.Window(title="Hello pySimpleGUI", layout=layout)

while True:
    event, values = window.read()
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break
    print(f'You entered {values[0]}')

window.close()

