#!/usr/bin/python3
import sys

class sensor_config():
    # find connected sensors
    def find_settings():
        print("connection_type=gpio")
        print("connection_address_list=")
        print("default_connection_address=")



def read_sensor(location="", extra="", sensor_name="", use_pigpio=False, *args):
    # Try importing the modules then give-up and report to user if it fails
    import datetime
    import time
    if use_pigpio == False:
        try:
            import board
            import adafruit_dht
        except:
            print("adafruit_dht22 module not installed, install using the command;")
            print("     sudo pip3 install adafruit-circuitpython-dht")
            return None


        # set up and read the sensor
        read_attempt = 1
        dht = adafruit_dht.DHT22(int(location))
        ### new line added - check if exit function exists
        dhtExit = callable(getattr(dht,'exit'))
        while read_attempt < 5:
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                #
                if humidity == None or temperature == None or humidity > 101:
                    print("--problem reading DHT22, try " + str(read_attempt))
                    time.sleep(2)
                    read_attempt = read_attempt + 1
                else:
                    humidity = round(humidity,2)
                    temperature = round(temperature, 2)
                    logtime = datetime.datetime.now()
                    ### new line exit dht after read freeing up pin lock
                    if dhtExit:
                        dht.exit()
                    return [['time',logtime], ['humid', humidity], ['temperature', temperature]]
            except Exception as e:
                print("--exception while reading DHT22, try " + str(read_attempt))
                print(" -- " + str(e))
                time.sleep(2)
                read_attempt = read_attempt + 1
        ### New line additional exit
        if dhtExit:
            dht.exit()
        if read_attempt > 4:
            read_sensor(location=sensor_location, use_pigpio=True)
        return None
    else:
        try:
            import subprocess
            from subprocess import Popen
            proc = Popen(["pigs", "t"],stdout=subprocess.PIPE)
            testVal = proc.stdout.read()
            if not testVal:
                print("Pigpio is not running")
                print("     sudo pigpio to start the daemon")
                print("     One time required on per boot")
                print("     may be add to 'sudo crontab -e' for autorun")
                print("     @reboot sudo pigpio")
            import pigpio
            import DHT22
        except:
            print("Pigpio DHT22 module not included, install using the commands;")
            print("     cd ~/Pigrow/scripts/gui/sensor_modules")
            print("     wget abyz.me.uk/rpi/pigpio/code/DHT22_py.zip")
            print("     unzip DHT22_py.zip")
            return None
        # set up and read the sensor
        read_attempt = 1
        while read_attempt < 5:
            try:
                pi = pigpio.pi()
                sensor = DHT22.sensor(pi,int(location))
                sensor.trigger()
                time.sleep(0.5)
                temperature = sensor.temperature()
                humidity = sensor.humidity()
                #print (temperature)
                #print (humidity)
                sensor.cancel()
                #pi.stop()
                #
                if humidity == None or temperature == None or humidity > 101:
                    print("--problem reading DHT22, try " + str(read_attempt))
                    time.sleep(2)
                    read_attempt = read_attempt + 1
                else:
                    humidity = round(humidity,2)
                    temperature = round(temperature, 2)
                    logtime = datetime.datetime.now()
                    pi.stop()
                    return [['time',logtime], ['humid', humidity], ['temperature', temperature]]
            except Exception as e:
                print("--exception while reading DHT22, try " + str(read_attempt))
                print(" -- " + str(e))
                time.sleep(2)
                read_attempt = read_attempt + 1
        return None


if __name__ == '__main__':
    '''
      The DHT22 requires the location of it's signal wire
      '''
     # check for command line arguments
    sensor_location = ""
    use_pigpio_value = False
    for argu in sys.argv[1:]:
        if "=" in argu:
            thearg = str(argu).split('=')[0]
            thevalue = str(argu).split('=')[1]
            if thearg == 'location':
                sensor_location = thevalue
            elif thearg == 'use_pigpio':
                use_pigpio_value = thevalue
        elif 'help' in argu or argu == '-h':
            print(" Modular control for dht22 temp sensors")
            print(" ")
            print("")
            print(" -config  ")
            print("        display the config information")
            print("")
            sys.exit(0)
        elif argu == "-flags":
            sys.exit(0)
        elif argu == "-config":
            sensor_config.find_settings()
            sys.exit()
    # read sensor
    if not sensor_location == "":
        output = read_sensor(location=sensor_location,use_pigpio=use_pigpio_value)
    else:
        print(" No sensor address supplied, this requries a sensor address.")
        sys.exit()
    #
    if output == None:
        print("!! Failed to read !!")
    else:
        for x in output:
            print(str(x[0]) + "=" + str(x[1]))

