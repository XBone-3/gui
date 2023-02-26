import PySimpleGUI as sg
import numpy as np
import cv2


def main():
    sg.theme("lightgreen")

    layouts = [
        [sg.Text("Computer Vision openCV", justification='center', size=(60, 1))],
        [sg.Image(filename='', key='-IMAGE-')],
        [sg.Radio("None", 'Radio', size=(10, 1))],
        [
            sg.Radio("Threshold", "Radio", size=(10, 1), key='-THRESH-'),
            sg.Slider(
                range=(0, 255),
                default_value=128,
                resolution=1,
                orientation='h',
                size=(40, 15),
                key='-THRESH SLIDER-'
            ),
        ],
        [
            sg.Radio('canny', "Radio", size=(10, 1), key='-CANNY-'),
            sg.Slider(range=(0, 255),
                      default_value=128,
                      resolution=1,
                      size=(20, 15),
                      orientation='h',
                      key='-CANNY SLIDER-A-',
                      ),
            sg.Slider(range=(0, 255),
                      default_value=128,
                      resolution=1,
                      orientation='h',
                      size=(20, 15),
                      key='-CANNY SLIDER B-',
                      ),
        ],
        [
            sg.Radio('blur', "Radio", size=(10, 1), key="-BLUR-"),
            sg.Slider(range=(0, 255),
                      default_value=128,
                      resolution=1,
                      size=(20, 15),
                      orientation='h',
                      key='-BLUR SLIDER-')
        ],
        [
            sg.Radio('hue', "Radio", size=(10, 1), key="-HUE-"),
            sg.Slider(range=(0, 255),
                      default_value=128,
                      resolution=1,
                      size=(20, 15),
                      orientation='h',
                      key='-HUE SLIDER-')
        ],
        [
            sg.Radio('enhance', "Radio", size=(10, 1), key="-ENHANCE-"),
            sg.Slider(range=(0, 255),
                      default_value=128,
                      resolution=1,
                      size=(20, 15),
                      orientation='h',
                      key='-ENHANCE SLIDER-')
        ],
        [sg.Button('Exit', size=(10, 1))]
    ]

    window = sg.Window('Computer Vision OpenCV',
                       layout=layouts, location=(800, 200))

    cap = cv2.VideoCapture(0)

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        ret, frame = cap.read()
        if values["-THRESH-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            frame = cv2.threshold(
                frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY
            )[1]
        elif values["-CANNY-"]:
            frame = cv2.Canny(
                frame, values["-CANNY SLIDER-A-"], values["-CANNY SLIDER B-"]
            )
        elif values["-BLUR-"]:
            frame = cv2.GaussianBlur(frame, (21, 21), values["-BLUR SLIDER-"])
        elif values["-HUE-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += int(values["-HUE SLIDER-"])
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        elif values["-ENHANCE-"]:
            enh_val = values["-ENHANCE SLIDER-"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()


if __name__ == '__main__':
    main()
