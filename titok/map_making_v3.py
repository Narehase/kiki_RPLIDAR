import cv2
import numpy as np
import math

class map_hint:
    '''
    def map(x, in_min, in_max, out_min, out_max) :
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    '''


    def pointer(self,Angle,c):
        self.Angle = Angle
        self.c = c
        r = self.r
        Angle += r
        Angle = math.radians(Angle)
        se = c * math.cos(Angle)

        ga = c * math.sin(Angle)
        return se,ga





    def re_pointer(self,s,g):
        rosx = self.rosx
        rosy = self.rosy
        s = rosy + s
        g = rosx + g

        self.s = s
        self.g = g


        return s,g

    def subway(self,image):
        rosx = self.rosx
        rosy = self.rosy
        Angle = self.Angle
        s = self.s
        g = self.g

        




    def sub_fly(self,image, insd : float = 1):
        rosx = self.rosx
        rosy = self.rosy
        Angle = self.Angle

        r = self.r
        sub_Angle = Angle + r
        c = self.c 

        sub_c = 0
        while True:
            sub_c += 1
            Angle = math.radians(sub_Angle)
            se = sub_c * math.cos(Angle)
            ga = sub_c * math.sin(Angle)
            s = int((rosy + se)) 
            g = int((rosx + ga))
            sub_color = [255,255,255]
            image[s,g] = sub_color

            if sub_c == c:
                break
        return image


    def point(self,image,x,y, color = [0,255,0] , traking = False, sensor_fly = True):

        if traking:
            rosx = self.rosx
            rosy = self.rosy
            image[int(rosy),int(rosx)] = [255,0,0]
            image[int(rosy)+1,int(rosx)] = [255,0,0]
            image[int(rosy)-1,int(rosx)] = [255,0,0]
            image[int(rosy),int(rosx)+1] = [255,0,0]
            image[int(rosy),int(rosx)-1] = [255,0,0]






        sub_color = [0,0,255]
        image[x,y] = color


        image[x,y+1] = sub_color
        image[x+1,y] = sub_color

        image[x,y-1] = sub_color
        image[x-1,y] = sub_color
        

        return image

    def run(self,x,y): #상대 좌표 작성
        rosx = self.rosx
        rosy = self.rosy

        s = rosy + y
        g = rosx + x

        self.rosx = g
        self.rosy = s


    def axis_run(self,c,r):
        ro = r

        self.ro = ro 
        
        Angle = math.radians(r)
        se = c * math.cos(Angle)

        ga = c * math.sin(Angle)

        #print(se,ga)



        self.r = r

        rosx = self.rosx
        rosy = self.rosy

        s = rosy + se
        g = rosx + ga

        self.rosx = g
        self.rosy = s

        
    def datafram(self):
        print(self.rosx," | ",self.rosy)




    def __init__(self,x,y): #최초 보정값
        self.rosx = x
        self.rosy = y
        self.r = 0
        print('\u001b[32m'+f"__edit_map_zero axis_X: {x} ,Y: {y} __"+'\u001b[0m')


def tutorial():

    #노트북 이온 i5 23gb 램 기준 360도 하나 그리는데 0.3164803981781006s 소요
    #튜토리얼
    #--------------------------------------------------------------

    ons = np.ones([5000,5000,3])* 180 #도화지 크기 설정 (세로, 가로) 가장 중요!!(이거 너무 작게 만들면 나중에 에러코드 뜸)
    x,y,c = ons.shape
    i = 0

    #--------------------------------------------------------------
    '''
    하얀색의 백지 생성

    '''
    #--------------------------------------------------------------
    hitori = map_hint(500,500)
    #--------------------------------------------------------------
    '''
    맵 좌표 시작점 생성
    '''


    ct = 0
    while True:
        #print(ct)
        for lil in range(360):    
            w,h = hitori.pointer(lil,150) #츠정 각도와 측정된 거리 입력
            #삼각함수를 이용해서 각도와 빗변을 이용해 밑변과 높이 구하기

            s,g = hitori.re_pointer(w,h)# 이전 함수에서 빗변과 높이 입력
            
            #현재 맵에 입력을 위해 좌표계에 맞춰 값 변환

            #=============
            s = int(s)
            g = int(g)
            #부동소수점을 자연수로 변환
            #=============


            ons = hitori.point(ons,s,g) #맵과 좌표를 입력
            ons = hitori.sub_fly(ons)
            #이미지에 그리기



        i += 1

        print(i)
        if i > 1000:
            break
        '''if i > 800 and lgu < 170: # 특정값에 맞추어 회전
            lgu += 1

            print("tun_up", lgu)
            hitori.axis_run(10,1) # 직진 거리와 회전각도 입력
        else:
            hitori.axis_run(1,0) # 위와 같음'''

        if i > 50 and 45 > ct:
            ct += 5


        
        hitori.axis_run(3,ct)


        #print('run : ', i, "    x : ", g, "    y : ", s , "     r : ", ct)
        #ain = cv2.resize(ons/255.,(1000,1000))
        #cv2.imshow("kiki", ain)
        #cv2.waitKey(1)
        

    cv2.imwrite("test_map.png",ons) # 이미지 저장
