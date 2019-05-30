### main4 --> Start from April 2018
### Major update:
### - Generate only desired ID, not using increment by 1 [done]
### - Arrays need to be splitted between 16 taxels & 8 taxels [done]
### - Check which ID is error.
###   If error is detected, stop the communication only with that sensor
### - Add flag for recording
### - Make them as a function?


#from mtb_function import generateID #if you want to import a specific function
import mtb_function as mtb #if you want to import all functions
import ntcan  #Importiere Wrapper fuer NTCAN.DLL
import time 
import getopt
import sys
import string
import os
import canopen
import thread
import util
import threading
import types
import time
import csv
import socket
#############################################

MTB_ID_16 = [1]
MTB_ID_8 = [] #leave it blank ([]) if there is no MTB with 2 SDA
MTB_ALL_ID = MTB_ID_16 + MTB_ID_8
num_of_board = len(MTB_ID_16 )
num_taxel = 8
num_taxel2 = 8
freq = 250
s_time = 1/freq
data_store = [];

##### initialize MTB ########
mtb.initialize(16, MTB_ID_16)
mtb.trigger(MTB_ALL_ID)
mtb.generateID(16, MTB_ID_16)

#### prepare a buffer for TCP/IP
##mtb.generate_tcp_buffer(16, MTB_ID_16, 8, MTB_ID_8)
##data_length = 6
##step = data_length * num_taxel
##
###### calculate baseline ######
##mtb.baseline_calculation(16, MTB_ID_16, 8 , MTB_ID_8)
##    
######## main program ########################
##raw_input("Press Enter to start")
##print('Press ctrl + c to stop')
##
##try:
##    while(True):
##        try:
##            #mtb.read(16, MTB_ID_16)
##            mtb.read3(16, MTB_ID_16, 8 , MTB_ID_8)
##        except IOError, (errno):
##            print "I/O error(%s): " % (errno)
##
##        mtb.store_tcp_buffer(16, MTB_ID_16, 8 , MTB_ID_8)
##        mtb.combine_msb_lsb(16, MTB_ID_16, 8 , MTB_ID_8)
##        
##        #print mtb.z_axis
##        #Put all MSB & LSB in a buffer
##        #for j in range (0, num_of_board):
##         #   for k in range (0, num_taxel):
##                #test_array[j*step + k*6] = mtb.mlx_buffer[j,k][1]
##                #test_array[j*step + k*6 + 1] = mtb.mlx_buffer[j,k][2]
##                #test_array[j*step + k*6 + 2] = mtb.mlx_buffer[j,k][3]
##                #test_array[j*step + k*6 + 3] = mtb.mlx_buffer[j,k][4]
##                #test_array[j*step + k*6 + 4] = mtb.mlx_buffer[j,k][5]
##                #test_array[j*step + k*6 + 5] = mtb.mlx_buffer[j,k][6]
##
##        #print (mtb.z_axis[0,0])
##
##        label = list()
##        for j in range (0, len(MTB_ID_16)):
##            for k in range (0, 16):
##                label.extend([mtb.x_axis[j,k], mtb.y_axis[j,k], mtb.z_axis[j,k]])
##
##        for j in range (len(MTB_ID_16),len(MTB_ID_16)+ len(MTB_ID_8)):
##            for k in range (0, 8):
##                label.extend([mtb.x_axis[j,k], mtb.y_axis[j,k], mtb.z_axis[j,k]])
##        data_store.append(label)
##        
##        time.sleep(1/250) #1/fs
##
##except KeyboardInterrupt:
##    print('Stop')
###### create excel file ######
##    mtb.createcsv(16, MTB_ID_16, 8, MTB_ID_8, data_store)

