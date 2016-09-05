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
directoryPath = "/home/chad/ns-allinone-3.14.1/ns-3.14.1"

print "This is your interval %i" % (n)

ns3_arguments = {}
#--ReceiveQueueSizeR2=75 --TXQueueSizeR2=100 --TXQueueSizeS=4000000 --TXQueueSizeR1=4000000 --SR1Delay=5ms --R1R2Delay=5ms --R2RDelay=5ms --SR1DataRate=50Mbps --R1R2DataRate=100Mbps --R2RDataRate=10Mbps --outputFile=./OUTPUT_FILES/P_H_H.dat --packetSize=100 --interPacketTime=0.00000001 --initialPacketTrainLength=1000 --separationPacketTrainLength=2 --numAptPriorityProbes=1000 --aptPriority='H'"
# Set the Default Values for NS3 Experiment Parameters
ns3_arguments['ReceiveQueueSizeR2'] ='75'
ns3_arguments['interPacketTime'] ='0.00000001'
ns3_arguments['TXQueueSizeR1']='4000000'
ns3_arguments['TXQueueSizeR2']='100'
ns3_arguments['TXQueueSizeS']='4000000'
# following are represented in Mbps
ns3_arguments['SR1DataRate']='20Mbps'
ns3_arguments['R1R2DataRate']='100Mbps'
ns3_arguments['R2RDataRate']='10Mbps'
# end
# following are represented in ms
ns3_arguments['SR1Delay']='5ms'
ns3_arguments['R1R2Delay']='5ms'
ns3_arguments['R2RDelay']='5ms'
# end
ns3_arguments['packetSize']='100'

# new additional arguments
ns3_arguments['separationPacketTrainLength'] = '2'
ns3_arguments['initialPacketTrainLength'] = '1000'
ns3_arguments['numAptPriorityProbes'] = '1000'

# These change between each simulation
ns3_arguments['aptPriority'] = 'H'
ns3_arguments['outputFile']="./OUTPUT_FILES/P_H_H.dat"

cmd_command = './waf --run "'
cmd_command += 'priority-queue-sim'
cmd_command += ' --interPacketTime='+ns3_arguments['interPacketTime']
cmd_command += ' --TXQueueSizeR1='+ns3_arguments['TXQueueSizeR1']
cmd_command += ' --TXQueueSizeR2='+ns3_arguments['TXQueueSizeR2']
cmd_command += ' --TXQueueSizeS='+ns3_arguments['TXQueueSizeS']
cmd_command += ' --ReceiveQueueSizeR2='+ns3_arguments['ReceiveQueueSizeR2']
cmd_command += ' --SR1DataRate='+ns3_arguments['SR1DataRate']
cmd_command += ' --R1R2DataRate='+ns3_arguments['R1R2DataRate']
cmd_command += ' --R2RDataRate='+ns3_arguments['R2RDataRate']
cmd_command += ' --SR1Delay='+ns3_arguments['SR1Delay']
cmd_command += ' --R1R2Delay='+ns3_arguments['R1R2Delay']
cmd_command += ' --R2RDelay='+ns3_arguments['R2RDelay']
cmd_command += ' --packetSize='+ns3_arguments['packetSize']
#cmd_command += ' --separationPacketTrainLength='+ns3_arguments['separationPacketTrainLength']
cmd_command += ' --initialPacketTrainLength='+ns3_arguments['initialPacketTrainLength']
cmd_command += ' --numAptPriorityProbes='+ns3_arguments['numAptPriorityProbes']

cmd_command2 = copy.deepcopy(cmd_command) 

# P A R A M E T E R S - T H A T - C H A N G E
# cmd_command += ' --outputFile='+ns3_arguments['outputFile']
# cmd_command += ' --aptPriority='+ns3_arguments['aptPriority']

# Second waf command is here... with 'L'
# ns3_arguments['aptPriority'] = 'L' # This parameter change each run!
# ns3_arguments['outputFile']="./OUTPUT_FILES/P_H_L.dat" # so is this!

# cmd_command2 += ' --outputFile='+ns3_arguments['outputFile']
# cmd_command2 += ' --aptPriority='+ns3_arguments['aptPriority']

# cmd_command += '"'
# cmd_command2 += '"'


#--------- SPQ Automation Waf parameters -------------------
separationExperiment = [] # list of changing parameter values
waf_commands = []	  # list of collected waf commands
all_waf = []		  # String of waf commands combinations in a list  
all_outputFileNames = ""  # all outfile foldernames holder for files-to-graph.txt
experiments = 10 #number of expected results
z = 1	# keeps count of the parameters for waf separation length SPQ
y=0	# keeps count on waf_commands current/overall indexes
for i in range(16):
	if i >= 10 and z < 40:
		z = 50
	elif z >= 50:
		z += 9
	currentLen = str(z)
	separationExperiment.append(currentLen)
	# priority L
	waf_commands.append(copy.deepcopy(cmd_command))
	ns3_arguments['separationPacketTrainLength'] = str(currentLen)
	ns3_arguments['aptPriority'] = "'L'"
	ns3_arguments['outputFile']="./OUTPUT_FILES/P_L" + "_" + str(z) + ".dat" # so is this!
	waf_commands[y] += ' --separationPacketTrainLength='+ns3_arguments['separationPacketTrainLength']
	waf_commands[y] += ' --outputFile='+ns3_arguments['outputFile']
	waf_commands[y] += ' --aptPriority='+ns3_arguments['aptPriority']
	waf_commands[y] += '"'
	all_outputFileNames += "P_L" + "_" + str(z) + "\n"
	all_waf += waf_commands[y] + '\n'
	z+=1
	y+=1
z=1
for i in range(16):
	if i >= 10 and z < 40:
		z = 50
	elif z >= 50:
		z += 9
	currentLen = str(z)
	separationExperiment.append(currentLen)
	# priority H
	separationExperiment.append(currentLen)
	waf_commands.append(copy.deepcopy(cmd_command))
	ns3_arguments['separationPacketTrainLength'] = str(currentLen)
	ns3_arguments['aptPriority'] = "'H'"
	ns3_arguments['outputFile']="./OUTPUT_FILES/P_H" + "_" + str(z) + ".dat" # so is this!
	waf_commands[y] += ' --separationPacketTrainLength='+ns3_arguments['separationPacketTrainLength']
	waf_commands[y] += ' --outputFile='+ns3_arguments['outputFile']
	waf_commands[y] += ' --aptPriority='+ns3_arguments['aptPriority']
	waf_commands[y] += '"'
	all_outputFileNames += "P_H" + "_" + str(z) + "\n"
	all_waf += waf_commands[y] + '\n'
	z+=1
	y+=1
#----------------------------

# print cmd_command
# print cmd_command2

# Opens File to input our waf commands to
AutoWaf = open("waf-commands.txt", "w")
filesToGraph = open("files-to-graph.txt", "w")
print("Currently Writing Waf Commands in the textfile")
AutoWaf.writelines(all_waf)
filesToGraph.writelines(all_outputFileNames)
AutoWaf.close()
filesToGraph.close()

# Opens File to extract our waf commands from
AutoWaf = open("waf-commands.txt", "r")
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
	data_H_L = open("separationexperiment_20mbps.csv", "w")
	data_Delta = open("separationwithdelta_20mbps.csv", "w")
	difference_value = []
	data_Delta.write("separationLength,LowPriority,HighPriority,DeltaLoss" + "\n")
	data_H_L.write("separationLength,LowPriority,HighPriority" + "\n")
	packetLossForH = []
	packetLossForL = []
	z = 0
	while(True):
		line_H = data_H.readline()
		line_L = data_L.readline()
		packet_H = line_H.split("\t")
		packet_L = line_L.split("\t")
		if not line_H or not line_L:
			break
		difference_value.append(round(float(packet_L[1]) - float(packet_H[1]),2))
		packetLossForH.append(float(packet_H[1]))
		packetLossForL.append(float(packet_L[1]))

	loop_max = int(len(difference_value))
	for x in range(0, loop_max):
		data_Delta.write(separationParameter[x] + "," + str(packetLossForL[x]) + "," + str(packetLossForH[x]) + "," + str(difference_value[x]) + "\n")
		data_H_L.write(separationParameter[x] + "," + str(packetLossForL[x]) + "," + str(packetLossForH[x]) + "\n")
		z+=1
	data_H_L.close()
	data_H.close()
	data_L.close()
	data_Delta.close()
		
# END OF HELPER FUNCTIONS

print "Changing working directory back to OUTPUT_FILE Folder"
os.chdir(directoryPath + "/OUTPUT_FILES")
print "Files listed: "
subprocess.call(['ls'])

print "Analyzing the output files for graphing"
outputFilenames = open("files-to-graph.txt", "r")
extensionNameH = ".dat-H"
extensionNameL = ".dat-L"
LossRateH_data = ""
LossRateL_data = ""
currentLength = 0

gFile = open("packetloss.csv", "w")

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
	packetLossRate_H = calculate_packet_loss(fileH, 'H')
	print "packetLossRate_H: %s " % (packetLossRate_H)
	packetLossRate_L = calculate_packet_loss(fileL, 'L')
	print "packetLossRate_H: %s " % (packetLossRate_L)
	print "Creating Directory for the output files ..."

	numAptPriorityProbes = get_max_packets(fileH)
	output_packet_loss_rate(fileR3,numAptPriorityProbes, packetLossRate_H)
	if currentLength >= 16: # get all dat-H data according to file-to-graphs.txt
		LossRateH_data += separationExperiment[currentLength-16] + "\t" +  str(calculate_loss_rate(numAptPriorityProbes,packetLossRate_H)) + "\n"
	
	numAptPriorityProbes = get_max_packets(fileL)
	output_packet_loss_rate(fileR4,numAptPriorityProbes, packetLossRate_L)
	create_packetloss_difference_rate(fileR3,fileR4)
	
	if currentLength < 16:	# get all dat-L data according to file-to-graphs.txt
		LossRateL_data += separationExperiment[currentLength] + "\t" +  str(calculate_loss_rate(numAptPriorityProbes,packetLossRate_L)) + "\n"

	currentLength+=1
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
os.chdir(directoryPath + "/OUTPUT_FILES")
LossRateH = open("LossRate_H", "w") # All H priority loss packets stored
LossRateL = open("LossRate_L", "w") # ALL L priority loss packets stored
LossRateH.writelines(LossRateH_data)
LossRateL.writelines(LossRateL_data)
LossRateH.close()
LossRateL.close()
AutoWaf.close()
create_r_graph("LossRate_H","LossRate_L",separationExperiment)
	
