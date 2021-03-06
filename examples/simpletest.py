#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BEGIN_COPYRIGHT
#
# The MIT License (MIT)
#
# Copyright (c) 2021 Diego Chialvi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# END_COPYRIGHT

# Comment/Uncomment to disable/enable debug output:
import logging
logging.basicConfig(level=logging.DEBUG)

import HYT939.HYT939 as HYT939

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = HYT939.HYT939()

# Optionally you can override the bus number:
#sensor = HYT939.HYT939(busnum=2)

# Optionally you can override the sensor's address:
#sensor = HYT939.HYT939(address=0x28)


print ('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print ('Humidity  = {0:0.2f} %'.format(sensor.read_humidity()))
print ('Dew Point = {0:0.2f} *C'.format(sensor.read_dewpoint()))
