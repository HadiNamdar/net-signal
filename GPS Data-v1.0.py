import os
import sys
import glob
import serial
import pynmea2

def serial_ports():

    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def main():
    print("Available serial ports include: ")
    print(serial_ports())
    COM_n = input("Please enter the COM number of GPS module (1-256): ")
    COM = str(f'COM{COM_n}')
    ser = serial.Serial()
    ser.port = COM
    ser.baudrate = 9600
    ser.timeout = 0.5
    ser.open()
    if ser.is_open == True:
        print("Serial Connection created successfully")
        while True:
            dataout = pynmea2.NMEAStreamReader()
            line = ser.readline()   # read a byte
            if line[0:6] == "$GPRMC":
                newmsg=pynmea2.parse(line)
                lat=newmsg.latitude
                lng=newmsg.longitude
                gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                print(gps)
        ser.close()
    else:
        print("Serial Connection is not established")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
