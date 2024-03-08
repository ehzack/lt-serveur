#
import configparser


def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config['Settings']


config = read_config('config.ini')

__author__ = 'Zakaria El Hedadi'

debug = True

PM_config = {
	'host': config.get("PM_HOST"),
	'port': config.get("PM_PORT"),
	'address': 1,
	'addressoffset': -1,
	'start_reg': 0,
	'max_regs': 125,
	'timeout': 2,
	'endian': 'big',
	'cacheEnabled': True,
	'base_commands': 5250
}

BACKEND_config = {
	'socket_url': config.get("SOCKET_URL"),
	'config':config.get("API_URL")

}
PM_settings = {
	'Set DateTime': {
		'command': 1003
	},
	'Set Wiring': {
		'command': 2000,
		'Power System Configuration': 11,
		'Nominal Frequency': 60,
		'VT Primary': 100.0,
		'VT Secondary': 100,
		'Number of CTs': 3,
		'CT Primary': 60,
		'CT Secondary': 5,
		'VT Connection type': 0
	},
	'Set Pulse Output': {
		'command': 2003,
		'Pulse Output enable': 1,
		'Pulse constant': 1,

		'command2': 2038,
		'Pulse width': 50
	},
	'Set Tariff': {
		'command': 2060,
		'Multi Tariff Mode': 0,
		'command2': 2008,
		'Tariff': 1
	},
	'Set Digital Input as Partial Energy Reset': {
		'command': 6017,
		'Digital Input to Associate': 0
	},
	'Input Metering Setup': {
		'command': 6014,
		'Input Metering Channel': 1,
		'Label': 'input',
		'Pulse Weight': 1000,
		'Digital Input Association': 0
	},
	'Overload Alarm Setup': {
		'command': 7000,
		'Alarm ID': 0,
		'Enabled': 0,
		'Pickup value': float(100000000),
		'command2': 20000,
		'Digital Output to Associate': 0,
		'command3': 20001
	},
	'Communications Setup': {
		'command': 5000,
		'Address': 1,
		'Baud Rate': 1,
		'Parity': 0
	},
	'Reset Partial Energy Counters': {
		'command': 2020
	},
	'Reset Input Metering Counter': {
		'command': 2023
	},
}

MODBUS_CONNECTIONRETRY = 3
PATH_LOGGING = 'configs/logging.json'
PATH_PM_SCHNEIDERELECTRICIM221 = 'configs/Map-Schneider-iM221.csv'
PM_SETTINGS_LABELS = [
	"Meter Name", "Meter Model", "Manufacturer", "Serial Number", 
	"Date of Manufacture", "Hardware Revision", "Firmware Version", 
	"Meter Operation Timer", "Number of Phases", "Number of Wires",
	"Power System", "Nominal Frequency", "Number VTs", "CT Primary", 
	"CT Secondary",	"Number CTs", "CT Primary", "CT Secondary", 
	"VT Connection Type", "Energy Pulse Duration", 
	"Digital Output Association", "Pulse Weight"
]

