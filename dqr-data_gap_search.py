import pandas as pd
import numpy as np
from astropy.time import Time
from datetime import datetime, timedelta
import argparse

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/') #Reading the HTML page using pandas
dftable = table_dqr[0] #Selecting the required table

orbit_id = dftable['Folder'] #Orbit folder name
obs_id = dftable['OBSID'] #Oservation ID
start_time = dftable['Date/time start'] #Orbit start time
end_time = dftable['Date/time end'] #Orbit end time

given_no = int(input('Enter number of orbits to check: ')) #Asking how many orbits to check for data gap

# parser = argparse.ArgumentParser(description='Enter number of orbits to check') #creating the parser
# parser.add_argument('arg1', type=int, help='Number of orbits') #adding the argument
# args = parser.parse_args() #parse the arguments
# given_no = args.arg1

missing = [] 	#created a list to add missing orbits
flag = 0 #Making a flag to print result properly

for i in range(given_no-1): #looping in "given number of orbits - 1"
	if len(orbit_id[i]) != 43: #checking and accepting orbit id's with character length = 43. Skipping merged entries
		continue
	start = datetime.strptime(start_time[i], '%Y-%m-%d %H:%M:%S') #Start time of orbit is converted to time format
	end = datetime.strptime(end_time[i+1], '%Y-%m-%d %H:%M:%S') #End time of previous orbit is converted to time format
	gap = start - end #gap between start time of one orbit and end time of its previous orbit is calculated
	if gap.total_seconds() > 0: #Taking the gap in seconds and checking its greater than 0 seconds
		gap_str = str(gap) #Converting data gap in to string to print in "hours, minutes, seconds"
		m = int(orbit_id[i+1][-5:]) #Saving lower orbit number 
		n = int(orbit_id[i][-5:]) #Saving higher orbit number
		for k in range((n-m)-1): #looping the "difference between to orbits - 1"
			m = m+1 #increasing the lower orbit number
			missing.append(m) #adding the missing orbits in the list. Orbits in bewteen higher and lower orbits will save
		if obs_id[i+1] == obs_id[i]: #if datagap have same oservation ID, then below lines will print
			print(f'--> Data gap in observation {obs_id[i][-4:]} between orbits {orbit_id[i+1][-5:]} and {orbit_id[i][-5:]} of ~ {gap_str[:1]} hours, {gap_str[2:4]} minutes, {gap_str[5:7]} seconds ({gap}).')
			print(f'---- Missing orbits: {missing}.\n')
		else: #if datagap have different oservation ID's, then below lines will print
			print(f'--> Data gap in observations {obs_id[i+1][-4:]} and {obs_id[i][-4:]} between orbits {orbit_id[i+1][-5:]} and {orbit_id[i][-5:]} of ~ {gap_str[:1]} hours, {gap_str[2:4]} minutes, {gap_str[5:7]} seconds ({gap}).')
			print(f'---- Missing orbits: {missing}.\n')
		flag = 1 #Flag will be 1 when if condition is satisfied.
	missing.clear() #clearing the missing orbit list to print new data gap orbits

if flag == 0: #checking the flag value is zero or not
    print(f'There are no data gaps in the given number of orbits')