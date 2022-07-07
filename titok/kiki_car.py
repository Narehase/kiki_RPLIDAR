import cv2
import numpy as np
import serial
from math import atan,pi,floor
import map_making_v3
def _CheckSum(data):
    try:
        ocs = _HexArrToDec((data[6],data[7]))
        LSN = data[1]
        cs = 0x55AA^_HexArrToDec((data[0],data[1]))^_HexArrToDec((data[2],data[3]))^_HexArrToDec((data[4],data[5]))
        for i in range(0,2*LSN,2):
            cs = cs^_HexArrToDec((data[8+i],data[8+i+1])) 
            
        if(cs==ocs):
            return True
        else:
            return False
    except Exception as e:
        return False
        
def _HexArrToDec(data):
    littleEndianVal = 0
    for i in range(0,len(data)):
        littleEndianVal = littleEndianVal+(data[i]*(256**i))
    return littleEndianVal

def _AngleCorr(dist):
    if dist==0:
        return 0
    else:
        return (atan(21.8*((155.3-dist)/(155.3*dist)))*(180/pi))
        


def _Calculate(d):
    ddict=[]
    LSN=d[1]
    Angle_fsa = ((_HexArrToDec((d[2],d[3]))>>1)/64.0)
    Angle_lsa = ((_HexArrToDec((d[4],d[5]))>>1)/64.0)
    if Angle_fsa<Angle_lsa:
        Angle_diff = Angle_lsa-Angle_fsa
    else:
        Angle_diff = 360+Angle_lsa-Angle_fsa
    for i in range(0,2*LSN,2):
        dist_i = _HexArrToDec((d[8+i],d[8+i+1]))/4
        Angle_i_tmp = ((Angle_diff/float(LSN))*(i/2))+Angle_fsa
        if Angle_i_tmp > 360:
            Angle_i = Angle_i_tmp-360
        elif Angle_i_tmp < 0:
            Angle_i = Angle_i_tmp+360
        else:
            Angle_i = Angle_i_tmp
        
        Angle_i = Angle_i +_AngleCorr(dist_i)
        ddict.append((dist_i,Angle_i))
    return ddict

def code(ser):
    ip = []
    data_1 = ser.read(6000)
    #print(data_1)
    
    data_2 = data_1.split(b"\xaa\x55")[1:-1]

    #print(bytearray(data_1))

    
    for i,e in enumerate(data_2):
        #print(i)
        try:
            if(e[0]==0):
                if(_CheckSum(e)):
                    d = _Calculate(e)
                    for ele in d:
                        #print(ele[1])
                        angle = (ele[1])
                        if angle >= 0 and angle < 360:
                            #print(ele[0], " || ", angle)
                            ip.append([angle,ele[0]])




        except Exception as e:
            pass
            print("err")

    return ip
    
    
    
    for i,e in enumerate(data_1):
        pass
        #print(i)
        #print(e)

    data_2 = data_1.split(b"\xaa\x55")[1:-1]

    #print(data_1)
    bist = {}

    for i in range(0, 360):
        bist.update({i:[]})
    
    for i,e in enumerate(data_2):
        try:
            pass
        except Exception as e:
            pass



#ser = serial.Serial(port='COM5',baudrate=128000)
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=128000)
values = bytearray([int('a5', 16),int('60', 16)])
ser.write(values)
mapza = np.ones([5000,5000,3])* 70
print(mapza.shape)
maps = map_making_v3.map_hint(2500,2500)



mapz = mapza.copy()

for i in range(10):
    mapz = mapza.copy()
    iop = code(ser)
    
    for l in iop:
        if l[1] > 2500:
            continue
        w,h = maps.pointer(360 - l[0],l[1])
        
        '''if l[0] < 90 or l[0] > 270 : 
            #print(l[1])
            if l[1] > 0 and l[1] < 30 :
                #print("warr")
                '''

        s,g = maps.re_pointer(w,h)
        s = int(s)
        g = int(g)

        if s >= 5000 or g >= 5000 or s <= 0 or g <= 0:
            continue
         
        #mapz = maps.sub_fly(mapz)
        mapz = maps.point(mapz, s, g, traking= True)
        #mapz = maps.sub_fly(mapz,1)
    lis = cv2.resize(mapz/255., (1000,1000))
    #cv2.imshow("lili", lis)
    #cv2.waitKey(1)
cv2.imwrite("test_map.png",lis*255.)


values = bytearray([int('a5', 16),int('65', 16)])
ser.write(values)
