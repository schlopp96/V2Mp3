#!/usr/bin/env python3

import logging
import os
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
    '[%(asctime)s - %(levelname)s] : %(message)s\n', "%Y-%m-%d %H:%M:%S")

logHandler = logging.FileHandler('./logs/v2mp3Log.log', 'a')
logHandler.setFormatter(logFormatter)

logger.addHandler(logHandler)
#&================================================================================#

psg.theme('DarkGrey11')

appLayout: list = [
    # Top Text
    [psg.Text('Welcome to V2Mp3')],
    [psg.HorizontalSeparator()],
    # Download Frame
    [
        psg.Frame(
            'Download YouTube Video/Audio',
            layout=[
                [psg.Text('Enter URL of YouTube Video to Download.')],
                [
                    psg.Text('URL:', s=7, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-URLInput-',
                        do_not_clear=False,
                        tooltip=
                        'Enter the URL of the content you wish to download.',
                        expand_x=True),
                    psg.VerticalSeparator(pad=5),
                    psg.Checkbox(
                        'Audio Only',
                        s=8,
                        key='-CB_AudioOnly-',
                        tooltip=
                        'Choose whether to download normally (video with audio), or audio ONLY.'
                    )
                ],
                [
                    psg.Text('Save As:', s=7, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-T2_SaveInput-',
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
    # Conversion Frame
    [
        psg.Frame(
            'Video to Audio Conversion',
            layout=[
                [psg.Text('Convert Local Videos to Mp3 Audio')],
                [
                    psg.Text('Filepath:', s=7, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-FileInput-',
                        do_not_clear=False,
                        tooltip=
                        'Enter the filepath of the video you wish to convert to an mp3.',
                        expand_x=True),
                    psg.VerticalSeparator(pad=5),
                    psg.FileBrowse(
                        s=10,
                        key='-FileBrowse-',
                        initial_folder='./downloads/video/',
                        target=(psg.ThisRow, -2),
                        tooltip=
                        'Browse local system storage for video file to convert to .mp3 formatting.'
                    )
                ],
                [
                    psg.Text('Save As:', s=7, justification='left'),
                    psg.VerticalSeparator(pad=5),
                    psg.Input(
                        key='-T1_SaveInput-',
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
                        'Start conversion of the specified video file to .mp3 formatting.'
                    )
                ]
            ],
            expand_x=True,
            element_justification='Center')
    ],
    # Event Output
    [
        psg.Multiline(size=(70, 30),
                      key='-Output-',
                      disabled=True,
                      auto_refresh=True,
                      autoscroll=True,
                      write_only=True,
                      expand_x=True,
                      expand_y=True)
    ],
    [psg.Exit(button_color='red', tooltip='Exit application.')]
]

program_win: psg.Window = psg.Window(f'V2Mp3 v{__version__}',
                                     layout=appLayout,
                                     auto_size_buttons=True,
                                     text_justification='Center',
                                     element_justification='Center',
                                     resizable=True,
                                     finalize=True)


def dl_ytVideo(link: str, save_as: str = None) -> None:
    """Download video found at YouTube URL: :class:`link`.

    ---

    :param link: URL address of YouTube content to download.
    :type link: :class:`str`
    :param save_as: optional name to save downloaded video as, defaults to `None`.
    :type save_as: :class:`str`, optional
    :returns: .mp4 file, can be found in `"~/V2Mp3/downloads/video"`.
    :rtype: None
    """
    try:
        url = YT(link)
        video = url.streams.get_highest_resolution()

        if save_as is None:
            save_as = f'{url.title}.mp4'
        video.download('downloads/video/', filename=save_as)

        program_win['-Output-'].print(
            f'\nSuccessfully downloaded video from YouTube!\n==> Video downloaded: "{url.title}"\n==> Saved As: "{save_as}".\n==> Content URL: {link}\n'
        )
        logger.info(
            f'Successfully downloaded video from YouTube!\n==> Video downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{link}"\n==> Please try again!\n'
        )
        logger.error(
            f'Something went wrong during attempt to download file...\n==> Content URL: "{link}"\n==> Exception:\n==> {exc}\n==> Please try again!'
        )


def dl_ytAudio(link: str, save_as: str = None) -> None:
    """Download audio from media content found at YouTube URL: :class:`link`.

    - Works with both standard YouTube video URLs, and songs from YouTube Music.

    ---

    :param link: URL of the intended download source.
    :type link: :class:`str`
    :param save_as: optional name to save downloaded audio as, defaults to `None`.
    :type save_as: :class:`str`, optional
    :returns: .mp3 audio file, can be found in `"~/V2Mp3/downloads/audio"`.
    :rtype: None
    """
    try:
        url = YT(link)
        audio = url.streams.get_audio_only()

        if save_as is None:
            save_as = f'{url.title}.mp3'
        audio.download('downloads/audio/', filename=save_as)

        program_win['-Output-'].print(
            f'\nSuccessfully downloaded audio from YouTube!\n==> Audio Downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}\n'
        )
        logger.info(
            f'Successfully downloaded audio from YouTube!\n==> Audio Downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}'
        )
    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{link}"\n==> Please try again!\n'
        )

        logger.error(
            f'Something went wrong during attempt to download file...\n==> Content URL: "{link}"\n==> Exception:\n==> {exc}\n==> Please try again!'
        )


def toMp3(file: str, save_as: str = None) -> None:
    """Convert locally stored video files to .mp3 audio format.

    - Can optionally save file with new filename by passing desired filename to :class:`save_as` parameter.

    - Works for any extension supported by ffmpeg, including:
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

    - See https://ffmpeg.org/general.html#Video-Codecs for full list of supported video codecs.

    ---

    :param file: path to video file.
    :type file: :class:`str`
    :param save_as: optional name to save resulting audio file as, defaults to `None`.
    :type save_as: :class:`str`, optional
    :returns: .mp3 audio file, can be found in `"~/V2Mp3/downloads/audio"` by default.
    :rtype: None
    """
    try:
        if save_as is None:
            basename: str = os.path.basename(file)
            save_as = f'{os.path.splitext(basename)[0]}_{uuid(3)}.mp3'  # Generate random 5-character uuid for file name & add .mp3 extension
        else:
            save_as = f'{save_as}.mp3'  # add .mp3 extension

        video = mv.VideoFileClip(file)
        audio = video.audio

        audio.write_audiofile(f'downloads/audio/{save_as}', logger=None)

        program_win['-Output-'].print(
            f'\nSuccessfully converted video to audio!\n==> File converted: "{file}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}\n'
        )

        logger.info(
            f'Successfully converted video to audio!\n==> File converted: "{file}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}'
        )

    except Exception as exc:
        program_win['-Output-'].print(
            f'\n[ERROR] - Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{file}"\n==> Intended conversion output: "{save_as}"\n\n==> Exception:\n==> {exc}\n\n==> Please try again!\n'
        )

        logger.error(
            f'Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{file}"\n==> Intended conversion output: "{save_as}"\n==> Exception:\n==> {exc}\n==> Please try again!'
        )


def v2mp3() -> None:
    """Program entry point.

    - Responsible for processing GUI events and responses.

    ---

    :returns: Program window.
    :rtype: None
    """
    while True:
        event, vals = program_win.read()
        logger.info(f'{event} : {vals}')

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
                toMp3(vals['-FileInput-'])
            else:
                toMp3(vals['-FileInput-'], vals['-T1_SaveInput-'])

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
