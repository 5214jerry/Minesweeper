from ctypes import sizeof
from glob import glob
from turtle import left
from xml.sax.handler import property_encoding
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options=Options()
PATH="Minesweeper/chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH,chrome_options=options)
driver.get("https://minesweeperonline.com/")
driver.maximize_window()

finishedcell = set()
board = list()
readedcell = set()
for i in range(480):
    board.append(int(999))

flags = set()
clicks = set()
table = list()
tmptable = driver.find_elements(By.CLASS_NAME,"square.blank")
for i in range(480):
    table.append(tmptable[i])

table[0].click()
time.sleep(1)
randomopen = False
while len(finishedcell) != 480:
    time.sleep(0.4)
    # print(flags)

    #插旗
    for index in flags:
        actionR = ActionChains(driver)
        actionR.context_click(table[index]).perform()
        board[index] = 10
        for i in (-31,-30,-29,-1,1,29,30,31):
            if index+i>=480 or index+i<0:
                continue
            if (index+1)%30 == 0 and (i in (-29,1,31)):
                continue
            if index%30 == 0 and (i in (-31,-1,29)):
                continue
            board[index+i] = board[index+i]-1

    #採雷
    clicks = clicks - flags
    flags = set()
    for index in clicks:
        # print("click="+str(index))
        table[index].click()
    clicks = set()

    for i in range(0,9):
        blocks =  driver.find_elements(By.CLASS_NAME,"open"+str(i))
        # print(len(blocks))
        for block in blocks:
            if block in readedcell:
                continue
            idstr = block.get_attribute("id").split('_',1)
            # print(idstr)
            row = int(idstr[1])-1
            column = int(idstr[0])-1
            index = 30*column+row
            bombnumber=block.get_attribute("class").replace("square ","")
            print(bombnumber)
            bombnumber=int(bombnumber.replace("open",""))
            print("bombnumber="+str(bombnumber))
            if bombnumber == 0:
                finishedcell.add(index)
            board[index] = board[index]-int(999)+bombnumber
            readedcell.add(block)
        
        for index in range(0,480):
            if index in finishedcell:
                continue
            block = board[index]
            if block>=9:
                continue
            if block <= 0:
                for i in (-31,-30,-29,-1,1,29,30,31):
                    if index+i>=480 or index+i<0:
                        continue
                    if (index+1)%30 == 0 and (i in (-29,1,31)):
                        continue
                    if index%30 == 0 and (i in (-31,-1,29)):
                        continue
                    if board[index+i] <= 10:
                        continue
                    table[index+i].click()
                    print("click="+str(index))
                finishedcell.add(index)
                continue
            uc = 0 #unopen_count
            tmpflags = set()
            sideopened = set()
            for i in (-31,-30,-29,-1,1,29,30,31):
                if index+i>=480 or index+i<0:
                    continue
                if (index+1)%30 == 0 and (i in (-29,1,31)):
                    continue
                if index%30 == 0 and (i in (-31,-1,29)):
                    continue
                if board[index+i] >= 100 :
                    uc = uc+1
                    tmpflags.add(index+i)
                    continue
                if board[index+i] <=9 and board[index+i]>=1 and i in(-30,-1,1,30):
                    sideopened.add(index+i)
                    continue

            if uc == block:
                flags = flags | tmpflags
                continue
            
            sideopened = sideopened - finishedcell
            if uc == block+1:
                # print(sideopened)
                for index2 in sideopened:
                    check = 0
                    fc2 = 0
                    uc2 = 0
                    tmpclicks = set()
                    for i in (-31,-30,-29,-1,1,29,30,31):
                        if index2+i>=480 or index2+i<0:
                            continue
                        if (index2+1)%30 == 0 and (i in (-29,1,31)):
                            continue
                        if index2%30 == 0 and (i in (-31,-1,29)):
                            continue
                        if index2+i in tmpflags:
                            check = check+1
                            continue
                        if board[index2+i] == 10:
                            fc2 = fc2+1
                            continue
                        if board[index2+i] >= 100:
                            uc2 = uc2+1
                            tmpclicks.add(index2+i)
                            continue
                    if board[index2]-1 <= 0 and check >=2:
                        clicks = clicks | tmpclicks
                        continue
                    if board[index2]-1 == uc2 and check >=2 and uc == 2:
                        flags = flags | tmpclicks
