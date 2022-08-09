import PySimpleGUI as psg

__version__ = '0.3.0'  # Current program version

theme = psg.theme('DarkGrey15')

layout: list = [
    # Top Text
    [psg.Text(f'V2Mp3 v{__version__}')],
    [psg.HorizontalSeparator()],
    [
        psg.Frame(
            None,
            layout=[
                # Download Frame
                [
                    psg.Frame(
                        'Download YouTube Video/Audio',
                        layout=[
                            [
                                psg.Text(
                                    'Enter URL of YouTube Video to Download.')
                            ],
                            [
                                psg.Text('URL:', s=8, justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-URLInput-',
                                    do_not_clear=False,
                                    tooltip=
                                    'Enter the web URL of the content you wish to download.',
                                    expand_x=True),
                            ],
                            [
                                psg.Text('Save Path:',
                                         s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-YTSaveTo-',
                                    do_not_clear=True,
                                    tooltip='Location to save downloaded file.',
                                    expand_x=True),
                                psg.VerticalSeparator(pad=5),
                                psg.FolderBrowse(
                                    s=10,
                                    key='-GetYTSaveTo-',
                                    initial_folder='./downloads/videos/',
                                    target=(psg.ThisRow, -2),
                                    tooltip=
                                    'Browse for location to save YouTube download.'
                                )
                            ],
                            [
                                psg.Text('Save As:', s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-YTSaveAs-',
                                    do_not_clear=False,
                                    tooltip=
                                    'Save name of downloaded file.\nLeave blank for default file name.',
                                    expand_x=True),
                            ],
                            [
                                psg.Checkbox(
                                    'Audio Only',
                                    key='-ToggleAudioDL-',
                                    tooltip=
                                    'Toggle downloading content as video or audio ONLY.'
                                )
                            ],
                            [
                                psg.ReadFormButton('Download',
                                                   button_color=('white',
                                                                 'green'),
                                                   key='-Download-',
                                                   tooltip='Start download.')
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
                                psg.Text('Filepath:',
                                         s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-FileInput-',
                                    do_not_clear=False,
                                    tooltip=
                                    'Enter filepath of video to convert to ".mp3" format.',
                                    expand_x=True),
                                psg.VerticalSeparator(pad=5),
                                psg.FileBrowse(
                                    s=10,
                                    key='-VideoFileBrowse-',
                                    initial_folder='./downloads/videos/',
                                    target=(psg.ThisRow, -2),
                                    tooltip=
                                    'Browse local storage for video file to convert to ".mp3" format.'
                                )
                            ],
                            [
                                psg.Text('Save Path:',
                                         s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-Mp3SaveTo-',
                                    do_not_clear=True,
                                    tooltip='Location to save ".mp3" file.',
                                    expand_x=True),
                                psg.VerticalSeparator(pad=5),
                                psg.FolderBrowse(
                                    s=10,
                                    key='-GetMp3SaveTo-',
                                    initial_folder='./downloads/audio/',
                                    target=(psg.ThisRow, -2),
                                    tooltip=
                                    'Choose save location of ".mp3" file.')
                            ],
                            [
                                psg.Text('Save As:', s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-Mp3SaveAs-',
                                    do_not_clear=False,
                                    tooltip=
                                    'Save name of resulting ".mp3" file.\nLeave blank for default file name.',
                                    expand_x=True)
                            ],
                            [
                                psg.ReadFormButton(
                                    'Convert',
                                    key='-ConvertToMp3-',
                                    button_color=('white', 'green'),
                                    tooltip=
                                    'Start conversion of video file to ".mp3" format.'
                                )
                            ],
                        ],
                        expand_x=True,
                        element_justification='Center')
                ],
            ],
            expand_x=True)
    ],
    [psg.HorizontalSeparator(pad=5)],
    [
        # Progress Bar
        [
            psg.ProgressBar(style='clam',
                            k='-ProgBar-',
                            s=(50, 5),
                            expand_x=True,
                            max_value=100,
                            orientation='horizontal')
        ]
    ],
    [psg.HorizontalSeparator(pad=5)],
    # Event Output Frame
    [
        psg.Frame('Output',
                  layout=[[
                      psg.Multiline(size=(50, 28),
                                    key='-Output-',
                                    disabled=True,
                                    auto_refresh=True,
                                    autoscroll=True,
                                    write_only=True,
                                    expand_x=True,
                                    expand_y=True,
                                    tooltip='Program task output.')
                  ]],
                  expand_x=True,
                  expand_y=True),
    ],
    [psg.HorizontalSeparator()],
    # Bottom Row
    [
        psg.Exit(button_color=('white', 'red'), tooltip='Exit application.'),
    ]
]

window: psg.Window = psg.Window('V2Mp3',
                                layout=layout,
                                auto_size_buttons=True,
                                text_justification='Center',
                                element_justification='Center',
                                resizable=True)
