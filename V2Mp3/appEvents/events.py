import os
import os.path
from posixpath import abspath
from secrets import token_urlsafe as uuid

import moviepy.editor as mv
import PySimpleGUI as psg
from pytube import YouTube as YT
from V2Mp3.appGUI import gui
from V2Mp3.appLogger.appLogger import setLogger

__version__ = '0.3.0'  # Current program version

logger = setLogger("V2Mp3")  # Initialize logger

_textborder: str = "=".ljust((78), "=")  # Text border for log organization.


class GUIEvents:
    """Provides methods for handling various GUI events.

    ---

    - Contains the following event-handler methods:

        - :func:`dl_ytVideo(url: str, save_as: str = None) -> None`
            - Downloads a YouTube video to the local system.
            - If :param:`save_as` is `None`, the default file name will be used.
            - Static method.

        - :func:`dl_ytAudio(url: str, save_as: str = None) -> None`
            - Downloads a YouTube video's audio to the local system.
            - If :param:`save_as` is `None`, the default file name will be used.
            - Works with both standard YouTube videos and videos with audio only.
            - Static method.

        - :func:`to_mp3(filepath: str, save_as: str = None) -> None`
            - Converts a locally stored video file to an mp3 file.
            - If :param:`save_as` is `None`, the default file name will be used.
            - Works for any file extension supported by `ffmpeg`.
            - Static method.
    """

    @staticmethod
    def dl_ytVideo(url: str,
                   save_as: str | None = None,
                   save_to: str | None = None) -> None:
        """Download video found at YouTube URL: :param:`url`.

        - If :param:`save_as` is `None`, the default file name will be used.
        - If :param:`save_to` is `None`, the default file location will be used: `"~./V2Mp3/downloads/videos"`.

        ---

        :param url: URL address of YouTube content to download.
        :type url: :class:`str`
        :param save_as: optional name to save downloaded video as, defaults to `None`
        :type save_as: :class:`str`, optional
        :param save_to: optional path to save download to, defaults to `None`
        :type save_to: :class:`str` | `None`, optional
        :returns: downloaded YouTube video file, can be found in `"~./V2Mp3/downloads/videos"` by default
        :rtype: None
        """

        try:
            yt_url = YT(url)  # Create YouTube object from URL.
            video = yt_url.streams.get_highest_resolution(
            )  # Get highest resolution video.

            if save_as is None:
                save_as = f'{yt_url.title}.mp4'  # Set default save name.

            if save_to is None:
                save_to = abspath(
                    './downloads/videos')  # Set default save location.

            video.download(output_path=save_to,
                           filename=save_as)  # Download video.

            gui.window['-Output-'].print(
                f'\nSuccessfully downloaded video from YouTube!\n==> Video downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"\n==> Content URL: {url}\n'
            )
            logger.info(
                f'Successfully downloaded video from YouTube!\n==> Video downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"\n==> Content URL: {url}'
            )

        except Exception as exc:
            gui.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Please try again!\n'
            )
            logger.error(
                f'Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )

    @staticmethod
    def dl_ytAudio(url: str,
                   save_as: str | None = None,
                   save_to: str | None = None) -> None:
        """Download audio from media content found at YouTube link: :param:`url`.

        - Works with both standard YouTube videos and videos with audio only (e.g. YouTube Music links).

        - If :param:`save_as` is `None`, the default file name will be used.
        - If :param:`save_to` is `None`, the default file location will be used: `"~./V2Mp3/downloads/audio"`.


        ---

        :param url: url of YouTube content to download.
        :type url: :class:`str`
        :param save_as: optional name to save downloaded audio as, defaults to `None`
        :type save_as: :class:`str`, optional
        :param save_to: optional path to save download to, defaults to `None`
        :type save_to: :class:`str` | `None`, optional
        :returns: downloaded YouTube audio file, can be found in `"~./V2Mp3/downloads/audio"` by default
        :rtype: None
        """

        try:
            yt_url = YT(url)  # Create YouTube object from URL
            audio = yt_url.streams.get_audio_only()  # Get audio-only stream

            if save_as is None:
                save_as = f'{yt_url.title}.mp3'  # Set default file name.

            if save_to is None:
                save_to = abspath(
                    './downloads/audio')  # Set default save location.

            audio.download(save_to, filename=save_as)  # Download audio

            gui.window['-Output-'].print(
                f'\nSuccessfully downloaded audio from YouTube!\n==> Audio Downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"\n==> Content URL: {url}\n'
            )
            logger.info(
                f'Successfully downloaded audio from YouTube!\n==> Audio Downloaded: "{yt_url.title}"\n==> Saved As: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"\n==> Content URL: {url}'
            )

        except Exception as exc:
            gui.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Please try again!\n'
            )

            logger.error(
                f'Something went wrong during attempt to download file...\n==> Content URL: "{url}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )

    @staticmethod
    def toMp3(filepath: str,
              save_as: str | None = None,
              save_to: str | None = None) -> None:
        """Convert locally stored video files to ".mp3" audio format.

        - Can optionally save file with custom filename by passing desired filename to :param:`save_as` parameter.
            - If :param:`save_as` is `None`, the default file name will be used.

        - Can optionally save file to custom location by passing desired filepath to :param:`save_to` parameter.
            - If :param:`save_to` is `None`, the default filepath will be used: `"~./V2Mp3/downloads/audio"`.

        - Works for any file extension supported by `ffmpeg`, including:
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

        - See https://ffmpeg.org/general.html#Video-Codecs for a full list of supported video codecs.

        ---

        :param filepath: path to video file.
        :type filepath: :class:`str`
        :param save_as: optional name to save resulting audio file as, defaults to `None`
        :type save_as: :class:`str` | `None`, optional
        :param save_to: optional path to save resulting audio file to, defaults to `None`
        :type save_to: :class:`str` | `None`, optional
        :returns: ".mp3" audio file, can be found in `"~./V2Mp3/downloads/audio"` by default
        :rtype: None
        """

        try:
            if save_as is None:  # If no save name is provided, use default.
                basename: str = os.path.basename(
                    filepath)  # Get file name from path.
                save_as = f'{os.path.splitext(basename)[0]}_{uuid(3)}.mp3'  # Generate 5-character uuid for filename & add ".mp3" extension

            else:
                save_as = f'{save_as}.mp3'  # Add ".mp3" extension

            if save_to is None:
                save_to = abspath(
                    './downloads/audio')  # Set default save location.

            video = mv.VideoFileClip(filepath)  # Load video file
            audio = video.audio  # Extract audio from video

            audio.write_audiofile(f'{save_to}/{save_as}',
                                  logger=None)  # Write audio to file.

            gui.window['-Output-'].print(
                f'\nSuccessfully converted video to audio!\n==> File converted: "{filepath}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"\n'
            )

            logger.info(
                f'Successfully converted video to audio!\n==> File converted: "{filepath}"\n==> Resulting audio file: "{save_as}"\n==> Save Location: "{save_to}/{save_as}"'
            )

        except Exception as exc:
            gui.window['-Output-'].print(
                f'\n[ERROR] - Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{filepath}"\n==> Intended conversion output: "{save_as}"\n\n==> Exception:\n==> {exc}\n\n==> Please try again!\n'
            )

            logger.error(
                f'Something went wrong during video to audio conversion...\n==> Intended video to be converted: "{filepath}"\n==> Intended conversion output: "{save_as}"\n==> Exception:\n==> {exc}\n==> Please try again!'
            )


events = GUIEvents()


def GUILoop(
) -> None:  # sourcery skip: low-code-quality, merge-else-if-into-elif
    """Application GUI event loop.

    ---

    :returns: event processing
    :rtype: `None`
    """

    logger.info(
        f'Started application...\n==> Welcome to V2Mp3 v{__version__}!')

    while True:
        event, vals = gui.window.read()
        logger.info(f'{event} : {vals}')  # Log GUI events

        #print(event, vals) # DEBUG

        if event in [psg.WIN_CLOSED, 'Exit']:
            break

        if event == '-Download-':  # Download video/audio from YouTube

            if vals['-URLInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue

            gui.window['-Output-'].print(
                f"Downloading File: {vals['-URLInput-']}")

            if vals['-YTSaveAs-'] == "" and vals['-YTSaveTo-'] == "":
                if vals['-ToggleAudioDL-']:
                    events.dl_ytAudio(vals['-URLInput-'])

                else:
                    events.dl_ytVideo(vals['-URLInput-'])

            elif vals['-YTSaveAs-'] == "":
                if vals['-ToggleAudioDL-']:
                    events.dl_ytAudio(vals['-URLInput-'],
                                      save_to=vals['-YTSaveTo-'])

                else:
                    events.dl_ytVideo(vals['-URLInput-'],
                                      save_to=vals['-YTSaveTo-'])

            elif vals['-YTSaveTo-'] == "":
                if vals['-ToggleAudioDL-']:
                    events.dl_ytAudio(vals['-URLInput-'],
                                      save_as=vals['-YTSaveAs-'] + '.mp3')

                else:
                    events.dl_ytVideo(vals['-URLInput-'],
                                      save_as=vals['-YTSaveAs-'] + '.mp4')

            else:
                if vals['-ToggleAudioDL-']:
                    events.dl_ytAudio(vals['-URLInput-'],
                                      save_as=vals['-YTSaveAs-'] + '.mp3',
                                      save_to=vals['-YTSaveTo-'])

                else:
                    events.dl_ytVideo(vals['-URLInput-'],
                                      save_as=vals['-YTSaveAs-'] + '.mp4',
                                      save_to=vals['-YTSaveTo-'])

        if event == '-ConvertToMp3-':  # Convert video to audio

            if vals['-FileInput-'] == "":
                psg.popup('ERROR',
                          '- Input must NOT be blank! -',
                          keep_on_top=True)
                logger.warning('Entry can\'t be blank!')
                continue

            gui.window['-Output-'].print(
                f"Converting File: {vals['-FileInput-']}")

            if vals['-Mp3SaveAs-'] == "" and vals['-Mp3SaveTo-'] == "":
                events.toMp3(vals['-FileInput-'])

            elif vals['-Mp3SaveTo-'] == "":
                events.toMp3(vals['-FileInput-'], save_as=vals['-Mp3SaveAs-'])

            elif vals['-Mp3SaveAs-'] == "":
                events.toMp3(vals['-FileInput-'], save_to=vals['-Mp3SaveTo-'])

            else:
                events.toMp3(vals['-FileInput-'], vals['-Mp3SaveAs-'],
                             vals['-Mp3SaveTo-'])

    gui.window.Close()  # Close window and return resources to OS
    logger.info(f'Exiting application...\n{_textborder}')
