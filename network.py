
# Written by Aditya Singgih

# developed using Python 3.5.1


# ipv4Address class
# subnet class
# Network class


class ipv4Address:
	'''
	ipv4Address("ip-address") -> new ipv4 object with a given address

	ip classification and private/public will be determined after creating
	the object
	'''
	
	def __init__(self, address):
		
		self.address = address;

	@property
	def address(self):
		return self._address


	@address.setter				# __init__ validation
	def address(self, a):
		maxNum = 255
		splitAddr = []

		if not a: 
			raise Exception("address cannot be empty")

		for i in a.split("."):

			if not i.isdigit():
				raise ValueError ('Please input a number')

			if int(i) > maxNum:
				raise TypeError ('Wrong IP address format. maximum digit is 255') 

			else:
				splitAddr.append(int(i))

		if len(splitAddr) < 4:
			raise ValueError('IP address must be in format x.x.x.x')
			return None

		self._address = a


		splitAddr = [int(i) for i in self.address.split(".")]


		## determining the class of the IP address, A, B, C, or D

		if splitAddr[0] >= 1 and splitAddr[0] <= 126:
			self.ipClass = 'A'

		elif splitAddr[0] >= 128 and splitAddr[0] <= 191:
			self.ipClass = 'B'

		elif splitAddr[0] >= 192 and splitAddr[0] <= 223:
			self.ipClass = 'C'

		elif splitAddr[0] >= 224 and splitAddr[0] <= 239:
			self.ipClass = 'D'

		else:
			if splitAddr[0] == 127:
				self.ipClass = 'localhost'
			else:
				self.ipClass = 'Wrong IP address'


		## determining if the IP is a public or private IP

		def validPrivate(ip, startFrom):
			validity = set()
			maxNum = 255
			for i in range(startFrom, len(ip)):
				if i <= maxNum:
					validity.add(1)
				else:
					validity.add(2)

			if len(validity) == 1:
				return True
			else:
				return False

		if splitAddr[0] == 10:
			if validPrivate(splitAddr, 1):
				self.private = 'Private'

		elif splitAddr[0] == 172 and (splitAddr[1] >= 16 and splitAddr[1] <= 31):
			if validPrivate(splitAddr, 2):
				self.private = 'Private'

		elif splitAddr[0] == 192 and (splitAddr[1] == 168):
			if validPrivate(splitAddr, 2):
				self.private = 'Private'

		else:
			if self.ipClass == 'localhost':
				self.private = 'Private'
			else:
				self.private = 'Public'


	def __repr__(self):
		return self.address

	def splitIP(self):
		return [int(i) for i in self.address.split(".")]


class Subnet:
	def __init__(self):
		self.name = None
		self.number = None

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def setNumber(self, number):
		self.number = int(number)

	def getNumber(self):
		return self.number

class Network:
	def __init__(self):
		self.name = None;
		self.networkID = None;
		self.minHost = None;
		self.maxHost = None;
		self.broadcastID = None;
		self.totalHost = None;
		self.ipClass = None;

	def setName(self, name):
		self.name = name;

	def getName(self):
		return self.name;

	def setNetworkID(self, networkID):
		self.networkID = networkID

	def getNetworkID(self):
		return self.networkID

	def setMinHost(self, minHost):
		self.minHost = minHost

	def getMinHost(self):
		return self.minHost

	def setMaxHost(self, maxHost):
		self.maxHost = maxHost

	def getMaxHost(self):
		return self.maxHost

	def setBroadcastID(self, broadcastID):
		self.broadcastID = broadcastID

	def getBroadcastID(self):
		return self.broadcastID

	def setTotalHost(self, totalHost):
		self.totalHost = int(totalHost)

	def getTotalHost(self):
		return self.totalHost

	def setIPclass(self, ipClass):
		self.ipClass = ipClass

	def getIPclass(self):
		return self.ipClass

	def display(self):
		print()
		if self.name == None:
			print('Network 1')
		else:
			print(self.getName())
		print("Network ID: \t{}".format(self.networkID.address))
		print("HostMin: \t\t{}".format(self.minHost.address))
		print("HostMax: \t\t{}".format(self.maxHost.address))
		print("Broadcast ID: \t{}".format(self.broadcastID.address))
		print("Host/net: \t\t{}".format(self.totalHost))
		print("{} internet".format(self.ipClass))
		print('---------------------------------------')










