#### import needed packages
import nidaqmx as ni 
import numpy as np 
from nidaqmx import constants
from nidaqmx.stream_readers import CounterReader
from nidaqmx import stream_writers

#### customised versions for the lab
from spinmob import egg
import pyqtgraph as pyqt 

#### constant initialisations #### needs to be moved to a separate file soon
PMT_COUNTS_HOLD = np.zeros(500)
PMT_COUNTS_RAW = np.zeros(500)
PMT_COUNTS_AVERAGE = np.zeros(500)
PMT_COUNTS_AVERAGE_HOLD = np.zeros(500)
COUNT_READ = np.zeros(2, dtype = np.uint32)
COUNT_HOLD = 0
COUNT_HOLD_AVERAGE = 0

#### NI constant initialisation #### needs to be moved to a separate file soon
SECONDS = ni.constants.TimeUnits.SECONDS
LOW = ni.constants.Level.LOW
HIGH = ni.constants.Level.HIGH
size = constants.READ_ALL_AVAILABLE

#### Analog Output Tasks ####
def set_AO0_level():
      VOLTS = ni.constants.VoltageUnits.VOLTS
      AO0 = ni.Task()
      AO0.ao_channels.add_ao_voltage_chan("Dev1/ao0", "ao0 level", 0, 5, units = VOLTS)
      AO0.start()
      print("Voltage func through")
      
      global AO0_OUT
      AO0_OUT = ni.stream_writers.AnalogSingleChannelWriter(AO0.out_stream)
      AO0_OUT.write_one_sample(2.0)
      print("voltage gone?")
      
      AO0.close()
      
      
#### Digital Out Tasks 0 ####

def initialise_DO0():
    global DO0
    global DO0_OUT

    DO0 = ni.Task()
    DO0.do_channels.add_do_chan("Dev1/port0/line0", "DO0_Laser", constants.LineGrouping.CHAN_PER_LINE)

    DO0.start()

    print("P0.0 initialised as Digital Output")

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

#### Digital Out Task 1 ####

def initialise_DO1():
    global DO1

    DO1 = ni.Task()
    DO1.do_channels.add_do_chan("Dev1/port0/line1", "DO1_Laser", constants.LineGrouping.CHAN_PER_LINE)

    DO1.start()

    print("P0.1 initialised as Digital Output")

def set_DO1_high():
    global DO1
    DO1.write(True)
    print("P0.1 set to 5V")

def set_DO1_low():
    global DO1
    DO1.write(False)
    print("P0.1 set to 0V")

def close_DO1():
    global DO1
    DO1.close()

#### initialising PMT and exposure time set in ms ####

def initialise_PMT(exposure = 20):
    global A
    global PMT_COUNT
    global TIMER1
    global COUNT_READ
    global PMT_COUNTS_RAW
    global PMT_COUNTS_HOLD

    RATE = (exposure*1e-3)**-1
    PMT_COUNT = ni.Task()
    TIMER1 = ni.Task()

    ## creates an output channel to be used as an internal timer ##
    TIMER1.co_channels.add_co_pulse_chan_freq("Dev1/ctr1", "PMT_TIMING", freq = RATE)

    TIMER1.timing.cfg_implicit_timing(sample_mode = constants.AcquisitionType.CONTINUOUS)
    
    PMT_COUNT.ci_channels.add_ci_count_edges_chan("Dev1/ctr0", "PMT_COUNTING", initial_count = 0)
    PMT_COUNT.timing.cfg_samp_clk_timing(rate = RATE, source = "/Dev1/Ctr1InternalOutput", sample_mode = ni.constants.AcquisitionType.CONTINUOUS)
    A = CounterReader(PMT_COUNT.in_stream)
    TIMER1.start()
    PMT_COUNT.start()

def close_PMT():
    PMT_COUNT.close()
    TIMER1.close()

def settings_changed(*a):
    settings.save()

#### functions for digital logic on/off for P0.0 ####

def onoff_DO0(*a):
    if settings["settings/Bean_Status/493_nm"] == "ON" and DO0.read() == True:
        set_DO0_low()
        print("493 is OFF")
        settings["settings/Bean_Status/493_nm"] = "OFF"

    elif settings["settings/Beam_Status/493_nm"] == "OFF" and DO0.read() == False:
        set_DO0_high()
        print("493 is ON")
        settings["settings/Beam_Status/493_nm"] = "ON"

    else:
        print("Error, 493 beam defaulted to OFF")
        set_DO0_low()
        settings["settings/Beam_Status/493_nm"] = "OFF"
        DO0_OnOff.set_checked(value = False)

def onoff_DO1(*a):
    if settings["settings/Beam_Status/650_nm"] == "ON" and DO1.read() == True:
        set_DO1_low()
        print("650 is OFF")
        settings["settings/Beam_Status/650_nm"] = "OFF"

    elif settings["settings/Beam_Status/650_nm"] == "OFF" and DO1.read() == False:
        set_DO1_high()
        print("650 is ON")
        settings["settings/Beam_Status/650_nm"] = "ON"

    else:
        print("Error, 650 beam defaulted to OFF")
        set_DO1_low()
        settings["settings/Beam_Status/650_nm"] = "OFF"
        DO1_OnOff.set_checked(value = False)

#### data taking functions ####

def EXP_AV(X, Y):
    alpha = 0.5
    LEN = len(X)
    Z = np.zeros(LEN)
    Z[0: -1] = X[1:]
    SUM = 0
    for i in range(0, LEN):
        SUM += (1-alpha)**(LEN + 1 - i)*X[i]
    Z[-1] = alpha*(Y + SUM)
    return Z

def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def ACQUIRE_PMT():
    global PMT_COUNTS_HOLD
    global PMT_COUNTS_RAW
    global COUNT_HOLD
    global COUNT_READ
    global A
    global PMT_COUNTS_AVERAGE
    global PMT_COUNTS_AVERAGE_HOLD

    try:
        A.read_many_sample_uint32(COUNT_READ, number_of_samples_per_channel = 2)
        new_val = np.average(COUNT_READ) - COUNT_HOLD
        PMT_COUNTS_RAW = EXP_AV(PMT_COUNTS_RAW, new_val)
        PMT_COUNTS_AVERAGE = smooth(PMT_COUNTS_RAW, 4)
        PMT_AVERAGE_DISPLAY = PMT_COUNTS_AVERAGE[1: len(PMT_COUNTS_AVERAGE) - 1]

        COUNT_HOLD = np.average(COUNT_READ)
    
    except:
        print("ERROR: Invalid source script.")
        close_PMT()
        COUNT_HOLD=0
        initialise_PMT(settings["settings/Acquisition Settings/exposure"])

    return PMT_AVERAGE_DISPLAY

#### function for when the acquire button is pressed ####

def acquire_button_clicked(*a):
    global COUNT_HOLD

    if not PMT_ACQUIRE_BUTTON.is_checked():
        return
    
    close_PMT()
    num_box.set_value(0)
    print("Starting acuisition loop... ")

    initialise_PMT(settings["settings/Acquisition Settings/exposure"])

    while PMT_ACQUIRE_BUTTON.is_checked() and (num_box.get_value() < settings["settings/Acquisition Settings/iterations"] or settings["settings/Acquisition Settings/iterations"] == 0):

        databox1.clear()
        databox2.clear()

        settings.send_to_databox_header(databox1)
        settings.send_to_databox_header(databox2)

        databox1['t'] = np.linspace(0, settings["settings/simulated_input/points"]*(settings["settings/Acquisition Settings/exposure"]), settings["settings/simulated_input/points"])
        databox1[0] = ACQUIRE_PMT()
        current_count.setText(str(np.round(databox1[0][-1])))

        num_box.increment()

        databox1.plot(); databox1.autosave()
        databox2.plot(); databox2.autosave()

        win.process_events()
    
    PMT_ACQUIRE_BUTTON.set_checked(False)
    print("Acquisition stopped")
    COUNT_HOLD = 0
    close_PMT()

def CLEAR_PMT_DATA():
    PMT_COUNT_RAW = np.zeros(500)
    PMT_COUNTS_AVERAGE = np.zeros(500)

#### GUI section #####

""" creating the main window """
win = egg.gui.Window(autosettings_path = 'NIDAQTESTING.cfg')

""" left side of the main window """
PMT_ACQUIRE_BUTTON = win.place_object(egg.gui.Button("Count Photons", checkable = True)).set_width(135)
num_box = win.place_object(egg.gui.NumberBox(int = True)).set_width(50)

tabs = win.place_object(egg.gui.TabArea(), row_span = 2, alignment = 0)

current_count = pyqt.QtGui.QLabel("No Data")
win.place_object(current_count).setFont(egg.pyqtgraph.QtGui.QFont("Times Roman"))

win.place_object(current_count, row = 3, column = 2)

win.new_autorow()
settings = win.place_object(egg.gui.TreeDictionary('NIDAQTESTINGSETTINGS.cfg'), column_span = 2)

win.new_autorow()
DO0_OnOff = win.place_object(egg.gui.Button("493 On/Off", checkable = True)).set_width(120)
DO1_OnOff = win.place_object(egg.gui.Button("650 On/Off", checkable = True)).set_width(120)

settings.add_parameter("settings/Acquisition Settings/iterations", value = 0, type = 'int')
settings.add_parameter("settings/ simulated_input/channels", value = 1, type = 'int', limits = (1, 8))
settings.add_parameter("settings/Acquisition Settings/exposure", value = 20, type = 'float', limits = (0.001, None), dec = True, siPrefix = True, suffix = 'ms')
settings.add_parameter("settings/simulated_input/points", value = 500, type = 'int', limits = (2, None))
settings.add_parameter("settings/simulated_input/Averaging", value = 2, type = 'int', limits = (1, 200))
settings.add_parameter("settings/Beam_Status/493_nm", value = "OFF", type = 'list', values = ["ON", "OFF"])
settings.add_parameter("settings/Beam_Status/650_nm", value = "OFF", type = 'list', values = ["ON", "OFF"])

""" tab 1 GUI """
tab1 = tabs.add_tab("PMT Signal")
databox1 = tab1.place_object(egg.gui.DataboxPlot(autosettings_path = 'NIDAQTESTp1.cfg'), alignment = 0)

""" tab 2 GUI """
tab2 = tabs.add_tab("Analysis")
databox2 = tab2.place_object(egg.gui.DataboxPlot(autosettings_path = 'NIDAQTESTp2.cfg'), alignment = 0)

""" tab 3 GUI """
tab3 = tabs.add_tab("Voltage Output")
btn1 = tab3.place_object(egg.gui.Button("Testing tings", checkable = False)).set_width(135)

settings.load()
initialise_PMT(settings["settings/Acquisition Settings/exposure"])
initialise_DO0()
initialise_DO1()

set_DO0_low()
set_DO1_low()

settings["settings/Beam_Status/493_nm"] = "OFF"
settings["settings/Beam_Status/650_nm"] = "OFF"

btn1.signal_clicked.connect(set_AO0_level)

PMT_ACQUIRE_BUTTON.signal_clicked.connect(acquire_button_clicked)
DO0_OnOff.signal_clicked.connect(onoff_DO0)
DO1_OnOff.signal_clicked.connect(onoff_DO1)

settings.connect_any_signal_changed(settings_changed)

def shutdown():
    print("Closing but not destorying...")
    PMT_ACQUIRE_BUTTON.set_checked(False)
    close_DO0()
    close_DO1()
    close_PMT
    return

win.event_close = shutdown

win.show(True)
