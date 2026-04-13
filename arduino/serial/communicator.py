import serial # pyserial
import serial.tools.list_ports # to scan all ports
from time import sleep

_DEBUG = True


def debug_wrap(msg):
    if _DEBUG:
        print(msg)


def pair_serial():

    # get all ports
    ports = serial.tools.list_ports.comports()

    # loop through all ports
    for port in ports:

        # try except to prevent runtime errors
        try:
            # attempt to open a connection, 9600 is arudino serial
            debug_wrap(f"Trying {port.device}...")
            ser = serial.Serial(port.device, 9600, timeout=1)
            sleep(2)  # allow arduino to reset

            # try reading a few lines in the serial monitor
            for _ in range(5):

                # look for stuff that is waiting to be read
                if ser.in_waiting:
                    # take lines in the serial monitor, ignore any errors
                    line = ser.readline().decode(errors='ignore').strip()
                    debug_wrap(f"[{port.device}] {line}")

                    # if the port has the message we're looking for, that's the arduino!
                    if "{PAIR}" in line:
                        debug_wrap(f"Found Arduino on {port.device}")

                        # return the serial port we found the arduino on
                        return ser
                    
            # close this port, not the arduino
            ser.close()

        # some error happened on this port device, print error
        except Exception as e:
            debug_wrap(f"Failed on {port.device}: {e}")

    # nothing worked, run "sudo rm -rf \"
    return None


if __name__ == "__main__":
    # find the serial port the arduino is connected to
    ser = pair_serial()

    # can't find it, abort
    if ser is None:
        print("Couldn't find arduino")
        exit()


    # we are now paired
    print(f"Paired with arduino on port {ser.port}")

    # continual communication with arduino, remember ctrl + c to keyboard interrupt
    while True:
        #sleep(.5)   # test lol
        if ser.in_waiting:
            # read line in serial monitor
            line = ser.readline().decode(errors='ignore').strip()
            # the data we got from the line
            print("Received:", line)

            # identify communication type
            if line.startswith("{"):
                # respond to continue communication
                debug_wrap("Sent: {ACK}")
                # b turns into binary
                ser.write(b"{ACK}\n")

