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
from utils import * #constructTMP, streamlitButton, generateID, generateConfigForm
from draw_grid import SaveDrawnGrid

# - FUNCTION -

# -- MAIN --
def main():
    
    # -- Setup the Paths -- 
    staticPath = os.path.join(os.path.dirname(__file__), 'src', 'static')
    pathFont_georgia = os.path.join(staticPath, 'fonts', 'georgia bold.ttf')
    pathImages_logo = os.path.join(staticPath, 'images', 'iconCYTECH.png')
    
    # -- Setup STREAMLIT Page -- 
    config_page_title, config_layout = 'ING3 IA | Puzzle Multi-Agents', "wide"
    st.set_page_config(page_title=config_page_title, page_icon=pathImages_logo, layout=config_layout)  # Set Page Configuration
    st.markdown("""<style>#MainMenu {visibility: visible;}footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 
    streamlitButton()

    # --- Title ---
    st.markdown("""
        <div style="text-align:center; margin-top:-50px; margin-bottom:30px">
            <h1 style="font-weight:bold; font-size:50px; font-family: monospace; padding:0px">Puzzle Multi-Agents</h1>
            <h2 style="font-style:italic; font-size:25px; font-family: monospace; margin-bottom:10px">CY TECH - AI Engineering Program</h2>
            <hr style="width:55%; margin: auto; border: 2px solid red; border-radius:25px"> 
        </div>
        """, unsafe_allow_html=True)
    
    
    # -- Setup the STREAMLIT Seassion State -- 
    if 'CONFIG' not in st.session_state:
        st.session_state['CONFIG'] = False
        st.session_state['GRID'] = {'N_ROWS': 5, 'N_COLS': 5} # Set the Grid Size at 5x5
        st.session_state['FILL_PRCT'] = 75 # Set the percentage of agents depending on the grid
        st.session_state['LIMIT_TIME'] = 120 # Set the execution time limit at 10Min
        st.session_state['DISPLAY_TIME'] = 1 # Set the display frequency at 2s
        st.session_state['P_IN_PROGRESS'] = False
        st.session_state['PATH_FOLDER'] = None
        st.session_state['PATH_FONT'] = pathFont_georgia
        st.session_state['FAST_VALIDATE'] = False
        st.session_state['LIST_IMAGES'] = []
        st.session_state['PATH_INIT_IM'] = ''
        st.session_state['PATH_SLCT_IM'] = ''
        st.session_state['EXEC_TIME'] = "!"
    # -- Setup Variables --
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    areaPlaceholder = st.empty()
    
    
    # -- PHASE_1 - PUZZLE CONFIGURATION --
    if not st.session_state['CONFIG']:
        Agent.agentDict = {}  # Reset the Agent Dictionary (remove any existing threads)
        areaPlaceholder.empty()
        with areaPlaceholder.container():
            st.markdown("""
                <div style="text-align:center; margin-top:10px; margin-bottom:10px">
                    <h3 style="font-size:30px; font-family: monospace; margin-bottom:10px">Phase 1 - Setup the Puzzle Configuration</h3>
                </div>
                """, unsafe_allow_html=True)
            if generateConfigForm():
                st.session_state['CONFIG'] = True
                st.experimental_rerun()
            return 
        
    # -- PHASE_2 - PUZZLE EXECUTION --
    
    # --- PHASE_2_1 - In Progress ---
    if not st.session_state['P_IN_PROGRESS']:
        
        # ---- Construct the TMP Folder ----
        st.session_state['PATH_FOLDER'] = f'data/tmp_{generateID()}'
        constructTMP(st.session_state['PATH_FOLDER'])

        # ---- Launch THREADS ----
        Agent.nbRow, Agent.nbCol = st.session_state['GRID']['N_ROWS'], st.session_state['GRID']['N_COLS']
        allPosition = [(r,c) for r in range(0,Agent.nbRow) for c in range(0,Agent.nbCol)]
        MAX_AGENT = ((Agent.nbRow) * (Agent.nbCol)) - 1
        NUMBER_AGENT = int(MAX_AGENT * st.session_state['FILL_PRCT']/100)
        
        allTarget = random.sample(allPosition, k=NUMBER_AGENT)
        dictInit = Agent.generateInit(allTarget)
        for target, init in dictInit.items():
            agent = Agent(init, target) 
            
        AgentList = list(Agent.agentDict.values())
        for agent in AgentList:
            agent.start()
        

        # ---- Run PROCESS ----
        isComplete = False
        initTime, imCount = time.time(), 0
        SaveDrawnGrid(Agent.nbRow, Agent.nbCol, Agent.agentDict, st.session_state['PATH_FONT'], st.session_state['PATH_FOLDER'], imCount)
        st.session_state['PATH_INIT_IM'] = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{Agent.nbRow}_{Agent.nbCol}-Im_{imCount}.png'
        imCount += 1
        while not isComplete:
            time.sleep(st.session_state['DISPLAY_TIME'])
            if (time.time() - initTime) >= (st.session_state['LIMIT_TIME'] * 60):
                isComplete = True
            
            if SaveDrawnGrid(Agent.nbRow, Agent.nbCol, Agent.agentDict, st.session_state['PATH_FONT'], st.session_state['PATH_FOLDER'], imCount) == True:
                imCount+=1

            areaPlaceholder.empty()
            st.session_state['PATH_SLCT_IM'] = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{Agent.nbRow}_{Agent.nbCol}-Im_{imCount-1}.png'
            with areaPlaceholder.container():
                st.markdown("""
                <div style="text-align:center; margin-top:10px; margin-bottom:10px">
                    <h3 style="font-size:30px; font-family: monospace; margin-bottom:10px">Phase 2 - Puzzle Resolution</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""<hr style="margin-top:20px; margin-bottom:20px; width:33%; margin: auto; border: 1px dashed black; border-radius:25px"> """, unsafe_allow_html=True)
        
                st.markdown(f"""
                <div style="text-align:center; margin-top:10px; margin-bottom:10px">
                    <h3 style="font-size:20px; font-family: monospace; margin-bottom:10px">Process in Progress... (since {round(time.time() - initTime)}s)</h3>
                </div>
                """, unsafe_allow_html=True)
                
                _, col1, _, col2, _ = st.columns([2, 3.5, 1, 3.5, 2])
                col1.markdown(f"""
                    <div style="text-align:center; margin-top:10px; margin-bottom:-20px">
                        <h3 style="font-size:20px; font-family: monospace">Puzzle - <span style="color:red">DEFAULT</span></h3>
                    </div>
                    """, unsafe_allow_html=True)
                col2.markdown(f"""
                    <div style="text-align:center; margin-top:10px; margin-bottom:-20px">
                        <h3 style="font-size:20px; font-family: monospace">Puzzle - <span style="color:red">STEP {imCount}</span></h3>
                    </div>
                    """, unsafe_allow_html=True)                    
                col1.image(st.session_state['PATH_INIT_IM'], use_column_width=True)
                col2.image(st.session_state['PATH_SLCT_IM'], use_column_width=True)
            
            isComplete = Agent.verifyRunning()
        
        SaveDrawnGrid(Agent.nbRow, Agent.nbCol, Agent.agentDict, st.session_state['PATH_FONT'], st.session_state['PATH_FOLDER'], imCount)
        # Turn of the Running
        for agent in AgentList:
            agent.isRunning = False
            
        st.session_state['EXEC_TIME'] = round(time.time() - initTime)
        st.session_state['P_IN_PROGRESS'] = True
        st.experimental_rerun()
            
        
        
    # --- PHASE_2_1 - Display Final ---
    areaPlaceholder.empty()
    with areaPlaceholder.container():
        st.markdown("""
        <div style="text-align:center; margin-top:10px; margin-bottom:10px">
            <h3 style="font-size:30px; font-family: monospace; margin-bottom:10px">Phase Final - COMPARISON</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""<hr style="margin-top:20px; margin-bottom:20px; width:33%; margin: auto; border: 1px dashed black; border-radius:25px"> """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align:center; margin-top:10px; margin-bottom:10px">
            <h3 style="font-size:20px; font-family: monospace; margin-bottom:10px">Puzzles over Time - Display - [Execution Time = {st.session_state['EXEC_TIME']}s]</h3>
        </div>
        """, unsafe_allow_html=True)
        
        _, col1, _, col2, _ = st.columns([2, 3.5, 1, 3.5, 2])
        col1.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the <span style="color:red">LEFT PUZZLE [<]</span></h3>
            </div>
            """, unsafe_allow_html=True)  
        col2.markdown("""
            <div style="text-align:center; margin-top:10px; margin-bottom:-35px">
                <h3 style="font-size:15px; font-family: monospace; margin-bottom:10px">Select the <span style="color:red">RIGHT PUZZLE [>]</span></h3>
            </div>
            """, unsafe_allow_html=True) 
        st.session_state['LIST_IMAGES'] = sorted(list(map(lambda fileIm : int(fileIm.split('-Im_')[-1].split('.')[0]), os.listdir(st.session_state["PATH_FOLDER"]))), reverse=False)
        st.session_state['INDEX_LEFT_IMAGE'] = col1.select_slider(label='Select the LEFT IMAGE', label_visibility='collapsed', options=st.session_state['LIST_IMAGES'], value=st.session_state['LIST_IMAGES'][0])
        st.session_state['INDEX_RIGHT_IMAGE'] = col2.select_slider(label='Select the RIGHT IMAGE', label_visibility='collapsed', options=st.session_state['LIST_IMAGES'], value=st.session_state['LIST_IMAGES'][-1])
        ImageInitPath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_LEFT_IMAGE"]}.png'
        ImagePath = f'{st.session_state["PATH_FOLDER"]}/PuzzleMA-{st.session_state["GRID"]["N_ROWS"]}_{st.session_state["GRID"]["N_COLS"]}-Im_{st.session_state["INDEX_RIGHT_IMAGE"]}.png'
        
        left = 'INITIAL' if st.session_state['INDEX_LEFT_IMAGE'] == 0 else st.session_state['INDEX_LEFT_IMAGE']
        right = 'INITIAL' if st.session_state['INDEX_RIGHT_IMAGE'] == 0 else st.session_state['INDEX_RIGHT_IMAGE']
        
        _, col1, col3, col2, _ = st.columns([2, 3, 1, 3, 2])
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
        col3.markdown(f"""
            <div style="text-align:center">
                <h4 style="font-weight:bold">COMPARED WITH</h4>
            </div>
            """, unsafe_allow_html=True)
        col1.image(ImageInitPath, use_column_width=True)
        col2.image(ImagePath, use_column_width=True)


    st.markdown("""<br>""", unsafe_allow_html=True)
    if st.button('NEW CONFIGURATION'):
        st.session_state['CONFIG'] = False
        st.session_state['P_IN_PROGRESS'] = False
        shutil.rmtree(st.session_state["PATH_FOLDER"])
        Agent.agentDict = {} 
        st.experimental_rerun()

        
    

# - CORE - 
if __name__ == "__main__":
    main()