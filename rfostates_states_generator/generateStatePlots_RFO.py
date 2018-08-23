import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import os
import sys

if len(sys.argv) <  2:
	print("No filename passed. Place the CSV file in the same folder.")
	exit(2)
rffile=sys.argv[1]
if not os.path.isfile(rffile):
	print("File not found!")
	exit(1)
try:
	dfp = pd.read_csv(rffile, usecols =['timestamp', 'data.A1', 'data.A2', 'data.A3'], parse_dates = ['timestamp'])
except:
	print("Invalid file!")

# dfp.dropna(subset = ['data.A1', 'data.A2', 'data.A3'])
pattern="%Y-%m-%dT%H:%M:%S.%f"
# dfp['timestamp'] =  pd.to_datetime(dfp['timestamp'], format=pattern)

dfp.sort_values('timestamp', inplace = True)
dfp['timestamp'] = dfp['timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))


dfp1=dfp[['timestamp', 'data.A1']]

dfp2=dfp[['timestamp', 'data.A2']]

dfp3=dfp[['timestamp', 'data.A3']]

# dfp1['timestamp'] = dfp1['timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
dfp1.index = dfp1['timestamp']
# dfp2['timestamp'] = dfp2['timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
dfp2.index = dfp2['timestamp']
# dfp3['timestamp'] = dfp3['timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
dfp3.index = dfp3['timestamp']

maxcur1 = dfp1['data.A1'].max()
maxcur2 = dfp2['data.A2'].max()
maxcur3 = dfp3['data.A3'].max()

#pointwise state for phase1 data
statep1 = pd.DataFrame(columns = ['timestamp', 'current', 'state'])
statep1['timestamp'] = dfp1['timestamp']
statep1['current'] = dfp1['data.A1']
statep1['state'] = np.where(dfp1['data.A1'] <= 1.5, 0, statep1['state'])
statep1['state'] = np.where(dfp1['data.A1'] >= .75 * maxcur1, 2, statep1['state'])
statep1['state'] = np.where((dfp1['data.A1'] <= .75 * maxcur1) & (dfp1['data.A1'] > 1.5), 1, statep1['state'])
#pointwise state for phase2 data
statep2 = pd.DataFrame(columns = ['timestamp', 'current', 'state'])
statep2['timestamp'] = dfp2['timestamp']
statep2['current'] = dfp2['data.A2']
statep2['state'] = np.where(dfp2['data.A2'] <= 1.5, 0, statep2['state'])
statep2['state'] = np.where(dfp2['data.A2'] >= .75 * maxcur2, 2, statep2['state'])
statep2['state'] = np.where((dfp2['data.A2'] <= .75 * maxcur2) & (dfp2['data.A2'] > 1.5), 1, statep2['state'])
#pointwise state for phase3 data
statep3 = pd.DataFrame(columns = ['timestamp', 'current', 'state'])
statep3['timestamp'] = dfp3['timestamp']
statep3['current'] = dfp3['data.A3']
statep3['state'] = np.where(dfp3['data.A3'] <= 1.5, 0, statep3['state'])
statep3['state'] = np.where(dfp3['data.A3'] >= .75 * maxcur3, 2, statep3['state'])
statep3['state'] = np.where((dfp3['data.A3'] <= .75 * maxcur3) & (dfp3['data.A3'] > 1.5), 1, statep3['state'])

# statep1.to_csv('statep1.csv')
# statep2.to_csv('statep2.csv')
# statep3.to_csv('statep3.csv')
directory=rffile[0:-4]
print('Now generating plots for '+directory+'.')
directory+='_plots'
if not os.path.exists(directory):
    os.makedirs(directory)


fig, ax = plt.subplots()
fig.set_size_inches(10,5)
ax.plot(statep1['current'], color='r', label='Phase 1', alpha=0.5)
ax.plot(statep2['current']+60, color='g', label='Phase 2', alpha=0.5)
ax.plot(statep3['current']+120, color='b', label='Phase 3', alpha=0.5)
ax.set_xlabel('Time')
ax.set_ylabel('Current in Amps. (60A offset between phases.)')
plt.legend()
plt.title('Raw Current Data Plot')
# plt.show()
fig.savefig(directory+'/Raw Current Data Plot.png')


# In[5]:


maxcur1 = statep1['current'].max()
print(maxcur1)
maxcur2 = statep2['current'].max()
print(maxcur2)
maxcur3 = statep3['current'].max()
print(maxcur3)
# maxcur = max(maxcur1, maxcur2, maxcur3)
maxcur=62.0
roll_width = 275
cur1 = pd.Series.to_frame(statep1.current.rolling(roll_width, center=True).mean())
cur2 = pd.Series.to_frame(statep1.current.rolling(roll_width, center=True).mean())
cur3 = pd.Series.to_frame(statep1.current.rolling(roll_width, center=True).mean())
st1 = pd.Series.to_frame(statep1.state.rolling(roll_width, center=True).mean())
st2 = pd.Series.to_frame(statep1.state.rolling(roll_width, center=True).mean())
st3 = pd.Series.to_frame(statep1.state.rolling(roll_width, center=True).mean())


# In[6]:


#blockwise state for phase1 data
st1['state'] = np.where(cur1['current'] <= 1.5, 0, st1['state'])
st1['state'] = np.where(cur1['current'] >= .42 * maxcur, 2, st1['state'])
st1['state'] = np.where((cur1['current'] <= .42 * maxcur) & (cur1['current'] > 1.5), 1, st1['state'])
#blockwise state for phase2 data
st2['state'] = np.where(cur2['current'] <= 1.5, 0, st2['state'])
st2['state'] = np.where(cur2['current'] >= .42 * maxcur, 2, st2['state'])
st2['state'] = np.where((cur2['current'] <= .42 * maxcur) & (cur2['current'] > 1.5), 1, st2['state'])
#blockwise state for phase3 data
st3['state'] = np.where(cur3['current'] <= 1.5, 0, st3['state'])
st3['state'] = np.where(cur3['current'] >= .42 * maxcur, 2, st3['state'])
st3['state'] = np.where((cur3['current'] <= .42 * maxcur) & (cur3['current'] > 1.5), 1, st3['state'])


# In[7]:


pow1 = cur1
pow1['state']=st1['state']
pow1['power'] = 231 * cur1['current']
pow2 = cur2
pow2['state']=st2['state']
pow2['power'] = 231 * cur2['current']
pow3 = cur3
pow3['state']=st3['state']
pow3['power'] = 231 * cur3['current']


# In[8]:


fig, ax = plt.subplots()
fig.set_size_inches(10,5)
ax.plot(pow1['current'], color='r', label='Phase 1', alpha=0.5)
ax.plot(pow2['current']+60, color='g', label='Phase 2', alpha=0.5)
ax.plot(pow3['current']+120, color='b', label='Phase 3', alpha=0.5)
ax.set_xlabel('Time')
ax.set_ylabel('Current in Amps. (60A offset between phases.)')
plt.legend()
plt.title('After Applying a Rolling Mean Function')
# plt.show()
fig.savefig(directory+'/After Applying a Rolling Mean Function.png')



# In[9]:


#phase 1 states
fig, ax1 = plt.subplots()
fig.set_size_inches(10,5)
ax1.plot(pow1['current'],color='orange')
ax1.xaxis.set_major_locator(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time')
ax1.set_ylabel('Current in Amps.', color='orange')
ax1.set_yticks(np.arange(0, 80, step=10))
ax1.tick_params('y', colors='orange')
ax2 = ax1.twinx()
ax2.plot(pow1['state'], 'r-', color='purple', alpha=0.5)
ax2.set_ylabel('State', color='purple')
ax2.tick_params('y', colors='purple')
ax2.set_yticks(np.arange(0, 3, step=1))
# ax2.set_yticks(np.arange(3), ('Off', 'Maintain', 'Heating'))
plt.title('Phase 1 States')
# plt.show()
plt.savefig(directory+'/Phase 1 States.png')

# In[10]:


# phase 2 states
fig, ax1 = plt.subplots()
fig.set_size_inches(10,5)
ax1.plot(pow2['current'],color='orange')
ax1.xaxis.set_major_locator(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time')
ax1.set_ylabel('Current in Amps.', color='orange')
ax1.tick_params('y', colors='orange')
ax1.set_yticks(np.arange(0, 80, step=10))
ax2 = ax1.twinx()
ax2.plot(pow2['state'], 'r-', color='purple', alpha=0.5)
ax2.set_ylabel('State', color='purple')
ax2.tick_params('y', colors='purple')
ax2.set_yticks(np.arange(0, 3, step=1))
# ax2.set_yticks(np.arange(3), ('Off', 'Maintain', 'Heating'))
# ax2.fill_betweenx(0,2, facecolor='green', alpha=0.3)
plt.title('Phase 2 States')
# plt.show()
plt.savefig(directory+'/Phase 2 States.png')

# In[11]:


#phase 3 states
fig, ax1 = plt.subplots()
fig.set_size_inches(10,5)
ax1.plot(pow3['current'], color='orange')
ax1.xaxis.set_major_locator(mdates.DateFormatter('%H:%M'))
ax1.set_xlabel('Time')
ax1.set_ylabel('Current in Amps.', color='orange')
ax1.set_yticks(np.arange(0, 80, step=10))
ax1.tick_params('y', colors='orange')
ax2 = ax1.twinx()
ax2.plot(pow3['state'], 'r-', color='purple', alpha=0.5)
ax2.set_ylabel('State', color='purple')
ax2.tick_params('y', colors='purple')
ax2.set_yticks(np.arange(0, 3, step=1))
# ax2.set_yticks(np.arange(3), ('Off', 'Maintain', 'Heating'))
plt.title('Phase 3 States')
# plt.show()
plt.savefig(directory+'/Phase 3 States.png')
