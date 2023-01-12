import pandas as pd
import numpy as np
from astropy.time import Time

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/') #Reading the HTML page using pandas
dftable = table_dqr[0] #Selecting the required table

dftable['Date/time start'] = dftable['Date/time start'].str.replace(' ','T') #Replacing "Space" in the start time entry with "T"
dftable['Date/time end'] = dftable['Date/time end'].str.replace(' ','T') #Replacing "Space" in the end time entry with "T"

orbit_id = dftable['Folder'] #Orbit folder name
obs_id = dftable['OBSID'] #Oservation ID
start_time = dftable['Date/time start'] #Orbit start time
end_time = dftable['Date/time end'] #Orbit end time

dftable_first = dftable.head(100) #Selecting first 100 orbits

time_input = input("Enter the Date & Time (YYYY-MM-DDTHH:MM:SS): ") #Asking for GRB trigger time in a specific format
given_time = Time(time_input, format='isot', scale='utc') #Converting the GRB trigger time into Astropy time format

print(f'               Orbit Folder                           Start                    End        ')
print(f'------------------------------------------------------------------------------------------')
for i in range(len(dftable_first)): #looping in the first 100 orbits
    if len(orbit_id[i]) != 43: #checking and accepting orbit id's with character length = 43. Skipping merged entries
        continue
    start = Time(start_time[i], format='isot', scale='utc') #Converting orbit start time to Astropy time format
    end = Time(end_time[i], format='isot', scale='utc') #Converting orbit end time to Astropy time format
    if start <= given_time <= end: #checking the given GRB trigger time is present in the start and end time duration
        print(f'{orbit_id[i]}    {start_time[i]}     {end_time[i]}') #Printing the orbit folder name for the GRB trigger time