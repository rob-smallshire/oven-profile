import sys

import docopt_subcommands as dsc

from oven_profile.version import __version__


@dsc.command()
def datalog_handler(args):
    """usage: {program} datalog <serial-port>

    Wait for an oven reflow cycle and log profile.
    """
    from oven_profile.datalog import datalog_command
    serial_port = args['<serial-port>']
    datalog_command(serial_port)
    return 0


@dsc.command()
def plot_handler(args):
    """usage: {program} plot <file>

    Wait for an oven reflow cycle and log profile.
    """
    from oven_profile.plot import plot_command
    file_path = args['<file>']
    plot_command(file_path)
    return 0


def main():
    return dsc.main(
        program='oven-profile',
        version=__version__)


if __name__ == '__main__':
    sys.exit(main())
