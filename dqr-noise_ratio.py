import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 	

url = 'https://web.iucaa.in/~astrosat/czti_dqr/' #URL of CZTI-DQR page
page_response = requests.get(url) #Fetching page content
soup = BeautifulSoup(page_response.text, "html.parser") #Parsing page content
links = soup.find_all("a") #finding all the links using "a" tag

#Reading all the orbit links and making individual links
linklist = []
for l in links:
	ilink = l.get('href')
	if len(ilink) != 59:
		continue
	url2 = 'https://web.iucaa.in/~astrosat/czti_dqr/' + ilink
	linklist.append(url2)

#Asking for number of orbits to check; Printing Header info
nos = int(input("Enter the number of orbits to check: "))
print('\n')
print('------------------Noise Ratio--------------------')
print(' ObsID    OrbitID     Quadrant     DetID   PixID')
print('-------------------------------------------------')

checklist = linklist[0:nos]
ObsID_val,OrbitID_val,noise_val,DetID_val,PixID_val = [],[],[],[],[]
flag = 0

for i in range(len(checklist)):
	#Checking URL of each orbits and getting details from tables
	url2 = checklist[i]
	ObsID = url2[71:75]
	OrbitID = url2[83:88]
	tables = pd.read_html(url2)
	noise_table = tables[5]
	noise = noise_table['Noise dominated (detector-on time)'].replace({'%':''}, regex=True).astype('float')
	quadrant = noise_table['Quadrant']
	noisepix_table = tables[6]
	DetID = np.array(noisepix_table.iloc[:,[1]])
	PixID = np.array(noisepix_table.iloc[:,[2]])
	for i in range(4):
		if noise[i] >= 5.0:
			ObsID_val.append(ObsID)
			OrbitID_val.append(OrbitID)
			noise_val.append(f'{quadrant[i]} = {noise[i]}%')
			if quadrant[i] == 'A':
				DetID_val.append(int(DetID[0]))
				PixID_val.append(int(PixID[0]))
			elif quadrant[i] == 'B':
				DetID_val.append(int(DetID[3]))
				PixID_val.append(int(PixID[3]))
			elif quadrant[i] == 'C':
				DetID_val.append(int(DetID[6]))
				PixID_val.append(int(PixID[6]))
			elif quadrant[i] == 'D':
				DetID_val.append(int(DetID[9]))
				PixID_val.append(int(PixID[9]))
			flag = 1
# Printing the Noise Ratio columns in reverse order
for j in range(len(ObsID_val)):
	print(f' {ObsID_val[j]}     {OrbitID_val[j]}      {noise_val[j].ljust(10)}      {DetID_val[j]}     {PixID_val[j]}')
if flag == 0: 
    print(f'There are no noise ratio to show for this given number of orbits!')