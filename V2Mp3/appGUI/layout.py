import PySimpleGUI as psg

theme = psg.theme('DarkGrey11')

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

window: psg.Window = psg.Window('V2Mp3',
                                layout=appLayout,
                                auto_size_buttons=True,
                                text_justification='Center',
                                element_justification='Center',
                                resizable=True,
                                finalize=True)
