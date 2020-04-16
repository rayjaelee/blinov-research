# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:15:30 2019

@author: Alex Kato
"""
"""
Ion trap control software for reading PMT data, scanning lasers, turning AOM's on/off, and measuring secular frequencies.
Uses NiDAQmx for interfacing with the NI card PCIe 6000 series. GUI uses spinmob egg for easy creation and quick prototyping--see examples online. (Thanks Jack Sankey!)
I hope you find this useful!
"""
######import stuff here
import numpy as np
import nidaqmx as ni
from nidaqmx import constants
from nidaqmx.stream_readers import CounterReader 
from nidaqmx.stream_writers import DigitalSingleChannelWriter
####my modified version to customize for our lab
from spinmob import egg
import time as _t
import spinmob as _s
import pyqtgraph as pyqt

#############define global variables#######################move to another file soon
PMT_COUNTS_HOLD=np.zeros(500)
PMT_COUNTS_RAW = np.zeros(500) 
PMT_COUNTS_AVERAGE=  np.zeros(500)
PMT_COUNTS_AVERAGE_HOLD=np.zeros(500)
COUNT_READ=np.zeros(2,dtype=np.uint32)
COUNT_HOLD=0
COUNT_HOLD_AVERAGE=0

######define some constants from NI ########################################move to another file soon
SECONDS=ni.constants.TimeUnits.SECONDS
LOW=constants.Level.LOW
HIGH=constants.Level.HIGH
size=ni.constants.READ_ALL_AVAILABLE



################################Digital out tasks
def initialize_DO0():
    global DO0
    global DO0_OUT
    
    DO0=ni.Task()
    DO0.do_channels.add_do_chan("Dev1/port0/line0","DO0_Laser",constants.LineGrouping.CHAN_PER_LINE)
#    DO0.add_do_chan("Dev1/port0/line0:7","DIO Click Control")
#      DO0.do_channels.add_do_chan()                          
    DO0.start()
#    DO0_OUT=DigitalSingleChannelWriter(DO0.out_stream)
    print("P0.0 initialized as Digital OutputV")

def set_DO0_high():
    global DO0
    DO0.write(True)
    print("P0.0 set to 5V")
def set_DO0_low():
    
    global DO0
    DO0.write(False)
    print("P0.0 set to 0V")
def close_DO0():
    global DO0
    DO0.close()
    
def initialize_DO1():
    global DO1
#    global DO1_OUT
    
    DO1=ni.Task()
    DO1.do_channels.add_do_chan("Dev1/port0/line1","DO1_Laser",constants.LineGrouping.CHAN_PER_LINE)
    DO1.start()
#    DO1_OUT=DigitalSingleChannelWriter(DO1.out_stream)
    print("P0.1 initialized as Digital OutputV")

def set_DO1_high():
    global D01
    DO1.write(True)
#    DO1_OUT.write_one_sample_port_uint32(True)
    print("P0.1 set to 5V")
def set_DO1_low():
    
    global DO1
    DO1.write(False)
    print("P0.1 set to 0V")
def close_DO1():
    global D01
    DO1.close()

#############################################################################
    
    
    ######initialize the PMT, exposure time set in ms
def initialize_PMT(exposure=20):
    global A
    global PMT_COUNT
    global TIMER1
    global COUNT_READ
    global PMT_COUNTS_RAW
    global PMT_COUNTS_HOLD
#   s["settings/simulated_input/iterations"]
    RATE=(exposure*1e-3)**-1
    PMT_COUNT=ni.Task()
    TIMER1=ni.Task()
    #######creates an output channel to be used as an internal timer
    TIMER1.co_channels.add_co_pulse_chan_freq("Dev1/ctr1","PMT_TIMING",freq=RATE)#,units=NIDAQ.constants.TimeUnits.SECONDS)#,idle_state=level,low_time=0.001,
       # high_time=0.001)
    #####sets the timing
    TIMER1.timing.cfg_implicit_timing(sample_mode=constants.AcquisitionType.CONTINUOUS)#rate = 1000, samps_per_chan = 1000,sample_mode=constants.AcquisitionType.CONTINUOUS)
    #####
    PMT_COUNT.ci_channels.add_ci_count_edges_chan("Dev1/ctr0","PMT_COUNTING",initial_count=0)
    
    PMT_COUNT.timing.cfg_samp_clk_timing(rate = RATE ,source="/Dev1/Ctr1InternalOutput",
                                  
                                  sample_mode=constants.AcquisitionType.CONTINUOUS)
    A=CounterReader(PMT_COUNT.in_stream)
    TIMER1.start()
    PMT_COUNT.start()
    
def close_PMT():
    PMT_COUNT.close()
    TIMER1.close()
 
 ##############################################################################


##### GUI DESIGN

# create the main window
w = egg.gui.Window(autosettings_path='NIDAQTESTING.cfg')

# add the "go" button
PMT_ACQUIRE_BUTTON = w.place_object(egg.gui.Button("Count Photons!", checkable=True)).set_width(135)
i = w.place_object(egg.gui.NumberBox(int=True)).set_width(50)

# add a tabbed interface for the plotting area, spanning the first and second rows
tabs = w.place_object(egg.gui.TabArea(), row_span=2, alignment=0)

# add a tab for some plots
t1 = tabs.add_tab("PMT Signal")
t2 = tabs.add_tab("Analysis")

# add a databox plotter object to the tab
d1 = t1.place_object(egg.gui.DataboxPlot(autosettings_path='NIDAQTESTp1.cfg'), alignment=0)
d2 = t2.place_object(egg.gui.DataboxPlot(autosettings_path='NIDAQTESTp2.cfg'), alignment=0)
Count_Current = pyqt.QtGui.QLabel("NO DATA")
w.place_object(Count_Current).setFont(egg.pyqtgraph.QtGui.QFont("Times", 30))


w.place_object(Count_Current,row=3,column=2)


# move to the second row and add a TreeDictionary for
# our "settings"
w.new_autorow()
s = w.place_object(egg.gui.TreeDictionary('NIDAQTESTINGSETTINGS.cfg'), column_span=2)
#####place buttons for laser turning on/off
w.new_autorow()
DO0_ONOFF=w.place_object(egg.gui.Button("493 On/Off", checkable=True)).set_width(120)
DO1_ONOFF=w.place_object(egg.gui.Button("650 On/Off", checkable=True)).set_width(120)



##### DATA OBJECTS

# add various parameters to use later
s.add_parameter("settings/Acquisition Settings/iterations", value=0,            type='int')
s.add_parameter("settings/simulated_input/channels",   value=1,            type='int',   limits=(1, 8))
s.add_parameter("settings/Acquisition Settings/exposure",   value=20,         type='float', limits=(0.001,None), dec=True, siPrefix=True, suffix='ms')
s.add_parameter("settings/simulated_input/points",     value=500,         type='int',   limits=(2,    None))
s.add_parameter("settings/simulated_input/Averaging",     value=2,         type='int',   limits=(1,    200))

#s.add_parameter("settings/simulated_input/source",     value="cos(500*t)", type='str')
#s.add_parameter("settings/simulated_input/noise",      value=0.2,          type='float')
#s.add_parameter("settings/other_stuff/name",           value="moose",      type='str')
#s.add_parameter("settings/other_stuff/quality",        value="round",      type='list', values=["round", "faceted", "regular moose"])
s.add_parameter("settings/Beam_Status/493_nm",        value="OFF",      type='list', values=["ON","OFF"])
s.add_parameter("settings/Beam_Status/650_nm",        value="OFF",      type='list', values=["ON","OFF"])



####commands that should be run upon startup
##############################################################################
# load previous settings if they exist
s.load()
initialize_PMT(s["settings/Acquisition Settings/exposure"]) 
initialize_DO1()
initialize_DO0()

set_DO1_low()
set_DO0_low()
s["settings/Beam_Status/493_nm"]="OFF"
s["settings/Beam_Status/650_nm"]="OFF"
def settings_changed(*a): 
    s.save()
#    initialize_PMT(s["settings/Acquisition Settings/exposure"]) 
##### FUNCTIONALITY of the GUI#####################################################################

#define functions to turn digital logic on/off for P0.0 (depending on initial buttion status). edit text on button and settings to change the wavelength
def onoff_DO0(*a):

    if s["settings/Beam_Status/493_nm"]=="ON" and DO0.read()==True:
        set_DO0_low()
        print("493 is OFF")
        s["settings/Beam_Status/493_nm"]="OFF"

        
    elif s["settings/Beam_Status/493_nm"]=="OFF" and DO0.read()==False:
        set_DO0_high()
        print("493 is ON")
        s["settings/Beam_Status/493_nm"]="ON"

    else:
        print("Error, 493 beam defaulted to OFF")
        set_DO0_low()
        s["settings/Beam_Status/493_nm"]="OFF"
        DO0_ONOFF.set_checked(value=False)
        
def onoff_DO1(*a):

    if s["settings/Beam_Status/650_nm"]=="ON" and DO1.read()==True:
        set_DO1_low()
        print("650 is OFF")
        s["settings/Beam_Status/650_nm"]="OFF"

        
    elif s["settings/Beam_Status/650_nm"]=="OFF" and DO1.read()==False:
        set_DO1_high()
        print("650 is ON")
        s["settings/Beam_Status/650_nm"]="ON"

    else:
        print("Error, 650 beam defaulted to OFF")
        set_DO1_low()
        s["settings/Beam_Status/650_nm"]="OFF"
        DO1_ONOFF.set_checked(value=False)

#define data taking function   $#######################################################
def EXP_AV(X,Y):
      alpha=0.5
      LEN=len(X)
      Z=np.zeros(len(X))
      Z[0:-1]=X[1:]
      SUM=0
      for i in range(0,len(X)):
            SUM+=(1-alpha)**(LEN+1-i)*X[i]
      Z[-1]=alpha*(Y+SUM)
      return Z
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
    
def ACQUIRE_PMT():
#    average=s["settings/simulated_input/Averaging]
    global PMT_COUNTS_HOLD
    global PMT_COUNTS_RAW
    global COUNT_HOLD
    global COUNT_READ
    global A
    global PMT_COUNTS_AVERAGE
    global PMT_COUNTS_AVERAGE_HOLD
#    global PMT_COUNTS_AVERAGE
#    global PMT_COUNTS_AVERAGE_HOLD
#    global COUNT_HOLD_AVERAGE
#e the source script
    try:
        
        
        A.read_many_sample_uint32(COUNT_READ,number_of_samples_per_channel=2)
        new_val=np.average(COUNT_READ)-COUNT_HOLD
        PMT_COUNTS_RAW=EXP_AV(PMT_COUNTS_RAW,new_val)
        PMT_COUNTS_AVERAGE=smooth(PMT_COUNTS_RAW,4)
        PMT_AVERAGE_DISPLAY=PMT_COUNTS_AVERAGE[1:len(PMT_COUNTS_AVERAGE)-1]
#        PMT_COUNTS_RAW[-1]=new_val
#        PMT_COUNTS_RAW[0:-1]=PMT_COUNTS_HOLD[1:]
#        PMT_COUNTS_HOLD=PMT_COUNTS_RAW
     
        
#        new_val2=((int(COUNT_READ)-COUNT_HOLD)+
#                  np.sum(PMT_COUNTS_RAW[(-s["settings/simulated_input/Averaging"]+1):]))/s["settings/simulated_input/Averaging"]
#        PMT_COUNTS_AVERAGE[-1]=new_val2
#        PMT_COUNTS_AVERAGE[0:-1]=PMT_COUNTS_AVERAGE_HOLD[1:]
#        PMT_COUNTS_AVERAGE_HOLD=PMT_COUNTS_AVERAGE
#        print(COUNT_READ)
        
        COUNT_HOLD=np.average(COUNT_READ)
#        g = np.__dict__

       
    except:
        print("ERROR: Invalid source script.")
#        
        close_PMT()
        COUNT_HOLD=0
#        COUNT_HOLD_AVERAGE=0
        initialize_PMT(s["settings/Acquisition Settings/exposure"])
#        

    return PMT_AVERAGE_DISPLAY


# define a function to be called whenever the acquire button is pressed
def acquire_button_clicked(*a):
    global COUNT_HOLD
    
    # don't start another loop if the button is unchecked!
    if not PMT_ACQUIRE_BUTTON.is_checked(): 
            
            return

    # reset the counter
    close_PMT()
    i.set_value(0)

    print("Sarting acquisition loop...")

    # start the loop and keep looping until someone
    # unchecks the acquisition button or we max out the iterations
    # setting iterations = 0 will loop infinitely
    initialize_PMT(s["settings/Acquisition Settings/exposure"])
    while PMT_ACQUIRE_BUTTON.is_checked()                                          \
    and (i.get_value() < s["settings/Acquisition Settings/iterations"] \
         or s["settings/Acquisition Settings/iterations"] == 0):

        # reset the databox
        d1.clear()
        d2.clear()
        
        # all the information to the databox headers
        s.send_to_databox_header(d1)
        s.send_to_databox_header(d2)

        # create the fake time data
        d1['t'] = np.linspace(0,s["settings/simulated_input/points"]*(s["settings/Acquisition Settings/exposure"]), s["settings/simulated_input/points"])
        d1[0]=ACQUIRE_PMT()
#        d1[1]=np.smooth(d1[0])
        Count_Current.setText(str(np.round(d1[0][-1])))
#         create the fake channel data and do some analysis on it         
#        for n in range(s["settings/simulated_input/channels"]):
#
#            # get the channel name
#            c = 'ch'+str(n)
#
#            # create the data
#            d1[c] = ACQUIRE_PMT()
     
        # increment the counter
        i.increment()

        # update the plot (note updating d1 updates p1.databox by reference)
        # and autosave (only does anything if this is enabled on the gui)
        d1.plot(); d1.autosave()
        d2.plot(); d2.autosave()
        
        # process other window events so the GUI doesn't freeze
        w.process_events()

    # in case the button is still checked
    PMT_ACQUIRE_BUTTON.set_checked(False)

    print("Acquisition stopped.")
    COUNT_HOLD=0
    close_PMT()
def CLEAR_PMT_DATA():
    PMT_COUNTS_RAW = np.zeros(500) 
    PMT_COUNTS_AVERAGE=  np.zeros(500)
# connect the button
PMT_ACQUIRE_BUTTON.signal_clicked.connect(acquire_button_clicked)
DO0_ONOFF.signal_clicked.connect(onoff_DO0)
DO1_ONOFF.signal_clicked.connect(onoff_DO1)


# connecting is a little different for TreeDictionaries
s.connect_any_signal_changed(settings_changed)



# overwrite the existing shutdown / destroy sequence
def shutdown():
    print("Closing but not destroying...")
    PMT_ACQUIRE_BUTTON.set_checked(False)
    close_DO0()
    close_DO1()
    close_PMT
#    t1.clear()
#    t2.clear()
    
    return
w.event_close = shutdown

# show the window!
w.show(True)