import sys

import serial


def datalog_command(serial_port):
    state = -1
    with serial.Serial(serial_port, 57600, timeout=1) as port:

        while True:
            previous_state = state
            line = port.readline().decode('ascii')
            if not line:
                print("Timeout", file=sys.stderr)
                continue
            text_fields = line.split(',')
            try:
                time_milliseconds = int(text_fields[0])
                state = int(text_fields[1])
                set_point = float(text_fields[2])
                heater_value = int(text_fields[3])
                fan_value = int(text_fields[4])
                temperature_1 = float(text_fields[5])
                temperature_2 = float(text_fields[6])
            except (IndexError, ValueError) as e:
                print("Could not parse {!r} because {}".format(line, e), file=sys.stderr)
            else:
                if state != 0:
                    print('{}, {}, {}, {}, {}, {}, {}'.format(
                        time_milliseconds,
                        state,
                        set_point,
                        heater_value,
                        fan_value,
                        temperature_1,
                        temperature_2
                    ))
                if previous_state > state:
                    break