#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smbus
import time
import math
import logging
from enum import IntEnum

I2C_BUS							= 1

# HYT939 default address
HYT939_I2CADDR					= 0x28	# HYT939 address, 0x28(40)

# Operating Modes
HYT939_NORMALMODE				= 0x80	# 0x80(128) Send normal mode
HYT939_COMMANDMODE				= 0xA0	# 0xA0(160) Send command mode

# HYT939 Registers
HYT939_READ_CONFIG				= 0x1C
HYT939_WRITE_CONFIG				= 0x5C

HYT939_MAX_SWITCHINGMODE_TIME	= 100	# mSec




# HYT939 Constants for Dew Point calculation
HYT939_A = 8.1332
HYT939_B = 1762.39
HYT939_C = 235.66





class TemperatureUnit(IntEnum):
	CELSIUS = 0
	FAHRENHEIT = 1
	KELVIN = 2

class HYT939_Modes(IntEnum):
	NORMALMODE = HYT939_NORMALMODE
	COMMANDMODE = HYT939_COMMANDMODE

class HYT939(object):

	def __init__(self, busnum=I2C_BUS, address=HYT939_I2CADDR, mode=HYT939_Modes.NORMALMODE):
		self._bus = smbus.SMBus(busnum)
		self._address = address

		self._logger = logging.getLogger('HYT939')

		self.switch_to_mode(mode)

	@property
	def bus(self):
		return self._bus

	@property
	def addr(self):
		return self._address

	def switch_to_mode(self, mode=HYT939_Modes.NORMALMODE):
		self.send_command(mode)
		time.sleep(HYT939_MAX_SWITCHINGMODE_TIME/1000)

	def change_address(self, new_addr):
		# ONLY UNDER 10MS FROM POWER ON RESET
		print("NOT TESTED")
		self.switch_to_mode(HYT939_Modes.COMMANDMODE)
		self._bus.write_byte(self._address, HYT939_WRITE_CONFIG)
		self._bus.write_byte(self._address, 0)
		self._bus.write_byte(self._address, new_addr)
		time.sleep(HYT939_MAX_SWITCHINGMODE_TIME/1000)
		self.switch_to_mode(HYT939_Modes.NORMALMODE)


	def send_command(self, command=0):
		self._bus.write_byte(self._address, command)


	def read_raw_humidity(self):
		# self.send_command(HYT939_NORMALMODE)
		# time.sleep(HYT939_MAX_SWITCHINGMODE_TIME/1000)

		# Read data back from 0x00(00), 4 bytes
		# Humidity MSB, Humidity LSB, Temp MSB, Temp LSB
		raw = self._bus.read_i2c_block_data(self._address, 0x00, 2)
		if raw:
			word = (raw[0]<<4) | (raw[1]>>4)
			self._logger.debug('Raw relative humidity 0x{0:04X} ({1})'.format(word & 0xFFFF, word))
			return raw
		return None

	def read_raw_temp(self):
		# self.send_command(HYT939_NORMALMODE)
		# time.sleep(HYT939_MAX_SWITCHINGMODE_TIME/1000)

		# Read data back from 0x00(00), 4 bytes
		# Humidity MSB, Humidity LSB, Temp MSB, Temp LSB
		raw = self._bus.read_i2c_block_data(self._address, 0x00, 4)[2:]
		if raw:
			word = (raw[0]<<4) | (raw[1]>>4)
			self._logger.debug('Raw temp 0x{0:X} ({1})'.format(word & 0xFFFF, word))
			return raw
		return None

	def read_humidity(self):
		data = self.read_raw_humidity()
		if data:
			humidity = ((data[0] & 0x3F) * 256 + data[1]) * (100 / 16383.0)
			self._logger.debug('Relative Humidity {0:.2f} %'.format(humidity))
			return humidity
		return None

	def read_temperature(self, T_UNIT=TemperatureUnit.CELSIUS):
		data = self.read_raw_temp()
		if data:
			unit = ""
			temp = ((data[0] * 256 + (data[1] & 0xFC)) / 4) * (165 / 16383.0) - 40
			if T_UNIT == TemperatureUnit.CELSIUS:
				unit = "C"
			elif T_UNIT == TemperatureUnit.FAHRENHEIT:
				unit = "F"
				temp = temp * 1.8 + 32
			elif T_UNIT == TemperatureUnit.KELVIN:
				unit = "K"
				temp = temp + 273.15

			self._logger.debug('Temperature {0:.2f} {1}'.format(temp, unit))
			return temp
		return None

	def read_partialpressure(self):
		"""Calculate the partial pressure in mmHg at ambient temperature."""
		v_temp = self.read_temperature()
		if v_temp:
			v_exp = HYT939_B / (v_temp + HYT939_C)
			v_exp = HYT939_A - v_exp
			v_part_press = 10 ** v_exp
			self._logger.debug('Partial Pressure {0:.2f} mmHg'.format(v_part_press))
			return v_part_press
		return None

	def read_dewpoint(self):
		"""Calculates the dew point temperature."""
		# Calculation taken straight from datasheet.
		ppressure = self.read_partialpressure()
		humidity = self.read_humidity()
		if ppressure and humidity:
			den = math.log10(humidity * ppressure / 100) - HYT939_A
			dew = -(HYT939_B / den + HYT939_C)
			self._logger.debug('Dew Point {0:.2f} C'.format(dew))
			return dew
		return None


if __name__ == "__main__":
	hyt = HYT939()

	# print(hyt.read_raw_temp())

	hum = hyt.read_humidity()
	print("Relative Humidity is : %.2f %%RH" %hum)
	temp = hyt.read_temperature()
	print("Temperature in Celsius is : %.2f C" %temp)
