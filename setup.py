"""A setuptools based setup module.

"""

from setuptools import setup, find_packages

setup(
    name='faqufinoubot',
    version='0.1.0',

    description="""
        Projet python basé sur Slackbot il permet de jouer au cadavre exquis
        """,

    url='https://github.com/ArnaudDroxler/slack-bot-python',

    author='Droxler Arnaud & Joaquim Perez',
    author_email='arnaud.droxler@gmail.com & endive@windowslive.com',

    license='MIT',

    keywords='bot, slackbot, game, cadavre, esquis',

    packages=find_packages(),

    install_requires=['slackclient'],
    extras_requires={
    },

    entry_points={
        'console_scripts': [
            'faqufinoubot=faqufinoubot:main',
        ],
    },
)
