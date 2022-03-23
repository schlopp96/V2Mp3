#!/usr/bin/env python3

import logging
from os import chdir
from os.path import dirname

import PySimpleGUI as psg

chdir(dirname(__file__))

__version__ = '0.0.1'
#&================================================================================#

#$ Establish logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

logHandler = logging.FileHandler('./logs/yt2mp3.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#
appLayout: list = [
    [
        psg.Text(
            'Download and create mp3 files of your favorite YouTube videos',
            justification='Center',
            auto_size_text=True)
    ], [psg.HorizontalSeparator('Black')],
    [psg.Text('Enter Relevant Information Below')],
    [
        psg.Text('Video File: ', auto_size_text=True),
        psg.Input(
            key='-FileInput-',
            s=(25, 1),
            do_not_clear=False,
            tooltip=
            'Enter the URL/filepath of the YouTube video you wish to convert to an mp3.',
        ),
        psg.FileBrowse(
            key='-FileBrowse-',
            tooltip=
            'Browse local system for video files to convert to mp3 format.')
    ],
    [
        psg.ReadFormButton(
            'Submit',
            bind_return_key=True,
            key='-Submit-',
            tooltip=
            'Submit URL of YouTube video to convert to mp3. Can also use return (ENTER) key.'
        )
    ],
    [
        psg.Multiline(size=(50, 20),
                      key='-Output-',
                      disabled=True,
                      auto_refresh=True,
                      autoscroll=True,
                      write_only=True)
    ], [psg.Exit(tooltip='Exit application.')]
]

program_win: psg.Window = psg.Window(f'YT2Mp3 v{__version__}',
                                     layout=appLayout,
                                     auto_size_buttons=True,
                                     text_justification='Center',
                                     element_justification='Center')


def main():
    while True:
        event, vals = program_win.read()
        logger.info(f'{event} : {vals}')
        print(event, vals)
        if event in [psg.WIN_CLOSED, 'Exit']:
            break
        if event == '-Submit-':
            if vals['-FileInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            program_win['-Output-'].print(f"URL: {vals['-FileInput-']}")
    program_win.Close()


if __name__ == '__main__':
    main()
