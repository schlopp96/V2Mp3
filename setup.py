from setuptools import setup, find_packages
with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('requirements.txt', 'r') as fh2:
    reqs = fh2.read()

    setup(
        name='V2Mp3',
        version='0.0.1',
        description='Converter for Youtube video files to mp3 audio format.',
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
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Utilities",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
        keywords=
        'youtube to mp3 video file convert converter download python py python3 audio'
    )
