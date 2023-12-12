
from settings import PM_config
from SocketIoHandler import SocketIoHandler
from CommandHandler import CommandHandler
from SchneiderElectric_iM221 import SchneiderElectric_iM221
from multiprocessing import Process


#MOCK https://mocki.io/v1/d9941b84-2179-499a-9697-f556daf5a90d
from logmanagement import logmanagement
log = logmanagement.getlog('main', 'utils').getLogger()

threads = []

def main():
	PM_cacheEnabled = PM_config['cacheEnabled']
	pm=None
	pm = SchneiderElectric_iM221(PM_config['host'], PM_config['port'], 
		int(PM_config['address']), PM_config['start_reg'], 
		PM_config['max_regs'], PM_config['timeout'], 
		PM_config['endian'], PM_config['addressoffset'], 
		PM_cacheEnabled, PM_config['base_commands'])
		
	print("Connesso? %s" % pm.mb.isConnected)
  
	SIO=SocketIoHandler()
	if not pm.mb.isConnected:
		print("-------------------- PM ERROR CONNECTIONS --------------------")
		return 
        # logmanagement.se

	CMD_HANDLER=CommandHandler(pm,SIO)
	SIO.setCallBackListener(CMD_HANDLER.run_command)
	zonesPayload=CMD_HANDLER.config
	CMD_HANDLER.runZoneAgent(zonesPayload[0])

	#for zone in zonesPayload:
		
	#		CMD_HANDLER.listener_handler(zone)
 			

                                                          
            
 

if __name__ == '__main__':
	main()
