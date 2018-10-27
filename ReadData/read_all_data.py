from __future__ import print_function
#telemetry staff
import socket
from structs import UDPPacket
import ctypes

import numpy as np
from PIL import ImageGrab
import cv2
import time
from grabscreen import grab_screen
import os




def set_telemetry(packet):


    telemetry_values  = {}
    telemetry_values['x'] = packet.x
    telemetry_values['y'] = packet.y
    telemetry_values['z'] = packet.z
    telemetry_values['speed'] = packet.speed
    telemetry_values['xv'] = packet.xv
    telemetry_values['yv'] = packet.yv 
    telemetry_values['zv'] = packet.zv 
    telemetry_values['xr'] = packet.xr
    telemetry_values['yr'] = packet.yr
    telemetry_values['zr'] = packet.zr 
    telemetry_values['xd'] = packet.xd
    telemetry_values['yd'] = packet.yd
    telemetry_values['zd'] = packet.zd
    telemetry_values['sRL'] = packet.susp_pos[0]
    telemetry_values['sRR'] = packet.susp_pos[1]
    telemetry_values['sFL'] = packet.susp_pos[2]
    telemetry_values['sFR'] = packet.susp_pos[3]
    telemetry_values['svRL'] = packet.susp_vel[0]
    telemetry_values['svRR'] = packet.susp_vel[1]
    telemetry_values['svFL'] = packet.susp_vel[2]
    telemetry_values['svFR'] = packet.susp_vel[3]
    telemetry_values['wsRL'] = packet.wheel_speed[0]
    telemetry_values['wsRR'] = packet.wheel_speed[1]
    telemetry_values['wsFL'] = packet.wheel_speed[2]
    telemetry_values['wsFR'] = packet.wheel_speed[3]
    telemetry_values['yaw'] = packet.yaw
    telemetry_values['pitch'] = packet.pitch
    telemetry_values['roll'] = packet.roll
    telemetry_values['xlv'] = packet.x_local_velocity
    telemetry_values['ylv'] = packet.y_local_velocity
    telemetry_values['zlv'] = packet.z_local_velocity
    telemetry_values['aax'] = packet.ang_acc_x
    telemetry_values['aay'] = packet.ang_acc_y
    telemetry_values['aaz'] = packet.ang_acc_z
    telemetry_values['throttle'] = packet.throttle
    telemetry_values['steer'] = packet.steer
    telemetry_values['brake'] = packet.brake



    return telemetry_values



def get_packet(address, port):
    """
    Recieve a single UDP telemetry packet from the specified port and ip address
    
    :param address: IP address for the socket
    :param port: Port for the socket
    :return: A UDPPacket
    """
    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind the socket to the specified ip address and port
    sock.bind((address, port))
    # recieve data
    data, addr = sock.recvfrom(ctypes.sizeof(UDPPacket))
    # convert from raw bytes to UDPPacket structure
    return UDPPacket.from_buffer_copy(data)


def get_telemetry(address, port):
    """
    Generator function which yields UDPPackets from the specified ip address and port
    
    :param address: IP address for receiving packets
    :param port: Port on which to receive packets
    :yeild: a UDPPacket for each udp packet received
    """
    last_packet = None
    while True:
        packet = get_packet(address, port)
        if last_packet is None or packet.time > last_packet.time:
            yield packet
            last_packet = packet


# countdown
for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

training_data = []
last_time = time.time()

starting_value = 1


SAVED_FILE_NAME = '6990_telemetry_training_data-{}.npy'

while True:
    file_name = SAVED_FILE_NAME.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along',starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!',starting_value)

        break


while (True):

    screen = grab_screen(region=(0, 100, 1000, 740))

    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    # resize frame
    screen = cv2.resize(screen, (250,250))

    # region of interest
    #screen = screen [78:150,0:250]

    #new region of interest
    screen = screen [70:290, 0:250]


    loop_time = time.time() - last_time


    for packet in get_telemetry('',20777):

        telemetry_values = set_telemetry(packet)

        break

    # read steering
    f = open("ReadData/current_steering.txt", "r")
    for line in f:
        steering = line

    # f = open("ReadData/current_throttle.txt", "r")
    # for line in f:
    #     throttle = line

    # f = open("ReadData/current_brakes.txt", "r")
    # for line in f:
    #     brakes = line



    current_controls = {}
    current_controls['steering'] = steering
    # current_controls['throttle'] = throttle
    # current_controls['brakes'] = brakes


    training_data.append([screen,telemetry_values,current_controls])

    last_time = time.time()


    #save the training data 500 at a time
    if len(training_data) % 500 == 0:
        
        if len(training_data) == 500:
                            np.save(file_name,training_data)
                            print('SAVED')
                            training_data = []
                            starting_value += 1
                            file_name = SAVED_FILE_NAME.format(starting_value)


    #quit with 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
