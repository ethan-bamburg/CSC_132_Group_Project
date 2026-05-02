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

            # clear startup garbage
            ser.reset_input_buffer()
            # ask for pair
            ser.write(b"PAIR\n")

            # try reading a few lines in the serial monitor
            for _ in range(10):

                # look for stuff that is waiting to be read
                if ser.in_waiting:
                    # take lines in the serial monitor, ignore any errors
                    line = ser.readline().decode(errors='ignore').strip()
                    debug_wrap(f"[{port.device}] {line}")

                    # if the port has a response, that's the arduino!
                    if "PAIR_OK" in line:
                        debug_wrap(f"Paired with Arduino on {port.device}")

                        # return the serial port we found the arduino on
                        return ser
                    
            # close this port, not the arduino
            ser.close()

        # some error happened on this port device, print error
        except Exception as e:
            debug_wrap(f"Failed on {port.device}: {e}")

    # nothing worked, run "sudo rm -rf \"
    return None


def handle_message(msg):
    # Handle what the arduino responds with
    debug_wrap("R: ", msg)

    if msg.startswith("DATA"):
        # Data protocol, everything after is what we need
        data = msg[5:]
        debug_wrap("Sensor data:", data)

    elif msg.startswith("EVENT"):
        # Event protocal, we need to log this
        event = msg[6:]
        debug_wrap("Event:", event)

    elif msg.startswith("ACK"):
        # Our operation was a success
        debug_wrap("Success:", msg)

if __name__ == "__main__":
    # find the serial port the arduino is connected to
    ser = pair_serial()

    # can't find it, abort
    if ser is None:
        print("Couldn't find arduino")
        exit()

    # continual communication with arduino, remember ctrl + c to keyboard interrupt
    if ser.in_waiting:
            msg = ser.readline().decode(errors='ignore').strip()
            handle_message(msg)



