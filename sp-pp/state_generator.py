start_time='2018-03-14 10:32:00'
stop_time='2018-03-14 10:36:30'

pp1_vib_f="pp1vib.csv"
loader_vib_f="ldr.csv"
sp_vaf_f="spvaf.csv"
pp1_vaf_f="pp1vaf.csv"

import pandas as pd
from datetime import datetime as dt
import numpy as np

pattern="%Y-%m-%dT%H:%M:%S.%f"
#read required columns from csv
pp1_vibration=pd.read_csv(pp1_vib_f,usecols=['data.timestamp','data.ax'])
loader_vibration=pd.read_csv(loader_vib_f,usecols=['data.timestamp','data.ax'])
pp1_vibration['data.timestamp']=pp1_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp1_vibration.index=pp1_vibration['data.timestamp']
pp1_vibration.sort_index()
loader_vibration['data.timestamp']=loader_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
loader_vibration.index=loader_vibration['data.timestamp']
loader_vibration.sort_index()
sp_vaf=pd.read_csv(sp_vaf_f,usecols=['data.timestamp','data.A1'])
sp_vaf['data.timestamp']=sp_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
sp_vaf.index=sp_vaf['data.timestamp']
sp_vaf.sort_index()
pp1_vaf=pd.read_csv(pp1_vaf_f,usecols=['data.timestamp','data.A1','data.A2','data.A3'])
pp1_vaf['data.timestamp']=pp1_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp1_vaf.index=pp1_vaf['data.timestamp']
pp1_vaf.sort_index()

#Find rolling variances
pp1_vib_var=pd.rolling_var(pp1_vibration[start_time:stop_time]['data.ax'].sort_index(),window=150)
pp1_vaf_var=pd.rolling_var(pp1_vaf[start_time:stop_time]['data.A1'].sort_index(),window=10)
loader_vib_var=pd.rolling_var(loader_vibration[start_time:stop_time]['data.ax'].sort_index(),window=175)


#Generate pp1 states
pp1_vib_var_threshold=pd.DataFrame((pp1_vib_var > 0.00001).astype(np.int_))
pp1_vib_var_threshold.reset_index(level=0, inplace=True)
index=0
state=pp1_vib_var_threshold['data.ax'][0]
anchor=0
count=0
pp1_timeline=[]

#Find Timestamps
print("Pick and Place active state times: ")
for index in range(1,pp1_vib_var_threshold.shape[0]):
    if(pp1_vib_var_threshold['data.ax'][index]!=state):
        update_state=pp1_vib_var_threshold['data.ax'][index-1]
        if (state==1 and update_state==1):
            print('At',pp1_vib_var_threshold['data.timestamp'][anchor],'to',pp1_vib_var_threshold['data.timestamp'][index],'time taken in seconds',pd.Timedelta(pp1_vib_var_threshold['data.timestamp'][index-1]-pp1_vib_var_threshold['data.timestamp'][anchor]).seconds)
            if(pd.Timedelta(pp1_vib_var_threshold['data.timestamp'][index-1]-pp1_vib_var_threshold['data.timestamp'][anchor]).seconds>=75):
                pp1_timeline.append((pp1_vib_var_threshold['data.timestamp'][anchor],pp1_vib_var_threshold['data.timestamp'][index-1]))
                count+=1
        anchor=index
        state=pp1_vib_var_threshold['data.ax'][index]
# print(pp1_vib_var_threshold)


#Generate loader states
loader_vibration_threshold=pd.DataFrame((loader_vib_var>0.00002).astype(np.int_))
names={loader_vibration_threshold.columns[0]:'state'}
loader_vibration_threshold.rename(columns=names,inplace=True)
loader_vibration_threshold.reset_index(level=0, inplace=True)

#Find timestamps
print("Loader loading state times: ")
pp1_timeline=[]
for index in range(1,loader_vibration_threshold.shape[0]):
    if(loader_vibration_threshold['state'][index]!=state):
        update_state=loader_vibration_threshold['state'][index-1]
        if (state==1 and update_state==1):
            print('At',loader_vibration_threshold['data.timestamp'][anchor],'to',loader_vibration_threshold['data.timestamp'][index],'time taken in seconds',pd.Timedelta(loader_vibration_threshold['data.timestamp'][index-1]-loader_vibration_threshold['data.timestamp'][anchor]).seconds)
            if(pd.Timedelta(loader_vibration_threshold['data.timestamp'][index-1]-loader_vibration_threshold['data.timestamp'][anchor]).seconds>=75):
                pp1_timeline.append((loader_vibartion_threshold['data.timestamp'][anchor],loader_vibration_threshold['data.timestamp'][index-1]))
                count+=1
    anchor=index
    state=loader_vibration_threshold['state'][index]
loader_vibration_threshold.reset_index(level=0, inplace=True)

#///////////To get the end timestamp of loading///////This is needed to calculate power consumed while printing
Loading_Finish=[]
index=0
for index in range(0,loader_vibration_threshold.shape[0]-1):

    if index >= loader_vibration_threshold.shape[0]:
        break
    if(loader_vibration_threshold['state'][index]!=loader_vibration_threshold['state'][index+1] and loader_vibration_threshold['state'][index]==0):
        Loading_Finish.append(loader_vibration_threshold['data.timestamp'][index])
loader_vibration_threshold.index=loader_vibration_threshold['data.timestamp']
Loading_Finish.sort()

sp_vaf_threshold=pd.DataFrame((sp_vaf[start_time:stop_time]['data.A1'] > 4).astype(np.int_))
sp_vaf_threshold['data.A1']=sp_vaf_threshold['data.A1']*2 # this just a value to represent a heating state
sp_vaf_threshold.reset_index(level=0,inplace=True)


# To get cleaning state time
print("Loader cleaning state times: ")
index=0
state=sp_vaf_threshold['data.A1'][0]
anchor=0
count=0
total_cleaning_time=pd.Timedelta('00:00:00')
sp_current=[]
for index in range(1,sp_vaf_threshold.shape[0]):
    if(sp_vaf_threshold['data.A1'][index]!=state):
        #update_state=a['data.ax'][index-1]
        if (state==2 and sp_vaf_threshold['data.A1'][index-1]==2):
            startpt=sp_vaf_threshold['data.timestamp'][anchor]
            stoppt=sp_vaf_threshold['data.timestamp'][index]
            delta=sp_vaf_threshold['data.timestamp'][index]-sp_vaf_threshold['data.timestamp'][anchor]
            sp_current.append([sp_vaf_threshold['data.timestamp'][anchor],sp_vaf_threshold['data.timestamp'][index],delta])
            print('At',start,'to',stoppt,'time is',delta.seconds,'seconds.')
            # print(anchor,index,'--------',delta)
            count+=1
            
        anchor=index
        state=sp_vaf_threshold['data.A1'][index]

sp_vaf_threshold.index=sp_vaf_threshold['data.timestamp']
sp_vaf_threshold.rename(columns={'data.A1': 'state'},inplace=True)
sp_states=pd.concat([loader_vibration_threshold,sp_vaf_threshold])
sp_states.sort_index()


loader_power=[]
sp_vaf_threshold.columns.values
sp_cleaning=pd.DataFrame(data=sp_current,columns=['start','stop','time_taken'])

#Calculate averagepower of loader cleaning state:
samples=0
current=0
for i in range(0,sp_cleaning.shape[0]):
    # print((sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values))
    samples+=len(sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values)
    current+=sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values.sum()
    # print(current)
print("Average Power consumed by screen printer in cleaning state: ",current*231/(samples*1000),"kVA.")
