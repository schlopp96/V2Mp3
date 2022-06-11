import os
import os.path
from posixpath import dirname
from secrets import token_urlsafe as uuid
import moviepy.editor as mv
import PySimpleGUI as psg
from pytube import YouTube as YT
from V2Mp3.appGUI import layout
from V2Mp3.appLogger.appLogger import applogger

__version__ = '0.2.0'

logger = applogger("V2Mp3")

_textborder: str = "=".ljust((78),
                             "=")  # Text border for log file organization.


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
        video.download('../downloads/video/', filename=save_as)

        layout.window['-Output-'].print(
            f'\nSuccessfully downloaded video from YouTube!\n==> Video downloaded: "{url.title}"\n==> Saved As: "{save_as}".\n==> Content URL: {link}\n'
        )
        logger.info(
            f'Successfully downloaded video from YouTube!\n==> Video downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}'
        )
    except Exception as exc:
        layout.window['-Output-'].print(
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
        audio.download('../downloads/audio/', filename=save_as)

        layout.window['-Output-'].print(
            f'\nSuccessfully downloaded audio from YouTube!\n==> Audio Downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}\n'
        )
        logger.info(
            f'Successfully downloaded audio from YouTube!\n==> Audio Downloaded: "{url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {link}'
        )
    except Exception as exc:
        layout.window['-Output-'].print(
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

        audio.write_audiofile(f'../downloads/audio/{save_as}', logger=None)

        layout.window['-Output-'].print(
            f'\nSuccessfully converted video to audio!\n==> File converted: "{file}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}\n'
        )

        logger.info(
            f'Successfully converted video to audio!\n==> File converted: "{file}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}'
        )

    except Exception as exc:
        layout.window['-Output-'].print(
            f'\n[ERROR] - Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{file}"\n==> Intended conversion output: "{save_as}"\n\n==> Exception:\n==> {exc}\n\n==> Please try again!\n'
        )

        logger.error(
            f'Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{file}"\n==> Intended conversion output: "{save_as}"\n==> Exception:\n==> {exc}\n==> Please try again!'
        )


def event_loop() -> None:
    """Processing for application events.

    ---

    :returns: event processing
    :rtype: None
    """

    logger.info(f'Started application...\n==> Welcome to V2Mp3 v{__version__}!')

    while True:
        event, vals = layout.window.read()
        logger.info(f'{event} : {vals}')

        #print(event, vals) # DEBUG

        if event in [psg.WIN_CLOSED, 'Exit']:
            break

        if event == '-ConvertToMp3-':
            if vals['-FileInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue
            layout.window['-Output-'].print(
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
            layout.window['-Output-'].print(
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

    layout.window.Close()
    logger.info(f'Exiting application...\n{_textborder}\n')
