from pyModbusTCP.client import ModbusClient
#from Database_functions import *
from datetime import datetime

#client class is for setting a function that read and write from a Modbus TCP device.
class client():
    def __init__(self, ip_address, port = 502 , mac = "Not Added"):
        self.ip_address = ip_address
        self.port = port
        self.client = ModbusClient(self.ip_address, self.port, auto_open=True, auto_close=True)
        self.mac = mac

    #read_coils return list of bits or None if error (Read and Write)
    def read_coils(self, bit_addr, bit_nb): 
        if bit_nb == 1:
            return self.client.read_coils(bit_addr)
        else:
            return self.client.read_coils(bit_addr, bit_nb)
        

    #read_discrete_inputs return list of bits or None if error (Read Only)
    def read_discrete_inputs(self, bit_addr, bit_nb):
        if bit_nb == 1:
            return self.client.read_discrete_inputs(bit_addr)
        else:
            return self.client.read_discrete_inputs(bit_addr, bit_nb)
    
    #read holding registers return list of int or None if error (Read and Write)
    def read_holding_registers(self, reg_addr, reg_nb):
        if reg_nb == 1:
            return self.client.read_holding_registers(reg_addr)
        else:
            return self.client.read_holding_registers(reg_addr, reg_nb)

    #read input registers return list of int or None if error (Read Only)
    def read_input_registers(self, reg_addr, reg_nb):
        if reg_nb == 1:
            return self.client.read_input_registers(reg_addr)
        else:
            return self.client.read_input_registers(reg_addr, reg_nb)

    #Write multiple coils return True if write is successful
    def write_multiple_coils(self, bits_addr, bits_value):
        return self.client.write_multiple_coils(bits_addr, bits_value)  
    
    #Write multiple registers return True if write is successful
    def write_multiple_registers(self, regs_addr, regs_value):
        return self.client.write_multiple_registers(regs_addr, regs_value)

    #Write single register return True if write is successful
    def write_single_register(self, regs_addr, reg_value):
        return self.client.write_single_register(regs_addr,reg_value)

    #Write single coil return True if write is successful
    def write_single_coil(self, bit_addr, bit_value):
        return self.client.write_single_coil(bit_addr, bit_value)

    def change_device_ip(self, new_ip_address, new_port = 502):
        self.ip_address = new_ip_address
        self.port = new_port
        self.client = ModbusClient(self.ip_address, self.port, auto_open=True, auto_close=True)


