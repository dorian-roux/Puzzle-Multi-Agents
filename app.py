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
from utils import constructTMP, streamlitButton, generateID
from draw_grid import SaveDrawnGrid

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
        st.session_state['PATH_FOLDER'] = None
        st.session_state['FILL_PRCT'] = 75 # Set the percentage of agents depending on the grid
        st.session_state['LIMIT_TIME'] = 60 * 10 # Set the execution time limit at 10Min
        st.session_state['DISPLAY_TIME'] = 1 # Set the display frequency at 2s
        st.session_state['P_IN_PROGRESS'] = False
        st.session_state['RESET_FOLDER'] = False
        st.session_state['FAST_VALIDATE'] = False
        st.session_state['LIST_IMAGES'] = []
        
    # -- Setup Variables --
    areaPlaceholder = st.empty()
    
    
    if not st.session_state['config']:
        areaPlaceholder.empty()
        with areaPlaceholder:
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
        Agent.agendDict = {}

        Agent.pathFont = 'src/static/fonts/georgia bold.ttf'
        if not st.session_state['PATH_FOLDER']:
            Agent.pathFolder = f'data/tmp_{generateID()}'
            st.session_state['PATH_FOLDER'] = Agent.pathFolder
            if not st.session_state['RESET_FOLDER']:
                if constructTMP(Agent.pathFolder):
                    st.session_state['RESET_FOLDER'] = True
    
        # Initialize the GRID information
        Agent.nbRow, Agent.nbCol = st.session_state['GRID']['N_ROWS'], st.session_state['GRID']['N_COLS']

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
        
        # Save the Initial GRID     
        initTime = time.time()
        isComplete = False
        
        imCount = 0
        SaveDrawnGrid(Agent.nbRow, Agent.nbCol, Agent.agentDict, Agent.pathFont, Agent.pathFolder, imCount)
        ImageInitPath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{Agent.nbRow}_{Agent.nbCol}-Im_{imCount}.png'
       
        try: 
            while not isComplete:
                time.sleep(st.session_state['DISPLAY_TIME'])
                # Verify if the process has reached the TIME LIMIT
                if initTime >= st.session_state['LIMIT_TIME'] * 60:
                    isComplete = True
                
                # Save and Display the current GRID
                # Agent.isMoving.acquire()
                SaveDrawnGrid(Agent.nbRow, Agent.nbCol, Agent.agentDict, Agent.pathFont, Agent.pathFolder, imCount)
                areaPlaceholder.empty()
                ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{Agent.nbRow}_{Agent.nbCol}-Im_{imCount}.png'
                with areaPlaceholder.container():
                    _, col1, _, col2, _ = st.columns([1, 4.5, 1, 4.5, 1])
                    col1.markdown(f"""
                        <div style="text-align:center">
                            <h4 style="font-weight:bold">INITIAL GRID</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    col2.markdown(f"""
                        <div style="text-align:center">
                            <h4 style="font-weight:bold">GRID - N°{imCount}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                    col1.image(ImageInitPath, use_column_width=True)
                    col2.image(ImagePath, use_column_width=True)

                imCount += 1

                # Agent.isMoving.release()
                
                # Verify if the process has reached is COMPLETE FORM
                isComplete = Agent.verifyRunning()
            
            # Turn of the Running
            for agent in AgentList:
                agent.isRunning = False
            
            st.session_state['P_IN_PROGRESS'] = True
            Agent.agentDict = {}
            st.experimental_rerun()
            
        except KeyError: 
            st.session_state['P_IN_PROGRESS'] = True
            Agent.agentDict = {}
            return
            
    # Display ALL IMAGES
    
    areaPlaceholder.empty()
    with areaPlaceholder.container():
        st.write('<hr>', unsafe_allow_html=True)
        st.write('<br>', unsafe_allow_html=True)

        
        _, col1, _, col2, _ = st.columns([1, 4, 2, 4, 1])
        st.session_state['LIST_IMAGES'] = sorted(list(map(lambda fileIm : int(fileIm.split('-Im_')[-1].split('.')[0]), os.listdir(st.session_state["PATH_FOLDER"]))), reverse=False)
        st.session_state['INDEX_LEFT_IMAGE'] = col1.select_slider(label='Select the LEFT IMAGE', options=st.session_state['LIST_IMAGES'], value=st.session_state['LIST_IMAGES'][0])
        st.session_state['INDEX_RIGHT_IMAGE'] = col2.select_slider(label='Select the RIGHT IMAGE', options=st.session_state['LIST_IMAGES'], value=st.session_state['LIST_IMAGES'][-1])
        ImageInitPath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_LEFT_IMAGE"]}.png'
        ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_RIGHT_IMAGE"]}.png'
    
        left = 'INITIAL' if st.session_state['INDEX_LEFT_IMAGE'] == 0 else st.session_state['INDEX_LEFT_IMAGE']
        right = 'INITIAL' if st.session_state['INDEX_RIGHT_IMAGE'] == 0 else st.session_state['INDEX_RIGHT_IMAGE']
        st.markdown(f"""
            <div style="text-align:center">
                <br>
                <h2 style="font-weight:bold">GRID {left} &nbsp; VS &nbsp; GRID {right}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        _, col1, _, col2, _ = st.columns([1, 4, 2, 4, 1])

        col1.markdown(f"""
            <div style="text-align:center">
                <h4 style="font-weight:bold">GRID {left}</h4>
            </div>
        """, unsafe_allow_html=True)
        col2.markdown(f"""
            <div style="text-align:center">
                <h4 style="font-weight:bold">GRID {right}</h4>
            </div>
            """, unsafe_allow_html=True)
        col1.image(ImageInitPath, use_column_width=True)
        col2.image(ImagePath, use_column_width=True)


        if st.button('reconfigure'):
            st.session_state['config'] = False
            st.session_state['P_IN_PROGRESS'] = False
            st.session_state['RESET_FOLDER'] = False
            st.experimental_rerun()
            
  
            
        

# - CORE - 
if __name__ == "__main__":
    main()