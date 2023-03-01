import os
import PySimpleGUI as sg
from pygame import mixer, error
import time

music_dict = {}
music_files = []
play_music = 'Player must be playing a music'
file_list = '-FILE_LIST-'
pause = '-PAUSE-'

def music_list(folder_path):
    items = os.listdir(folder_path)
    if folder_path not in music_dict.keys():
        music_dict[folder_path] = []
    for item in items:
        if os.path.isdir(os.path.join(folder_path, item)):
            music_list(os.path.join(folder_path, item))
        elif item.lower().endswith(('.mp3')):
            music_files.append(item)
            music_dict[folder_path].append(item)


def layouts():
    file_list_column = [
        [
            sg.Text('Folder', auto_size_text=True),
            sg.In(key='-PATH-', enable_events=True, size=(25, 1)),
            sg.FolderBrowse(button_text='Browse', auto_size_button=True)
        ],
        [sg.Listbox(values=[], enable_events=True,
                    size=(40, 20), key='-FILE_LIST-')]
    ]
    music_player_column = [
        [sg.Text('Choose a song from the list to play or press start to start a random song',
                 justification='center', auto_size_text=True)],
        [sg.Text('', size=(20, 2), auto_size_text=True,
                 justification='center', key='-TOUT-')],
        [
            sg.VSeparator(),
            sg.ProgressBar(max_value=1000,
                           size=(20, 10),
                           orientation='h',
                           key='progressbar'
                           ),
            sg.VSeparator()
        ],
        [sg.HSeparator(pad=10)],
        [
            sg.Button(button_text='Pause', auto_size_button=True,
                      key='-PAUSE-', enable_events=True),
            sg.Button(button_text='Stop', auto_size_button=True,
                      enable_events=True, key='-STOP-'),
            sg.Button(button_text='Restart', auto_size_button=True,
                      enable_events=True, key='-RESTART-'),
        ],
        [
            sg.Radio(text='Repeat', key='repeat', group_id='Radio', enable_events=True),
            sg.Slider(range=(0, 10), default_value=5, resolution=1, enable_events=True, orientation='h', key='volume'),
            sg.Radio(text="Shuffle", key='shuffle',group_id='shufle', enable_events=True)
        ]

    ]
    layout = [
        [
            sg.Text(text='Search: '),
            sg.In(size=(50, 1), justification='center', key='search', enable_events=True)
        ],
        [
            sg.Column(file_list_column, element_justification='center'),
            sg.VSeparator(),
            sg.Column(music_player_column, element_justification='center')
        ],
        [sg.Button(button_text='Exit', button_color='blue')]
    ]
    return layout

def load_files(window, event, values):
    if event == '-PATH-':
        folder_path = values['-PATH-']
        music_list(folder_path)
        window[file_list].update(music_files)
        window['-TOUT-'].update(f'{len(music_files)} songs found')


def player_loop(window):
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        load_files(window, event, values)

        progress_bar = window['progressbar']

        if event == file_list:
            song = values[file_list][0]
            window['-TOUT-'].update(song)
            song_details = [(key, song) for key, value in music_dict.items() if song in value]
            mixer.music.load(os.path.join(
                song_details[0][0], song_details[0][1]))
            mixer.music.play()
            song_length = mixer.Sound(os.path.join(
                song_details[0][0], song_details[0][1])).get_length()
            progress_bar.update(0, int(song_length))
            play = True
            i = 0
        
        if event == pause:
            try:
                if play:
                    mixer.music.pause()
                    window[pause].update('Play')
                    play = False
                else:
                    mixer.music.unpause()
                    window[pause].update('Pause')
                    play = True
            except UnboundLocalError:
                window['-TOUT-'].update(play_music)

        if event == '-STOP-':
            try:
                progress_bar.UpdateBar(0)
                mixer.music.stop()
            except UnboundLocalError:
                window['-TOUT-'].update(play_music)

        if event == '-RESTART-':
            try:
                mixer.music.play()
                i = 0
                progress_bar.UpdateBar(i)
            except error:
                window['-TOUT-'].update(play_music)

        if mixer.music.get_busy():
            progress_bar.UpdateBar(i)
            i += 1
            time.sleep(1)


if __name__ == '__main__':
    mixer.init()
    sg.theme('DarkAmber')
    layout = layouts()
    window = sg.Window('Music Player', layout, location=(400, 100), element_justification='center')
    player_loop(window)

    window.close()
