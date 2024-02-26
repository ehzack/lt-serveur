
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
    self.coils_values=None
    self.holding_registers_values=None
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

    response = requests.get(BACKEND_config['config']+"/macro/exec")      
    self.macro=response.json()

    log.debug("Get All Configuration(Zones,Normal Source,electricity,generator_alarme,gasoline,macro)")


  def read_data_handler(self,item):

    
      resPayload={"id":item["id"],"ValeurRealTime":0,"equipements":[]}
      # LevelRealTime=self.PM._modbusRead(item["Adress"],3,"uint16")
      eq_values=[]
      for j,eq in enumerate(item["equipements"],start=0):
        alarmePayload=[]
        extraData=[]
        # ITEMS
        for k,tmpitem in enumerate(eq["items"],start=0):
           tmp1={"id":tmpitem["id"],"ValeurRealTime":self.coils_values_mapper(tmpitem["adresse"])}
           alarmePayload.append(tmp1)

        # # EXTRA_DATA  
        if eq["extra_data"] :     
         for k,tmpExtraData in enumerate(eq["extra_data"],start=0):
           tmp2={"id":tmpExtraData["id"],"Value":self.holding_registers_mapper(tmpExtraData["adress"])}
           extraData.append(tmp2)

        val=self.holding_registers_mapper(eq["Adress"])  
        eq_values.append(val)
 
        resPayload["equipements"].append({"id":eq["id"],"LevelRealTime":val,"extra_data":extraData,'items':alarmePayload,"ModeTel_Value":self.coils_values_mapper(eq["modeTel_adress"]),"heur_Value":self.holding_registers_mapper(eq["heur_adress"]),"min_Value":self.holding_registers_mapper(eq["min_adress"])}) 


      if (self.allEqual(eq_values)):
        resPayload['ValeurRealTime']=val     
      else:
        resPayload['ValeurRealTime']=-1
      log.debug('Prepare Payload  Zone %s : %s',item["id"],json.dumps(resPayload))

      return resPayload 


  def listener_handler(self):
      
    for zone in self.config:
  
      if   self.socketHandler.isConnected():
       data_reader=self.read_data_handler(zone)
      if  self.socketHandler.isConnected() == True:
           log.debug("Zone %s : %s",zone["id"],json.dumps(data_reader))
           self.socketHandler.socket.emit('real_time_data', data_reader)

      #  sleep(20)
     
     
  def coils_values_mapper(self,val):
    val=int(val)
    if val in self.coils_values:
      return int(bool(self.coils_values[val]))
    else:
      log.debug("%s not Found in Coils",val)
      log.debug(self.coils_values)

      return -100

  def holding_registers_mapper(self,val):
    val=int(val)

    if val in self.holding_registers_values:
      return self.holding_registers_values[val]
    else:
      log.debug("%s not Found in Registers",val)
      log.debug(self.holding_registers_values)

      return -100
#################### NORMAL SOURCE ###########################""

  def read_normal_source(self):
    try: 
      data = self.normal_source
      log.debug("Normal Source Data : %s",json.dumps(data))    
      
      resPayload=[]
      for i,item in enumerate(data,start=0):
       resPayload.append({"id":item["id"],"value":int(self.coils_values_mapper(item["adress"]))})
    except: 
      log.error("read normal source :An exception occurred")    
      return []
    return resPayload 


  def listener_normal_source(self):

      
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
       resPayload.append({"id":item["id"],"value":int(self.coils_values_mapper(item["adress"]))})
    except: 
      log.error("Read Electricity : An exception occurred")    
      return []
    return resPayload 


  def listener_electricity(self):

        
      if    self.socketHandler.isConnected():
       data_reader=self.read_electricity()
       log.debug("electricity : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_electricity', data_reader)
      #  sleep(20)
     


#################### generator_alarme ###########################""

  def read_generator_alarme(self):
      data = self.generator_alarme
      log.debug("GGenerator Alarm : %s",json.dumps(data))    

      resPayload=[]
      for i,item in enumerate(data,start=0):
       resPayload.append({"id":item["id"],"value":int(self.holding_registers_mapper(item["adress"]) if item["label"] == 'Niveau_Gasoil' else self.coils_values_mapper(item["adress"]))})

      return resPayload 


  def listener_generator_alarme(self):

        
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
       
       resPayload.append({"id":item["id"],"value":int(self.holding_registers_mapper(item["adress"]))})
    except: 
      log.error("Read Gasoline : An exception occurred")    
      return []
    return resPayload 


  def listener_gasoline(self):

        
      if    self.socketHandler.isConnected():
       data_reader=self.read_gasoline()
       log.debug("Gasoline : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('real_time_gasoline', data_reader)
      #  sleep(20)

     



#################### MACRO VERIFY ###########################""

  def read_macro(self):
    try: 
      data = self.macro
      log.debug("Macro Data : %s",json.dumps(data))    

      resPayload=[]
      for i,item in enumerate(data,start=0):
       
       resPayload.append({"id":item["id"],"value":int(self.coils_values_mapper(item["exec_adress"]))})
    except: 
      log.error("Read Gasoline : An exception occurred")    
      return []
    return resPayload 


  def listener_macro(self):

        
      if    self.socketHandler.isConnected():
       data_reader=self.read_macro()
       log.debug("Macro Verification : %s ",json.dumps(data_reader))
      if  self.socketHandler.isConnected() == True:
          self.socketHandler.socket.emit('macro_exec', data_reader)
      #  sleep(20)

     

  def run_command (self,data): 
   
   log.debug("Run Command: %s", json.dumps(data)) 

   if  self.socketHandler.isConnected() == False:
      log.error("Cannot Connect to socket") 
      return False
   if True: 
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


  def readHoldingRegisters(self):
    startAdd = 0
    count = 708
    max_count_per_read = 125

    values = {}

# Perform multiple reads in chunks of max_count_per_read
    for i in range(0, count, max_count_per_read):
      read_count = min(max_count_per_read, count - i)  # Ensure not to exceed the remaining count
      read_values = self.PM._modbusRead(address=startAdd + i, count=read_count, mb_funcall=3, type="unit64")
      values.update({startAdd + i + j: read_values[j] for j in range(read_count)})

    self.holding_registers_values = values

  def readCoils(self):
      startAdd=4
      count=667
      values= self.PM._modbusRead(address=startAdd,count=count,mb_funcall=1,type="bool")
      self.coils_values = {startAdd + i: values[i] for i in range(count)}






  def start(self):
    while True: 
      
#      if self.PM.mb.isConnected is False:
#        continue
      try:
        self.readCoils()
        log.debug('Reading Coils %s ',json.dumps(self.coils_values))

        self.readHoldingRegisters()
        log.debug('Reading Registers %s ',json.dumps(self.holding_registers_values))

        self.listener_handler()

        self.listener_normal_source()
        self.listener_electricity()
        self.listener_generator_alarme()
        self.listener_gasoline()
        self.listener_macro()
      except:
        log.debug('Automate disconnected !!!!')
      sleep(0.2)
