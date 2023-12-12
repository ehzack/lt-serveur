
import requests
from time import sleep
import json

from settings import BACKEND_config
from logmanagement import logmanagement
log = logmanagement.getlog('CommandHandler', 'utils').getLogger()
class CommandHandler(object):

  def allEqual(self,iterable):
    iterator = iter(iterable)
    
    try:
        firstItem = next(iterator)
    except StopIteration:
        return True
        
    for x in iterator:
        if x!=firstItem:
            return False
    return True



  def __init__(self,PM,socket):
    self.PM=PM
    self.socketHandler=socket

    self.config=None
    self.normal_source=None
    self.electricity=None
    self.generator_alarme=None
    self.gasoline=None
    log.debug("Instanciate  Handler Class")

    self.init_config()

  def init_config(self):
    response = requests.get(BACKEND_config['config']+"/zone/api")      
    self.config=response.json()

    response = requests.get(BACKEND_config['config']+"/normal_source")      
    self.normal_source=response.json()

    response = requests.get(BACKEND_config['config']+"/electricity")      
    self.electricity=response.json()

    response = requests.get(BACKEND_config['config']+"/generator_alarme")      
    self.generator_alarme=response.json()

    response = requests.get(BACKEND_config['config']+"/gasoline")      
    self.gasoline=response.json()

    log.debug("Get All Configuration(Zones,Normal Source,electricity,generator_alarme,gasoline)")



  def read_data_handler(self,item):
   try: 
      log.debug("Reading Zone %s",item["id"])
      resPayload={"id":item["id"],"ValeurRealTime":0,"equipements":[]}
      # LevelRealTime=self.PM._modbusRead(item["Adress"],3,"uint16")
      eq_values=[]
      for j,eq in enumerate(item["equipements"],start=0):
        alarmePayload=[]
        extraData=[]
        # ITEMS
        for k,tmpitem in enumerate(eq["items"],start=0):
           tmp1={"id":tmpitem["id"],"ValeurRealTime":int(self.PM._modbusRead(tmpitem["adresse"],1,"bool"))}
           alarmePayload.append(tmp1)

        # # EXTRA_DATA  
        if eq["extra_data"] :     
         for k,tmpExtraData in enumerate(eq["extra_data"],start=0):
           tmp2={"id":tmpExtraData["id"],"Value":int(self.PM._modbusRead(tmpExtraData["adress"],3,"uint16"))}
           extraData.append(tmp2)

        val=self.PM._modbusRead(eq["Adress"],3,"uint16")  
        eq_values.append(val)
 
        resPayload["equipements"].append({"id":eq["id"],"LevelRealTime":val,"extra_data":extraData,'items':alarmePayload,"ModeTel_Value":int(self.PM._modbusRead(eq["modeTel_adress"],1,"bool"))}) 


      if (self.allEqual(eq_values)):
        resPayload['ValeurRealTime']=val     
      else:
        resPayload['ValeurRealTime']=-1
      log.debug('Prepare Payload  Zone %s : %s',item["id"],json.dumps(resPayload))
   except: 
    log.error("An exception occurred on data handler reader ZONE")    
    return []
   return resPayload 


  def listener_handler(self,item):
    while True:
        
      if   self.socketHandler.isConnected():
       data_reader=self.read_data_handler(item)

      if  self.socketHandler.isConnected() == True:
           log.debug("Zone %s : %s",item["id"],json.dumps(data_reader))
           self.socketHandler.socket.emit('real_time_data', data_reader)
      #  sleep(20)
     




#################### NORMAL SOURCE ###########################""

  def read_normal_source(self):
    try: 
      data = self.normal_source
      log.debug("Normal Source Data : %s",json.dumps(data))    
      
      resPayload=[]
      for i,item in enumerate(data,start=0):
       resPayload.append({"id":item["id"],"value":int(self.PM._modbusRead(645,1,"bool"))})
    except: 
      log.error("read normal source :An exception occurred")    
      return []
    return resPayload 


  def listener_normal_source(self):
    #log.debug("Start Normal Source")
    while True:
      
      if    self.socketHandler.isConnected():
       data_reader=self.read_normal_source()
       log.debug("Normal Source : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_normal_source', data_reader)
      #  sleep(20)
     












#################### electricity ###########################""

  def read_electricity(self):
    try: 
      data = self.electricity
      log.debug("Electricity Data : %s",json.dumps(data))    

      resPayload=[]
      for i,item in enumerate(data,start=0):
       resPayload.append({"id":item["id"],"value":int(self.PM._modbusRead(645,1,"bool"))})
    except: 
      log.error("Read Electricity : An exception occurred")    
      return []
    return resPayload 


  def listener_electricity(self):
    while True:
        
      if    self.socketHandler.isConnected():
       data_reader=self.read_electricity()
       log.debug("electricity : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_electricity', data_reader)
      #  sleep(20)
     















#################### generator_alarme ###########################""

  def read_generator_alarme(self):
    try: 
      data = self.generator_alarme
      log.debug("GGenerator Alarm : %s",json.dumps(data))    

      resPayload=[]
      for i,item in enumerate(data,start=0):
       resPayload.append({"id":item["id"],"value":int(self.PM._modbusRead(645,1,"bool"))})
    except: 
      log.error(" read_generator_alarme : An exception occurred")    
      return []
    return resPayload 


  def listener_generator_alarme(self):
    while True:
        
      if    self.socketHandler.isConnected():
       data_reader=self.read_generator_alarme()
       log.debug("generator_alarme : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_alarme', data_reader)
      #  sleep(20)















#################### gasoline ###########################""

  def read_gasoline(self):
    try: 
      data = self.gasoline
      log.debug("Gasoline Data : %s",json.dumps(data))    

      resPayload=[]
      for i,item in enumerate(data,start=0):
       
       resPayload.append({"id":item["id"],"value":int(self.PM._modbusRead(645,1,"bool"))})
    except: 
      log.error("Read Gasoline : An exception occurred")    
      return []
    return resPayload 


  def listener_gasoline(self):
    while True:
        
      if    self.socketHandler.isConnected():
       data_reader=self.read_gasoline()
       log.debug("Gasoline : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_gasoline', data_reader)
      #  sleep(20)






       
  def run_command (self,data): 
   
   log.debug("Run Command: %s", json.dumps(data)) 

   if  self.socketHandler.isConnected() == False:
      log.error("Cannot Connect to socket") 
      return False
   try: 
      if(type([]) == type(data)):
       for i,item in enumerate(data,start=0):
        try: 
         l1 = self.PM.cmd_set_value(int(item["Adress"]),int(item["value"]),6)
         log.debug("Output Command: %s",l1)
        except: 
         log.error("Commande : %s, value: %s An exception occurred",item["Adress"],item["value"])


      else:
       l1 = self.PM.cmd_set_value(int(data),1)
       log.debug("Output Command: %s",l1)

   except: 
    log.error("Commande : %s An exception occurred",data)

