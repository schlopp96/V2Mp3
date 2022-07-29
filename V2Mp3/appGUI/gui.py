import PySimpleGUI as psg

__version__ = '0.3.0'

theme = psg.theme('DarkGrey15')

layout: list = [
    # Top Text
    [psg.Text(f'Welcome to V2Mp3 v{__version__}')],
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
                                    do_not_clear=False,
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
                                    'New filename of resulting "*.mp3" file.\nLeave blank for default file name.',
                                    expand_x=True),
                            ],
                            [
                                psg.Checkbox(
                                    'Audio Only',
                                    key='-CB_AudioOnly-',
                                    tooltip=
                                    'Choose whether to download normally (video with audio), or audio ONLY.'
                                )
                            ],
                            [
                                psg.ReadFormButton(
                                    'Download',
                                    button_color=('white', 'green'),
                                    key='-Download-',
                                    tooltip=
                                    'Begin downloading content from YouTube URL.'
                                )
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
                                    'Enter the filepath of the video you wish to convert to an "*.mp3".',
                                    expand_x=True),
                                psg.VerticalSeparator(pad=5),
                                psg.FileBrowse(
                                    s=10,
                                    key='-VideoFileBrowse-',
                                    initial_folder='./downloads/videos/',
                                    target=(psg.ThisRow, -2),
                                    tooltip=
                                    'Browse local system storage for video file to convert to "*.mp3" formatting.'
                                )
                            ],
                            [
                                psg.Text('Save Path:',
                                         s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-Mp3SaveTo-',
                                    do_not_clear=False,
                                    tooltip='Location to save "*.mp3" file.',
                                    expand_x=True),
                                psg.VerticalSeparator(pad=5),
                                psg.FolderBrowse(
                                    s=10,
                                    key='-GetMp3SaveTo-',
                                    initial_folder='./downloads/audio/',
                                    target=(psg.ThisRow, -2),
                                    tooltip=
                                    'Browse for location to save "*.mp3" file to.'
                                )
                            ],
                            [
                                psg.Text('Save As:', s=8,
                                         justification='left'),
                                psg.VerticalSeparator(pad=5),
                                psg.Input(
                                    key='-Mp3SaveAs-',
                                    do_not_clear=False,
                                    tooltip=
                                    'New filename of resulting "*.mp3" file.\nLeave blank for default file name.',
                                    expand_x=True)
                            ],
                            [
                                psg.ReadFormButton(
                                    'Convert',
                                    key='-ConvertToMp3-',
                                    button_color=('white', 'green'),
                                    tooltip=
                                    'Start conversion of the specified video file to "*.mp3" formatting.'
                                )
                            ],
                        ],
                        expand_x=True,
                        element_justification='Center')
                ],
                [
                    # Progress Bar
                    psg.Frame(None,
                              layout=[[
                                  psg.ProgressBar(style='clam',
                                                  k='-ProgressBar-',
                                                  s=(50, 5),
                                                  expand_x=True,
                                                  max_value=100,
                                                  orientation='horizontal')
                              ]],
                              expand_x=True)
                ]
            ],
            expand_x=True)
    ],
    # Event Output Frame
    [
        psg.Frame('Output',
                  layout=[[
                      psg.Multiline(size=(50, 29),
                                    key='-Output-',
                                    disabled=True,
                                    auto_refresh=True,
                                    autoscroll=True,
                                    write_only=True,
                                    expand_x=True,
                                    expand_y=True,
                                    tooltip='Program output.')
                  ]],
                  expand_x=True,
                  expand_y=True),
    ],
    [psg.HorizontalSeparator()],
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
