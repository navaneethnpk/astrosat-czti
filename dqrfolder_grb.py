import pandas as pd
import numpy as np
from astropy.time import Time

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/')
dftable = table_dqr[0]

dftable['Date/time start'] = dftable['Date/time start'].str.replace(' ','T')
dftable['Date/time end'] = dftable['Date/time end'].str.replace(' ','T')

orbit_id = dftable['Folder']
obs_id = dftable['OBSID']
start_time = dftable['Date/time start']
end_time = dftable['Date/time end']

dftable_first = dftable.head(100)

time_input = input("Enter the Date & Time (YYYY-MM-DDTHH:MM:SS): ")
given_time = Time(time_input, format='isot', scale='utc')

print(f'               Orbit Folder                           Start                    End        ')
print(f'------------------------------------------------------------------------------------------')
for i in range(len(dftable_first)):
    if len(orbit_id[i]) != 43:
        continue
    start = Time(start_time[i], format='isot', scale='utc')
    end = Time(end_time[i], format='isot', scale='utc')
    if start <= given_time <= end:
        print(f'{orbit_id[i]}    {start_time[i]}  -  {end_time[i]}')