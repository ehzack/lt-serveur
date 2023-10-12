from settings import PM_config
from SchneiderElectric_iM221 import SchneiderElectric_iM221

def main():
    PM_cacheEnabled = PM_config['cacheEnabled']
    pm=None
    pm = SchneiderElectric_iM221(PM_config['host'], PM_config['port'], 
		int(PM_config['address']), PM_config['start_reg'], 
		PM_config['max_regs'], PM_config['timeout'], 
		PM_config['endian'], PM_config['addressoffset'], 
		PM_cacheEnabled, PM_config['base_commands'])
		
    print("Connesso? %s" % pm.mb.isConnected)
    payload = [[5, 'int16'],[1, 'uint16']]

    
    pm.cmd_set_value(491,1,6)

  


if __name__ == '__main__':
	main()