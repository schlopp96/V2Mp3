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

logHandler = logging.FileHandler('./logs/v2mp3.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#
appLayout: list = [
    [psg.Text('Enter Relevant Information Below')],
    [psg.HorizontalSeparator('Black')],
    [
        psg.Frame(
            'Mp3 Conversion',
            layout=[
                [psg.Text('Convert Local Videos to Mp3 Audio')],
                [
                    psg.Text('Filepath:'),
                    psg.VerticalSeparator('Black'),
                    psg.Input(
                        s=(25, 1),
                        key='-FileInput-',
                        do_not_clear=False,
                        tooltip=
                        'Enter the filepath of the video you wish to convert to an mp3.',
                        expand_x=True),
                    psg.VerticalSeparator('Black'),
                    psg.FileBrowse(
                        key='-FileBrowse-',
                        initial_folder='video/',
                        target=(psg.ThisRow, -2),
                        tooltip=
                        'Browse local system for video files to convert to .mp3 format.'
                    )
                ],
                [
                    psg.Text('Save As:'),
                    psg.VerticalSeparator('Black'),
                    psg.Input(
                        key='-Convert_Filename-',
                        s=(35, 1),
                        do_not_clear=False,
                        tooltip=
                        'New filename of resulting mp3 file.\nLeave blank for default file name.',
                        expand_x=True),
                ],
                [
                    psg.ReadFormButton(
                        'Convert',
                        key='-ConvertToMp3-',
                        tooltip=
                        'Submit filepath of video to convert to .mp3 format.')
                ]
            ],
            expand_x=True,
            element_justification='Center')
    ],
    [
        psg.Frame(
            'YouTube Video/Audio',
            layout=[
                [psg.Text('Enter URL of YouTube Video to Download.')],
                [
                    psg.Text('URL:', auto_size_text=True),
                    psg.VerticalSeparator('Black'),
                    psg.Input(
                        key='-URLInput-',
                        s=(25,
                           1),
                        do_not_clear=False,
                        tooltip=
                        'Enter the URL of the content you wish to download.',
                        expand_x=True),
                    psg.VerticalSeparator('Black'),
                    psg.Checkbox(
                        'Audio Only',
                        key='-CB_AudioOnly-',
                        auto_size_text=True,
                        tooltip=
                        'Choose whether to download normally (video with audio), or audio ONLY.'
                    )
                ],
                [
                    psg.Text('Save As:'),
                    psg.VerticalSeparator('Black'),
                    psg.Input(
                        key='-DL_SaveAs-',
                        s=(35, 1),
                        do_not_clear=False,
                        tooltip=
                        'New filename of resulting mp3 file.\nLeave blank for default file name.',
                        expand_x=True),
                ],
                [
                    psg.ReadFormButton(
                        'Download',
                        key='-Download-',
                        tooltip=
                        'Begin downloading specified content from YouTube.')
                ]
            ],
            expand_x=True,
            element_justification='Center')
    ],
    [
        psg.Multiline(size=(50, 25),
                      key='-Output-',
                      disabled=True,
                      auto_refresh=True,
                      autoscroll=True,
                      write_only=True)
    ], [psg.Exit(tooltip='Exit application.')]
]

program_win: psg.Window = psg.Window(f'V2Mp3 v{__version__}',
                                     layout=appLayout,
                                     auto_size_buttons=True,
                                     text_justification='Center',
                                     element_justification='Center')


def dl_ytVideo(link: str, name: str):
    try:
        url = YT(link)
        video = url.streams.get_highest_resolution()
        video.download('video/', filename=name)

        program_win['-Output-'].print(
            f'Successfully downloaded video from YouTube: "{url.title}"!\n==> Url: {link}\n'
        )
        logger.info(
            f'Successfully downloaded video from YouTube: "{url.title}"!\n==> Url: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'[ERROR] - Something went wrong during attempt to download "{link}"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during attempt to download "{link}"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def dl_ytAudio(link: str, name: str):
    try:
        url = YT(link)
        audio = url.streams.get_audio_only()
        audio.download('audio/', filename=name)
        program_win['-Output-'].print(
            f'Successfully downloaded audio from YouTube: "{url.title}"!\n==> Url: {link}\n'
        )
        logger.info(
            f'Successfully downloaded audio from YouTube: "{url.title}"!\n==> Url: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'[ERROR] - Something went wrong during attempt to download "{link}"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during attempt to download "{link}"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def convert_local(file: str, name: str):
    try:
        video = mv.VideoFileClip(file)
        audio = video.audio

        audio.write_audiofile(f'audio/{name}.mp3')

        program_win['-Output-'].print(
            f'\nSuccessfully converted "{file}" to "{name}.mp3"!\n')
        logger.info(f'Successfully converted "{file}" to "{name}.mp3"!')

    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during conversion of "{file}" to "{name}.mp3"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during conversion of "{file}" to "{name}.mp3"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def v2mp3():
    while True:
        event, vals = program_win.read()
        logger.info(f'{event} : {vals}')

        print(event, vals)

        if event in [psg.WIN_CLOSED, 'Exit']:
            break

        if event == '-ConvertToMp3-':
            if vals['-FileInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            program_win['-Output-'].print(
                f"Converting File: {vals['-FileInput-']}")
            if vals['-Convert_Filename-'] == "":
                convert_local(vals['-FileInput-'], f'sample_{uuid(5)}')
            else:
                convert_local(vals['-FileInput-'], vals['-Convert_Filename-'])

        if event == '-Download-':
            if vals['-URLInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            program_win['-Output-'].print(
                f"Downloading File: {vals['-URLInput-']}")
            if vals['-DL_SaveAs-'] == "":
                if vals['-CB_AudioOnly-']:
                    dl_ytAudio(vals['-URLInput-'], f'sample_{uuid(5)}.mp3')
                else:
                    dl_ytVideo(vals['-URLInput-'], f'video_{uuid(5)}.mp4')
            elif vals['-CB_AudioOnly-']:
                dl_ytAudio(vals['-URLInput-'], vals['-DL_SaveAs-'] + '.mp3')
            else:
                dl_ytVideo(vals['-URLInput-'], vals['-DL_SaveAs-'] + '.mp4')

    program_win.Close()


if __name__ == '__main__':
    v2mp3()
