import serial
import threading
import msvcrt
import time
import sys


lat=1
lon=1
lat_min=1
lon_min=1
lat_max=1
lon_max=1
decision=''
pending_decision=''
read=True;
node_count=0
cont=True
desicion_read=''
pressed=False

ser=serial.Serial()
ser.port=4
ser.baudrate=115200
ser.open()


def key_pressed():
    global pressed
    return pressed

def set_pressed(pr):
    global pressed
    pressed=pr

def send(a):
    global ser
    ser.write(a+'\n')


def inc_node_count():
    global node_count
    node_count += 1

def dec_count():
    global node_count
    node_count -= 1

def reset_node_count():
    global node_count
    node_count = 0

def get_node_count():
     global node_count
     return node_count

def set_pending_decision(d):
    global pending_decision
    pending_decision=d

def get_pending_decision():
    global pending_decision
    return pending_decision

def set_read(r):
    global read
    read=r

def get_read():
    global read
    return read

def set_decision(dec):
    global decision
    decision=dec

def get_decision():
        global decision
        return decision

def set_des():
    global desicion_read
    if get_read():
        desicion_read=get_decision()

def get_des():
    global desicion_read
    return desicion_read


def get_next(node):
    fo2=open("nodes.txt","r")
    a=0
    while a<node*5:
        fo2.readline()
        a+=1
    global lat_min
    global lon_min
    global lat_max
    global lon_max
    line=fo2.readline().rstrip()
    if line!='end':
        lat_min=float(line)
        lat_max=fo2.readline().rstrip()
        lat_max=float(lat_max)
        lon_min=fo2.readline().rstrip()
        lon_min=float(lon_min)
        lon_max=fo2.readline().rstrip()
        lon_max=float(lon_max)
        set_pending_decision(fo2.readline().rstrip())
    else:
        dec_count()
    fo2.close()

def quit():
    global cont
    cont=False

def contn():
    global cont
    return cont

def get_coord(a):
    time.sleep(0.5)
    get_next(get_node_count())
    while contn():
        fo1=open("C:/xampp/htdocs/gps_data/file.txt","r")
        global lat
        global lon
        global lat_min
        global lon_min
        global lat_max
        global lon_max
        lon=fo1.readline().rstrip()
        lon=float(lon)
        lat=fo1.readline().rstrip()
        lat=float(lat)
        time.sleep(1)
        if (lat_min < lat < lat_max ) and (lon_min < lon < lon_max):
            set_decision(get_pending_decision())
            set_des()
            set_read(False)
            inc_node_count()
            get_next(get_node_count())
        else:
             set_decision('straight')
             set_des()
        fo1.close()


try:
   thread = threading.Thread(target=get_coord, args=(0,))
   thread.start()
except:
   print "Error: unable to start thread"

def manual_control(a):
    while contn():
        while msvcrt.kbhit():
            set_pressed(True)
            k=msvcrt.getch()
            send(k)
            if k=='w':
               send('accelerate')
            if k=='s':
                send('deaccelerate')
            if k=='a':
                send('left')
            if k=='d':
                send('right')

            if k=='q':
                quit()
            time.sleep(0.1)
        if(key_pressed()):
            time.sleep(0.5)
            set_pressed(False)

        time.sleep(0.1)


try:
   thread2 = threading.Thread(target=manual_control, args=(0,))
   thread2.start()
except:
   print "Error: unable to start thread2"



