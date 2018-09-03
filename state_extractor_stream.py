
import pandas as pd
from datetime import datetime as dt
import numpy as np
import yaml
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class machine_state_generator():
    def __init__(self,filenames):
        with open(filenames,'r') as files:
            self.data_files=yaml.load(files)
        self.loader_flag=False
        self.sp_flag=False
        self.pp1_flag=False
        self.pp2_flag=False
        self.reflow_flag=False
    def _loadData(self, machine):

        pattern="%Y-%m-%dT%H:%M:%S.%f" # format of the timestamp
        ################Loader's data loading###################
        if(self.loader_flag):
            print("Loader vibration data started loading... \n")
            try  :
                self.loader_vibration=pd.read_csv(self.data_files['file names']['loader']['vibration'],usecols=['data.timestamp','data.ax','data.ay','data.az'])
                self.loader_vibration['data.timestamp']=self.loader_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
                self.loader_vibration.index=self.loader_vibration['data.timestamp']
                self.loader_vibration.sort_index()
                print("Loader's vibration data finished loading... \n")
            except : 
                print("Specified file doesn't exist, change path in yaml file ") 
                sys.stderr.write('Ok. Quitting...')
                sys.exit(1)
        
        ###################################################################

        #######################pick and place1 data loading############################
        elif (self.pp1_flag):
            print("Pick and place data loading... \n")
            print("Pick and place vibration data loading... \n")
            try :
                self.pp1_vibration=pd.read_csv(self.data_files['file names']['pick and place1']['vibration'],usecols=['data.timestamp','data.ax','data.ay','data.az'])
                self.pp1_vibration['data.timestamp']=self.pp1_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
                self.pp1_vibration.index=self.pp1_vibration['data.timestamp']
                self.pp1_vibration.sort_index()
                print("Pick and place 1 vaf loading... \n")
                self.pp1_vaf=pd.read_csv(self.data_files['file names']['pick and place1']['power'],usecols=['data.timestamp','data.A1','data.A2','data.A3'])
                self.pp1_vaf['data.timestamp']=self.pp1_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
                self.pp1_vaf.index=self.pp1_vaf['data.timestamp']
                self.pp1_vaf.sort_index()
            except : 
                print("Specified file doesn't exist, change path in yaml file ") 
                sys.stderr.write('Ok. Quitting...')
                sys.exit(1)

        #########################screen printer data loading############################
        elif (self.sp_flag):
            try :
                print("Screen printer data loading... \n")
                print("Screen printer power loading... \n")
                self.sp_vaf=pd.read_csv(self.data_files['file names']['screen printer']['power'], usecols=['data.timestamp','data.A1','data.A2','data.A3'])
                self.sp_vaf['data.timestamp']=self.sp_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
                self.sp_vaf.index=self.sp_vaf['data.timestamp']
                self.sp_vaf.sort_index()
            except :
                print("Specified file doesn't exist, change path in yaml file ") 
                sys.stderr.write('Ok. Quitting...')
                sys.exit(1)
        ##################################################################################
        #########################reflow oven data loading############################
        elif (self.reflow_flag):     
            try :
                print("Reflow oven data loading... \n")
                print("Reflow oven power loading... \n")
                # self.rf_vaf=pd.read_csv(self.data_files['file names']['reflow oven']['power'],usecols=['data.timestamp','data.A1'])
                self.rf_vaf=pd.read_csv('abc.csv',usecols=['timestamp','data.A1'])
                self.rf_vaf['timestamp']=self.rf_vaf['timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
                self.rf_vaf.index=self.rf_vaf['timestamp']
                self.rf_vaf.sort_index()
            except :
                print("Specified file doesn't exist, change path in yaml file ") 
                sys.stderr.write('Ok. Quitting...')
                sys.exit(1)
        ##################################################################################

    def setMachine(self,machine):

        self.reflow_flag=True
        self._loadData(machine)
        return 

    # def setTimeFrame(self,start_time,stop_time):

    def genMachineStates(self):
        if(self.reflow_flag):
            maxcur=62.0
            roll_width = 30
            #generate pointwise states
            # statep1 = pd.DataFrame(columns = ['timestamp', 'current', 'state'])
            # statep1['timestamp'] = self.rf_vaf['timestamp']
            # statep1['current'] = self.rf_vaf['data.A1']
            # statep1['state'] = np.where(self.rf_vaf['data.A1'] <= 1.5, 0, statep1['state'])
            # statep1['state'] = np.where(self.rf_vaf['data.A1'] >= .75 * maxcur, 2, statep1['state'])
            # statep1['state'] = np.where((self.rf_vaf['data.A1'] <= .75 * maxcur) & (self.rf_vaf['data.A1'] > 1.5), 1, statep1['state'])

            #generate blockwise states

            st1 = pd.DataFrame(columns = ['timestamp', 'current', 'state'])
            st1['timestamp'] = self.rf_vaf['timestamp']
            st1['current'] = self.rf_vaf['data.A1']
            st1 = pd.Series.to_frame(st1.current.rolling(roll_width, center=True).mean())
            st1=st1
            st1['state'] = np.where(st1['current'] <= 1.5, 0, st1['state'])
            st1['state'] = np.where(st1['current'] >= .42 * maxcur, 2, st1['state'])
            st1['state'] = np.where((st1['current'] <= .42 * maxcur) & (st1['current'] > 1.5), 1, st1['state'])
            
            #PLot generated States
            fig, ax1 = plt.subplots()
            fig.set_size_inches(10,5)
            ax1.plot(st1['current'],color='orange')
            ax1.xaxis.set_major_locator(mdates.DateFormatter('%H:%M'))
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Current in Amps.', color='orange')
            ax1.set_yticks(np.arange(0, 80, step=10))
            ax1.tick_params('y', colors='orange')
            ax2 = ax1.twinx()
            ax2.plot(st1['state'], 'r-', color='purple', alpha=0.5)
            ax2.set_ylabel('State', color='purple')
            ax2.tick_params('y', colors='purple')
            ax2.set_yticks(np.arange(0, 3, step=1))
            # ax2.set_yticks(np.arange(3), ('Off', 'Maintain', 'Heating'))
            plt.title('Reflow Oven States')
            # plt.show()
            plt.savefig('Reflow_Oven_States.png')


            #Return the dataFrame containing states
            return(st1)



    # def genNetworkLvlStates(self):


if __name__=='__main__':
    data_rfo=machine_state_generator('data.yml')
    data_rfo.setMachine('reflow')
    df_rf_states=data_rfo.genMachineStates()
    print(df_rf_states)


