import math

#튕기기용 각도 계산기
def angle(angle_in):
    return 360-angle_in

def rad(angle): return math.radians(angle)

#속도,각도->x,y 변화량
def coordi(speed,angle):
    x=speed*math.cos(rad(angle))
    y=speed*math.sin(rad(angle))
    x=round(x)
    y=round(y)
    return x,y

def circle(r,c_x,c_y,x,y):
    if (x-c_x)**2+(y-c_y)**2<=r**2: return True
    else: return False
    
def square(l,r_x,r_y,x,y):
    if (r_x<=x<r_x+l)*(r_y<=y<r_y+l): return True
    else: return False
    
def rect(len_x,len_y,pos_x,pos_y,x,y):
    if (pos_x<=x<pos_x+len_x)*(pos_y<=y<pos_y+len_y): return True
    else: return False