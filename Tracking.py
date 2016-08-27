from __future__ import division
import numpy as np
import cv2
import time
import comm
global LeftRight_validity
LeftRight_validity  = 0.9
global straight_validity
straight_validity = 0.4
import msvcrt

def get_straight_cordinates(frame_height, frame_width, var):
    y1_bottom_right=int(frame_height)
    x1_bottom_right=int((frame_width/2)+var)

    x2_top_right=int((frame_width/2)+var)
    y2_top_right=int((frame_height/1.75))


    x3_bottom_left=int((frame_width/2)-var)
    y3_bottom_left=int(frame_height)

    x4_top_left=int((frame_width/2)-var)
    y4_top_left=int((frame_height/1.75))

    return x1_bottom_right, y1_bottom_right, x2_top_right, y2_top_right, x3_bottom_left, y3_bottom_left, x4_top_left, y4_top_left

def get_slight_left_cordinates(frame_height, frame_width, var):
    x1_bottom_right, y1_bottom_right, x2_top_right, y2_top_right, x3_bottom_left, y3_bottom_left, x4_top_left, y4_top_left = get_straight_cordinates(frame_height, frame_width, var)

    x1_sl_left_bottom=int(x3_bottom_left-(var/2))
    y1_sl_left_bottom=y3_bottom_left
    x2_sl_left_top=int(x3_bottom_left-(var/2))
    y2_sl_left_top=y4_top_left

    x3_sl_bottom=x3_bottom_left
    y3_sl_bottom=y3_bottom_left

    x4_sl_top=x4_top_left
    y4_sl_top=y4_top_left

    return x1_sl_left_bottom, y1_sl_left_bottom, x2_sl_left_top, y2_sl_left_top, x3_sl_bottom, y3_sl_bottom, x4_sl_top, y4_sl_top

def get_slight_right_cordinates(frame_height, frame_width, var):
    x1_bottom_right, y1_bottom_right, x2_top_right, y2_top_right, x3_bottom_left, y3_bottom_left, x4_top_left, y4_top_left = get_straight_cordinates(frame_height, frame_width, var)

    x1_sl_right_bottom=int(x1_bottom_right+(var/2))
    y1_sl_right_bottom=y1_bottom_right
    x2_sl_right_top=int(x1_bottom_right+(var/2))
    y2_sl_right_top=y2_top_right

    x3_sl_bottom=x1_bottom_right
    y3_sl_bottom=y1_bottom_right

    x4_sl_top=x2_top_right
    y4_sl_top=y2_top_right

    return x1_sl_right_bottom, y1_sl_right_bottom, x2_sl_right_top, y2_sl_right_top, x3_sl_bottom, y3_sl_bottom, x4_sl_top, y4_sl_top

def check_validity(list_array, comparision):
    correct=0
    for value in list_array:
        if value==comparision:
            correct+=1
    validity=correct/len(list_array)
    return validity
    

def computation(frame, lower_x, higher_x, lower_y, higher_y, received_validity):
    road=[]
    count=0
    array_beta = np.array([-20.0])
    cv2.add(frame, array_beta, frame)
    for y in xrange(lower_y,higher_y):
        for x in xrange(lower_x,higher_x):
            #print y, x
            b=frame.item(y,x,0)
            g=frame.item(y,x,1)
            r=frame.item(y,x,2)

            #print g


            if (b-g)>8 and (b-r)>10:
                  g=b
                  r=b

            elif (r-g)>8 and (r-b)>10:
                  g=r
                  b=r
            
            d1=(r-g)/255
            d2=(g-b)/255
            d3=(r-b)/255

            d1=abs(d1)
            d2=abs(d2)
            d3=abs(d3)

            

            if d1<0.1 and d2<0.1 and d3<0.1 and 49<r<221 and 49<g<221 and 49<b<221:
                road.append('v')
            else:
                road.append('not valid')

    for value in road:
        if value=='v':
            count+=1


    #the default validity for right and left should be 0.8
    #for straight it should be 0.5
    validity=count/len(road)
    #print count

    if validity>received_validity:
        return 1
        #cv2.rectangle(frame,(x2,y2),(x3,y3),(0,255,0),2)
    else:
        return 0
        #cv2.rectangle(frame,(x2,y2),(x3,y3),(0,0,255),2)
    


def straight_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left):
    check_slight_left=computation(frame, x_l_b, x_r_l, y_l_t, y_l_b, LeftRight_validity)
    check_slight_right=computation(frame, x_sli_r_l, x_r_b, y_r_t, y_r_b, LeftRight_validity)
    check_straight=computation(frame, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left, straight_validity)
    if check_slight_left==0 and check_straight==1 and check_slight_right==1:
        #print "R" needs to be slight right
        print 'IMAGE PROCESSING : right'
        comm.send('right')

            

    elif check_slight_left==1 and check_straight==1 and check_slight_right==0:
        #print "L"
        print 'IMAGE PROCESSING : left'
        comm.send('left')
    elif check_slight_left==1 and check_straight==1 and check_slight_right==1:
        print 'IMAGE PROCESSING : straight'
        comm.send('straight')


    else:
        print 'IMAGE PROCESSING : STOP'
        comm.send('stop')


def right_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left):
    check_slight_left=computation(frame, x_l_b, x_r_l, y_l_t, y_l_b, LeftRight_validity)
    check_slight_right=computation(frame, x_sli_r_l, x_r_b, y_r_t, y_r_b, LeftRight_validity)
    check_straight=computation(frame, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left, straight_validity)

    #print check_slight_right

    if check_slight_right==1:
        print 'IMAGE PROCESSING : right'
        comm.send('right')   #"R"

    elif check_slight_right==0 and check_straight==1:
        #print "S"
        print 'IMAGE PROCESSING : straight'
        comm.send('straight')

    elif check_slight_right==0 and check_straight==0 and check_slight_left==1:
        #print "L"
        print 'IMAGE PROCESSING : left'
        comm.send('left')

    else:
        print "STOP"
        print 'IMAGE PROCESSING : stop'


def left_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left):
    check_slight_left=computation(frame, x_l_b, x_r_l, y_l_t, y_l_b, LeftRight_validity)
    check_slight_right=computation(frame, x_sli_r_l, x_r_b, y_r_t, y_r_b, LeftRight_validity)
    check_straight=computation(frame, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left, straight_validity)

    #print check_slight_right

    if check_slight_left==1:
        #print "L"
        print 'IMAGE PROCESSING : left'
        comm.send('left')

    elif check_slight_left==0 and check_straight==1:
        #print "S"
        print 'IMAGE PROCESSING : straight'
        comm.send('straight')

    elif check_slight_left==0 and check_straight==0 and check_slight_right==1:
        #print "R"
        print 'IMAGE PROCESSING : right'
        comm.send('right')

    else:
        #STOP
        print 'IMAGE PROCESSING : stop'
        comm.send('stopt')

        #comm.send('t')
    
    

frame_width=1280
frame_height=720
var=425
time.sleep(4)
x1_bottom_right, y1_bottom_right, x2_top_right, y2_top_right, x3_bottom_left, y3_bottom_left, x4_top_left, y4_top_left = get_straight_cordinates(frame_height, frame_width, var)
x_l_b, y_l_b, x_l_t, y_l_t, x_r_l, y_r_l, x_r_t, y_r_t=get_slight_left_cordinates(frame_height, frame_width, var)
x_r_b, y_r_b, x_r_t, y_r_t, x_sli_r_l, y_sli_r_l, x_sli_r_t, y_sli_r_t=get_slight_right_cordinates(frame_height, frame_width, var)

#print y_r_b, y_r_t
#print x_sli_r_l, x_r_b

cap = cv2.VideoCapture(0)
cap.set(3,1280)

cap.set(4,720)

cap.set(6,15)
#time.sleep(2)
cap.set(37, 1)
direction_count=0
#cap.set(15, 8.0)
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        continue
    if not comm.key_pressed():
        direction=comm.get_des()

#comm.send('')

        print 'GPS: ',direction,' coordinates : ',comm.lat,' , ',comm.lon
       # msvcrt.getch()
        #direction="left"
        cv2.line(frame,(x1_bottom_right, y1_bottom_right),(x2_top_right, y2_top_right),(255,0,0),2)
        cv2.line(frame,(x3_bottom_left, y3_bottom_left),(x4_top_left, y4_top_left),(255,0,0),2)
        cv2.line(frame,(x_l_b, y_l_b),(x_l_t, y_l_t),(255,0,0),2)
        cv2.line(frame,(x_r_b, y_r_b),(x_r_t, y_r_t),(255,0,0),2)
        cv2.imshow('houghlines5',frame)
        #while_count+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if direction=="left":
            #set_read(True)
            print "Left funtion being executed"
            left_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left)
            direction_count+=1
            if direction_count%10==0:
                comm.set_read(True)
                direction_count=0

        elif direction=="straight":
            straight_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left)
        else: #for right
            #set_read(True)
            print "right funtion being executed"
            right_way(frame,x_l_b, x_r_l, y_l_t, y_l_b, x_sli_r_l, x_r_b, y_r_t, y_r_b, x4_top_left, x2_top_right, y2_top_right, y3_bottom_left)
            direction_count+=1
            if direction_count%10==0:
                comm.set_read(True)
                direction_count=0

        

print "\nprogram broke"
#cap.release()
cv2.destroyAllWindows()




