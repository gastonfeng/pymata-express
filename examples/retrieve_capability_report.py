"""
 Copyright (c) 2018-2019 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import asyncio
import sys

from pymata_express.pymata_express import PymataExpress

# This is a demo of retrieving an Firmata capability report and
# printing a formatted report to the console

def format_capability_report(data):
    """
    This method prints a formatted capability report to the console.

    :param data: Capability report

    :returns: None
    """

    pin_modes = {0: 'Digital_Input', 1: 'Digital_Output',
                 2: 'Analog_Input', 3: 'PWM', 4: 'Servo',
                 6: 'I2C', 8: 'Stepper',
                 11: 'Digital_Input_Pullup', 12: 'HC-SR04_Sonar', 13: 'Tone'}
    x = 0
    pin = 0

    print('\nCapability Report')
    print('-----------------\n')
    while x < len(data):
        # get index of next end marker
        print('{} {}{}'.format('Pin', str(pin), ':'))
        while data[x] != 127:
            mode_str = ""
            pin_mode = pin_modes.get(data[x])
            mode_str += str(pin_mode)
            x += 1
            bits = data[x]
            print('{:>5}{}{} {}'.format('  ', mode_str, ':', bits))
            x += 1
        x += 1
        pin += 1


async def retrieve_capability_report(my_board):
    """

    :param my_board: a pymata-express instance
    """
    # get the report
    report = await my_board.get_capability_report()

    # print a human readable version
    format_capability_report(report)

# Get the loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = PymataExpress()

try:
    # run the program
    loop.run_until_complete(retrieve_capability_report(board))

    # orderly shutdown
    loop.run_until_complete(board.shutdown())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
