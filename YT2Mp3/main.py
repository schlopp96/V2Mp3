#!/usr/bin/env python3

import logging
from os import chdir
from os.path import dirname
from secrets import token_urlsafe as uuid

import moviepy.editor as mv
import PySimpleGUI as psg
from pytube import YouTube as YT

chdir(dirname(__file__))

__version__ = '0.0.1'
#&================================================================================#

#$ Establish logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter(
    '[%(asctime)s - %(levelname)s] : %(message)s\n')

logHandler = logging.FileHandler('./logs/yt2mp3.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#
appLayout: list = [
    [psg.Text('Convert Local Videos OR YouTube URLs to Mp3 Audio')],
    [psg.HorizontalSeparator('Black')],
    [psg.Text('Enter Relevant Information Below')],
    [
        psg.Text('Filepath:'),
        psg.VerticalSeparator('Black'),
        psg.Input(
            key='-FileInput-',
            s=(25, 1),
            do_not_clear=False,
            tooltip=
            'Enter the URL/filepath of the video you wish to convert to an mp3.',
        ),
        psg.VerticalSeparator('Black'),
        psg.FileBrowse(
            key='-FileBrowse-',
            target=(psg.ThisRow, -2),
            tooltip=
            'Browse local system for video files to convert to mp3 format.')
    ],
    [
        psg.Text('Output Filename:'),
        psg.Input(
            key='-Out_Local-',
            s=(30, 1),
            do_not_clear=False,
            tooltip=
            'New filename of resulting mp3 file. Leave blank for a default file name.'
        ),
    ],
    [
        psg.ReadFormButton(
            'Submit',
            bind_return_key=True,
            key='-Submit-',
            tooltip=
            'Submit URL/filepath of video to convert to mp3. Can also use return (ENTER) key.'
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


def dl_ytAudio():
    pass


def convert_local(file, name):
    try:
        video = mv.VideoFileClip(file)
        audio = video.audio

        audio.write_audiofile(f'out/{name}.mp3')

        program_win['-Output-'].print(
            f'\nSuccessfully converted "{file}" to "{name}.mp3"!\n')
        logger.info(f'Successfully converted "{file}" to "{name}.mp3"!')

    except:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during conversion of "{file}" to "{name}.mp3"...\n===> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during conversion of "{file}" to "{name}.mp3"...\n===> Please try again!'
        )


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
            program_win['-Output-'].print(
                f"Converting File: {vals['-FileInput-']}")
            if vals['-Out_Local-'] == "":
                convert_local(vals['-FileInput-'], f'sample_{uuid(5)}')
            else:
                convert_local(vals['-FileInput-'], vals['-Out_Local-'])

    program_win.Close()


if __name__ == '__main__':
    main()
