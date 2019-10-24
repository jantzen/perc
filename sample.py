# file: sample.py

import numpy as np
import serial
import time
import glob
import sys
import getopt
import pdb

# globals for reading temperature
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
 

def main(soil_type, p_set, p_tol=9.5, sampling_rate=100.):
    # create and open serial ports
    print("Setting up serial connections...")
    serUNO = serial.Serial('/dev/ttyUSB0',baudrate=115200, timeout=5.0)
    serNANO = serial.Serial('/dev/ttyACM0',baudrate=115200, timeout=5.0)
    time.sleep(3.)

    # pass pressure parameters to Arduino Nano
    serNANO.write(bytes(str(p_set)+'\n','utf-8'))
    serNANO.flush()
    time.sleep(0.5)
    try:
        if serNANO.in_waiting > 0:
            msg = serNANO.readline()
            assert int(msg) == 1
    except:
        print("NANO failed to confirm receipt of paramerter")
    serNANO.write(bytes(str(p_tol)+'\n','utf-8'))
    serNANO.flush()
    time.sleep(0.5)
    try:
        if serNANO.in_waiting > 0:
            msg = serNANO.readline()
            assert int(msg) == 1
    except:
        print("NANO failed to confirm receipt of paramerter")
    time.sleep(0.5)

    # confirm pressure can be read
    try:
        tmp = serNANO.readline()
        pressure = float(tmp)
        assert 0. < pressure < 2000.
        print("Pressue sensor ready (reports pressure of {} hPa)".format(pressure))
    except:
        raise IOError("cannot read from pressure sensor")

    # confirm depth can be acquired from Arduino Uno
    try:
        tmp = serUNO.readline()
        depth = float(tmp)
        assert 0. < depth < 1000.
        print("VL53 ready (reports depth of {})".format(depth))
    except:
        raise IOError("cannot read from VL53")

    # confirm temperature sensor can be read
    try:
        temp = read_temp()
        print("Temperature probe ready (reports {} deg C)".format(temp))
    except:
        raise IOError("cannot read from temperature probe")

    # loop
        # read depth, pressure, and temperature every 0.01 seconds
    for i in range(100):
        tmp = serNANO.readline()
        print(float(tmp))
        time.sleep(0.1)

    # save data
        # filename should contain: p_set, p_tol, soil_type, sampling rate,
        # start_time, end_time

    # reset the pump controller
    time.sleep(0.5)
    serNANO.write(b'r')


def usage():
    print("Script command usage:")
    cmd_line = ("python3 sample.py" +
            " -s soil_type -p pressure_setpoint" + 
            " [-t pressure_error_tolerance]" +
            " [-r sampling rate]")
    print(cmd_line)


if __name__ == '__main__':
    # read command line arguments
    # require: pressure setpoint, soil type
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:p:t:o:h") 
    except getopt.GetoptError as err:
        # print help information and exit:
        err = "Unrecognized options."
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    soil_type = None
    p_set = None
    p_tol = None
    sampling_rate = None
    for o, a in opts:
        if o == "-s":
            soil_type = a
            print("Soil type is: {}.".format(soil_type))
        elif o == '-p':
            p_set = float(a)
            print("Pressure set to: {}".format(p_set))
        elif o == '-t':
            p_tol = float(a)
            print("Pressure error tolerance changed to {}.".format(p_tol))
        elif o == '-r':
            sampling_rate = float(a) 
            print("Sampling rate changed to {}.".format(sampling_rate))
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    if soil_type is None:
        print("soil_type must be specified\n")
        usage()
        sys.exit(2)
    elif p_set is None:
        print("pressure setpoint must be specified\n")
        usage()
        sys.exit(2)
    if p_tol is None and sampling_rate is None:
        main(soil_type, p_set)
    elif p_tol is None:
        main(soil_type, p_set, sampling_rate=sampling_rate)
    else:
        main(soil_type, p_set, p_tol=p_tol, sampling_rate=sampling_rate)
