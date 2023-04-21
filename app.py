##############################
# CLIP - SEARCH ENGINE - APP #
##############################


# - IMPORTS -

# -- Add "src" folder to the system Paths --
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.setrecursionlimit(1500)

# -- General Libraries --
import time
import random
import streamlit as st
from src.agentsV2 import Agent
from PIL import ImageFile

# -- Custom Variables and Functions --
from utils import constructTMP, streamlitButton


# - FUNCTION -

# -- MAIN --
def main():
    
    # -- Setup Paths -- 
    staticPath = os.path.join(os.path.dirname(__file__), 'src', 'static')
    
    
    # -- Setup STREAMLIT Page -- 
    config_page_title, config_page_icon, config_layout = 'ING3 IA | Puzzle Multi-Agents', os.path.join(staticPath, 'images', 'iconCYTECH.png'), "wide"
    st.set_page_config(page_title=config_page_title, page_icon=config_page_icon, layout=config_layout)  # Set Page Configuration
    st.markdown("""<style>#MainMenu {visibility: visible;}footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 
    streamlitButton()
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    st.markdown("""
        <div style="text-align:center; margin-top:-50px">
            <h2 style="font-weight:bold; font-size:45px; padding:0px">Puzzle Multi-Agents</h2>
            <h3 style="font-style:italic">CY TECH - AI Engineering Program</h3>
        </div>
        """, unsafe_allow_html=True)
    
    
    # -- Setup the STREAMLIT Seassion State -- 
    if 'config' not in st.session_state:
        st.session_state['config'] = False
        st.session_state['GRID'] = {'N_ROWS': 5, 'N_COLS': 5} # Set the Grid Size at 5x5
        st.session_state['PATH_FOLDER'] = 'tmp'
        st.session_state['FILL_PRCT'] = 75 # Set the percentage of agents depending on the grid
        st.session_state['LIMIT_TIME'] = 60 * 10 # Set the execution time limit at 10Min
        st.session_state['DISPLAY_TIME'] = 1 # Set the display frequency at 2s
        st.session_state['P_IN_PROGRESS'] = False
        st.session_state['RESET_FOLDER'] = False
        st.session_state['FAST_VALIDATE'] = False
        st.session_state['LIST_IMAGES'] = []
        
    # -- Setup Variables --
    if not st.session_state['config']:

        st.subheader('Setup the Configuration')
        with st.form('grid-config'):
            
            st.write('Configuration of the Grid')
            _, col1, _, col2, _ = st.columns([1, 3, 0.25, 3, 1])
            st.session_state['GRID']['N_ROWS'] = col1.slider(label='Select the "Row Size"', label_visibility='visible', min_value=1, max_value=20, value=5, step=1)
            st.session_state['GRID']['N_COLS'] = col2.slider(label='Select the "Column Size"', label_visibility='visible', min_value=1, max_value=20, value=5, step=1)

            st.markdown("""<br>""", unsafe_allow_html=True)
            
            st.write('Limit and Display Frequency')
            _, col1, _, col2, _, col3, _ = st.columns([0.5, 3, 0.5, 3, 0.5, 3, 0.5])
            st.session_state['FILL_PRCT'] = col1.slider(label='Select the "Agent Fill Percentage"', label_visibility='visible', min_value=50, max_value=100, value=75, step=5)
            st.session_state['LIMIT_TIME'] = col2.number_input(label='Select the "Execution Time Limit in Minute"', label_visibility='visible', min_value=1, max_value=60, value=10, step=1)
            st.session_state['DISPLAY_TIME'] = col3.number_input(label='Select the "Display Time Frequency in Seconds"', label_visibility='visible', min_value=0.01, max_value=20.00, value=1.00, step=0.01)
            
            if st.form_submit_button('Launch the Puzzle Multi-Agents'):
                st.session_state['config'] = True
                st.experimental_rerun()
        return 


    # -- Launch the Puzzle Multi-Agents --
    
    # Step by Step
    
    if not st.session_state['P_IN_PROGRESS']:
        Agent.limitTime = st.session_state['LIMIT_TIME'] * 60 
        Agent.displayTime = st.session_state['DISPLAY_TIME'] 
        Agent.pathFolder = 'data/tmp'
        Agent.pathFont = 'src/static/fonts/georgia bold.ttf'
        st.session_state['PATH_FOLDER'] = Agent.pathFolder
        if not st.session_state['RESET_FOLDER']:
            if constructTMP(Agent.pathFolder):
                st.session_state['RESET_FOLDER'] = True
    
        # Initialize the GRID information
        Agent.nbRow, Agent.nbCol = st.session_state['GRID']['N_ROWS'], st.session_state['GRID']['N_COLS']
        Agent.agendDict = {}

        allPosition = [(r,c) for r in range(0,Agent.nbRow) for c in range(0,Agent.nbCol)]

        MAX_AGENT = ((Agent.nbRow) * (Agent.nbCol)) - 1
        NUMBER_AGENT = int(MAX_AGENT * st.session_state['FILL_PRCT']/100)

        allTarget = []
        for _ in range(NUMBER_AGENT):
            target = random.choice(allPosition)
            allPosition.remove(target)
            allTarget.append(target)

        dictInit = Agent.generateInit(allTarget)
        for target, init in dictInit.items():
            agent = Agent(init, target)
            
        AgentList = list(Agent.agentDict.values())
        for agent in AgentList:
            agent.start()
        st.session_state['P_IN_PROGRESS'] = True
        st.experimental_rerun()

    if not Agent.verifyRunning():
        try:
            maxIm = max(list(map(lambda fileIm : int(fileIm.split('-Im_')[-1].split('.')[0]), os.listdir(st.session_state["PATH_FOLDER"]))))
            ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{Agent.nbRow}_{Agent.nbCol}-Im_{maxIm}.png'
            _, col1, _ = st.columns([4, 4, 4])
            col1.image(ImagePath, use_column_width=True)
        except:
            pass
        st.experimental_rerun()
       
    
    # Display ALL IMAGES    
    st.write('<hr>', unsafe_allow_html=True)
    st.write('<br>', unsafe_allow_html=True)
    st.subheader('Display the Puzzle Multi-Agents')
    _, col1, _ = st.columns([4.5,3,4.5])
    st.session_state['LIST_IMAGES'] = sorted(list(map(lambda fileIm : int(fileIm.split('-Im_')[-1].split('.')[0]), os.listdir(st.session_state["PATH_FOLDER"]))), reverse=False)
    st.session_state['INDEX_IMAGE'] = col1.select_slider(label='Find the Image', options=st.session_state['LIST_IMAGES'], value=st.session_state['LIST_IMAGES'][-1])
    ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_IMAGE"]}.png'
    _, col1, _ = st.columns([4, 4, 4])
    col1.markdown(f"""
                  <div style="text-align:center">
                    <h2 style="font-weight:bold">IMAGE {st.session_state['INDEX_IMAGE']}</h2>
                  </div>
                  """, unsafe_allow_html=True)
    try:
        ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_IMAGE"]}.png'
        col1.image(ImagePath, use_column_width=True)
    except:
        ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["LIST_IMAGES"][-2]}.png'
        col1.image(ImagePath, use_column_width=True)

  
    if st.button('reconfigure'):
        st.session_state['config'] = False
        st.session_state['P_IN_PROGRESS'] = False
        st.session_state['RESET_FOLDER'] = False
        Agent.defaultConfig()

        st.experimental_rerun()
        
        
        

# - CORE - 
if __name__ == "__main__":
    main()