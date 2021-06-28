from prodLine import * 

class room:
	"""docstring for room"""
	def __init__(self, number, oCount=1, tBcount=2, humidActCount =1, roomActCount =1):
		super(room, self).__init__()
		self.number = number
		self.oCount = oCount
		self.tBcount = tBcount
		self.humidActCount = humidActCount
		self.roomActCount = roomActCount

		#create the prodLine instance
		self.prodline = prodLine(number)

		#create instances of room temperatur actuator
		self.roomActList =[]
		for i in range (0,roomActCount):
			id = createInstanceID(number, 'A', ABV_DICT["roomtempActuator"], i)
			self.roomActList.append(tempAction(instanceID = id))
			print(id)

		#create instances of room temperatur actuator
		self.humidityActList =[]
		for i in range (0,humidActCount):
			id = createInstanceID(number, 'A', ABV_DICT["humidityActuator"], i)
			self.humidityActList.append(humidityAction(instanceID = id))
			print(id)


cl = room(1)
