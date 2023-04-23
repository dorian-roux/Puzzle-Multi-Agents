from PIL import Image, ImageDraw, ImageFont
import re

def setupImageBoard(nbRow, nbCol):
    borderSize = max(nbRow, nbCol)
    ImGrid = Image.new(size=((nbRow*100) + borderSize, (nbCol*100) + borderSize), mode='RGB', color=(0,0,0,0))
    ImDraw = ImageDraw.Draw(ImGrid)
    ImDraw.rounded_rectangle((0, 0, ImGrid.width, ImGrid.height), fill="white", outline="black", width=borderSize, radius=15)
    return ImGrid

def SaveDrawnBoard(nbRow, nbCol, dictAgents, pathFont, pathFolder, count):
    ImGrid = setupImageBoard(nbRow, nbCol)
    borderSize = max(nbRow, nbCol)

    limitWidth, limitHeight = ImGrid.width * 0.05, ImGrid.height * 0.05
    ImDraw = ImageDraw.Draw(ImGrid)
    ImDraw.rectangle((limitWidth, limitHeight, ImGrid.width - limitWidth, ImGrid.height - limitHeight), fill="white", outline="black", width=round(borderSize/10))
    sizeWidth = (ImGrid.width - (2 * limitWidth))   
    sizeHeight = (ImGrid.height - (2 * limitHeight))
    
    lsAgentsDone = []
    lsAgentsNumb = sorted(list(map(lambda agentPos : str(re.findall(r'Thread-\d+', str(dictAgents[agentPos]))[0].split('-')[-1]), dictAgents.keys())), reverse=False)
    upAgents = {agentNumb : str(agentIndex+1) for agentIndex, agentNumb in enumerate(lsAgentsNumb)}
    for r in range(0, nbRow+1):    
        for c in range(0, nbCol+1):
            initWidth, initHeight = (limitWidth + (r/nbRow) * sizeWidth), (limitHeight + (c/nbCol) * sizeHeight)
            ImDraw.line((initWidth, limitHeight, initWidth, ImGrid.height - limitHeight), fill="black", width=round(borderSize/10))  
            ImDraw.line((limitWidth, initHeight, ImGrid.width - limitWidth, initHeight), fill="black", width=round(borderSize/10))


            minWidth, maxWidth = (limitWidth + (r/nbRow) * sizeWidth), (limitWidth + ((r+1)/nbRow) * sizeWidth)
            minHeight, maxHeight = (limitHeight + (c/nbCol) * sizeHeight), (limitHeight + ((c+1)/nbCol) * sizeHeight)
            middleWidth, middleHeight = minWidth + (maxWidth - minWidth)/2, minHeight + (maxHeight - minHeight)/2 
            if (r, c) in dictAgents:
                content = upAgents[re.findall(r'Thread-\d+', str(dictAgents[(r, c)]))[0].split('-')[-1]]
                if content in lsAgentsDone:
                    continue
                lsAgentsDone.append(content)
                fill = "green" if dictAgents[(r, c)].target == (r, c) else "red"
                font = ImageFont.FreeTypeFont(pathFont, size=25)
                textBox = ImDraw.textbbox((0,0), content, font=font)
                textWidth, textHeight = textBox[2] - textBox[0],  textBox[3]
                ImDraw.text((middleWidth - textWidth/2, middleHeight - textHeight/2), content, fill=fill, font=ImageFont.FreeTypeFont(pathFont, size=25))   
                
    if len(lsAgentsDone) == len(upAgents):
        ImGrid.save(f'{pathFolder}/PuzzleMA-{nbRow}_{nbCol}-Im_{count}.png')
        return True 
    return False

