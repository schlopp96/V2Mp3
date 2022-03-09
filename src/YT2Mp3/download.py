#!/usr/bin/env python3

import logging
from os import mkdir, chdir
from os.path import dirname
import PySimpleGUI as psg
from os.path import exists

__version__ = '0.0.0'

chdir(dirname(__file__))
#&================================================================================#

#$ Establish logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logFormatter = logging.Formatter('%(levelname) : %(asctime)s : %(message)s')

logHandler = logging.FileHandler('../logs/yt2mp3.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#
appLayout = [
    [
        psg.Text(
            'Download and create mp3 files of your favorite YouTube videos',
            justification='Center')
    ], [psg.HorizontalSeparator('Black')],
    [psg.Text('Enter Relevant Information Below')],
    [
        psg.Text('Video URL: '),
        psg.Input(
            key='-URL-',
            tooltip=
            'Enter the URL of the YouTube video you wish to convert to an mp3.',
        ),
        psg.Submit(auto_size_button=True,
                   bind_return_key=True,
                   focus=True,
                   key='-Submit_URL-',
                   tooltip='Submit URL of YouTube video to convert to mp3.')
    ], [psg.Multiline(size=(75, 10), key='-Output-', auto_refresh=True)]
]

appWin = psg.Window('YT2Mp3',
                    layout=appLayout,
                    auto_size_buttons=True,
                    text_justification='Center',
                    element_justification='Center')

if __name__ == '__main__':
    while True:
        event, vals = appWin.Read()
        print(event, vals)

        if event in [psg.WIN_CLOSED, 'Exit']:
            break

    appWin.Close()