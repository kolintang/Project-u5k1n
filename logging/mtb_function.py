# Updated April 19th
# New CAN Message ID structure
#    
#    PMsgID = 0x000;
#    PMsgID |= (chip_id | sda_no << 4 | BoardConfig.EE_CAN_BoardAddress << 8); //configure Message ID

#     | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
#     |    Board  ID    |  N/A  |  SDA  |     Chip      |

import ntcan
import util
import os
import csv
import time
# ---> cif = ntcan.CIF( net, RxQueueSize, RxTimeOut, TxQueueSize, TxTimeOut, Flags)
net=0                                   # logical CAN Network [0, 255]
RxQS=1                                 # RxQueueSize [0, 10000]
RxTO=2000                               # RxTimeOut in Millisconds
TxQS=1                                  # TxQueueSize [0, 10000]
TxTO=1000                               # TxTimeOut in Millseconds
##
cif_array   = {}#Number of CAN ID or equal to taxel
cif_array2   = {}

cmsg_array  = {}
cmsg_array2  = {}
id_base = 0x200  #Target ID of the MTB that we want to trigger 
CAN_address = []
CAN_temp = []
headerID = 0x7
CAN_ID = {}

label = []
data_length = 6  # xyz * (MSB, LSB)

### arrays ###
mlx_buffer = {} 

x_axis = {} 
y_axis = {}
z_axis = {}

x_baseline = {}
y_baseline = {}
z_baseline = {}

#def generateID(num_taxel, MTB_ID):
#    for j in range (0, len(MTB_ID)):
#        for i in range (0,num_taxel):
#            CAN_ID[j,i] = headerID << 8 | MTB_ID[j] << 4 | i
#            print hex(CAN_ID[j,i])

##################### MTB CAN communication related ###############       
def initialize(num_taxel, MTB_ID, baud):
    for j in range(0 , len(MTB_ID)):
        for k in range(0, num_taxel):
            cif_array[j,k] = ntcan.CIF(net,RxQS) #configure parameters
            cif_array[j,k].baudrate = baud  # set baudrate 0 = 1MBaud
            cmsg_array[j,k] = ntcan.CMSG() #for
            
    # validate the configuration & check the CAN-USB availability
    print (cif_array[0,0])
    print (cif_array[0,0].net)
    print (cif_array[0,0].tx_timeout)
    print (cif_array[0,0].rx_timeout)
    print (cif_array[0,0].features)
    util.print2lines()

    print "cmsg lost: %d"%(cmsg_array[0,0].msg_lost)
    print "cmsg2 %s" %(cmsg_array[0,0])

def initialize2(num_taxel, MTB_ID, num_taxel2, MTB_ID2, baud):
    for j in range(0 , len(MTB_ID)):
        for k in range(0, num_taxel):
            cif_array[j,k] = ntcan.CIF(net,RxQS) #configure parameters
            cif_array[j,k].baudrate = baud  # set baudrate 0 = 1MBaud
            cmsg_array[j,k] = ntcan.CMSG() 

    for j in range(len(MTB_ID) , len(MTB_ID) + len(MTB_ID2)):
        for k in range(0, num_taxel2):
            cif_array[j,k] = ntcan.CIF(net,RxQS) #configure parameters
            cif_array[j,k].baudrate = baud  # set baudrate 0 = 1MBaud
            cmsg_array[j,k] = ntcan.CMSG()
    
def trigger(MTB_ID):
    for j in range (0, len(MTB_ID)): 
	cmsg_array[j,0].canWriteByte(cif_array[j,0],(id_base|MTB_ID[j]),2,7,0)

def generateID(num_taxel, MTB_ID):
    for j in range (0, len(MTB_ID)):
        for k in range (0,num_sda):
            for l in range (0,num_taxel):
                cif_array[j,(k+1)*l].canIdAdd( MTB_ID[j] << 8| k << 4 | l)

def generateID2(num_taxel, MTB_ID, num_taxel2, MTB_ID2):
    for j in range (0, len(MTB_ID)):
        for k in range (0,num_sda):
            for l in range (0,num_taxel):
                cif_array[j,(k+1)*l].canIdAdd( MTB_ID[j] << 8| k << 4| l)

    for j in range (len(MTB_ID), len(MTB_ID) + len(MTB_ID2)):
        for k in range (0,num_taxel2):
            for l in range (0,num_taxel):
                cif_array[j,(k+1)*l].canIdAdd( MTB_ID2[j-len(MTB_ID)] << 8 | k<<4 |l)

    
def read(num_taxel, MTB_ID):
    for j in range (0, len(MTB_ID)):
        cmsg_array[j,0].canWriteByte(cif_array[j,0],(id_base|MTB_ID[j]),2,7,0)
        for k in range (0, num_taxel):
            cmsg_array[j,k].canRead(cif_array[j,k])

def read2(num_taxel, MTB_ID, num_taxel2, MTB_ID2):
    for j in range (0, len(MTB_ID)):
        cmsg_array[j,0].canWriteByte(cif_array[j,0],(id_base|MTB_ID[j]),2,7,0)
        for k in range (0, num_taxel):
            cmsg_array[j,k].canRead(cif_array[j,k])

    for j in range (len(MTB_ID), len(MTB_ID) + len(MTB_ID2)):
        cmsg_array[j,0].canWriteByte(cif_array[j,0],(id_base|MTB_ID2[j-len(MTB_ID)]),2,7,0)
        for k in range (0, num_taxel2):
            cmsg_array[j,k].canRead(cif_array[j,k])

def read3(num_taxel, MTB_ID, num_taxel2, MTB_ID2):
    MTB_ALL = MTB_ID + MTB_ID2
    trigger(MTB_ALL)
    
    for j in range (0, len(MTB_ID)):
        for k in range (0, num_taxel):
            cmsg_array[j,k].canRead(cif_array[j,k])

    for j in range (len(MTB_ID), len(MTB_ID) + len(MTB_ID2)):
        for k in range (0, num_taxel2):
            cmsg_array[j,k].canRead(cif_array[j,k])
################# Buffer & array related ###########


def generate_tcp_buffer(num_taxel, MTB_ID, num_taxel2, MTB_ID2): # Prepare a buffer for TCP communication #   
    size = len(MTB_ID) * data_length * num_taxel + len(MTB_ID2) * data_length * num_taxel2    
    tcp_array = bytearray(size)
    tcp_buffer = buffer(tcp_array,0, size)

def store_tcp_buffer(num_taxel, MTB_ID, num_taxel2, MTB_ID2):
    for j in range (0, len(MTB_ID)):
        for k in range (0, num_taxel):
            mlx_buffer[j,k] = cmsg_array[j,k].data.c

    for j in range (len(MTB_ID), len(MTB_ID)+len(MTB_ID2)):
        for k in range (0, num_taxel2):
            mlx_buffer[j,k] = cmsg_array[j,k].data.c

    #print mlx_buffer #for debugging
    

def combine_msb_lsb(num_taxel, MTB_ID, num_taxel2, MTB_ID2): #combine MSB | LSB  
    for j in range(0, len(MTB_ID)):
        for k in range (0, num_taxel):
            x_axis[j,k] = ((mlx_buffer[j,k][1] << 8 | mlx_buffer[j,k][2]) - x_baseline[j,k])
            y_axis[j,k] = ((mlx_buffer[j,k][3] << 8 | mlx_buffer[j,k][4]) - y_baseline[j,k])
            z_axis[j,k] = ((mlx_buffer[j,k][5] << 8 | mlx_buffer[j,k][6]) - z_baseline[j,k])

    for j in range(len(MTB_ID),len(MTB_ID)+len(MTB_ID2)):
        for k in range (0, num_taxel2):
            x_axis[j,k] = ((mlx_buffer[j,k][1] << 8 | mlx_buffer[j,k][2]) - x_baseline[j,k])
            y_axis[j,k] = ((mlx_buffer[j,k][3] << 8 | mlx_buffer[j,k][4]) - y_baseline[j,k])
            z_axis[j,k] = ((mlx_buffer[j,k][5] << 8 | mlx_buffer[j,k][6]) - z_baseline[j,k])    

    #print z_axis #for debugging
############ CSV related ################
# create a csv file
def createcsv(num_taxel, MTB_ID, num_taxel2, MTB_ID2,data_store):
    label = []
    j = 0
    while os.path.exists("LOG%s.csv" %j): #Check the last csv file number
        j += 1

    csvfile = open('LOG%s.csv'%j ,'wb' ) #Create a new csv file
    filewrite = csv.writer(csvfile)

    for j in range (0, len(MTB_ID)):
        for k in range (0, num_taxel):
            label += ['MTB%s'%MTB_ID[j]+ 'S%s'%(k+1) +'X',
                      'MTB%s'%MTB_ID[j]+ 'S%s'%(k+1) +'Y',
                      'MTB%s'%MTB_ID[j]+ 'S%s'%(k+1) +'Z']
        
    for j in range (len(MTB_ID), len(MTB_ID)+len(MTB_ID2)):
        for k in range (0, num_taxel2):
            label += ['MTB%s'%MTB_ID2[j-len(MTB_ID)]+'S%s'%(k+1)+'X',
                      'MTB%s'%MTB_ID2[j-len(MTB_ID)]+'S%s'%(k+1)+'Y',
                      'MTB%s'%MTB_ID2[j-len(MTB_ID)]+'S%s'%(k+1)+'Z'] 
    filewrite.writerow(label)            

    for i in range (0,len(data_store)):
        filewrite.writerow(data_store[i])
    csvfile.close()

########################### Baseline recording part ###########
def baseline_calculation(num_taxel, MTB_ID, num_taxel2, MTB_ID2):
    print('Calculating the baseline...')

    num_of_sample = 100 #number of sample to calculate the baseline
    for j in range (0, len(MTB_ID)+len(MTB_ID2)): #zeros
        for k in range (0, num_taxel): #zeros
            x_axis[j,k] = 0
            y_axis[j,k] = 0
            z_axis[j,k] = 0
    
    time.sleep(1)

    for i in range (0,num_of_sample):
        try:
            read2(num_taxel, MTB_ID, num_taxel2, MTB_ID2)
        except IOError, (errno):
            print "I/O error(%s): " % (errno)
    
        store_tcp_buffer(num_taxel, MTB_ID, num_taxel2, MTB_ID2)

        for j in range(0,len(MTB_ID)):
            for k in range (0, num_taxel):
                x_axis[j,k] = x_axis[j,k] + (mlx_buffer[j,k][1] << 8 | mlx_buffer[j,k][2])
                y_axis[j,k] = y_axis[j,k] + (mlx_buffer[j,k][3] << 8 | mlx_buffer[j,k][4])
                z_axis[j,k] = z_axis[j,k] + (mlx_buffer[j,k][5] << 8 | mlx_buffer[j,k][6])        
        #must save according to the label array
        for j in range(len(MTB_ID),len(MTB_ID)+len(MTB_ID2)):
            for k in range (0, num_taxel2):
                x_axis[j,k] = x_axis[j,k] + (mlx_buffer[j,k][1] << 8 | mlx_buffer[j,k][2])
                y_axis[j,k] = y_axis[j,k] + (mlx_buffer[j,k][3] << 8 | mlx_buffer[j,k][4])
                z_axis[j,k] = z_axis[j,k] + (mlx_buffer[j,k][5] << 8 | mlx_buffer[j,k][6])        
        #must save according to the label array
                
        time.sleep(0.01)     

    for j in range(0,len(MTB_ID)):
        for k in range (0, num_taxel):
            x_baseline[j,k] = x_axis[j,k]/num_of_sample
            y_baseline[j,k] = y_axis[j,k]/num_of_sample
            z_baseline[j,k] = z_axis[j,k]/num_of_sample

    for j in range(len(MTB_ID),len(MTB_ID)+len(MTB_ID2)):
        for k in range (0, num_taxel2):
            x_baseline[j,k] = x_axis[j,k]/num_of_sample
            y_baseline[j,k] = y_axis[j,k]/num_of_sample
            z_baseline[j,k] = z_axis[j,k]/num_of_sample
            
    #print(x_baseline) #for debugging
    #print(y_baseline)
    #print(z_baseline)
    #print ('')
        
    print('Baseline calculation has finished')

