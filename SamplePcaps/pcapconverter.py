#!/usr/bin/python
# 
# Authors:
# Richard Dean D. 
#
# CONVERTING PCAP FILES via TCPDUMP 
# Given a pcap with unique payload to determine
# packet ID in UDP protocol
# Tested on: Shaping, Policing and SPQ


import os
import copy
import subprocess
import shutil
import datetime
import time
import sys


############################################################################
#
# FUNCTION: Convert filename pcap first to TCPDUMP.txt then analyze the
# 	    Payload in Hex converted to int. with supported overflow.
#
############################################################################
os.getcwd()

# Directory Path to save the converted TSV files
# Change to your own path 
sanitizeDirectoryPath = "/home/amethyst/ns3-automation/SamplePcaps/SanitizedSPQ/"

# Directory Path to save the PCAP converted to text files via TCPDUMP.
# Change this to your own path
convertedPcaps = "/home/amethyst/ns3-automation/SamplePcaps/convertedPcaps/"

def sanitizePcap(filenamePcap):
	
	pcapFile = filenamePcap + ".pcap"	# Get the file's pcap file
	outFile = filenamePcap + ".txt"		# Get the desired output file for tcp dump
	sanitizeFile = "s" + filenamePcap + ".txt"	# Name of the output file being sanitized. (END RESULT)

	# Commandline argument for converting pcap to tcpdump readable text
	# file. Open the text file for read and also for our sanitize file.
	os.system("tcpdump -nnXS -r "+ str(pcapFile) +" > " + convertedPcaps + "/"+ str(outFile))
	os.system("tcpdump -r "+ str(pcapFile) +" > " + convertedPcaps + "/"+ str("deb_" + outFile))
	os.chdir(convertedPcaps)
	pcapTextFile = open(outFile, "r")
	os.chdir(sanitizeDirectoryPath)
	sanitizeWrite = open(sanitizeFile, "w")
	# ---------------------------------------------------------------
	previousPacketID = 1 #Storing previous packets for keeping count
	numPackets = 0	# Total packets being sent.
	PID = 0		# Packet IDs converted in int(hex)
	overflow = 0	# Overflows when hex reaches 0xffff
	totalPackets = 0 
	# Start Reading file (LOOP)
	while(True): 
		packetPayload = pcapTextFile.readline()
		if(not packetPayload): #If we reach the end of the file <3 we stop!
			break
		# Now extract the data in each line...
		payloadData = packetPayload.split("\n")
		payLoads = str(payloadData[0])
		payloadDataPointer = payLoads.split(" ")
		

		# If we hit the "IP" in the List returned, we assume index[1] is the value for
		# Time stamp for each packets.
		if(str(payloadDataPointer[1]) == "IP"):
			packetTimeStamp = str(payloadDataPointer[0])
			timeStampInSeconds = packetTimeStamp.split(':')
			# Converting the time stamp in milliseconds.
			timeStampInMilliseconds = float(timeStampInSeconds[2]) * 1000
			
		# Location of the packet's ID in the payload by extracting the index position
		# from the returned List by the payLoads list
		if(str(payloadDataPointer[0]) == "\t0x0010:"):
			# convert the HEX to an integer.
			PID = int("0x" + payloadDataPointer[8], 16)
			totalPackets+=1
			#print "PID: %s" % (str(PID))
			#print "Packet Detected: %s" % (totalPackets)
			# Check if we currently have overflow means we exceed 0xffff
			if(previousPacketID > PID):
				overflow = previousPacketID
			
			PID = PID + overflow	# Add the overflow value to the next PID
			
			# Calculates the packets being skipped. (-1) for timestamp.
			packetLoss = (PID-overflow) - numPackets #(previousPacketID-overflow)
			print "Packet STATUS: DONE || arrival:" + str(timeStampInMilliseconds) + "s || Packet ID: %s --> %s " % (payloadDataPointer[8], str(PID))
			if packetLoss > 1:
				for i in range(1, packetLoss):
					#print "Lost Packet ID: %s" % (str(i))
					numPackets = numPackets + 1
					print "Packet STATUS: DROP || arrival: -1 || Packet ID: %s " % (str(i + overflow))
					sanitizeWrite.write(str(numPackets) + "\t" + "-1\n")
				previousPacketID = PID
			previousPacketID = PID
			sanitizeWrite.write(str(numPackets +1) + "\t" + str(timeStampInMilliseconds) + "\n")
			numPackets = numPackets + 1
		
	print "packets detected %s " % (numPackets)
	pcapTextFile.close()	#Close the files
	sanitizeWrite.close()
	#print "Packets Counted in PCAP: %s" % (totalPackets)
 
#End While

# END OF HELPER FUNCTIONS

#--------- MAIN ------------
def main():
	#pcapFile = raw_input("Input Pcaps to sanitize: ")
	
	# This variables holds the starting number of pcap files 
	# onto the last number. (e.g 1567.pcap to 1780.pcap) 
	# enter only the number and exclude the extension file.
	startPcap = raw_input("PCAP STARTING NUMBER: ")
	endPcap = raw_input("PCAP ENDING NUMBER: ")
	
	# Directory Path of the PCAP Data files. (Change this)
	# Change this to the Path of your PCAP Files directory.
	# OR Comment this line if your pcap files is in the current dir
	dataDirectory = "/media/amethyst/CCinc/RESEARCHWORK/TestResults/SPQ"
	
	for i in range(int(startPcap),int(endPcap)+1):
		# Comment this line if you commented out the previous line.
		os.chdir(dataDirectory)
		pcapFile = str(i)
		print "Reading Data: %s" % (pcapFile)
		sanitizePcap(pcapFile)	
main()

	
