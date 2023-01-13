import pandas as pd
import numpy as np
from astropy.time import Time
from datetime import datetime, timedelta

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/')
dftable = table_dqr[0]

orbit_id = dftable['Folder']
obs_id = dftable['OBSID']
start_time = dftable['Date/time start']
end_time = dftable['Date/time end']

given_no = int(input('Enter number of orbits to check: '))

missing = []
for i in range(given_no-1):
	if len(orbit_id[i]) != 43: #checking and accepting orbit id's with character length = 43. Skipping merged entries
		continue
	start = datetime.strptime(start_time[i], '%Y-%m-%d %H:%M:%S')
	end = datetime.strptime(end_time[i+1], '%Y-%m-%d %H:%M:%S')
	gap = start - end
	#print(f'{start} - {end} = {gap}')
	if gap.total_seconds() > 0:
		gap_str = str(gap)
		m = int(orbit_id[i+1][-5:])
		n = int(orbit_id[i][-5:])
		for k in range((n-m)-1):
			m = m+1
			missing.append(m)
		if obs_id[i+1] == obs_id[i]:
			print(f'--> Data gap in obervation {obs_id[i][-4:]} between orbits {orbit_id[i+1][-5:]} and {orbit_id[i][-5:]} of ~ {gap_str[:1]} hours, {gap_str[2:4]} minutes, {gap_str[5:7]} seconds ({gap}).')
			print(f'---- Missing orbits: {missing}.\n')
		else:
			print(f'--> Data gap in obervations {obs_id[i+1][-4:]} and {obs_id[i][-4:]} between orbits {orbit_id[i+1][-5:]} and {orbit_id[i][-5:]} of ~ {gap_str[:1]} hours, {gap_str[2:4]} minutes, {gap_str[5:7]} seconds ({gap}).')
			print(f'---- Missing orbits: {missing}.\n')
	missing.clear()
