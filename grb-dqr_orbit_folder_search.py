import pandas as pd
import numpy as np
from astropy.time import Time
from datetime import datetime, timedelta
import argparse

#Reading the HTML page using pandas and selecting the required table and its columns
table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/') 
dftable = table_dqr[0] 
orbit_id = dftable['Folder'] 
obs_id = dftable['OBSID'] 
start_time = dftable['Date/time start'] 
end_time = dftable['Date/time end'] 

dftable_first = dftable.head(200) #Selecting first 100 orbits (This is just to speed up to process)

time_input = input("Enter the Date & Time (YYYY-MM-DD HH:MM:SS): ") #Asking for GRB trigger time in a specific format

# #Using argparse module to give GRB trigger date and time in the command line
# parser = argparse.ArgumentParser(description='Enter the Date & Time (YYYY-MM-DD HH:MM:SS)') 
# parser.add_argument('arg1', type=str, help='GRB trigger date') 
# parser.add_argument('arg2', type=str, help='GRB trigger time') 
# args = parser.parse_args() 
# time_input = args.arg1 + ' ' + args.arg2 

given_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M:%S') 

print(f'\n               Orbit Folder                            Start                     End        ')
print(f'--------------------------------------------------------------------------------------------')

flag = 0 #Making a flag to print result properly
final_time = datetime.strptime(end_time[0], '%Y-%m-%d %H:%M:%S') 
if given_time > final_time:
    print(f'                  The CZTI data for the GRB is not uploaded to DQR yet!')
    flag = 1 

for i in range(len(dftable_first)): 
    if len(orbit_id[i]) != 43 or pd.isnull(obs_id[i]): #Skipping merged entries and red orbit
        continue
    try:
        start = datetime.strptime(start_time[i], '%Y-%m-%d %H:%M:%S') 
        end = datetime.strptime(end_time[i], '%Y-%m-%d %H:%M:%S') 
    except:
        start = datetime.strptime(start_time[i], '%Y-%m-%d %H-%M-%S') 
        end = datetime.strptime(end_time[i], '%Y-%m-%d %H-%M-%S') 
    if start <= given_time <= end: 
        print(f'{orbit_id[i][:37]} {orbit_id[i][-5:]}     {start_time[i]}     {end_time[i]}') 
        flag = 1 

if flag == 0: 
    print(f'     No orbit information: GRB maybe in the data gap. Check and verify it from DQR page.')
