
from settings import PM_config
from SocketIoHandler import SocketIoHandler
from threading import Lock
from CommandHandler import CommandHandler
from threading import Thread
from SchneiderElectric_iM221 import SchneiderElectric_iM221
import json
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


	for zone in zonesPayload:
		log.debug('Start Zone Thread  %s',json.dumps(zone))	
		Thread(target=CMD_HANDLER.listener_handler,args=(zone,)).start()
 			
	log.debug('Start Normal Source Thread  %s',json.dumps(zone))	
	Thread(target=CMD_HANDLER.listener_normal_source).start()

	log.debug('Start Electricity Thread  %s',json.dumps(zone))	
	Thread(target=CMD_HANDLER.listener_electricity).start()

	log.debug('Start Generator Alarm Thread  %s',json.dumps(zone))	
	Thread(target=CMD_HANDLER.listener_generator_alarme).start()

	log.debug('Start Gasoline Thread  %s',json.dumps(zone))		
	Thread(target=CMD_HANDLER.listener_gasoline).start()


	log.debug('Start Run Command Thread')		

	Thread(target=SIO.call_backs).start()
    	 
 



if __name__ == '__main__':
	main()
