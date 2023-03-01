import os
import PySimpleGUI as sg
from pygame import mixer, error
import time
from threading import Thread, Event

music_dict = dict()
music_files = list()
path_tracker = list()
play_music = 'Player must be playing a music'
file_list = '-FILE_LIST-'
pause = '-PAUSE-'
thread_event = Event()

def music_list(folder_path):
    items = os.listdir(folder_path)
    if folder_path not in music_dict.keys():
        music_dict[folder_path] = []
    for item in items:
        destination = os.path.join(folder_path, item)
        if os.path.isdir(destination):
            music_list(destination)
        elif item.lower().endswith(('.mp3')):
            if item not in music_files:
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
            sg.Checkbox(text='Repeat', key='repeat', enable_events=True),
            sg.Slider(range=(0, 10), default_value=5, resolution=1, enable_events=True, orientation='h', key='volume'),
            sg.Checkbox(text="Shuffle", key='shuffle', enable_events=True)
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
        [sg.Button(button_text='Exit', button_color='red')]
    ]
    return layout

def load_files(window, event, values):
    if event == '-PATH-':
        folder_path = values['-PATH-']
        music_list(folder_path)
        window[file_list].update(music_files)
        window['-TOUT-'].update(f'{len(music_files)} songs found')

def progressbar_update(progress_bar):
    i = 0
    while True:
        if mixer.music.get_busy():
            progress_bar.UpdateBar(i)
            time.sleep(1)
            i += 1
        if thread_event.is_set():
            break
    
def search_song(window, event, values):
    if event == 'search':
        search_str = values['search']
        new_music_list = [song for song in music_files if search_str.lower() in song.lower()]
        window[file_list].update(new_music_list)

def volume_setter(event, values):
    if event == 'volume':
        volume = values['volume']
        mixer.music.set_volume(volume/10)

def player_loop(window):
    progress_bar = window['progressbar']
    while True:
        event, values = window.read(timeout=20)
        load_files(window, event, values)
        search_song(window, event, values)
        if event == file_list:
            song = values[file_list][0]
            window['-TOUT-'].update(song)
            song_details = [(key, song) for key, value in music_dict.items() if song in value]
            mixer.music.load(os.path.join(
                song_details[0][0], song_details[0][1]))
            mixer.music.set_volume(0.5)
            mixer.music.play()
            song_length = mixer.Sound(os.path.join(
                song_details[0][0], song_details[0][1])).get_length()
            progress_bar.update(0, int(song_length))
            thread_event.clear()
            progress_bar_thread = Thread(target=progressbar_update, args=(progress_bar, ), daemon=True)
            progress_bar_thread.start()
        
        volume_setter(event, values)
        if event == pause:
            if mixer.music.get_busy():
                mixer.music.pause()
                window[pause].update('Play')
            else:
                mixer.music.unpause()
                window[pause].update('Pause')

        if event == '-STOP-' and mixer.music.get_busy():
            progress_bar.UpdateBar(0)
            mixer.music.stop()
            thread_event.set()

        if event == '-RESTART-':
            try:
                mixer.music.play()
            except (error, UnboundLocalError):
                window['-TOUT-'].update(play_music)
                
        if event in (sg.WIN_CLOSED, 'Exit'):
            break


if __name__ == '__main__':
    mixer.init()
    sg.theme('Dark')
    layout = layouts()
    window = sg.Window('Music Player', layout, location=(400, 100), element_justification='center')
    player_loop(window)
    window.close()
