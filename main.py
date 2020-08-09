import pycom
import time
from machine import Pin
from machine import Timer
from onewire import OneWire #Library for Onewire
from onewire import DS18X20 #Library for dealing with DS18X20 sensors

pycom.heartbeat(False) #Disable pycom rgbled heartbeat function
ow = OneWire(Pin('P10')) #Create an object for interfacing through onewire on P10
temp = DS18X20(ow) #Create on object for temperature from DS18B20 with onewire
owtemp = temp.read_temp_async() #Read the temperature value from DS18B20
temp.start_conversion() #This is called after reading the temperature

print("DS18B20 - Temperature at start: %d C" % owtemp) #Output the DS18B20 temperature at boot-up

pybytes.send_signal(1,owtemp)

if owtemp < 23.0:
    pycom.rgbled(0x007f00) # led on board green if temp below 23 C degrees
    time.sleep(3)
else:
    pycom.rgbled(0x7f0000) # led on board red if temp above 23 C degrees
    time.sleep(3)

pycom.rgbled(0x000008) # led on board blue between measurements


button = Pin("P14", mode=Pin.IN, pull=Pin.PULL_UP) #Create a button object with internal pull up connected to P14

chrono = Timer.Chrono() #Create a Chrono object from Timer to measure time
chrono.start() #Start measuring time

#Main loop for sending measurements, time based or manually triggered with push button
#the led on the expansion board will change color depending on temperature. if the temp is above 23 it shall turn red of below 23 it shall turn green.
#between the measurements it shall be kept blue

while True:
    #Read button value
    button_value = button() #Get the current state of the button, 1 is not pressed, 0 is pressed
    elapsed_seconds = chrono.read() #Get the elapsed time since start of chrono (or reset)

    if button_value == 1 and elapsed_seconds < 900: #Check if button is not pressed AND that the elapsed time is below threshold
        time.sleep(1) #Sleep before next loop

    elif button_value == 0: #Button has been pressed, send measurements to PyBytes and output to terminal
        print("Button has been pushed after %f seconds, sending values to PyBytes" % elapsed_seconds)
        owtemp = temp.read_temp_async()
        pybytes.send_signal(1,owtemp)
        temp.start_conversion()
        if owtemp < 23.0:
            pycom.rgbled(0x007f00) # led on board green
        else:
            pycom.rgbled(0x7f0000) # led on board red
        time.sleep(3)
        pycom.rgbled(0x000008) # led on board blue
        chrono.reset() #Reset chrono for next measurement

    elif elapsed_seconds > 900: #Timer threshold has been reached, send measurements to PyBytes and output to terminal
        print("Idle time out limit reached after %f seconds, sending values to PyBytes" % elapsed_seconds)
        owtemp = temp.read_temp_async()
        pybytes.send_signal(1,owtemp)
        temp.start_conversion()
        if owtemp < 23.0:
            pycom.rgbled(0x007f00) # led on board green
        else:
            pycom.rgbled(0x7f0000) # led on board red
        time.sleep(3)
        pycom.rgbled(0x000008) # led on board blue
        chrono.reset()
