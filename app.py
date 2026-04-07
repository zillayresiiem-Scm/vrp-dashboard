import streamlit as st

def route_card():
    # Building HTML status string outside f-string
    tw_status_html = '<p style="color: green;">TW Status: Active</p>'
    return f'<div>{tw_status_html}</div>'

# Main Streamlit application
st.title('VRP Dashboard')
st.write('Welcome to the VRP Dashboard')

if st.button('Show Route Card'):
    st.markdown(route_card(), unsafe_allow_html=True)