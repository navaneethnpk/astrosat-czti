import pandas as pd
import numpy as np
from astropy.time import Time
from datetime import datetime, timedelta

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/') #Reading the HTML page using pandas
dftable = table_dqr[0] #Selecting the required table

orbit_id = dftable['Folder'] #Orbit folder name
obs_id = dftable['OBSID'] #Oservation ID
start_time = dftable['Date/time start'] #Orbit start time
end_time = dftable['Date/time end'] #Orbit end time

dftable_first = dftable.head(100) #Selecting first 100 orbits

time_input = input("Enter the Date & Time (YYYY-MM-DD HH:MM:SS): ") #Asking for GRB trigger time in a specific format
given_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M:%S') #Converting the GRB trigger time into time format

print(f'               Orbit Folder                            Start                     End        ')
print(f'--------------------------------------------------------------------------------------------')
for i in range(len(dftable_first)): #looping in the first 100 orbits
    if len(orbit_id[i]) != 43: #checking and accepting orbit id's with character length = 43. Skipping merged entries
        continue
    start = datetime.strptime(start_time[i], '%Y-%m-%d %H:%M:%S') #Converting orbit start time to time format
    end = datetime.strptime(end_time[i], '%Y-%m-%d %H:%M:%S') #Converting orbit end time to time format
    if start <= given_time <= end: #checking the given GRB trigger time is present in the start and end time duration
        print(f'{orbit_id[i][:37]} {orbit_id[i][-5:]}     {start_time[i]}     {end_time[i]}') #Printing the orbit folder name for the GRB trigger time