#!/usr/bin/env python3


import sys
import subnetting
import network

if __name__ == '__main__':

	mainIP = network.ipv4Address(input('Please input the IP address: '))	

	netmask = int(input('Please input the subnet mask (e.g., 24): '))

	if netmask > 32 or netmask < 8:
		raise ValueError('8 <= netmask <= 32')

	split = input('Will you divide the IP into smaller subnets? (y/n): ')
	split = split.lower()
	if split in ['n', 'no']:						# don't want to divide it further
		out = subnetting.networkBundle(netmask, mainIP)
		out.display()
		
	else:											# want to divide it into smaller subnets

		try:
			numOfNetworks = int(input('Please input the number of subnets: '))

		except ValueError:
			print('Please input integers')
			print('restart the program')
		
		print()
		print('Please input the subnet name and IP address required, separated by space')
		print('This includes netID and Broadcast')
		print()

		if numOfNetworks == 1:

			out = subnetting.networkBundle(netmask, mainIP)
			out.display()

		else:

			try:
				netList = subnetting.processDivision(mainIP, netmask, numOfNetworks)

				for network in netList:
					network.display()

			except TypeError:
				print('Not enough IP address with the given netmask')








				
