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

dftable_first = dftable.head(200) #Selecting first 100 orbits (This is just to speed up to process)

time_input = input("Enter the Date & Time (YYYY-MM-DD HH:MM:SS): ") #Asking for GRB trigger time in a specific format

# #Using argparse module to give GRB trigger date and time in the command line
# parser = argparse.ArgumentParser(description='Enter the Date & Time (YYYY-MM-DD HH:MM:SS)') #creating the parser
# parser.add_argument('arg1', type=str, help='GRB trigger date') #adding the argument for GRB date
# parser.add_argument('arg2', type=str, help='GRB trigger time') #adding the argument for GRB time
# args = parser.parse_args() #parse the arguments
# time_input = args.arg1 + ' ' + args.arg2 #Connecting the GRB date and time to convert into time format

given_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M:%S') #Converting the GRB trigger time into time format

print(f'               Orbit Folder                            Start                     End        ')
print(f'--------------------------------------------------------------------------------------------')

flag = 0 #Making a flag to print result properly
final_time = datetime.strptime(end_time[0], '%Y-%m-%d %H:%M:%S') #The end time of last uploaded orbit
if given_time > final_time: #checking the GRB trigger time is after the final_time
    print(f'                  The CZTI data for the GRB is not uploaded to DQR yet!')
    flag = 1 #Flag will be 1 when if condition is satisfied.

for i in range(len(dftable_first)): #looping in the first 100 orbits
    if len(orbit_id[i]) != 43: #checking and accepting orbit id's with character length = 43. Skipping merged entries
        continue
    try:
        start = datetime.strptime(start_time[i], '%Y-%m-%d %H:%M:%S') #Converting orbit start time to time format
        end = datetime.strptime(end_time[i], '%Y-%m-%d %H:%M:%S') #Converting orbit end time to time format
    except:
        start = datetime.strptime(start_time[i], '%Y-%m-%d %H-%M-%S') #Converting orbit start time to time format
        end = datetime.strptime(end_time[i], '%Y-%m-%d %H-%M-%S') #Converting orbit end time to time format
    if start <= given_time <= end: #checking the given GRB trigger time is present in the start and end time duration
        print(f'{orbit_id[i][:37]} {orbit_id[i][-5:]}     {start_time[i]}     {end_time[i]}') #Printing the orbit folder name for the GRB trigger time
        flag = 1 #Flag will be 1 when if condition is satisfied.

if flag == 0: #checking the flag value is zero or not
    print(f'     No orbit information: GRB maybe in the data gap. Check and verify it from DQR page.')
