
import pandas as pd
from datetime import datetime as dt
import numpy as np
import yaml
import os
import sys
class csv_data():
    def __init__(self,filenames):
        with open(filenames,'r') as files:
            self.data_files=yaml.load(files)
        self.loader_vibration_flag=False
        self.sp_vibration_flag=False
        self.sp_vaf_flag=False
        self.pp1_vibration_flag=False
        self.pp1_vaf_flag=False
        self.pp2_vibration_flag=False
        self.pp2_vaf_flag=False
        self.reflow_vaf_flag=False
    def loadData(self, machine):

        pattern="%Y-%m-%dT%H:%M:%S.%f" # format of the timestamp
        ################Loader's vibration data loading###################

        print("loader vibration data started loading \n")
        try  :
            self.loader_vibration=pd.read_csv(self.data_files['file names']['loader']['vibration'],usecols=['data.timestamp','data.ax','data.ay','data.az'])
            self.loader_vibration['data.timestamp']=self.loader_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
            self.loader_vibration.index=self.loader_vibration['data.timestamp']
            self.loader_vibration.sort_index()
            print("loader's vibration data finished loading \n")
        except : 
            print("Specified file doesn't exist,change in yaml file ") 
            # sys.stderr.write('Ok quitting')
            # sys.exit(1)
        
        ###################################################################

        #######################pick and place1 data loading############################
        print("pick and place data loading \n")
        print("pick and place vibration data loading \n")
        try :
            self.pp1_vibration=pd.read_csv(self.data_files['file names']['pick and place1']['vibration'],usecols=['data.timestamp','data.ax','data.ay','data.az'])

            self.pp1_vibration['data.timestamp']=self.pp1_vibration['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
            self.pp1_vibration.index=self.pp1_vibration['data.timestamp']
            self.pp1_vibration.sort_index()
            print("finish loading pickandplace1 vibration")
        except : 
            print("Specified file doesn't exist,change in yaml file ") 
            # sys.stderr.write('Ok quitting')
            # sys.exit(1)
        #########################pick and place1 vaf loading############################
        try :
            print("pick and place 1 vaf loading \n")
            self.pp1_vaf=pd.read_csv(self.data_files['file names']['pick and place1']['power'],usecols=['data.timestamp','data.A1','data.A2','data.A3'])
            self.pp1_vaf['data.timestamp']=self.pp1_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
            self.pp1_vaf.index=self.pp1_vaf['data.timestamp']
            self.pp1_vaf.sort_index()
        except : 
            print("Specified file doesn't exist,change in yaml file ") 
            # sys.stderr.write('Ok quitting')
            # sys.exit(1)
        #########################screen printer data loading############################
        try :
            print("screen printer data loading \n")
            print("screen printer power loading \n")
            self.sp_vaf=pd.read_csv(self.data_files['file names']['screen printer']['power'],usecols=['data.timestamp','data.A1'])
            self.sp_vaf['data.timestamp']=self.sp_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
            self.sp_vaf.index=self.sp_vaf['data.timestamp']
            self.sp_vaf.sort_index()
        except :
            print("Specified file doesn't exist,change in yaml file ") 
            # sys.stderr.write('Ok quitting')
            # sys.exit(1)
        ##################################################################################
        #########################reflow oven data loading############################
        try :
            print("reflow oven data loading \n")
            print("reflow oven power loading \n")
            self.rf_vaf=pd.read_csv(self.data_files['file names']['reflow oven']['power'],usecols=['data.timestamp','data.A1'])
            self.rf_vaf['data.timestamp']=self.sp_vaf['data.timestamp'].apply(lambda x: pd.to_datetime(x,format=pattern,box=False)+pd.Timedelta('05:30:00'))
            self.rf_vaf.index=self.sp_vaf['data.timestamp']
            self.rf_vaf.sort_index()
        except :
            print("Specified file doesn't exist,change in yaml file ") 
            # sys.stderr.write('Ok quitting')
            # sys.exit(1)
        ##################################################################################

    def setMachine(self,machine,sensor):
        #try :
        self.loadData(machine)
        mach=eval("self.%s_%s"%(machine,sensor))
        self.machine=[]
        self.machine = mach

        if hasattr(self.machine,'attr_name'):
            print("%s is not an attribute in the object csv_data"%(self.machine))
        #except NameError :
        #print("There's some problem!, pass machine and sensor as string '' !")
        try:
            #var=eval("%s_flag"%(self.machine))
            temp='flag'
            var=eval("self.%s_%s_flag"%(machine,sensor))
            try :
                if hasattr(var,'attr_name'):
                    var=not(var)
            except :
                print("Error while setting the flag!!")
        except NameError:
            print("error!!")
        return 
    def setTimeFrame(self,start_time,stop_time):
        self.start_time=start_time
        self.stop_time=stop_time
    
    def getData(self,field):
        return self.machine[self.start_time][self.stop_time][str("data."+field)].sort_index()
    
    # def analyse(self,start_time,stop_time):
    #     pass
    # def VibrationRollingVariance(self,start_time,stop_time,window):
    #     self.varianceResult=self.machine[start_time:stop_time]['data.ax'].sort_index().rolling(window=window).var()
    #     return self.varianceResult
    
    # def varianceThreshold(self,values,threshold):
    #     variance_Threshold=pd.DataFrame((values > threshold).astype(np.int_))
    #     variance_Threshold.reset_index(level=0, inplace=True)
    #     return 


if __name__=='__main__':
    data=csv_data('data.yaml')
    data.setMachine('rf','power')
    # data.setTimeFrame('2018-03-14 10:30:00','2018-03-14 10:35:00')
    data.getData('ax')
    #data.setMachine('loader','vibration')
    #loader_variance=data.VibrationRollingVariance('2018-03-14 10:30:00','2018-03-14 10:35:00',150)