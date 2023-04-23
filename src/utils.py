import os
import streamlit as st
import shutil
import random
import string
import time


# -- --
def constructTMP(tmpPath):
    if os.path.exists(tmpPath):
        shutil.rmtree(tmpPath)
        print(f'Folder "{tmpPath}" removed')
    os.makedirs(tmpPath, exist_ok=True)
    print(f'Folder "{tmpPath}" created')
    return True
    
    
# -- --
def streamlitButton(txt_col="rgb(255, 255, 255)", txth_col="rgb(0, 0, 0)", bg_col="rgb(204, 49, 49)", bgh_color="rgb(255, 255, 255)"):
    """Modify the intial style of the Streamlit Buttons
    Args:
        txt_col (str, optional): Text color . Defaults to "rgb(255, 255, 255)".
        txth_col (str, optional): Text color when hovering. Defaults to "rgb(0, 0, 0)".
        bg_col (str, optional): Background color. Defaults to "rgb(204, 49, 49)".
        bgh_color (str, optional): Backgrond color when hovering. Defaults to "rgb(255, 255, 255)".
    """
    st.markdown("""
        <style>
            div.stButton {text-align: center;}
            div.stButton > button:first-child {background-color:""" + bg_col + """;color:""" + txt_col + """;}
            div.stButton > button:first-child:hover {background-color:""" + bgh_color + """;color:""" + txth_col + """;}
        </style>
    """, unsafe_allow_html=True)
    
    
# -- -- 
def generateID(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def exitProcess():
    for agent in st.session_state['AGENT_LIST']:
        agent.isRunning = False
    st.session_state['EXEC_TIME'] = round(time.time() - st.session_state['P_INIT_TIME'])
    st.session_state['P_IN_PROGRESS'] = True    
    time.sleep(1) 
    st.experimental_rerun()
            

# -- STREAMLIT related Functions --

def hideRunButton(state=True):
    hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# --- ---
def generateConfigForm():                
    with st.form('form-config'):
        st.markdown("""
        <div style="text-align:center; margin-top:10px; margin-bottom:10px">
            <h3 style="font-size:20px; font-family: monospace; margin-bottom:10px">Configuration of the BOARD</h3>
        </div>
        """, unsafe_allow_html=True)
        
        _, col1, _, col2, _, col3, _ = st.columns([1, 3, 0.5, 3, 0.5, 3, 1])
        col1.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the number of <span style="color:red">ROWS</span></h3>
            </div>
            """, unsafe_allow_html=True)  
        col2.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the number of <span style="color:red">COLUMNS</span></h3>
            </div>
            """, unsafe_allow_html=True)  
        col3.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the <span style="color:red">FILLING PERCENTAGE [%]</span></h3>
            </div>
            """, unsafe_allow_html=True)         
        st.session_state['BOARD']['N_ROWS'] = col1.slider(label='Select the "Row Size"', label_visibility='collapsed', min_value=1, max_value=15, value=5, step=1)
        st.session_state['BOARD']['N_COLS'] = col2.slider(label='Select the "Column Size"', label_visibility='collapsed', min_value=1, max_value=15, value=5, step=1)
        st.session_state['FILL_PRCT'] = col3.slider(label='Select the "Agent Fill Percentage"', label_visibility='collapsed', min_value=50, max_value=100, value=100, step=5)

        st.markdown("""<hr style="width:33%; margin: auto; border: 1px dashed black; margin-top:10px; margin-bottom:10px; border-radius:25px"> """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center; margin-top:10px; margin-bottom:10px">
            <h3 style="font-size:20px; font-family: monospace; margin-bottom:10px">Configuration of the SYSTEM PERFORMANCE</h3>
        </div>
        """, unsafe_allow_html=True)
           
        _, col1, _, col2, _ = st.columns([1.25, 4.5, 0.5, 4.5, 1.25])
        col1.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the <span style="color:red">MAX EXECUTION TIME [min]</span></h3>
            </div>
            """, unsafe_allow_html=True) 
        col2.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the <span style="color:red">DISPLAY FREQUENCY [s]</span></h3>
            </div>
            """, unsafe_allow_html=True)       
        
        st.session_state['LIMIT_TIME'] = col1.number_input(label='Select the "Execution Time Limit in Minute"', label_visibility='collapsed', min_value=1, max_value=60, value=2, step=1)
        st.session_state['DISPLAY_TIME'] = col2.number_input(label='Select the "Display Time Frequency in Seconds"', label_visibility='collapsed', min_value=0.1, max_value=20.0, value=2.0, step=0.1)
        
        if st.form_submit_button('Launch the Puzzle Multi-Agents'):
            return True