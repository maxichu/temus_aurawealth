"""AuraWealth — AI Wealth Management Platform."""

import streamlit as st

from lib import config

# Page config
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="",
    layout="wide",
)

# Title
st.title(config.APP_TITLE)

# Placeholder
st.info("AuraWealth platform initialised. Features will be added during the assessment.")
