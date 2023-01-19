import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#Reading all the orbit links and making individual links
url = 'https://web.iucaa.in/~astrosat/czti_dqr/' #URL of CZTI-DQR page
page_response = requests.get(url) #Fetching page content
soup = BeautifulSoup(page_response.text, "html.parser") #Parsing page content
links = soup.find_all("a") #finding all the links using "a" tag
linklist = []
for l in links:
    ilink = l.get('href')
    if len(ilink) != 59:
        continue
    url2 = 'https://web.iucaa.in/~astrosat/czti_dqr/' + ilink
    linklist.append(url2)

#Asking for number of orbits to check
nos = int(input("Enter the number of orbits to check: "))
checklist = linklist[0:nos]
print('\n')

for i in range(len(checklist)):
    #Checking URL of each orbits and getting details from tables
    url2 = checklist[i]
    ObsID = url2[54:75]
    OrbitID = url2[83:88]
    tables = pd.read_html(url2)
    modeM0,modeM9,modeSS = tables[1],tables[2],tables[3]
    modeM9_qd,modeM9_tp,modeM9_dp = np.array(modeM9.iloc[:,[0]]),np.array(modeM9.iloc[:,[2]]),np.array(modeM9.iloc[:,[3]])
    modeSS_qd,modeSS_tp,modeSS_dp = np.array(modeSS.iloc[:,[0]]),np.array(modeSS.iloc[:,[2]]),np.array(modeSS.iloc[:,[3]])
    modeM0_qd,modeM0_tp,modeM0_dp = np.array(modeM0.iloc[:,[0]]),np.array(modeM0.iloc[:,[2]]),np.array(modeM0.iloc[:,[3]])
    modeM9_qd,modeSS_qd,modeM0_qd = modeM9_qd.flatten(),modeSS_qd.flatten(),modeM0_qd.flatten() #making 2D array to 1D for better output format
    modeM9_val,modeSS_val,modeM0_val = [],[],[]
    modeM9_val2,modeSS_val2,modeM0_val2 = [],[],[]
    for i in range(4):
        #Calculating Telemetry Error percentage
        modeM9_per = float((modeM9_dp[i]/modeM9_tp[i]) * 100)
        modeSS_per = float((modeSS_dp[i]/modeSS_tp[i]) * 100)
        modeM0_per = float((modeM0_dp[i]/modeM0_tp[i]) * 100)
        modeM9_val.append(modeM9_per)
        modeSS_val.append(modeSS_per)
        modeM0_val.append(modeM0_per)
        #Saving the values into new lists for nice output format
        modeM9_val2.append(f'{modeM9_qd[i]} - {modeM9_per:5.2f}%')
        modeSS_val2.append(f'{modeSS_qd[i]} - {modeSS_per:5.2f}%')
        modeM0_val2.append(f'{modeM0_qd[i]} - {modeM0_per:5.2f}%')
    #Checking Telemetry error is > 5 and printing results accordingly
    if any(value > 5 for value in modeM9_val or modeSS_val or modeM0_val):
        print(f'--> Telemetry Error for ObsID = {ObsID} and OrbitID = {OrbitID}')
        print(f'          Mode M0         Mode M9         Mode SS')
        for j in range(4):
            print(f'       {modeM0_val2[j]}      {modeM9_val2[j]}      {modeSS_val2[j]}')
    else:
        print(f'--> No Telemetry Error for ObsID = {ObsID} and OrbitID = {OrbitID}')