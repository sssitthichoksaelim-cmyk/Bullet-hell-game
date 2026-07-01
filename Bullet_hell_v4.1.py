
import tkinter as tk, random, math
W,H=1000,700
HS='highscore.txt'
PLAYER=18

class Game:
    def __init__(self,r):
        self.r=r
        self.high=self.load_high()
        self.menu()

    def load_high(self):
        try:return int(open(HS).read())
        except:return 0

    def save_high(self,s):
        open(HS,'w').write(str(s))

    def clear(self):
        for w in self.r.winfo_children(): w.destroy()

    def menu(self):
        self.clear()
        self.r.configure(bg='#141428')
        tk.Label(self.r,text='TETRIS DODGE ARENA V4.1',font=('Consolas',30,'bold'),fg='#00FFFF',bg='#141428').pack(pady=40)
        tk.Label(self.r,text=f'High Score : {self.high}',font=('Consolas',18),fg='#FFD700',bg='#141428').pack()
        tk.Button(self.r,text='SINGLE PLAYER',command=lambda:self.start(1),font=('Consolas',18,'bold')).pack(pady=10)
        tk.Button(self.r,text='DOUBLE PLAYER',command=lambda:self.start(2),font=('Consolas',18,'bold')).pack(pady=10)
        tk.Button(self.r,text='EXIT',command=self.r.destroy,font=('Consolas',18,'bold')).pack(pady=10)

    def start(self,mode):
        self.mode=mode
        self.score=0
        self.tick=0
        self.b=[]
        self.keys=set()
        self.running=True

        self.clear()
        self.cv=tk.Canvas(self.r,width=W,height=H,bg='black',highlightthickness=0)
        self.cv.pack()

        self.p1=[400,560]
        self.p2=[600,560]

        self.r.bind('<KeyPress>',lambda e:self.keys.add(e.keysym.lower()))
        self.r.bind('<KeyRelease>',lambda e:self.keys.discard(e.keysym.lower()))
        self.loop()

    def spawn_pattern(self):
        s=4+self.tick/1200
        p=random.randint(1,8)

        if p==1:
            for _ in range(15):
                self.b.append([random.randint(20,W-20),-20,0,s,'#FF3333'])
        elif p==2:
            for i in range(10):
                self.b.append([-20,40+i*60,s,0,'#FF8800'])
        elif p==3:
            for i in range(10):
                self.b.append([W+20,40+i*60,-s,0,'#AA44FF'])
        elif p==4:
            gap=random.randint(150,W-150)
            for x in range(0,W,25):
                if abs(x-gap)>90:
                    self.b.append([x,-20,0,s*1.2,'#00AAFF'])
        elif p==5:
            for i in range(0,W,90):
                self.b.append([i,-20,0,s,'#FFD700'])
            for i in range(0,H,90):
                self.b.append([-20,i,s,0,'#FFD700'])
        elif p==6:
            for i in range(24):
                a=math.radians(i*15)
                self.b.append([W/2,H/2,math.cos(a)*s,math.sin(a)*s,'#00FFFF'])
        elif p==7:
            center=random.randint(200,800)
            for i in range(8):
                self.b.append([center-i*40,-i*30,-1,s,'#FF5555'])
                self.b.append([center+i*40,-i*30,1,s,'#FF5555'])
        else:
            x=random.randint(100,800)
            shape=random.choice(['I','O','T'])
            pts=[]
            if shape=='I': pts=[(0,0),(30,0),(60,0),(90,0)]
            if shape=='O': pts=[(0,0),(30,0),(0,30),(30,30)]
            if shape=='T': pts=[(0,0),(30,0),(60,0),(30,30)]
            for px,py in pts:
                self.b.append([x+px,py,0,s,'#AA44FF'])

    def end(self,msg):
        self.running=False
        if self.mode==1 and self.score>self.high:
            self.high=int(self.score)
            self.save_high(self.high)

        self.clear()
        tk.Label(self.r,text=msg,font=('Consolas',30,'bold')).pack(pady=60)
        tk.Label(self.r,text=f'Score : {int(self.score)}',font=('Consolas',18)).pack()
        tk.Button(self.r,text='Menu',command=self.menu,font=('Consolas',18)).pack(pady=20)

    def move(self):
        s=7
        if 'a' in self.keys:self.p1[0]-=s
        if 'd' in self.keys:self.p1[0]+=s
        if 'w' in self.keys:self.p1[1]-=s
        if 's' in self.keys:self.p1[1]+=s

        if self.mode==2:
            if 'left' in self.keys:self.p2[0]-=s
            if 'right' in self.keys:self.p2[0]+=s
            if 'up' in self.keys:self.p2[1]-=s
            if 'down' in self.keys:self.p2[1]+=s

            dx=self.p2[0]-self.p1[0]
            dy=self.p2[1]-self.p1[1]
            d=max(math.hypot(dx,dy),0.01)
            if d<40:
                push=(40-d)/2
                self.p1[0]-=(dx/d)*push
                self.p2[0]+=(dx/d)*push
                self.p1[1]-=(dy/d)*push
                self.p2[1]+=(dy/d)*push

        players=[self.p1] if self.mode==1 else [self.p1,self.p2]
        for p in players:
            p[0]=max(PLAYER,min(W-PLAYER,p[0]))
            p[1]=max(PLAYER,min(H-PLAYER,p[1]))

    def loop(self):
        if not self.running:return

        self.tick+=1
        self.score+=0.25

        if self.tick%35==0:
            self.spawn_pattern()

        self.move()

        self.b=[b for b in self.b if -100<b[0]<W+100 and -100<b[1]<H+100]

        self.cv.delete('all')
        self.cv.create_text(90,20,text=f'SCORE {int(self.score)}',fill='white')
        self.cv.create_text(90,40,text=f'HIGH {self.high}',fill='#FFD700')

        for bb in self.b:
            bb[0]+=bb[2]
            bb[1]+=bb[3]
            self.cv.create_rectangle(bb[0]-6,bb[1]-6,bb[0]+6,bb[1]+6,fill=bb[4],outline='')

            if abs(bb[0]-self.p1[0])<20 and abs(bb[1]-self.p1[1])<20:
                self.end('PLAYER 2 WINS!' if self.mode==2 else 'GAME OVER')
                return

            if self.mode==2 and abs(bb[0]-self.p2[0])<20 and abs(bb[1]-self.p2[1])<20:
                self.end('PLAYER 1 WINS!')
                return

        self.cv.create_rectangle(self.p1[0]-PLAYER,self.p1[1]-PLAYER,self.p1[0]+PLAYER,self.p1[1]+PLAYER,fill='#00FFFF')

        if self.mode==2:
            self.cv.create_rectangle(self.p2[0]-PLAYER,self.p2[1]-PLAYER,self.p2[0]+PLAYER,self.p2[1]+PLAYER,fill='#FFD700')

        self.r.after(16,self.loop)

root=tk.Tk()
root.title('Tetris Dodge Arena V4.1')
Game(root)
root.mainloop()
