import pandas as pd
import numpy as np
import datetime as dt

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/')
#print(f'Total tables: {len(table_dqr)}')

dftable = table_dqr[0]
#print(dftable.head())
#print(dftable.info())

orbit_id = dftable['Folder']
obs_id = dftable['OBSID']
start_time = dftable['Date/time start']
end_time = dftable['Date/time end']
for i in range(len(obs_id)):
	if len(orbit_id[i]) == 43:
		print(f"{start_time[i]} - {end_time[i]} - {orbit_id[i]} - {obs_id[i]}")
	else:
		continue
