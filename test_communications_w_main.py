# file: test_communications.py

""" This code verifies that data can be written to an Arduino for initialization,
    and read back from the same Arduino.
"""
import serial
import time

def main():
    ser = serial.Serial('/dev/ttyUSB0',baudrate=115200, timeout=5.0)
    time.sleep(2.)
    data = 3.14
    returned_data = None
    #ser.write(b'3.14\n')
    ser.write(bytes(str(data)+'\n','utf-8'))
    ser.flush()
    #print("wrote to serial")
    time.sleep(0.5)
    print(ser.in_waiting)
    if ser.in_waiting > 0:
        print("reading return message")
        msg = ser.readline()
        returned_data = float(msg)
    print(returned_data)
    assert returned_data == data

    # Now grab ten data entries
    data_array = []
    for i in range(10):
        msg = ser.readline()
        data_array.append(float(msg))

    print(data_array)

if __name__ == '__main__':
    main()
