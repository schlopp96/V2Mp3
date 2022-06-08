from setuptools import setup, find_packages
with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('requirements.txt', 'r') as fh2:
    reqs = fh2.read()

    setup(
        name='V2Mp3',
        version='0.2.0',
        description=
        'Compact video-to-audio conversion tool with built-in YouTube video/audio download functionality.',
        url='https://github.com/schlopp96/V2Mp3',
        author='schlopp96',
        author_email='schloppdaddy@gmail.com',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[reqs],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Multimedia",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Sound/Audio :: Conversion",
            "Topic :: Multimedia :: Video",
            "Topic :: Multimedia :: Video :: Conversion",
            "Topic :: Utilities",
        ],
        keywords=
        'youtube, to, mp3, video, file, convert, converter, download, python, py, python3, audio, conversion, gui, mp4, avi, mpeg, format'
    )
