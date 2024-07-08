"""
## Purpose
**Main navigation file** containing the links to the subpages: app1, app2, etc. 

## Packages
All used subpages have to be imported:
```python3 linenums="1"
import app1
import app2
import streamlit as st
from hfunc import make_url_link
```
## Key Elements/Variables
### PAGES (dictionary)
The page references are stored in a dictionary:
```python3 linenums="1"
PAGES = {
    'Startpage': app1,
    'Quick Check': app2,
}
```

"""

# Importing packages and subpages
import app1
import app2
import streamlit as st
import func_readability as rc  # here to use make_url_link


## Preparing user manual link
URL = ''
text = 'Link'
link = rc.make_url_link(URL, text)

## Building subpage navigation
PAGES = {
    'Startpage': app1,
    'Quick Check': app2,
}


## Setting up streamlit page config
st.set_page_config(
    page_title="rcBOT",
    # page_icon="",
    layout="centered",  # wide or centered
    initial_sidebar_state="expanded",
)


## Rendering streamlit webpage
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]
st.sidebar.write('')
#st.sidebar.write(f'User Manual: {link}', unsafe_allow_html=True)
page.app()
