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
def sanitizePcap(filenamePcap):
	
	pcapFile = filenamePcap + ".pcap"	# Get the file's pcap file
	outFile = filenamePcap + ".txt"		# Get the desired output file for tcp dump
	sanitizeFile = "s" + filenamePcap + ".csv"	# Name of the output file being sanitized. (END RESULT)

	# Commandline argument for converting pcap to tcpdump readable text
	# file. Open the text file for read and also for our sanitize file.
	os.system("tcpdump -nnXS -r "+ str(pcapFile) +" > " + str(outFile))
	pcapTextFile = open(outFile, "r")
	sanitizeWrite = open(sanitizeFile, "w")
	# ---------------------------------------------------------------
	previousPacketID = 1 #Storing previous packets for keeping count
	numPackets = 0;	# Total packets being sent.
	PID = 0;	# Packet IDs converted in int(hex)
	overflow = 0	# Overflows when hex reaches 0xffff

	currentSrcPort = " ";
	currentDestPort = " ";

	sanitizeWrite.write("PType," + "PID" + "," + "Timestamp" + "," + "FrameNumber" + "\n") 
	# Start Reading file (LOOP)
	while(True):
		
		packetPayload = pcapTextFile.readline()
		if(not packetPayload): #If we reach the end of the file <3 we stop!
			break
		# Now extract the data in each line...
		payloadData = packetPayload.split("\n")
		payLoads = str(payloadData[0])
		payloadDataPointer = payLoads.split(" ")

		# If we hit the "IP" in the List returned, we assume index[0] is the value for
		# Time stamp for each packets. [2] = Source Address [4] = destination Address
		
		if(str(payloadDataPointer[1]) == "IP"):
			#Extract the addresses on a given index
			sourceAddress = str(payloadDataPointer[2])
			destinationAddress = str(payloadDataPointer[4])

			#extract the ports from the IP Addresses from [2] and [4]
			sourcePortHandler = sourceAddress.split(".")
			destinationPortHandler = destinationAddress.split(".")
			currentSrcPort = sourcePortHandler[4]
			#2222 - High, 4444 - low,
			currentDestPort = destinationPortHandler[4]
			
			packetTimeStamp = str(payloadDataPointer[0])
			timeStampInSeconds = packetTimeStamp.split(':')
			# Converting the time stamp in milliseconds.
			timeStampInMilliseconds = float(timeStampInSeconds[2]) * 1000
			
			
		# Location of the packet's ID in the payload by extracting the index position
		# from the returned List by the payLoads list
		if(str(payloadDataPointer[0]) == "\t0x0010:"):
			# convert the HEX to an integer.
			PID = int("0x" + payloadDataPointer[8], 16)
			numPackets = numPackets + 1
			# Check if we currently have overflow means we exceed 0xffff
			if(previousPacketID > PID):
				overflow = previousPacketID
			
			#PID = PID + overflow	# Add the overflow value to the next PID
			
			# Calculates the packets being skipped. (-1) for timestamp.
			#packetLoss = (PID-overflow) - (previousPacketID-overflow)
			#print "Packet STATUS: DONE || arrival:" + str(timeStampInMilliseconds) + "s || Packet ID: %s --> %s " % (payloadDataPointer[8], str(PID))
			#if packetLoss > 1:
			#	for i in range(previousPacketID+1, PID):
					#print "Lost Packet ID: %s" % (str(i))
					#numPackets = numPackets + 1
					#print "Packet STATUS: DROP || arrival: -1 || Packet ID: %s " % (str(i + overflow))
					#sanitizeWrite.write(str(i + overflow) + "\t" + "-1\n")
				#previousPacketID = PID
			#previousPacketID = PID
			print("Packet Detected: " + "ID: " + str(PID)+ " || " + currentSrcPort + " > " + currentDestPort + " @Frame || " + str(numPackets))
			if currentDestPort == "22222:" and currentSrcPort == "20000":
				sanitizeWrite.write("H," + str(PID) + "," + str(timeStampInMilliseconds) + "," + str(numPackets) + "\n")
			elif currentDestPort == "44444:" and currentSrcPort == "20000":
				sanitizeWrite.write("L," + str(PID) + "," + str(timeStampInMilliseconds) + "," + str(numPackets) + "\n")
			elif currentSrcPort != "20000" and currentDestPort == "44444:":
				sanitizeWrite.write("L," + str(PID) + "," + str(timeStampInMilliseconds) + "," + str(numPackets) + "\n")
			elif currentSrcPort != "20000" and currentDestPort == "22222:":
				sanitizeWrite.write("H," + str(PID) + "," + str(timeStampInMilliseconds) + "," + str(numPackets) + "\n")
			
		
	#print "packets detected %s " % (numPackets)
	pcapTextFile.close()	#Close the files
	sanitizeWrite.close()
 
#End While

# END OF HELPER FUNCTIONS

#--------- MAIN ------------
def main():
	pcapFile = raw_input("Input Pcaps to sanitize: ")
	print "Data: %s" % (pcapFile)
	sanitizePcap(pcapFile)	
main()

	
