#!/usr/bin/python
# 
# Richard Dean D.
# Sample Python Program
# 
# For automating ns-3 ./waf with different parameters.
# With a small configuration to the previous python program
# in the github repository by Armen Arslanian

# For automating NS-3 Commands for different parameters.
import os
import subprocess
import shutil

# This is each interval to compute in your output data
n = input('Interval n: ')
n = int(n)
numAptPriorityProbes = 0

print "This is your number %i" % (n)
directoryPath = "/home/chad/ns-allinone-3.14.1/ns-3.14.1"

print "This is your interval %i" % (n)

# Opens File to extract our waf commands from
AutoWaf = open("waf-commands.txt", "r")
commandLists = [] #Create an array to store our waf commands 
os.getcwd()
print("Currently Reading Waf Commands in the textfile")

# Start While
while(True): # For iterating the commands from the text file
	aCommand = AutoWaf.readline()
	if(not aCommand): #If we reach the end of the file <3
		break
	# Now extract the waf commands from the file with \n as breakpoints
	wafCommand = aCommand.split("\n")
	commandLists.append(wafCommand[0])

	# Printing command extracted
	print "Command: %s" % (wafCommand[0])
	
	# Execute command
	print "Executing command --->"
	print "..Changing Directory to NS-3.14.1 folder"
	
	# Changing the Processing Directory to NS-3.14.1 for the ./waf
	os.chdir(directoryPath)
	subprocess.call(["ls"])
	print "..Executing command waf in NS-3.14.1"
	os.system(wafCommand[0])
	print "Successfully executed commmand..."
	print "Preparing for analyzing data for R"
#End While

# HELPER FUNCTIONS
def output_packet_loss_rate(outputfilename,maxPackets,dropRate):
	print "Calculating values for %s ..." % (outputfilename)
	
	loop_length = maxPackets
	print "Total packets values passed: %s" % (str(maxPackets))
	print "Total packet lose values passed: %s" % (str(dropRate))
	j = 0
	R4 = open(outputfilename, "w")
	for x in range(0, loop_length):
		lossRates = float((float(dropRate)/ float(maxPackets)) * 100)
		lossRates = round(lossRates, 2)
		print "packet loss rate: %s\n" % (lossRates)
		R4.write(str(j)+"\t" + str(lossRates) + "\n")
		j = j + (n+1)
	print "Generated %s" % (fileR4)
	R4.close()

def calculate_packet_loss(apt_filename):
	packetLossRate = 0
	packetReader = open(apt_filename, "r")
	while(True): # start while --> 2
		line = packetReader.readline()
		line_parts = line.split("\t")
		if(not line):
			break
		if(line_parts[1] == '-1\n'):
			packetLossRate+=1
	print "total packet loss: %s" % (str(packetLossRate))
	return packetLossRate

def get_max_packets(filename):
	numAptPriorityProbes1 = 0
	packetReader = open(filename, "r")
	while(True): # start while --> 2
		line = packetReader.readline()
		line_parts = line.split("\t")
		if(not line):
			break
		numAptPriorityProbes1+=1
	return numAptPriorityProbes1

def get_post_drop_rate(filename):
	packetReader = open(filename, "r")
	packetsDrop = 0
	afterFirstPacketDrop = 0
	isPacketDrop = False
	while(True):
		p = packetReader.readline()
		p_packets = p.split("\t")
		if not p:
			break
		if isPacketDrop == False:
			if p_packets[1] == '-1\n':
				isPacketDrop = True
		else:
			afterFirstPacketDrop+=1
			if p_packets[1] == '-1\n':
				packetsDrop+=1
	
	lossRate = float(( float(packetsDrop)/float(afterFirstPacketDrop) ) * 100)
	return ("%.1f" % round((lossRate),1)) 

def create_packetloss_difference_rate(file_H, file_L):
	data_H = open(file_H, "r")
	data_L = open(file_L, "r")
	data_H_L = open("spq_last_link_bw_effect.dat", "w")
	difference_value = []
	while(True):
		line_H = data_H.readline()
		line_L = data_L.readline()
		packet_H = line_H.split("\t")
		packet_L = line_L.split("\t")
		if not line_H or not line_L:
			break
		difference_value.append(round(float(packet_L[1]) - float(packet_H[1]),2))

	loop_max = int(len(difference_value))
	i = 0
	for x in range(0, loop_max):
		data_H_L.write(str(i+n) + "\t" + str(difference_value[x]) + "\n")
		i = i + (n+1)
	data_H_L.close()
	data_H.close()
	data_L.close()
	
		
# END OF HELPER FUNCTIONS

print "Changing working directory back to OUTPUT_FILE Folder"
os.chdir(directoryPath + "/OUTPUT_FILES")
print "Files listed: "
subprocess.call(['ls'])

print "Analyzing the output files for graphing"
outputFilenames = open("files-to-graph.txt", "r")
extensionNameH = ".dat-H"
extensionNameL = ".dat-L"

# Iteration for code snippet from Armen Arslanian
# Code has been modified for automation and cleanliness of each
# waf command generated output files.
while(True): # Start While ---> 1
	aFilename = outputFilenames.readline()
	if(not aFilename):
		break
	filename = aFilename.split("\n")
	fileH = filename[0] + extensionNameH
	fileL = filename[0] + extensionNameL
	fileR3 = filename[0] + "R3.txt"
	fileR4 = filename[0] + "R4.txt"
	R1 = open(fileH, "r")
	R2 = open(fileL, "r")
	packetLossRate_H = calculate_packet_loss(fileH)
	print "packetLossRate_H: %s " % (packetLossRate_H)
	packetLossRate_L = calculate_packet_loss(fileL)
	print "packetLossRate_H: %s " % (packetLossRate_L)
	print "Creating Directory for the output files ..."

	numAptPriorityProbes = get_max_packets(fileH)
	output_packet_loss_rate(fileR3,numAptPriorityProbes, packetLossRate_H)
	numAptPriorityProbes = get_max_packets(fileL)
	output_packet_loss_rate(fileR4,numAptPriorityProbes, packetLossRate_L)
	create_packetloss_difference_rate(fileR3,fileR4)

	if not os.path.exists(filename[0]):
		os.makedirs(filename[0])
	os.chdir(directoryPath + "/OUTPUT_FILES/" + filename[0])
	
	print "Closing files"
	R1.close()
	R2.close()

	os.chdir(directoryPath + "/OUTPUT_FILES")
	print "Moving created files to its designated folder ..."
	shutil.move(fileH, filename[0])
	shutil.move(fileL, filename[0])
	shutil.move(fileR3, filename[0])
	shutil.move(fileR4, filename[0])
	shutil.move("spq_last_link_bw_effect.dat", filename[0])	
	print "Finished Creating required files"
	print "Finished automation."
# end while --> 1
AutoWaf.close()

	
