#!/usr/bin/python
# 
# Authors:
# Richard Dean D. & Omri Gabay
# 
# For automating ns-3 ./waf with different parameters.
# With a small configuration to the previous python program
# in the github repository by David Mayer

# For automating NS-3 Commands for different parameters.
import os
import copy
import subprocess
import shutil
import time
import sys

# This is each interval to compute in your output data
n = input('Interval n: ')
n = int(n)

print "This is your number %i" % (n)
directoryPath = "/home/chad/ns-allinone-3.14.1/ns-3.14.1/"

print "This is your interval %i" % (n)

ns3_arguments = {}
#./waf --run "compression-sim --outputFile=./OUTPUT_FILES/compression.dat --entropy=h --numPackets=10000 --packetSize=1070 --interPacketTime=.00000001 --s0p0Delay=30ms --p0p1Delay=30ms --p1r0Delay=30ms --s0p0DataRate=5Mbps --p0p1DataRate=4Mbps --p1r0DataRate=5Mbps --s0QueueSize=600000 --p0QueueSize=75 --p1QueueSize=75 --compression=1 --queueMode=p"
# Set the Default Values for NS3 Experiment Parameters
ns3_arguments['numPackets'] ='10000'
ns3_arguments['interPacketTime'] ='0.00000001'
ns3_arguments['s0QueueSize']='600000'
ns3_arguments['p0QueueSize']='75'
ns3_arguments['p1QueueSize']='75'
# following are represented in Mbps
ns3_arguments['s0p0DataRate']='5Mbps'
ns3_arguments['p0p1DataRate']='1Mbps'
ns3_arguments['p1r0DataRate']='5Mbps'
# end
# following are represented in ms
ns3_arguments['s0p0Delay']='30ms'
ns3_arguments['p0p1Delay']='30ms'
ns3_arguments['p1r0Delay']='30ms'
# end
ns3_arguments['packetSize']='1070'

# new additional arguments
ns3_arguments['compression'] = '1'
ns3_arguments['queueMode'] = 'p'
ns3_arguments['entropy'] = 'h'

cmd_command = './waf --run "'
cmd_command += 'compression-sim'
cmd_command += ' --interPacketTime='+ns3_arguments['interPacketTime']
cmd_command += ' --s0QueueSize='+ns3_arguments['s0QueueSize']
cmd_command += ' --p0QueueSize='+ns3_arguments['p0QueueSize']
cmd_command += ' --p1QueueSize='+ns3_arguments['p1QueueSize']
cmd_command += ' --numPackets='+ns3_arguments['numPackets']
cmd_command += ' --s0p0DataRate='+ns3_arguments['s0p0DataRate'] # X
#cmd_command += ' --p0p1DataRate='+ns3_arguments['p0p1DataRate'] # Y
cmd_command += ' --p1r0DataRate='+ns3_arguments['p1r0DataRate'] # Z
cmd_command += ' --s0p0Delay='+ns3_arguments['s0p0Delay']
cmd_command += ' --p0p1Delay='+ns3_arguments['p0p1Delay']
cmd_command += ' --p1r0Delay='+ns3_arguments['p1r0Delay']
#cmd_command += ' --packetSize='+ns3_arguments['packetSize'] #Experiment PacketSize increases
cmd_command += ' --queueMode='+ns3_arguments['queueMode']
cmd_command += ' --compression='+ns3_arguments['compression']
#cmd_command += ' --entropy='+ns3_arguments['entropy'] # interchanging 'h' -> 'l'

cmd_command2 = copy.deepcopy(cmd_command) 

#--------- SPQ Automation Waf parameters -------------------
separationExperiment = [] # list of changing parameter values
waf_commands = []	  # list of collected waf commands
all_waf = []		  # String of waf commands combinations in a list  
all_outputFileNames = ""  # all outfile foldernames holder for files-to-graph.txt
experiments = 10 #number of expected results

# ------------ COMPRESSION Automation Waf parameters -------
YDataRateValue = ["1Mbps","5Mbps"] # Y data rate according to the Parameters above
packetSizes = []

y=0	# keeps count on waf_commands current/overall indexes
currentPacketSize = 50
while(True):
	# Low Entropy
	if currentPacketSize > 1500:
		break;
	packetSizes.append(currentPacketSize)
	print "%s" % (str(currentPacketSize))
	currentPacketSize += 50

for i in range(2):
	currentPacketSize = 50
	while(True):
		# Low Entropy
		if currentPacketSize > 1500:
			break;
		waf_commands.append(copy.deepcopy(cmd_command))
		ns3_arguments['packetSize'] = str(currentPacketSize)
		ns3_arguments['entropy'] = 'l'
		ns3_arguments['p0p1DataRate']= str(YDataRateValue[i])
		ns3_arguments['outputFile']="./OUTPUT_FILES/P_C"+ "_"+ str(YDataRateValue[i]) + "_" + str(currentPacketSize) + ".dat-L"
		waf_commands[y] += ' --outputFile='+ns3_arguments['outputFile']
		waf_commands[y] += ' --entropy='+ns3_arguments['entropy']
		waf_commands[y] += ' --p0p1DataRate='+ns3_arguments['p0p1DataRate']
		waf_commands[y] += ' --packetSize='+ns3_arguments['packetSize']
		waf_commands[y] += '"'
		all_outputFileNames += "P_C"+ "_"+ str(YDataRateValue[i]) + "_" + str(currentPacketSize) + "\n"
		all_waf += waf_commands[y] + '\n'
		currentPacketSize += 50
		y+=1

currentPacketSize = 50
for i in range(2):
	currentPacketSize = 50
	while(True):
		# Low Entropy
		if currentPacketSize > 1500:
			break;
		waf_commands.append(copy.deepcopy(cmd_command))
		ns3_arguments['packetSize'] = str(currentPacketSize)
		ns3_arguments['entropy'] = 'h'
		ns3_arguments['p0p1DataRate']= str(YDataRateValue[i])
		ns3_arguments['outputFile']="./OUTPUT_FILES/P_C"+ "_"+ str(YDataRateValue[i]) + "_" + str(currentPacketSize) + ".dat-H"
		waf_commands[y] += ' --outputFile='+ns3_arguments['outputFile']
		waf_commands[y] += ' --entropy='+ns3_arguments['entropy']
		waf_commands[y] += ' --p0p1DataRate='+ns3_arguments['p0p1DataRate']
		waf_commands[y] += ' --packetSize='+ns3_arguments['packetSize']
		waf_commands[y] += '"'
		# No need to put the names P_H since we're opening both dat-H and dat-L using a single filename.
		#all_outputFileNames += "P_H"+ "_"+ str(YDataRateValue[i]) + "_" + str(currentPacketSize) + "\n"
		all_waf += waf_commands[y] + '\n'
		currentPacketSize += 50
		y+=1
#----------------------------

# print cmd_command
# print cmd_command2

# Opens File to input our waf commands to
AutoWaf = open("waf-commands-compression-2.txt", "w")
filesToGraph = open("files-to-graph-compression-2.txt", "w")
print("Currently Writing Waf Commands in the textfile")
AutoWaf.writelines(all_waf)
filesToGraph.writelines(all_outputFileNames)
AutoWaf.close()
filesToGraph.close()

# Opens File to extract our waf commands from
AutoWaf = open("waf-commands-compression-2.txt", "r")
commandLists = [] # Create an array to store our waf commands 
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
	print commandLists

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
		#print "packet loss rate: %s\n" % (lossRates)
		R4.write(str(j)+"\t" + str(lossRates) + "\n")
		j = j + (n+1)
	print "Generated %s" % (fileR4)
	R4.close()

def calculate_loss_rate(maxPackets,dropRate):
	lossRates = 0
	loop_length = maxPackets
	print "Total packets values passed: %s" % (str(maxPackets))
	print "Total packet lose values passed: %s" % (str(dropRate))

	lossRates = float((float(dropRate)/ float(maxPackets)) * 100)
	lossRates = round(lossRates, 2)
	print "packet loss rate: %s\n" % (lossRates)
	return lossRates

def calculate_packet_loss(apt_filename,priority):
	packetLossRate = 0
	packetReader = open(apt_filename, "r")
	while(True): # start while --> 2
		line = packetReader.readline()
		line_parts = line.split("\t")
		if(not line):
			break
		if(line_parts[1] == '-1\n' and priority=="L"):
			packetLossRate+=1
		if(int(line_parts[0])>=1000 and priority=="H" and line_parts[1] == '-1\n'):
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
	if packetsDrop > 1:
		lossRate = float(( float(packetsDrop)/float(afterFirstPacketDrop) ) * 100)
		return ("%.1f" % round((lossRate),1))
		print "total packet loss: %s" % (str(lossRate)) 
	else:
		#print "total packet loss: %s" % (str(lossRate))
		return 0

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
		# This line is responsible for outputting the X (packet number) and the 
		# Y (difference between packet from H and packet from L)
		data_H_L.write(str(i+n) + "\t" + str(difference_value[x]) + "\n")
		i = i + (n+1)
	data_H_L.close()
	data_H.close()
	data_L.close()

def create_r_graph(lossp_H, lossp_L, separationParameter):
	data_H = open(lossp_H, "r")
	data_L = open(lossp_L, "r")
	data_H_L = open("compressionExperiment-2.csv", "w")
	data_Delta = open("compressionExperiment-diff-2.csv", "w")
	difference_value = []
	data_Delta.write("packetSizes,1Mbps,5Mbps" + "\n")
	#data_H_L.write("numPackets,Speed,LossRates" + "\n")
	packetLossForH = []
	packetLossForL = []
	DataRateValue = []
	packetSize = []
	z = 0
	aMbpsRow = 30
	while(True):
		line_H = data_H.readline()
		line_L = data_L.readline()
		packet_H = line_H.split("\t")
		packet_L = line_L.split("\t")
		if not line_H or not line_L:
			break
		difference_value.append(round(float(packet_H[2]) - float(packet_L[2]),2))
		packetLossForH.append(float(packet_H[2]))
		packetLossForL.append(float(packet_L[2]))
		packetSize.append(float(packet_H[0]))
		DataRateValue.append(packet_H[1])
	loop_max = int(len(difference_value))
	for x in range(0, 30):
		data_Delta.write(str(packetSize[x]) + "," + str(difference_value[x]) + "," + str(difference_value[x+aMbpsRow]) + "\n")
		z+=1
	data_H_L.close()
	data_H.close()
	data_L.close()
	data_Delta.close()
		
# END OF HELPER FUNCTIONS

#--------- MAIN ------------
print "Changing working directory back to OUTPUT_FILE Folder"
os.chdir(directoryPath + "/OUTPUT_FILES")
print "Files listed: "
subprocess.call(['ls'])

print "Analyzing the output files for graphing"
outputFilenames = open("files-to-graph-compression-2.txt", "r")
extensionNameH = ".dat-H"
extensionNameL = ".dat-L"
LossRateH_data = ""
LossRateL_data = ""
currentLength = 0

gFile = open("packetloss-2.csv", "w")
currentDataRateValue = 0
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
	packetLossRate_H = get_post_drop_rate(fileH)
	print "packetLossRate_H: %s " % (packetLossRate_H)
	packetLossRate_L = get_post_drop_rate(fileL)
	print "packetLossRate_L: %s " % (packetLossRate_L)
	print "Creating Directory for the output files ..."
	

	
	#output_packet_loss_rate(fileR3,numAptPriorityProbes, packetLossRate_H)
	#if currentLength >= 16: # get all dat-H data according to file-to-graphs.txt
	LossRateH_data += str(packetSizes[currentDataRateValue]) + "\t" + YDataRateValue[currentLength] + "\t" +  str(packetLossRate_H) + "\n"
	
	#if currentLength < 16:	# get all dat-L data according to file-to-graphs.txt
	LossRateL_data +=  str(packetSizes[currentDataRateValue]) + "\t" + YDataRateValue[currentLength] + "\t" +  str(packetLossRate_L) + "\n"

	
	currentDataRateValue+=1
	if currentDataRateValue >= 30:
		currentLength+=1
		currentDataRateValue=0
	if currentLength > 2:
		currentLength =0 
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
	print "Finished Creating required files"
	print "Finished automation."
# end while --> 1
os.chdir(directoryPath + "/OUTPUT_FILES")
LossRateH = open("LossRate_H-compression", "w") # All H priority loss packets stored
LossRateL = open("LossRate_L-compression", "w") # ALL L priority loss packets stored
LossRateH.writelines(LossRateH_data)
LossRateL.writelines(LossRateL_data)
LossRateH.close()
LossRateL.close()
AutoWaf.close()
create_r_graph("LossRate_H-compression","LossRate_L-compression",packetSizes)
	
