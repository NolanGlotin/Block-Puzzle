import tkinter
from PIL import ImageTk, Image
import numpy
import random
import time

# Création de la grille
def create_grid(width,height,cell,border):
    for x in range (width+1):
        canvas.create_line(border+x*cell,border,border+x*cell,border+height*cell,fill='white')
    for y in range (height+1):
        canvas.create_line(border,border+y*cell,border+height*cell,border+y*cell,fill='white')

# Création d'une pièce
def create_block(y):
    shape = random.randint(0,len(Shapes)-1)
    color = random.randint(0,len(colors)-1)
    Hand[y] = {'shape':shape,'imgs':[]}
    for pos in Shapes[shape]:
        Hand[y]['imgs'].append(canvas.create_image((pos[0]+width+4)*cell,(pos[1]+2+y*4)*cell,image=Blocks[colors[color]],anchor='nw'))
    tk.update()

# Gestion de la souris

# Clic de la souris
def press(event):
    global Move_objects
    for y in range(len(Hand)):
        for pos in Shapes[Hand[y]['shape']]:
            if (pos[0]+width+4)*cell<event.x<(pos[0]+width+5)*cell and (pos[1]+2+y*4)*cell<event.y<(pos[1]+3+y*4)*cell:
                Move_objects = Hand[y].copy()
                global Y
                Y = y
    if len(Move_objects)>0:
        for obj in Move_objects['imgs']:
            canvas.tag_raise(obj)
        global mouse_x
        global mouse_y
        global dx
        global dy
        mouse_x, mouse_y = event.x, event.y
        dx, dy = event.x-((width+4)*cell), event.y-((2+Y*4)*cell)

# Mouvement de la souris
def move(event):
    global mouse_x
    global mouse_y
    if len(Move_objects)>0:
        for obj in Move_objects['imgs']:
            canvas.move(obj,event.x-mouse_x,event.y-mouse_y)
        mouse_x, mouse_y = event.x, event.y

# Relâchement de la souris
def release(event):
    global Move_objects
    if len(Move_objects)>0:
        valid = True
        for pos in Shapes[Move_objects['shape']]:
            x = round((event.x-dx+pos[0]*cell)/cell-2)
            y = round((event.y-dy+pos[1]*cell)/cell-2)
            if not(0<=x<width and 0<=y<height) or M[x][y]!=0:
                valid = False # L'emplacement n'est pas valide pour poser la pièce
        if valid:
            img = 0
            global Score
            for pos in Shapes[Move_objects['shape']]:
                M[round((event.x-dx+pos[0]*cell)/cell-2)][round((event.y-dy+pos[1]*cell)/cell-2)] = 1
                M_imgs[round((event.x-dx+pos[0]*cell)/cell-2)][round((event.y-dy+pos[1]*cell)/cell-2)] = Move_objects['imgs'][img]
                img += 1
                Score += 1
                canvas.itemconfig(Score_txt,text='Score : '+str(Score))
            for obj in Move_objects['imgs']:
                canvas.move(obj,(x+2)*cell-(event.x-dx+pos[0]*cell),(y+2)*cell-(event.y-dy+pos[1]*cell))
            Move_objects = []
            Hand[Y] = []
            create_block(Y)
        else:
            for img in Move_objects['imgs']:
                canvas.move(img,(width+4)*cell-(event.x-dx),(2+Y*4)*cell-(event.y-dy))
        Move_objects = []
        check_lines()


# Vérification d'éventuelles lignes/colonnes complétées
def check_lines():
    Delete = []
    for x in range(width):
        line = True
        for y in range (height):
            if M[x][y]!=1:
                line = False
        if line:
            for y in range(height):
                if not (x,y) in Delete:
                    Delete.append((x,y))
    for y in range(height):
        line = True
        for x in range (width):
            if M[x][y]!=1:
                line = False
        if line:
            for x in range(width):
                if not (x,y) in Delete:
                    Delete.append((x,y))
    for pos in Delete:
        canvas.itemconfig(M_imgs[pos[0]][pos[1]],image=white)
    global Score
    for pos in Delete:
        canvas.delete(M_imgs[pos[0]][pos[1]])
        M[pos[0]][pos[1]] = 0
        M_imgs[pos[0]][pos[1]] = 0
        Score += 1
        canvas.itemconfig(Score_txt,text='Score : '+str(Score))
        tk.update()
        time.sleep(0.05)

# Paramètres
width, height = 10,10                                                    # Dimensions de la grille
cell = 60                                                                # Taille d'une cellule
border = 2*cell                                                          # Largeur de la bordure
dim = ((width+12)*cell,(height+4)*cell)                                  # Dimensions de la fenêtre
colors = ['darkBlue','green','lightBlue','orange','pink','red','yellow'] # Couleurs possibles des blocs
Shapes = [                                                               # Formes des pièces
    ((0,0),(1,0)),
    ((0,0),(0,1)),
    ((0,0),(1,0),(2,0),(2,1),(2,2)),
    ((0,0),(0,1),(0,2),(1,2),(2,2)),
    ((0,0),(0,1),(0,2),(1,0),(2,0)),
    ((0,2),(1,2),(2,2),(2,1),(2,0)),
    ((0,0),(1,0),(0,1),(0,2),(1,2)),
    ((1,0),(0,0),(1,1),(1,2),(0,2)),
    ((0,0),(1,0),(2,0),(0,1),(2,1)),
    ((0,1),(1,1),(2,1),(0,0),(2,0)),
    ((1,0),(0,1),(1,1)),
    ((0,0),(1,0),(0,1)),
    ((1,0),(0,1),(1,1),(2,0)),
    ((1,0),(2,0),(1,1),(0,1)),
    ((0,0),(1,0),(2,0),(0,1)),
    ((0,0),(1,0),(2,0),(2,1)),
    ((0,0),(0,1),(1,0),(1,1)),
    ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)),
    ((0,0),(1,0),(2,0)),
    ((0,0),(1,0),(2,0),(3,0)),
    ((0,0),(0,1),(0,2),(0,3)),
    ((0,0),(0,1),(0,2)),
]

# Variables
Hand = [None,None,None]                         # Pièces disponibles (en "main")
M = numpy.zeros(shape=(width,height),dtype=int) # Tableau de l'état de la grille
M_imgs = M.copy()                               # Tableau de l'état graphique de la grille
mouse_x, mouse_y = 0, 0                         # Position de la souris
dx, dy = 0, 0                                   # Vecteurs déplacement de la souris
Move_objects = []                               # Objets déplacés par la souris
Y = 0                                           # Indice de la pièce actuellement déplacée parmi les pièces disponibles
Score = 0                                       # Score actuel

# Création de la fenêtre
tk = tkinter.Tk()
tk.title('Block puzzle')
canvas = tkinter.Canvas(tk,width=dim[0],height=dim[1],bg='#333333')
create_grid(width,height,cell,border)
Score_txt = canvas.create_text((width/2+2)*cell,cell,text='Score : 0',fill='white',font=('Helvetica','30'))
canvas.pack()
tk.update()

# Importation des blocs de couleur
Blocks = {}
for col in colors:
    Blocks[col] = ImageTk.PhotoImage(Image.open('Assets\\'+col+'.png').resize((cell,cell)))
white = ImageTk.PhotoImage(Image.open('assets\\white.png').resize((cell,cell)))
for y in range (3):
    create_block(y)

# Association des touches
canvas.bind_all('<B1-Motion>',move)
canvas.bind_all('<Button-1>',press)
canvas.bind_all('<ButtonRelease-1>',release)

# Boucles principale
canvas.mainloop()