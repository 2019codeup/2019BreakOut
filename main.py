import pygame,calc,color,copy,random

#+(self.ball_pos[1]>=SIZE[1]-10)

SIZE=(800,600)
run,started,ended=True,False,False
SPEED_B,SIZE_B,MULTI,X_LEN,Y_LEN=10,15,0.8,10,3
life,score,level=3,0,1
debug=0
stage=[]

pygame.init()
screen=pygame.display.set_mode(SIZE)
clock=pygame.time.Clock()
pygame.display.set_caption('Breakout by 2019 Code-up dev')

#공 Class
class Ball(pygame.sprite.Sprite):
    def __init__(self,pos_in):
        global SPEED_B,pos
        #self.ball_angle,self.tmp=random.randint(225,315),0
        self.ball_angle,self.tmp=270,0 #for test
        pygame.sprite.Sprite.__init__(self)
        self.ball_pos=pos_in
        self.img=pygame.transform.smoothscale(pygame.image.load('resources/ball.png').convert_alpha(),(SIZE_B*2,SIZE_B*2))
        self.rect=pygame.Rect(tuple(self.ball_pos),(SIZE_B*2,SIZE_B*2))
    def update(self): #공 업데이트(게임 도중)
        old_pos=copy.deepcopy(self.ball_pos)
        k=0
        for a in calc.coordi(SPEED_B,self.ball_angle):
            self.ball_pos[k]=old_pos[k]+a
            k+=1
        self.rect=pygame.Rect(tuple(self.ball_pos),(SIZE_B*2,SIZE_B*2))
    def update2(self): #공 업데이트(게임 시작 상태)
        self.ball_pos[0]=pygame.mouse.get_pos()[0]
        self.rect=pygame.Rect((self.ball_pos[0]-SIZE_B,self.ball_pos[1]-SIZE_B*2),(SIZE_B*2,SIZE_B*2))
    def render(self): #공 렌더링
        screen.blit(self.img,self.rect)
#경계선
class Line(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,size_x,size_y,color):
        pygame.sprite.Sprite.__init__(self)
        self.rect=pygame.Rect(pos_x,pos_y,size_x,size_y)
    def update(self):
        pygame.draw.rect(screen,pygame.Color(0,0,0),self.rect)
#블럭 Class
class Block(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,size,color):
        pygame.sprite.Sprite.__init__(self)
        self.img=pygame.transform.smoothscale(pygame.image.load('resources/block_%s.png' %color).convert_alpha(),(size,size))
        self.rect=pygame.Rect(pos_x,pos_y,size,size)
    def update(self):
        screen.blit(self.img,self.rect)
#막대 클래스        
class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size=(160,20)
        self.mouse_coord=pygame.mouse.get_pos()[0]
        self.img=pygame.transform.smoothscale(pygame.image.load('resources/bar.png').convert_alpha(),self.size)
        self.rect=pygame.Rect((self.mouse_coord-80,570),self.size)
    def update(self):
        self.mouse_coord=pygame.mouse.get_pos()[0]
        #좌표 범위 제한
        if self.mouse_coord<80: self.mouse_coord=80
        elif self.mouse_coord>720: self.mouse_coord=720
        self.rect=pygame.Rect((self.mouse_coord-80,570),self.size)
        #막대 그리기
        screen.blit(self.img,self.rect)
#main
class main():
    def __init__(self,num_x,num_y):
        global SPEED_B,MULTI,SIZE
        self.moveBall,self.drawLine=False,True #공 그리기, 윤곽선 보이기
        self.mouse_coord=0 #마우스 좌표
        self.num=(num_x,num_y)
        self.num_b=num_x*num_y
        self.ball,self.bar=Ball([pygame.mouse.get_pos()[0],569]),Bar() #바, 공 생성
        self.line_w,self.line_e,self.line_n=Line(-5,80,5,SIZE[1]-80,color.BLACK),Line(SIZE[0],80,5,SIZE[1]-80,color.BLACK),Line(0,75,800,5,color.BLACK) #가상 라인 그리기
        self.blocks,self.block_pos=[],[]
        self.block_g=pygame.sprite.Group()
        #블럭 그리기
        self.block_size=int(min((SIZE[0])/num_x,(SIZE[1]-SIZE_B*5+200)/num_y)//1)
        #self.block_size=100 #for test
        for x in range(0,num_x):
            self.block_pos.append([])
            self.blocks.append([])
            for y in range(0,num_y):
                self.block_pos[x].append((x*self.block_size,y*self.block_size+SIZE_B*5+100))
                self.blocks[x].append(Block(self.block_pos[x][y][0],self.block_pos[x][y][1],self.block_size,random.choice(('r','g','b'))))
                self.block_g.add(self.blocks[x][y])
    def coli_side(self):
        global life
        if pygame.sprite.collide_rect(self.bar,self.ball):
            self.ball.ball_angle=MULTI*(self.ball.ball_pos[0]+SIZE_B)-MULTI*self.mouse_coord+270
        if pygame.sprite.collide_rect(self.ball,self.line_w):
            if pygame.sprite.collide_rect(self.ball,self.line_e):
                self.ball.ball_angle=45
            elif pygame.sprite.collide_rect(self.ball,self.line_n):
                self.ball.ball_angle=315
            else:
                self.ball.ball_angle=180-self.ball.ball_angle
        elif pygame.sprite.collide_rect(self.ball,self.line_e):
            if pygame.sprite.collide_rect(self.ball,self.line_n):
                self.ball.ball_angle=135
            else:
                self.ball.ball_angle=180-self.ball.ball_angle
        elif pygame.sprite.collide_rect(self.ball,self.line_n):
            self.ball.ball_angle=360-self.ball.ball_angle
        elif self.ball.ball_pos[1]>=610:
            life-=1
            self.ball.ball_pos=[pygame.mouse.get_pos()[0]-80,570]
            self.moveBall=False
    def coli_block(self):
        global score
        coli=[]
        l,r,a,b=self.block_size,SIZE_B,self.ball.ball_pos[0]+SIZE_B,self.ball.ball_pos[1]+SIZE_B
        for x in range(0,self.num[0]):
            for y in range(0,self.num[1]):
                if self.blocks[x][y]:
                    if pygame.sprite.collide_rect(self.ball,self.blocks[x][y]):
                        coli.append((x,y))
        if len(coli)==0: pass
        #elif len(coli)==1:
        else:
            for x,y in coli:
                self.block_g.remove(self.blocks[x][y])
                self.blocks[x][y]=None
            p1,p2=coli[0][0],coli[0][1]
            x,y=self.block_pos[p1][p2]
            if (calc.rect(l,r,x,y-r,a,b)) or (calc.rect(l,r,x,y+l,a,b)): self.ball.ball_angle=360-self.ball.ball_angle #상하
            elif (calc.rect(r,l,x-r,y,a,b)) or (calc.rect(r,l,x+l,y,a,b)): self.ball.ball_angle=180-self.ball.ball_angle #좌우
            elif (calc.circle(r,x,y,a,b))*(calc.square(r,x-r,y-r,a,b)): self.ball.ball_angle=225 #좌상단
            elif (calc.circle(r,x+l,y,a,b))*(calc.square(r,x+l,y-r,a,b)): self.ball.ball_angle=315 #우상단
            elif (calc.circle(r,x,y+l,a,b))*(calc.square(r,x-r,y+l,a,b)): self.ball.ball_angle=135 #좌하단
            elif (calc.circle(r,x+l,y+l,a,b))*(calc.square(r,x+l,y+l,a,b)): self.ball.ball_angle=45 #우하단
            else:
                self.ball.ball_angle=90
        '''
        else:
            for x,y in coli:
                self.block_g.remove(self.blocks[x][y])
                self.blocks[x][y]=None
            self.ball.ball_angle=90
        '''
        score+=len(coli)
        self.num_b-=len(coli)
    def run(self):
        global life,ended
        #블럭, 바 업데이트
        self.block_g.update()
        self.bar.update() 
        #좌표 범위 제한
        self.mouse_coord=pygame.mouse.get_pos()[0] #마우스 포인터 x좌표
        if self.mouse_coord<65: self.mouse_coord=65
        elif self.mouse_coord>735: self.mouse_coord=735
        #윤곽선 그리기
        if self.drawLine==True:
            self.line_w.update()
            self.line_e.update()
            self.line_n.update()
        #점수판
        for a in range(0,life):
            pygame.draw.circle(screen,color.GRAY,(65*a+45,35),20)
        screen.blit(pygame.font.SysFont('mgodic',50).render('Lv. %s' % level,True,(0,0,0)),(325,15))
        screen.blit(pygame.font.SysFont('mgodic',50).render('{0:0>3}'.format(score),True,(0,0,0)),(725,15))
        #공 그리기
        if self.moveBall==True: #게임 도중 업데이트
            self.ball.update()
            self.coli_side()
            self.coli_block()
            if life>-1:
                self.ball.render()
                self.block_g.update()
        else: #게임 시작 전 업데이트
            self.ball.update2()
            self.ball.render()
            self.block_g.update()
#end of main
#시작시
def stage_start():
    #점수판
    for a in range(0,life):
        pygame.draw.circle(screen,color.GRAY,(65*a+45,35),20)
    pygame.draw.rect(screen,color.BLACK,(0,75,SIZE[0],5))
    screen.blit(pygame.font.SysFont('mgodic',50).render('Lv. %s' % level,True,color.BLACK),(325,15))
    screen.blit(pygame.font.SysFont('mgodic',50).render('{0:0>3}'.format(score),True,color.BLACK),(725,15))
    screen.blit(pygame.font.SysFont('mgodic',100).render('Breakout',True,color.BLACK),((SIZE[0]-350)//2,(SIZE[1]-100)//2))
    screen.blit(pygame.font.SysFont('mgodic',50).render('Press A Key To Start',True,color.BLACK),((SIZE[0]-375)//2,(SIZE[1]+100)//2))
#end of stage_start
#목숨 없을 시
def stage_end():
    #점수판
    for a in range(0,life):
        pygame.draw.circle(screen,color.GRAY,(65*a+45,35),20)
    pygame.draw.rect(screen,color.BLACK,(0,75,SIZE[0],5))
    screen.blit(pygame.font.SysFont('mgodic',50).render('Lv. %s' % level,True,color.BLACK),(325,15))
    screen.blit(pygame.font.SysFont('mgodic',50).render('{0:0>3}'.format(score),True,color.BLACK),(725,15))
    screen.blit(pygame.font.SysFont('mgodic',100).render('Game Over',True,color.BLACK),((SIZE[0]-400)//2,(SIZE[1]-100)//2))
    screen.blit(pygame.font.SysFont('mgodic',50).render('Press A Key To Start Over',True,color.BLACK),((SIZE[0]-443)//2,(SIZE[1]+100)//2))
#end of stage_end
#실행 초기화
def init():
    global stage
    stage=[]
    stage.append(main(8,2))
    stage.append(main(15,3))
    stage.append(main(20,4))
    stage.append(main(25,5))
init()
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_ESCAPE]: run=False
            elif life<0:
                life,score,level,started,ended=3,0,1,False,False
                init()
            elif started==False: started=True
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                stage_now.moveBall=True
            if pygame.key.get_pressed()[pygame.K_c]:
                debug=0
            elif pygame.key.get_pressed()[pygame.K_d]:
                debug+=1
            if debug>=5:
                if (pygame.key.get_pressed()[pygame.K_UP])*(level<len(stage)):
                    level+=1
                    stage_now=stage[level-1]
                if (pygame.key.get_pressed()[pygame.K_DOWN])*(level>1):
                    level-=1
                    stage_now=stage[level-1]
                if (pygame.key.get_pressed()[pygame.K_PLUS])+(pygame.key.get_pressed()[pygame.K_KP_PLUS]):
                    life+=1
                if (pygame.key.get_pressed()[pygame.K_MINUS])+(pygame.key.get_pressed()[pygame.K_KP_MINUS]):
                    life-=1
    screen.fill(color.WHITE)
    if started==False: stage_start()
    elif life<0: stage_end()
    elif debug>=5:
        stage_now.run()
    else:
        k=0
        for a in range(0,len(stage)):
            if (stage[a].num_b!=0)*(k==0):
                stage_now=stage[a]
                level=a+1
                k=1
                stage_now.run()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()