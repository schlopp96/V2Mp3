#!/usr/bin/env python3

import logging
from os import chdir
from os.path import dirname
from secrets import token_urlsafe as uuid

import moviepy.editor as mv
import PySimpleGUI as psg
from pytube import YouTube as YT

chdir(dirname(__file__))

__version__ = '0.2.0'
#&================================================================================#

#$ Establish logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter(
    '[%(asctime)s - %(levelname)s] : %(message)s\n')

logHandler = logging.FileHandler('./logs/v2mp3_log.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#

psg.theme('Dark Grey 11')

appLayout: list = [
    [psg.Text('Fill Required Fields Below')], [psg.HorizontalSeparator()],
    [
        psg.Frame(
            'Mp3 Conversion',
            layout=[
                [psg.Text('Convert Local Videos to Mp3 Audio')],
                [
                    psg.Text('Filepath:', s=6, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        s=(27, 1),
                        key='-FileInput-',
                        do_not_clear=False,
                        tooltip=
                        'Enter the filepath of the video you wish to convert to an mp3.',
                        expand_x=True),
                    psg.VerticalSeparator(pad=5),
                    psg.FileBrowse(
                        key='-FileBrowse-',
                        initial_folder='video/',
                        target=(psg.ThisRow, -2),
                        tooltip=
                        'Browse local system for video files to convert to .mp3 format.'
                    )
                ],
                [
                    psg.Text('Save As:', s=6, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-T1_SaveInput-',
                        s=(35, 1),
                        do_not_clear=False,
                        tooltip=
                        'New filename of resulting mp3 file.\nLeave blank for default file name.',
                        expand_x=True)
                ],
                [
                    psg.ReadFormButton(
                        'Convert File',
                        key='-ConvertToMp3-',
                        button_color='green',
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
                    psg.Text('URL:', s=6, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-URLInput-',
                        s=(27,
                           1),
                        do_not_clear=False,
                        tooltip=
                        'Enter the URL of the content you wish to download.',
                        expand_x=True),
                    psg.VerticalSeparator(pad=5),
                    psg.Checkbox(
                        'Audio Only',
                        key='-CB_AudioOnly-',
                        auto_size_text=True,
                        tooltip=
                        'Choose whether to download normally (video with audio), or audio ONLY.'
                    )
                ],
                [
                    psg.Text('Save As:', s=6, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-T2_SaveInput-',
                        s=(35, 1),
                        do_not_clear=False,
                        tooltip=
                        'New filename of resulting mp3 file.\nLeave blank for default file name.',
                        expand_x=True),
                ],
                [
                    psg.ReadFormButton(
                        'Start Download',
                        button_color='green',
                        key='-Download-',
                        tooltip='Begin downloading content from YouTube URL.')
                ]
            ],
            expand_x=True,
            element_justification='Center')
    ],
    [
        psg.Multiline(size=(50, 30),
                      key='-Output-',
                      disabled=True,
                      auto_refresh=True,
                      autoscroll=True,
                      write_only=True,
                      expand_x=True)
    ], [psg.Exit(button_color='red', tooltip='Exit application.')]
]

program_win: psg.Window = psg.Window(f'V2Mp3 v{__version__}',
                                     layout=appLayout,
                                     auto_size_buttons=True,
                                     text_justification='Center',
                                     element_justification='Center')


def dl_ytVideo(link: str, saveAs: str = f'video_{uuid(5)}.mp4') -> None:
    """Download YouTube video found at url: `link`.

    ---

    Parameters:
        :param link: URL of intended YouTube video download.
        :type link: str
        :param saveAs: name to save downloaded video as, defaults to f'video_{uuid(5)}.mp4'
        :type saveAs: str, optional
        :returns: .mp4 file, can be found in `"./V2Mp3/video"`.
        :rtype: None
    """
    try:
        url = YT(link)
        video = url.streams.get_highest_resolution()
        video.download('video/', filename=saveAs)

        program_win['-Output-'].print(
            f'\nSuccessfully downloaded video from YouTube: "{url.title}"!\n==> Url: {link}\n'
        )
        logger.info(
            f'Successfully downloaded video from YouTube: "{url.title}"!\n==> Url: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during attempt to download file:\n==> "{link}"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during attempt to download file:\n==> "{link}"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def dl_ytAudio(link: str, saveAs: str = f'audio_{uuid(5)}.mp3') -> None:
    """Download audio from media content found at YouTube url: `link`.

    - Works with both standard YouTube videos, and songs from YouTube Music addresses.

    ---

    Parameters:
        :param link: URL of the intended download source.
        :type link: str
        :param saveAs: name to save downloaded audio as, defaults to f'audio_{uuid(5)}.mp3'
        :type saveAs: str, optional
        :returns: .mp3 audio file, can be found in `"./V2Mp3/audio"`.
        :rtype: None
    """
    try:
        url = YT(link)
        audio = url.streams.get_audio_only()
        audio.download('audio/', filename=saveAs)
        program_win['-Output-'].print(
            f'\nSuccessfully downloaded audio from YouTube: "{url.title}"!\n==> Url: {link}\n'
        )
        logger.info(
            f'Successfully downloaded audio from YouTube: "{url.title}"!\n==> Url: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'[ERROR] - Something went wrong during attempt to download file:\n==> "{link}"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during attempt to download file:\n==> "{link}"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def convert_local(file: str, saveAs: str = f'audio_{uuid(5)}') -> None:
    """Convert locally stored video files to .mp3 audio format.

    - Works for any extension supported by ffmpeg, such as:
        - .aiff
        - .avi
        - .flv
        - .gif
        - .mov
        - .mp4
        - .mpg
        - .ogv
        - .qt
        - .wmv
        - many others.

    ---

    Parameters:
        :param file: path to video file.
        :type file: str
        :param saveAs: name to save resulting audio file as, defaults to f'audio_{uuid(5)}.mp3'
        :type saveAs: str
        :returns: .mp3 audio file, can be found in `"./V2Mp3/audio"`.
        :rtype: None
    """
    try:
        video = mv.VideoFileClip(file)
        audio = video.audio

        audio.write_audiofile(f'audio/{saveAs}.mp3', logger=None)

        program_win['-Output-'].print(
            f'\nSuccessfully converted "{file}" to "{saveAs}.mp3"!\n')
        logger.info(f'Successfully converted "{file}" to "{saveAs}.mp3"!')

    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during conversion of "{file}" ==> "{saveAs}.mp3"...\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during conversion of "{file}" ==> "{saveAs}.mp3"...\n==> Please try again!\n\n==> Exception:\n==> {exc}'
        )


def v2mp3() -> None:
    """Run main event loop.

    - Responsible for processing events from GUI and responding with correct functionality.

    ---

    Parameters:
        :returns: Program window.
        :rtype: None
    """
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
            if vals['-T1_SaveInput-'] == "":
                convert_local(vals['-FileInput-'])
            else:
                convert_local(vals['-FileInput-'], vals['-T1_SaveInput-'])

        if event == '-Download-':
            if vals['-URLInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            program_win['-Output-'].print(
                f"Downloading File: {vals['-URLInput-']}")
            if vals['-T2_SaveInput-'] == "":
                if vals['-CB_AudioOnly-']:
                    dl_ytAudio(vals['-URLInput-'])
                else:
                    dl_ytVideo(vals['-URLInput-'])
            elif vals['-CB_AudioOnly-']:
                dl_ytAudio(vals['-URLInput-'], vals['-T2_SaveInput-'] + '.mp3')
            else:
                dl_ytVideo(vals['-URLInput-'], vals['-T2_SaveInput-'] + '.mp4')

    program_win.Close()


if __name__ == '__main__':
    v2mp3()
