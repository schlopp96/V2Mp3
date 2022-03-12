#!/usr/bin/env python3

from os import chdir
from os.path import dirname
import PySimpleGUI as psg
import logging

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
appLayout = [
    [
        psg.Text(
            'Download and create mp3 files of your favorite YouTube videos',
            justification='Center',
            auto_size_text=True)
    ], [psg.HorizontalSeparator('Black')],
    [psg.Text('Enter Relevant Information Below')],
    [
        psg.Text('Video URL: ', auto_size_text=True),
        psg.Input(
            key='-URLInput-',
            s=(25, 1),
            do_not_clear=False,
            tooltip=
            'Enter the URL of the YouTube video you wish to convert to an mp3.',
        ),
        psg.ReadFormButton(
            'Submit',
            auto_size_button=True,
            bind_return_key=True,
            key='-Submit-',
            tooltip='Submit URL of YouTube video to convert to mp3.')
    ],
    [
        psg.Multiline(size=(50, 20),
                      key='-Output-',
                      disabled=True,
                      auto_refresh=True,
                      autoscroll=True,
                      write_only=True)
    ]
]

program_win = psg.Window(f'YT2Mp3 v{__version__}',
                         layout=appLayout,
                         auto_size_buttons=True,
                         text_justification='Center',
                         element_justification='Center')

if __name__ == '__main__':
    while True:
        event, vals = program_win.read()
        logger.info(f'{event} : {vals}')
        print(event, vals)

        if event in [psg.WIN_CLOSED, 'Exit']:
            break

        if event == '-Submit-':
            if vals['-URLInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            program_win['-Output-'].print(f"URL: {vals['-URLInput-']}")

    program_win.Close()