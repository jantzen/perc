# file: test_communications.py

""" This code verifies that data can be written to an Arduino for initialization,
    and read back from the same Arduino.
"""
import serial
import time

ser = serial.Serial('/dev/ttyUSB0',baudrate=115200, timeout=5.0)
ser.write(b'3.14\n')
ser.flush()
print("wrote to serial")
time.sleep(2.)
print(ser.in_waiting)
if ser.in_waiting > 0:
    print("reading return message")
    msg = ser.readline()
    print(msg)
#    wait = True
#    while wait:
##        if ser.out_waiting == 0 and ser.in_waiting > 0:
#        print(ser.in_waiting)
#        if ser.in_waiting > 0:
#            msg = ser.readline()
#            wait = False
#        time.sleep(0.1)
#    print(msg)
##    assert msg == 3.14
            

