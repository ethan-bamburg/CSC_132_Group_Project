"""
This file will be used to launch the app, serves as the temporary todo list- create tasks as seen fit

-- Project Details --
The project itself will contain many parts and each
of which must communicate to one another. The arduino
Uno will be connected to a main power supply, with the
option of inputting a computer connection for the gui.
The uno will transmit and recieve information from the
nano- the nano serving as a secondary way to change
the system's settings.

The arduino nano will handle function and communication,
it will transmit and recieve information from the nano and,
optionally, the system.

#TODO: GUI
    # TODO - Main User Interface
    # TODO - Connect Buttons to event hooks

#TODO: Arduino Uno
    # TODO - Create a transmitter system (transmit info until it receives a response from computer and transmit live data)
    # TODO - Create a listener system (recieve info from system/nano to change physical circuit)
    # TODO - Create a built-in set of functions to easily change motor, servo, etc. activity

#TODO: Arduino Nano
    # TODO - Create LCD compatability
    # TODO - Create transmitter and listener system

#TODO: System Architecture
    # TODO - Create a listening system (wait for arduino input)
    # TODO - Create communicator (Serve as the intermediatry between arduino communication and gui display)
    # TODO - Connect GUI to Arduino Information

#TODO: Circuit (Uno)
    # TODO - Motor, servo, 3d printed parts, ir transciever

#TODO: Circuit (Nano)
    # TODO - LCD, push buttons, ir transciever

#TODO: Outreach goals
    # TODO - Graph data
    # TODO - Database (SQL?)
    # TODO - Weather webhook / API


"""