"""
## Purpose
Rendering the startpage displaying the bot name, version and release date.
---
# Functions
"""


# Importing packages
import streamlit as st
import configparser
import func_readability as rc  # here to use make_url_link


# Declaring global parameters
CONFIG_FILE = "resources/rcBOT_config.ini"


def load_config(CONFIG_FILE):
    """Loads the config.ini file and returns the required values.
    
    Args:
        CONFIG_FILE (string): Path to the config file + config file name

    Returns:
        bot_version (string): bot_version
        bot_release_date (string): bot_release_date
    """

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    bot_version = config['VERSIONS']['rcBOT_version']
    bot_release_date = config['VERSIONS']['release_date']

    return (bot_version, bot_release_date)


def app():
    """Main function which renders the streamlit webpage and calls the functions."""
    
    ## Creating link to the user manual
    URL = ''
    text = 'Link'
    link = rc.make_url_link(URL, text)  # create html link

    ## Loading config file
    bot_version, bot_release_date = load_config(CONFIG_FILE)

    # Render streamlit webpage
    st.subheader('rcBOT: Bot for automated readability check')
    st.write(" Made with ❤️ in Swizterland ⛰️​")
    st.write('')
    st.write('')
    st.write('')
    st.write(f'Version: {bot_version}')
    st.write(f'Release date: {bot_release_date}')
