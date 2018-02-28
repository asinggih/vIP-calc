
# Written by Aditya Singgih

# developed using Python 3.5.1

# plenty of functions:
# - netmaskClass
# - countTotal
# - powerOfTwo
# - bitAddressing
# - glueIP
# - networkBundle
# - isEnough
# - targetToNetmask
# - ipIncrement
# - processDivision



import sys
import copy

import network
from MyPriorityQueue import MyPriorityQueue

def netmaskClass(netmask):
	if netmask >= 24 and netmask <= 32:
		return 'C'
	elif netmask >= 16 and netmask <= 23:
		return 'B'
	elif netmask >= 8 and netmask <= 15:
		return 'A'
	else:
		raise ValueError('8 <= netmask <= 32')

def countTotal(netmask):

	info = []					# [number of networks, available IP, available hosts]

	temp = divmod(netmask, 8)

	workBit = temp[1]			# x.x.x.y where y is the workbit

	numberOfNetworks = 0
	availableIP = 0
	availableHosts = 0

	if netmaskClass(netmask) == 'C':
		numberOfNetworks = 2**workBit
		availableIP = 2**(8-workBit)

	elif netmaskClass(netmask) == 'B':
		numberOfNetworks = 2**(workBit)
		availableIP = 2**(8+(8-workBit))

	elif netmaskClass(netmask) == 'A':
		numberOfNetworks = 2**(workBit)
		availableIP = 2**(16+(8-workBit))

	info.append(numberOfNetworks)
	info.append(availableIP)
	info.append(availableIP-2)

	return info

def powerOfTwo(target):
	x = 2
	change = 0
	power = 0
	for i in range(target+1):
		number = x ** change
		change = i
		if number >= target:  
			power = number    
			return change-1

def bitAddressing(netmask, mainIP):

	def group(shift):
		final = []
		bitCount = [128, 64, 32, 16, 8, 4, 2, 1]
		index = []
		total = 0
		for i in range(len(bitCount)):
			if bitCount[i] <= splitAddr[-shift]:
				if total + bitCount[i] <= splitAddr[-shift]:
					index.append(i)
					total += bitCount[i]

		return index 

	def prettyOut(shift, mainIP, finalNetID, finalBID):

		finalOut = []

		networkIP = mainIP.splitIP()
		networkIP = networkIP[:-1*shift]
		# networkIP.append(sum(finalNetID))

		broadcastIP = mainIP.splitIP()
		broadcastIP = broadcastIP[:-1*shift]

		if shift == 1:
			networkIP.append((sum(finalNetID)))
			broadcastIP.append((sum(finalBID)))
			finalOut.extend((networkIP, broadcastIP))

		elif shift == 2:
			networkIP.extend((sum(finalNetID), 0))
			broadcastIP.extend((sum(finalBID), 255))
			finalOut.extend((networkIP, broadcastIP))

		else:
			networkIP.extend((sum(finalNetID),0,0))
			broadcastIP.extend((sum(finalBID),255,255))
			finalOut.extend((networkIP, broadcastIP))

		return finalOut

	bitCount = [128, 64, 32, 16, 8, 4, 2, 1]
	splitAddr = [int(i) for i in mainIP.splitIP()]
	base = [0 for x in range(8)]

	index = None
	if netmaskClass(netmask) == 'C':
		index = group(1)
	elif netmaskClass(netmask) == 'B':
		index = group(2)
	elif netmaskClass(netmask) == 'A':
		index = group(3)

	netID = copy.copy(base)
	bID = copy.copy(base)

	x = divmod(netmask, 8)

	dividerIndex = x[1]						     # separating network bit and host bit

	for i in index:								 # filling up netID
		if dividerIndex > i:
			netID[i], bID[i] = 1, 1 

	for i in range(dividerIndex, len(bID)):		 # filling up bID
		bID[i] = 1

	finalNetID = copy.copy(netID)
	finalBID = copy.copy(bID)

	for i in range(len(bitCount)-1):
		if finalNetID[i] == 1:
			finalNetID[i] = bitCount[i]
		if finalBID[i] == 1:
			finalBID[i] = bitCount[i]

	final = None
	if netmaskClass(netmask) == 'C':
		final = prettyOut(1, mainIP, finalNetID, finalBID)
	elif netmaskClass(netmask) == 'B':
		final = prettyOut(2, mainIP, finalNetID, finalBID)
	elif netmaskClass(netmask) == 'A':
		final = prettyOut(3, mainIP, finalNetID, finalBID)

	return final


def glueIP(ip):
	x = '.'.join(str(x) for x in ip)
	return x


def networkBundle(netmask, mainIP):

	n = network.Network()
	
	# --------------------------------------------------------
	#					setting up network ID
	# --------------------------------------------------------
	netBroad = bitAddressing(netmask, mainIP)
	netID = netBroad[0]
	ip = network.ipv4Address(glueIP(netID))
	n.setNetworkID(ip)


	# --------------------------------------------------------
	#				  setting up broadcast ID
	# --------------------------------------------------------
	bID = netBroad[1]
	ip = network.ipv4Address(glueIP(bID))
	n.setBroadcastID(ip)

	# --------------------------------------------------------
	#				   setting up minimum host
	# --------------------------------------------------------
	hostMinimum = copy.copy(netID)
	temp = netID[-1]+1
	hostMinimum.pop()
	hostMinimum.append(temp)
	ip = network.ipv4Address(glueIP(hostMinimum))
	n.setMinHost(ip)

	# --------------------------------------------------------
	#				   setting up maximum host
	# --------------------------------------------------------
	hostMaximum = copy.copy(bID)
	temp = bID[-1]-1
	hostMaximum.pop()
	hostMaximum.append(temp)
	ip = network.ipv4Address(glueIP(hostMaximum))
	n.setMaxHost(ip)

	# --------------------------------------------------------
	#				   setting up total host
	# --------------------------------------------------------
	n.setTotalHost(countTotal(netmask)[2])

	# --------------------------------------------------------
	#				 check public or private IP
	# --------------------------------------------------------
	a = n.getNetworkID().private
	b = n.getBroadcastID().private

	if a == 'Private' and b == 'Private':
		n.setIPclass('Private')
	else:
		n.setIPclass('Public')
	
	return n

def isEnough(netmask, totalIPneeded):
	
	maximumAvailable = countTotal(netmask)[1]
	totalIPneeded = sum(totalIPneeded)

	if totalIPneeded <= maximumAvailable:
		return True

	else:
		return False

def targetToNetmask(x):

	temp = powerOfTwo(x)
	netmask = 32-temp

	return netmask

def ipIncrement(subnet, ip):

	nm = targetToNetmask(subnet.getNumber())

	netName = subnet.getName()

	n = networkBundle(nm, ip)
	n.setName(netName)

	return n


def processDivision(ip, netmask, numOfNetworks):

	netCollect = []

	myPQ = MyPriorityQueue()
	minPowOfTwo = []
	for i in range(numOfNetworks):
		userinput = input('{}. = '.format(i)).split()
		sub = network.Subnet()

		sub.setName(userinput[0])
		sub.setNumber(int(userinput[1]))

		minPowOfTwo.append(2**powerOfTwo(sub.getNumber()))	# need to sum the list to check if we hv enough IP

		myPQ.insert(-1*(sub.getNumber()), sub)				# so that it prioritise the largest number of network first

	if isEnough(netmask, minPowOfTwo) == False:
		return 

	else:

		a = 0
		while myPQ.empty() == False:

			x = myPQ.remove()								# subnet, consists of name and number of hosts

			if a == 0:
															# first iteration only
				try:

					netCollect.append(ipIncrement(x, ip))

					a += 1
				except:

					print("required IP address should be greater or equal than 2")
					sys.exit()


			else:
				tempIP = None

				tempIP = netCollect[-1].getBroadcastID()

				split = tempIP.splitIP()

				maxNum = 255

				last = int(split[-1])
				if last + 1 + x.getNumber() <= maxNum:
					split[-1] = split[-1] + 1
					nextIP = network.ipv4Address(glueIP(split))
					netCollect.append(ipIncrement(x, nextIP))

				else:
					split[-2], split[-1] = (split[-2] + 1), 0
					nextIP = network.ipv4Address(glueIP(split))
					netCollect.append(ipIncrement(x, nextIP))

	return netCollect






