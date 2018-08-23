
#CSV filenames
filename="pp1vib.csv"
pp2_vib_csv="pp2vib.csv"
loader_vib_file="ldr.csv"
sp_vaf_csv="spvaf.csv"
pp1_vaf_csv="pp1vaf.csv"
pp2_vaf_csv="pp2vaf.csv"


# Define start and stop times

start_time='2018-03-14 10:32:00'  #For 14th March
stop_time='2018-03-14 10:40:00'

'''
______USE THESE START STOP TIMES_________

start_time='2018-03-14 10:32:00'  #For 14th March
stop_time='2018-03-14 10:40:00'


start_time='2018-03-17 09:32:00'  #For 17th March
stop_time='2018-03-17 10:56:00'



start_time='2018-03-20 14:48:00'  #for 20th March
stop_time='2018-03-20 14:58:00'




'''
import pandas as pd
from datetime import datetime as dt
import numpy as np

pattern="%Y-%m-%dT%H:%M:%S.%f"

# Load CSVs into DF
pp1_vibration=pd.read_csv(filename,usecols=['data.timestamp','data.ax'])
pp2_vibration=pd.read_csv(pp2_vib_csv,usecols=['data.timestamp','data.ax'])
loader_vibration=pd.read_csv(loader_vib_file,usecols=['data.timestamp','data.ax'])
pp1_vibration['data.timestamp']=pp1_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp1_vibration.index=pp1_vibration['data.timestamp']
pp2_vibration['data.timestamp']=pp2_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp2_vibration.index=pp2_vibration['data.timestamp']
loader_vibration['data.timestamp']=loader_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
loader_vibration.index=loader_vibration['data.timestamp']
sp_vaf=pd.read_csv(sp_vaf_csv,usecols=['data.timestamp','data.A1'])
sp_vaf['data.timestamp']=sp_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
sp_vaf.index=sp_vaf['data.timestamp']
sp_vaf.sort_index()
pp1_vaf=pd.read_csv(pp1_vaf_csv,usecols=['data.timestamp','data.A1','data.A2','data.A3'])
pp1_vaf['data.timestamp']=pp1_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp1_vaf.index=pp1_vaf['data.timestamp']
pp1_vaf.sort_index()
pp2_vaf=pd.read_csv(pp2_vaf_csv,usecols=['data.timestamp','data.A1','data.A2','data.A3'])
pp2_vaf['data.timestamp']=pp2_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
pp2_vaf.index=pp2_vaf['data.timestamp']
pp2_vaf.sort_index()


# Calculate variances

vib_var=(pd.rolling_var(pp1_vibration[start_time:stop_time]['data.ax'].sort_index(),window=150))
pp2_vib_var=(pd.rolling_var(pp2_vibration[start_time:stop_time]['data.ax'].sort_index(),window=150))
#variance of loader vibration
loader_vib_var=pd.rolling_var(loader_vibration[start_time:stop_time]['data.ax'].sort_index(),window=175)
#variance of current in One phase
pp1_I_var=pd.rolling_var(pp1_vaf[start_time:stop_time]['data.A1'].sort_index(),window=10)
# store loader vibration variance series in dataframe a
a=pd.DataFrame((vib_var > 0.00001).astype(np.int_))
# store loader vibration variance series in dataframe a
pp2_vibration_threshold=pd.DataFrame((pp2_vib_var > 0.00005).astype(np.int_))
pp2_vibration_threshold.reset_index(level=0, inplace=True)
a.reset_index(level=0, inplace=True)
#To get the count based on time of vibration for pickandplace1, 
index=0
state=a['data.ax'][0]
anchor=0
count=0
pp1_timeline=[]
for index in range(1,a.shape[0]):
    if(a['data.ax'][index]!=state):
        update_state=a['data.ax'][index-1]
        if (state==1 and update_state==1):
            if(pd.Timedelta(a['data.timestamp'][index-1]-a['data.timestamp'][anchor]).seconds>=75):
                print('At',a['data.timestamp'][anchor],'to',a['data.timestamp'][index],'time taken in seconds',pd.Timedelta(a['data.timestamp'][index-1]-a['data.timestamp'][anchor]).seconds)
                pp1_timeline.append((a['data.timestamp'][anchor],a['data.timestamp'][index-1]))
                count+=1
                if(pd.Timedelta(a['data.timestamp'][index-1]-a['data.timestamp'][anchor]).seconds>=140):
                    count+=1
        anchor=index
        state=a['data.ax'][index]
print(count)
total_pp1_power=[] #pick and place1 total power for selected time range 
for t1,t2 in pp1_timeline:
    powpp1=(pp1_vaf[t1:t2]['data.A1'].mean()+pp1_vaf[t1:t2]['data.A2'].mean()+pp1_vaf[t1:t2]['data.A3'].mean())*231/1000
    total_pp1_power.append(powpp1)
print("Average power spent on each pcb by pickandplace during active",sum(total_pp1_power)/len(total_pp1_power),'kVA')

#### this gets the time line for  pp2 
index=0
state=pp2_vibration_threshold['data.ax'][0]
anchor=0
count=0
pp2_timeline=[] # this list has start and stop time of pp2 active state
for index in range(1,pp2_vibration_threshold.shape[0]):
    if(pp2_vibration_threshold['data.ax'][index]!=state):
        update_state=pp2_vibration_threshold['data.ax'][index-1]
        if (state==1 and update_state==1):
            
            if(pd.Timedelta(pp2_vibration_threshold['data.timestamp'][index-1]-pp2_vibration_threshold['data.timestamp'][anchor]).seconds>=50):
                print('At',pp2_vibration_threshold['data.timestamp'][anchor],'to',pp2_vibration_threshold['data.timestamp'][index],'time taken in seconds',pd.Timedelta(pp2_vibration_threshold['data.timestamp'][index-1]-pp2_vibration_threshold['data.timestamp'][anchor]).seconds)
                pp2_timeline.append((pp2_vibration_threshold['data.timestamp'][anchor],pp2_vibration_threshold['data.timestamp'][index-1]))
                count+=1
                if(pd.Timedelta(pp2_vibration_threshold['data.timestamp'][index-1]-pp2_vibration_threshold['data.timestamp'][anchor]).seconds>=100):
                    count+=1
        anchor=index
        state=pp2_vibration_threshold['data.ax'][index]
print(count)

total_pp2_power=[] #pick and place2 total power for selected time range 
for t1,t2 in pp2_timeline:
    powpp2=(pp2_vaf[t1:t2]['data.A1'].mean()+pp2_vaf[t1:t2]['data.A2'].mean()+pp2_vaf[t1:t2]['data.A3'].mean())*231/1000
    total_pp2_power.append(powpp2)
print("Average power spent on each pcb by pickandplace2 during active",sum(total_pp2_power)/len(total_pp2_power),'kVA')




# threshold the variance of loader vibration (0.00002)
loader_vibration_threshold=pd.DataFrame((loader_vib_var>0.00002).astype(np.int_))
# to rename the column names to 'state' instead of 'data.ax'
names={loader_vibration_threshold.columns[0]:'state'}
loader_vibration_threshold.rename(columns=names,inplace=True)
loader_vibration_threshold.reset_index(level=0, inplace=True)




index=0
state=loader_vibration_threshold['state'][0]
anchor=0
count=0
loader_timeline=[]
for index in range(1,loader_vibration_threshold.shape[0]):
    if(loader_vibration_threshold['state'][index]!=state):
        update_state=loader_vibration_threshold['state'][index-1]
        if (state==1 and update_state==1):
            print('At',loader_vibration_threshold['data.timestamp'][anchor],'to',loader_vibration_threshold['data.timestamp'][index],'time taken in seconds',pd.Timedelta(loader_vibration_threshold['data.timestamp'][index-1]-loader_vibration_threshold['data.timestamp'][anchor]).seconds)
            if(pd.Timedelta(loader_vibration_threshold['data.timestamp'][index-1]-loader_vibration_threshold['data.timestamp'][anchor]).seconds>=75):
                loader_timeline.append((loader_vibartion_threshold['data.timestamp'][anchor],loader_vibration_threshold['data.timestamp'][index-1]))
                count+=1
    anchor=index
    state=loader_vibration_threshold['state'][index]




#reset the index of loader_vibration _threshold to continuous samples instead of timestamp
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




# get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
from matplotlib import rc as rc



print("$$$$$$$$$$$$$$$$$$PP1TIMELINES INCOMING$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(pp1_timeline)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

fig, (f1, f2) = plt.subplots(nrows=2, sharex=True)
fig.set_size_inches(6,9)
f1.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
f1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
f1.plot(pp1_vibration[start_time:stop_time]['data.ax'].sort_index(),'g',label='vibration')
f1.set_ylabel('pickandplace1 vibration',color='k')


f2.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
f2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
f2.plot(pp1_vaf[start_time:stop_time]['data.A1'],'b')
f2.set_ylabel('current of pickandplace1(Amps)',color='k')
fig.text(0.5, 0.01, 'Timestamp in hh:mm:ss', ha='center',fontsize=9)

plt.xticks(rotation='vertical')
for x in [f1,f2]:
    for t1,t2 in pp1_timeline:
        if(t2-t1>= pd.Timedelta('00:00:75')):
            x.axvspan(t1,t2,alpha=0.2,label='Working',facecolor='r')

red_patch = mpatches.Patch(color='red', label='active',alpha=0.2)
f1.legend(handles=[red_patch], loc='upper left')

plt.savefig('pp1plots.png')





fig2, (g1, g2) = plt.subplots(nrows=2, sharex=True)
fig2.set_size_inches(6,9)
g1.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
g1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
g1.plot(pp2_vibration[start_time:stop_time]['data.ax'].sort_index(),'g',label='vibration')
g1.set_ylabel('pickandplace2 vibration',color='k')


g2.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
g2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
g2.plot(pp2_vaf[start_time:stop_time]['data.A1']*231/1000,'b')
g2.set_ylabel('Current of pickandplace2(Amps)',color='k')
fig2.text(0.5, 0.01, 'Timestamp in hh:mm:ss', ha='center',fontsize=9)
plt.xticks(rotation='vertical')
for x in [g1,g2]:
    for t1,t2 in pp2_timeline:
        if(t2-t1>= pd.Timedelta('00:00:75')):
            x.axvspan(t1,t2,alpha=0.2,label='Working',facecolor='r')

red_patch = mpatches.Patch(color='red', label='active',alpha=0.2)
g1.legend(handles=[red_patch],loc='upper left')
plt.savefig('pp2plots.png')




sp_vaf_threshold=pd.DataFrame((sp_vaf[start_time:stop_time]['data.A1'] > 4).astype(np.int_))
sp_vaf_threshold['data.A1']=sp_vaf_threshold['data.A1']*2 # this just a value to represent a heating state




sp_vaf_threshold.reset_index(level=0,inplace=True)




#////////////////to get the cleaning time/////////////////////
index=0
state=sp_vaf_threshold['data.A1'][0]
anchor=0
total_cleaning_time=pd.Timedelta('00:00:00')
sp_current=[]
print("Screen printing Cleaning timeline \n")
print("start,end,timetaken")
for index in range(1,sp_vaf_threshold.shape[0]):
    if(sp_vaf_threshold['data.A1'][index]!=state):
        #update_state=a['data.ax'][index-1]
        if (state==2 and sp_vaf_threshold['data.A1'][index-1]==2):
            delta=sp_vaf_threshold['data.timestamp'][index]-sp_vaf_threshold['data.timestamp'][anchor]
            sp_current.append((sp_vaf_threshold['data.timestamp'][anchor],sp_vaf_threshold['data.timestamp'][index],delta))
            print('At',sp_vaf_threshold['data.timestamp'][anchor],'to',sp_vaf_threshold['data.timestamp'][index],'time is',delta)
            print(anchor,index,'--------',delta)
        anchor=index
        state=sp_vaf_threshold['data.A1'][index]


# sp_vaf_threshold.reset_index(level=0, inplace=True)
# sp_vaf_threshold.index=sp_vaf_threshold['count']



sp_vaf_threshold.index=sp_vaf_threshold['data.timestamp']
sp_vaf_threshold.rename(columns={'data.A1': 'state'},inplace=True)




sp_states=pd.concat([loader_vibration_threshold,sp_vaf_threshold])




sp_states.sort_index()




sp_current




fig, fl = plt.subplots(nrows=2, sharex=True,)
fig.set_size_inches(6,6)
fl[0].xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
fl[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fl[0].plot(loader_vibration[start_time:stop_time]['data.ax'].sort_index(),'g')
fl[0].set_ylabel('loader vibration',color='k',fontsize=8)

red_patch = mpatches.Patch(color='red', label='cleaning',alpha=0.3)
blue_patch = mpatches.Patch(color='blue', label='Applying Paste',alpha=0.3)
fl[0].legend(handles=[red_patch,blue_patch], loc='upper left')

fl[1].xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
fl[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fl[1].plot(sp_vaf[start_time:stop_time]['data.A1'],'r')
fl[1].set_ylabel('screen printer current(Amps)',color='k',fontsize=8)

for x in fl:
    for t1,t2,t3 in sp_current:
        if(t2-t1>= pd.Timedelta('00:00:09')):
            x.axvspan(t1-pd.Timedelta('00:00:03'),t2,alpha=0.3,facecolor='r')
for y in fl:
    for t in Loading_Finish:
        y.axvspan(t,t+pd.Timedelta("00:00:12"),alpha=0.3,facecolor='b')
for x in fl:    
    x.grid(color='gold', linestyle='--', linewidth=1) 

plt.xticks(fontsize=8)

fig.text(0.5, 0.02, 'Timestamp in hh:mm:ss', ha='center',fontsize=8)

rc('ytick', labelsize=8) 
plt.savefig("screenprinterplots.png")
#plt.show()




sp_states.rename(columns={},inplace=True)




loader_power=[]




sp_vaf_threshold




sp_current
#sp_vaf_threshold.reset_index(level=0, inplace=True)




sp_cleaning=pd.DataFrame(data=sp_current,columns=['start','stop','time_taken'])









samples=0
current=0
avgpow=[]
for i in range(0,sp_cleaning.shape[0]):
    # print((sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values))
    samples=len(sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values)
    avgpow.append(sp_vaf[sp_cleaning['start'][i]:sp_cleaning['stop'][i]]['data.A1'].values.sum()*231/samples)




print("Average Power consumed by screen printer per cleaning: ", sum(avgpow)/(len(avgpow)*1000),"kVA")

