import pandas as pd
import numpy as np
import datetime as dt

table_dqr = pd.read_html('https://web.iucaa.in/~astrosat/czti_dqr/')
#print(f'Total tables: {len(table_dqr)}')

dftable = table_dqr[0]
#print(dftable.head())
#print(dftable.info())

