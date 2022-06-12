import os
import os.path
from secrets import token_urlsafe as uuid

import moviepy.editor as mv
import PySimpleGUI as psg
from pytube import YouTube as YT
from V2Mp3.appGUI import layout
from V2Mp3.appLogger.appLogger import setLogger

__version__ = '0.2.0'

logger = setLogger("V2Mp3")

_textborder: str = "=".ljust((78),
                             "=")  # Text border for log file organization.


class Events:
    """Handle GUI events.

    - Contains the following class methods:

        - :function:`dl_ytVideo(self, url: str, save_as: str = None) -> None`
            - Downloads a YouTube video to the local system.
            - If :param:`save_as` is :NoneType:`None`, the default file name will be used.

        - :function:`dl_ytAudio(self, url: str, save_as: str = None) -> None`
            - Downloads a YouTube video's audio to the local system.
            - If :param:`save_as` is :NoneType:`None`, the default file name will be used.
            - Works with both standard YouTube videos and videos with audio only.

        - :function:`to_mp3(self, filepath: str, save_as: str = None) -> None`
            - Converts a locally stored video file to an mp3 file.
            - If :param:`save_as` is :NoneType:`None`, the default file name will be used.
            - Works for any file extension supported by ffmpeg.

    """

    def dl_ytVideo(self, url: str, save_as: str = None) -> None:
        """Download video found at YouTube URL: :class:`url`.

        - If :param:`save_as` is :NoneType:`None`, the default file name will be used.

        ---

        :param url: URL address of YouTube content to download.
        :type url: :class:`str`
        :param save_as: optional name to save downloaded video as, defaults to :NoneType:`None`.
        :type save_as: :class:`str`, optional
        :returns: .mp4 file, can be found in `"~/V2Mp3/downloads/videos"`.
        :rtype: :NoneType:`None`
        """

        try:
            yt_url = YT(url)  # Create YouTube object from URL.
            video = yt_url.streams.get_highest_resolution(
            )  # Get highest resolution video.

            if save_as is None:
                save_as = f'{yt_url.title}.mp4'  # Set default save name.

            video.download('./downloads/videos/',
                           filename=save_as)  # Download video.

            layout.window['-Output-'].print(
                f'\nSuccessfully downloaded video from YouTube!\n==> Video downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}".\n==> Content URL: {url}\n'
            )
            logger.info(
                f'Successfully downloaded video from YouTube!\n==> Video downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {url}'
            )
        except Exception as exc:
            layout.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Please try again!\n'
            )
            logger.error(
                f'Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )

    def dl_ytAudio(self, url: str, save_as: str = None) -> None:
        """Download audio from media content found at YouTube URL: :class:`url`.

        - Works with both standard YouTube videos and videos with audio only (e.g. YouTube Music links).

        - If :param:`save_as` is :NoneType:`None`, the default file name will be used.

        ---

        :param url: URL address of YouTube content to download.
        :type url: :class:`str`
        :param save_as: optional name to save downloaded audio as, defaults to :NoneType:`None`.
        :type save_as: :class:`str`, optional
        :returns: .mp3 audio file, can be found in `"~/V2Mp3/downloads/audio"`.
        :rtype: :NoneType:`None`
        """

        try:
            yt_url = YT(url)  # Create YouTube object from URL
            audio = yt_url.streams.get_audio_only()  # Get audio-only stream

            if save_as is None:
                save_as = f'{yt_url.title}.mp3'  # Set default file name.

            audio.download('./downloads/audio/',
                           filename=save_as)  # Download audio

            layout.window['-Output-'].print(
                f'\nSuccessfully downloaded audio from YouTube!\n==> Audio Downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {url}\n'
            )
            logger.info(
                f'Successfully downloaded audio from YouTube!\n==> Audio Downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Content URL: {url}'
            )
        except Exception as exc:
            layout.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Please try again!\n'
            )

            logger.error(
                f'Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )

    def toMp3(self, filepath: str, save_as: str = None) -> None:
        """Convert locally stored video files to .mp3 audio format.

        - Can optionally save file with custom filename by passing desired filename to :class:`save_as` parameter.

        - Works for any file extension supported by ffmpeg, including:
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

        - See <https://ffmpeg.org/general.html#Video-Codecs> for a full list of supported video codecs.

        ---

        :param filepath: path to video file.
        :type filepath: :class:`str`
        :param save_as: optional name to save resulting audio file as, defaults to :NoneType:`None`.
        :type save_as: :class:`str`, optional
        :returns: .mp3 audio file, can be found in `"~/V2Mp3/downloads/audio"` by default.
        :rtype: :NoneType:`None`
        """

        try:
            if save_as is None:
                basename: str = os.path.basename(
                    filepath)  # Get file name from path.
                save_as = f'{os.path.splitext(basename)[0]}_{uuid(3)}.mp3'  # Generate random 5-character uuid for file name & add .mp3 extension
            else:
                save_as = f'{save_as}.mp3'  # Add .mp3 extension

            video = mv.VideoFileClip(filepath)  # Load video file
            audio = video.audio  # Extract audio from video

            audio.write_audiofile(f'./downloads/audio/{save_as}',
                                  logger=None)  # Write audio to file.

            layout.window['-Output-'].print(
                f'\nSuccessfully converted video to audio!\n==> File converted: "{filepath}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}\n'
            )

            logger.info(
                f'Successfully converted video to audio!\n==> File converted: "{filepath}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: ~/V2Mp3/audio/{save_as}'
            )

        except Exception as exc:
            layout.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{filepath}"\n==> Intended conversion output: "{save_as}"\n\n==> Exception:\n==> {exc}\n\n==> Please try again!\n'
            )

            logger.error(
                f'Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{filepath}"\n==> Intended conversion output: "{save_as}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )

events = Events()

def _event_loop() -> None:
    """Processing for application events.

    ---

    :returns: event processing
    :rtype: None
    """

    logger.info(
        f'Started application...\n==> Welcome to V2Mp3 v{__version__}!')

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
                events.toMp3(vals['-FileInput-'])
            else:
                events.toMp3(vals['-FileInput-'], vals['-T1_SaveInput-'])

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
                    events.dl_ytAudio(vals['-URLInput-'])
                else:
                    events.dl_ytVideo(vals['-URLInput-'])
            elif vals['-CB_AudioOnly-']:
                events.dl_ytAudio(vals['-URLInput-'], vals['-T2_SaveInput-'] + '.mp3')
            else:
                events.dl_ytVideo(vals['-URLInput-'], vals['-T2_SaveInput-'] + '.mp4')

    layout.window.Close()  # Close window and return resources to OS
    logger.info(f'Exiting application...\n{_textborder}')