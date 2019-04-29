#***************************************
#*Tecnologico de Costa Rica            *
#*                                     *
#*Estudiantes:                         *
#*                                     *
#*Armando Fallas Garro  2019226675     *
#*Kevin Calderón Esquivel  20191517479 *
#*                                     *
#*Taller de programacion               *
#*                                     *
#*Profesor: Antonio González Torres    *
#*                                     *
#***************************************
import tkinter
from tkinter import *
from tkinter import messagebox
import pygame,sys
from pygame import *
from random import randint
import winsound
import csv
import json
import threading
#______________________Ventana Principal_____________________
#Se configura el titulo de la ventana, dimensiones, color del fondo
Ventana = tkinter.Tk()
pygame.init()
Ventana.title ("Space Invaders") 
Ventana.wm_state('zoomed') 
Ventana.config(bg='black')
img = PhotoImage(file='Logo2.png')
Logo = Label(Ventana, image=img)
Logo.pack()
print (pygame.display.list_modes())

#_________________________Variables globales_______________________________
ancho = 1366
alto = 768

global marcador, nivel, Velocidad, Disparo_enemigo, Imagen_Disparo_Jugador, Asteroides, Num_x, Aparicion , Name, datos, explosion, lista_invasores
nivel = 1
marcador = 0
Velocidad = 5
Disparo_enemigo = 1600
Asteroides = 500
Imagen_Disparo_Jugador = "proyectil_v2.png"
Num_x = 0
Aparicion = 0
Name = ''
datos = [[],[]]
explosion = False
lista_invasores = []
#______________________Funciones para cerrar el programa______________________________
# Se crea las funciones ya sea saliendo pulsando el botn o la x de la ventana
def Cerrar():
        if messagebox.askokcancel("Salir", "¿Desea salir del juego?"):
            print ("Ha cerrado la ventana") 
            Ventana.destroy() 
def Salir():
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            Ventana.destroy()


#_________________________Clases_________________________________
#Se crean las extrellas que se moveran alrrededor del mapa de batalla

class estrellas(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_estrella = pygame.image.load ("estrella.png")
                self.imagen_estrella = pygame.transform.scale(self.imagen_estrella,(15,15))
                self.rect = self.imagen_estrella.get_rect()
                global Num_x
                self.v_estrella = 1
                self.rect.top = -75
                self.rect.left = Num_x
                self.aparicion_estrella = 5
                self.lista_estrella = []
                self.Num_x = 0
                
                
        # Define los tiempos para llamar las funciones de rango
        def comportamiento(self, tiempo):
                self.Rango()
                self.Rango_x()

        # Origina numeros al azar para el eje x para que las estrellas aparescan en distintios lugares
        def Rango_x(self):
                global Num_x
                Num_x = (randint(0,1200))
                
                
        # Define el movimiento de las estrellas
        def Trayecto(self):
                self.rect.top = self.rect.top + self.v_estrella

        #Define el tiempo de aparicion de cada una de las estrellas

        def Rango(self):
                global Asteroides
                if (randint(0,7) == self.aparicion_estrella):
                        x = self.rect.left
                        y = self.rect.top
                        self.aparicion(x,y)

        
                
        #Agrega las estrellas creadas en una lista        
        def aparicion(self,x,y):
                Aparicion = estrellas()
                self.lista_estrella.append(Aparicion)
                 
                        
        # Se dibuja en la ventana las estrellas
        def Dibujar (self, superficie):
                superficie.blit (self.imagen_estrella, self.rect)

# Se crea las variables correspondientes la el correcto funcionamiento de los asteroides en el mapa
            
class asteroide(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_asteroide = pygame.image.load ("Meteoro.png")
                self.rect = self.imagen_asteroide.get_rect()
                global Num_x
                self.v_asteroide = 1
                self.rect.top = -75
                self.rect.left = Num_x
                self.aparicion_asteroide = 5
                global Aparicion
                self.lista_asteroide = []
                self.Num_x = 0
                print (self.rect.left)

        def explosion_asteroide(self):
                x = self.rect.centerx
                y = self.rect.centery
                self.explotar(x,y)
                        

        def explotar(self,x,y):
                EXP(x,y)
                
        # Define los tiempos para llamar las funciones de rango
        def comportamiento(self, tiempo):
                self.Rango()
                self.Rango_x()

        # Origina numeros al azar para el eje x para que los asteroides aparescan en distintios lugares
        def Rango_x(self):
                global Num_x
                Num_x = (randint(0,1200))
                
                
        # Define el movimiento de los asteroides
        def Trayecto(self):
                self.rect.top = self.rect.top + self.v_asteroide

        #Define el tiempo de aparicion de cada una de los asteroides
        def Rango(self):
                global Asteroides
                if (randint(0,Asteroides) == self.aparicion_asteroide):
                        x = self.rect.left
                        y = self.rect.top
                        self.aparicion(x,y)

        #Agrega los asteroides creadas en una lista        
        def aparicion(self,x,y):
                Aparicion = asteroide()
                self.lista_asteroide.append(Aparicion)
                 
                        
        #Se crea una superficie para dibujar los asteroides
        def Dibujar (self, superficie):
                superficie.blit (self.imagen_asteroide, self.rect)

# Se crea las variables correspondientes la el correcto funcionamiento de los proyectiles en el mapa
        
class Proyectil(pygame.sprite.Sprite):
        def __init__(self,posx,posy, imagen, personaje):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_proyectil = pygame.image.load (imagen)
                self.imagen_proyectil = pygame.transform.scale(self.imagen_proyectil,(50,45))
                self.rect = self.imagen_proyectil.get_rect()
                self.v_disparo = 13
                self.rect.top = posy
                self.rect.left = posx
                self.disparo_personaje = personaje

                
                
        # Define el movimiento de los proyectiles
        
        def Trayecto(self):
                if self.disparo_personaje == False:
                        self.rect.top = self.rect.top + self.v_disparo
                else:
                        self.rect.top = self.rect.top - self.v_disparo
                 
                        
        #Se crea una superficie para dibujar los proyectiles

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_proyectil, self.rect)

# Se define laclase para la aparicion de explosiones 
                
class EXP(pygame.sprite.Sprite):
        def __init__(self,posx,posy):
                global juego
                pygame.sprite.Sprite.__init__(self)
                self.imagen_exp = pygame.image.load("exp.gif")
                self.imagen_exp = self.imagen_exp.convert()
                self.imagen_exp = pygame.transform.scale(self.imagen_exp,(100,100))
                self.rect = self.imagen_exp.get_rect()
                self.rect.top = posy -30
                self.rect.left = posx -30
                self.Dibujar(juego)
                
        # Se dibuja la explosion en la ventana principal del juego       
        def Dibujar (self, superficie):
                
                superficie.blit (self.imagen_exp, self.rect)      
                
# Se crea las variables correspondientes la el correcto funcionamiento de los proyectiles en el mapa
            
class Enemigos(pygame.sprite.Sprite):
        def __init__(self, posx, posy, distancia, imagen):
                pygame.sprite.Sprite.__init__(self)

                self.imagen_enemigo1 = pygame.image.load (imagen)
                self.imagen_enemigo1 = pygame.transform.scale(self.imagen_enemigo1,(60,60))
                
                self.lista_invasores = [self.imagen_enemigo1]
                self.posImagen = 0

                self.imag_invasor = self.lista_invasores[self.posImagen]
                self.rect = self.imag_invasor.get_rect()

                # Se llaman las variables globales velocidad y explosion
                global Velocidad, explosion
                
                self.rect.top = posy
                self.rect.left = posx
                self.Rango_Disparo = 5
                self.Rango_Movimiento = 5
                self.lista_disparo1 = []
                self.lista_exp = []
                

                self.derecha = True
                self.contador = 0
                self.Maximo_Descenso = self.rect.top + 15

                #Se crean las variables para el movimiento de derecha a izquierda de los enemigos
                self.limite_derecha = posx + distancia
                self.limite_izquierda= posx - distancia

                
        def explosion_enemigo(self):
                x = self.rect.centerx
                y = self.rect.centery
                self.explotar(x,y)
                        

        def explotar(self,x,y):
                EXP(x,y)
                

        #Se crea los tiempos en el que la nave llama la funciones de ataque y movimiento

        def comportamiento(self, tiempo):
                self.Ataque()
                self.Movimientos()

        #Se encarga de cuantas veces las naves se moveran lateralmente antes del descenso
        def Movimientos(self):
            if self.contador < 2:
                self.Mov_Lateral()
            else:
                self.Mov_Descenso()

        #Se define los movimientos de izquierda a derecha de los enemigos y sus limites
        def Mov_Lateral(self):
            if self.derecha == True:
                self.rect.left = self.rect.left + Velocidad
                if self.rect.left > self.limite_derecha:
                    self.derecha = False
                    self.contador += 1
            else:
                self.rect.left = self.rect.left - Velocidad
                if self.rect.left < self.limite_izquierda:
                    self.derecha = True

        #Se define cuanto deben bajar los enemigos
        def Mov_Descenso(self):
            if  self.Maximo_Descenso == self.rect.top:
                self.contador = 0
                self.Maximo_Descenso = self.rect.top + 15
                
                
            else:
                self.rect.top += 1

        # Define al azar cual enemigo disparará hacia el jugador
        def Ataque(self):
                global Disparo_enemigo
                if (randint(0,Disparo_enemigo) == self.Rango_Disparo):
                        x = self.rect.centerx
                        y = self.rect.centery
                        self.Disparo_enemigo(x,y)

        
        #Llama la funcion proyectil para dibujar y darle la trayectoria al disparo enemigo       
                
        def Disparo_enemigo(self,x,y):
                disparo = Proyectil(x,y,"proyectil_v3.png",False)
                self.lista_disparo1.append(disparo)        

        #Se crea una superficie para dibujar los enemigos
                
        def Dibujar (self, superficie):
                self.imag_invasor = self.lista_invasores[self.posImagen]
                superficie.blit (self.imag_invasor, self.rect)

# Se crea las variables correspondientes la el correcto funcionamiento de la nave del jugador en el mapa

class Nave_espacial(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.Nave = pygame.image.load("nave2.png")   
                self.Nave = pygame.transform.scale(self.Nave,(70,70))
                self.rect = self.Nave.get_rect()
                self.rect.centerx = 683
                self.rect.centery = 690
                self.velocidad_nave = 10
                self.negro = (0,0,0)
                
                self.lista_disparo = []
                print (self.rect)
                
        #Llama la funcion proyectil para dibujar y darle la trayectoria al disparo del jugador       

        def Disparar (self,x,y):
        
                global Imagen_Disparo_Jugador
                disparo = Proyectil(x,y, Imagen_Disparo_Jugador,True)
                self.lista_disparo.append(disparo)

        #Se crea una superficie para dibujar los enemigos
      
        def Dibujar (self, superficie):
                superficie.blit (self.Nave, self.rect)


#Se carga las imagenes de los enemigos, y se le asigna una posicion en un determinado rango

def Cargar_Enemigos():
        
    posx = 340
    for x in range(1,7):
        enemigo = Enemigos (posx,120,340,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 120


    posx = 340
    for x in range(1,7):
        enemigo = Enemigos (posx,20,340,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 120
        
    posx = 340
    for x in range(1,7):
        enemigo = Enemigos (posx,220,340,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 120
        
    posx = 340
    for x in range(1,7):
        enemigo = Enemigos (posx,420,340,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 120
        
    posx = 340
    for x in range(1,7):
        enemigo = Enemigos (posx,320,340,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 120    
        


# Obtener el nombre del jugador y agregarlo en un archivo csv        

class Nombre_Jugador():
        def __init__(self):
        
                global Name, marcador
                marcador = 0
                pygame.font.init()
                self.Canvas_Jugador = Canvas (Ventana, bg = "black", width = 250, height = 300)
                self.Canvas_Jugador.pack()

                self.dato=tkinter.StringVar()
                self.Nombre = Entry(self.Canvas_Jugador, bd = 5, justify = LEFT, textvariable=self.dato)
                self.Nombre.place(x=120,y=20)
                
                self.Label_Jugador = Label (self.Canvas_Jugador,text = "Jugador:",fg = "white",bg = "black")
                self.Label_Jugador.place (x=20,y=20)
                
                self.B_Guardar = tkinter.Button(self.Canvas_Jugador, text="Guardar",fg="white",width=9,height=2,bg="GREEN",command=self.Lista_J, cursor='hand2')
                self.B_Guardar.place(x=120,y=50)
                self.B_Jugar2 = tkinter.Button(self.Canvas_Jugador, text="Jugar",fg="white",width=9,height=2,bg="GREEN",command=Iniciar_nivel, cursor='hand2')
                self.B_Jugar2.place(x=120,y=100)

        def Lista_J(self):
                global Name
                archivo = open ("Jugadores.csv","a")
                Name = self.dato.get()
                archivo.write(Name)
                archivo.write("\n")
                print (Name)
                archivo.close
                

#Esta funcion creara una ventana nueva cuando se superen los tres niveles del juego y colocará el puntaje final obtenido

def Win():
        global Name
        pygame.init()
        WIN = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Texto_WIN= pygame.font.Font (None, 80)
        Texto = Texto_WIN.render("Ganó el juego" , 0,(51,159,17))

        Texto_Name = pygame.font.Font (None, 80)
        Texto_N = Texto_Name.render("Jugador: " + Name, 0,(51,159,17))

        Texto_Puntaje = pygame.font.Font (None, 80)
        Texto_P = Texto_Puntaje.render("Puntaje: " + str(marcador), 0,(51,159,17))

        Texto_indicacion = pygame.font.Font (None, 60)
        Texto_in = Texto_indicacion.render("Presione [s] para ir a la ventana principal ", 0,(51,159,17))
        
        #Se le asigna un ciclo whie para que la ventana se cierre al presionar la tecla S
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        Ventana.deiconify()
                                        pygame.display.quit()
                                        pygame.quit()
                                        sys.exit()
                                                
                
                        
                                        
                # Se dibuja los diferentes texto en la pantalla, indicandole sus coordenadas                  
                WIN.blit(Texto_N,(850,200))  
                WIN.blit(Texto,(100,200))
                WIN.blit(Texto_P,(100,300))
                WIN.blit(Texto_in,(200,550))
                pygame.display.update()


def Resultados():
        global Name, marcador, datos
        datos= [datos[0] + [Name], datos[1] + [marcador]]
        #datos = {'Jugado' : [Name], 'Puntuacion' : [marcador]}
        
        with open('Jugadores.json', 'w') as file:
                json.dump(datos, file)
        print ()

#Esta funcion creara una ventana nueva cuando el jugador pierda y colocará el puntaje final obtenido
def Game_Over():
        global Name
        pygame.init()
        G_O = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")

        imagen_gameover = pygame.image.load ('game_over.gif')
        imagen_gameover = pygame.transform.scale(imagen_gameover,(400,500))

        Texto_Name = pygame.font.Font (None, 45)
        Texto_N = Texto_Name.render("Jugador: " + Name, 0,(255,255,255))
        

        Texto_Puntaje = pygame.font.Font (None, 45)
        Texto_P = Texto_Puntaje.render("Puntaje: " + str(marcador), 0,(255,255,255))

        Texto_indicacion = pygame.font.Font (None, 30)
        Texto_in = Texto_indicacion.render("Presione [s] para ir a la ventana principal ", 0,(255,255,255))
        

        #Se le asigna un ciclo whie para que la ventana se cierre al presionar la tecla S

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        Ventana.deiconify()
                                        pygame.display.quit()
                                        pygame.quit()
                                        sys.exit()
                                                
                
                        
                                        
                 # Se dibuja los diferentes texto en la pantalla, indicandole sus coordenadas                  
                G_O.blit(imagen_gameover,(500,100))
                G_O.blit(Texto_N,(550,500))        
                G_O.blit(Texto_P,(550,550))
                G_O.blit(Texto_in,(500,700))
                pygame.display.update()


#Esta funcion creara una ventana nueva cuando el jugador presione el boton de jugar y indicara en que nivel se encuentra el jugador
        

def Iniciar_nivel():
        global Name
        pygame.font.init()
        nivel_txt =str(nivel)
        Level = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Texto_nivel = pygame.font.Font (None, 80)
        Texto = Texto_nivel.render("Nivel: " + nivel_txt, 0,(51,159,17))
        Puntos = 0
        Texto_Name = pygame.font.Font (None, 80)
        Texto_N = Texto_Name.render("Jugador: " + Name, 0,(51,159,17))
        Texto_indicacion = pygame.font.Font (None, 60)
        Texto_in = Texto_indicacion.render("Presione [s] para empezar... ", 0,(51,159,17))

        #Se le asigna un ciclo whie para que la ventana se cierre y comience el juego al presionar la tecla S


        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        pygame.display.quit()
                                        Jugar()
                                        pygame.quit()


                # Se dibuja los diferentes texto en la pantalla, indicandole sus coordenadas                  

                Level.blit(Texto_N,(850,200))
                Level.blit(Texto,(100,200))
                Level.blit(Texto_in,(200,550))
                pygame.display.update()
                


#            Se crea la pantalla del juego y se minimiza la ventana del menu, se da una resolucion a la pantalla del juego
#            se carga la imagen de la nave, se le da su posicionamiento y se carga la cancion del juego
def Jugar():
        pygame.init()
        #Se llaman las variables globales
        global nivel, Velocidad, Disparo_enemigo, Imagen_Disparo_Jugador, marcador,lista_asteroide,Aparicion, Asteroides, explosion, juego, lista_invasores

        
        #Se minimixa la ventana principal
        Ventana.withdraw()
        #Se definen el tamaño de la pantalladel juego
        juego = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")

        #Se crea una variable reloj 
        reloj = pygame.time.Clock()

        #se define una cancion de fondo para el juego
        
        pygame.mixer.music.load("Cancion. verificar peso.mpeg")
        pygame.mixer.music.play(3)

        #Se le asignan unas variables a funciones y a clases para ser llamadas cuando se necesiten
        Nombre = Nombre_Jugador()
        Jugador = Nave_espacial()
        jugando = True
        Enemig = Cargar_Enemigos()
        AST = asteroide()
        EST = estrellas()
        Aparicion = asteroide()
        
        
        
        
        # El while es donde se estara ejecutando cada una de las instrucciones de las clases para que el juego corra
        while True:
                tiempo = pygame.time.get_ticks()/1000

                Texto_puntaje = pygame.font.Font (None, 50)
                Texto_Pantalla = Texto_puntaje.render("Puntaje: " + str(marcador), 0,(255,255,255))
                
                #Se define el color de fondo, tiempo, posicion de la imagen de nave
                juego.fill(Jugador.negro)

                # Se le asigna una variable al evento cuando se dejapresionada una tecla
                keys = pygame.key.get_pressed()

               # juego.blit(Jugador.Nave,(Jugador.posx,Jugador.posy))
                reloj.tick(60)
                
                # Se define los eventos para los movimientos derecha, izquierda, arriba, abajo, y disparo de la nave
                # y las coordenadas limites para que no se salga de la ventana

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if jugando == True:
                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                                #Se crean variables x,y para tomar la posicio actual de la nave, para asignarselo a la trayectoria del disparo
                                                x = Jugador.rect.centerx
                                                y = Jugador.rect.centery
                                                Jugador.Disparar(x,y)
                                                # Se define un sonido al disparo de la nave
                                                Disparo_son = pygame.mixer.Sound("disparo de nave.wav")
                                                Disparo_son.play()
                                                print ("disparo")

                                                
                # Se definen los eventos al presionar las teclas
                                        
                if keys[K_LEFT]:
                        if Jugador.rect.left > -1:
                                Jugador.rect.left -= Jugador.velocidad_nave
                                if keys[K_UP]:
                                        if Jugador.rect.top > -75:
                                                Jugador.rect.top -= 10
                                elif keys[K_DOWN]:
                                        if Jugador.rect.top < 660:
                                                Jugador.rect.top += 10
                elif keys[K_RIGHT]:
                        if Jugador.rect.right < 1350:
                                Jugador.rect.right += Jugador.velocidad_nave
                                if keys[K_UP]:
                                        if Jugador.rect.top > -75:
                                                Jugador.rect.top -= 10
                                elif keys[K_DOWN]:
                                        if Jugador.rect.top < 660:
                                                Jugador.rect.top += 10
                elif keys[K_UP]:
                        if Jugador.rect.top > -75:
                                Jugador.rect.top -= 10
                elif keys[K_DOWN]:
                        if Jugador.rect.top < 660:
                                Jugador.rect.top += 10


                #Funcion Dibujar del jugador
                              
                Jugador.Dibujar(juego)

                # Indica cuandose debe dibujar el disparo del jugador y detectar las coliciones con los asteroides y enemigos

                if len(Jugador.lista_disparo) > 0:
                    for x in Jugador.lista_disparo:
                        x.Dibujar(juego)
                        x.Trayecto()
                        if x.rect.top < -20:
                                Jugador.lista_disparo.remove(x)        
                        
                        else:
                                for enemigo in lista_invasores:
                                        if x.rect.colliderect(enemigo.rect):
                                                enemigo.explosion_enemigo()
                                                lista_invasores.remove(enemigo)
                                                Jugador.lista_disparo.remove(x)
                                                marcador += 1
                                                Exp_son = pygame.mixer.Sound("muerte.wav")
                                                Exp_son.play()
                                                
                                                
                        for Aparicion in AST.lista_asteroide:
                                        if x.rect.colliderect(Aparicion.rect):
                                                Aparicion.explosion_asteroide()
                                                AST.lista_asteroide.remove(Aparicion)
                                                Jugador.lista_disparo.remove(x)
                                                marcador += 1
                                                Exp_son = pygame.mixer.Sound("muerte.wav")
                                                Exp_son.play()
                                        
                AST.comportamiento(tiempo)
                EST.comportamiento(tiempo)

                # Indica cuandose debe dibujar las estrellas 
                
                if len(EST.lista_estrella) > 0:
                                 for x in EST.lista_estrella:
                                         x.Dibujar(juego)
                                         x.Trayecto()
                                         if AST.rect.top > 900:
                                                 AST.lista_estrella.remove(x)

                 # Indica cuandose debe dibujar los asteroides y detectar las coliciones con el jugador y las balas del jugador
                                       
                if len(AST.lista_asteroide) > 0:
                                 for x in AST.lista_asteroide:
                                         x.Dibujar(juego)
                                         x.Trayecto()
                                         if AST.rect.top > 1200:
                                                 AST.lista_asteroide.remove(x)
                                         if x.rect.colliderect(Jugador.rect):
                                                 Imagen_Disparo_Jugador = "proyectil_v2.png"
                                                 Disparo_enemigo = 1600
                                                 Velocidad = 5
                                                 nivel = 1
                                                 Asteroides = 500
                                                 lista_invasores = []
                                                 Resultados()
                                                 pygame.display.quit()
                                                 pygame.quit()
                                                 Game_Over()
                                                 
                                        
                      
                    
                # Indica cuandose debe dibujar los enemigos y sus movimientos y detectar las coliciones con el jugador y las balas del jugador

                if len(lista_invasores) > 0:
                    for enemigo in lista_invasores:
                        enemigo.comportamiento(tiempo)
                        enemigo.Dibujar(juego)

                        if enemigo.rect.colliderect(Jugador.rect):
                                Imagen_Disparo_Jugador = "proyectil_v2.png"
                                Disparo_enemigo = 1600
                                Velocidad = 5
                                nivel = 1
                                Asteroides = 500
                                lista_invasores = []
                                Resultados()
                                pygame.display.quit()
                                pygame.quit()
                                Game_Over()
                                
                        
                        
                        if len(enemigo.lista_disparo1) > 0:
                                 for x in enemigo.lista_disparo1:
                                         x.Dibujar(juego)
                                         x.Trayecto()
                                         if x.rect.colliderect(Jugador.rect):
                                                 Imagen_Disparo_Jugador = "proyectil_v2.png"
                                                 Disparo_enemigo = 1600
                                                 Velocidad = 5
                                                 nivel = 1
                                                 Asteroides = 500
                                                 lista_invasores = []
                                                 Resultados()
                                                 pygame.display.quit()
                                                 pygame.quit()
                                                 Game_Over()
                                                 
                                                 
                                                 
                                         if x.rect.top > 900:
                                                 enemigo.lista_disparo1.remove(x)
                        #if len(enemigo.lista_exp) > 0:
                                 #for x in enemigo.lista_exp:
                                  #       print ("Hola")
                                   #      x.Dibujar(juego)
                                         
                                         
                #Se incrementa el nivel cuando la lista de invasores es igual a 0
                
                                 
                elif len(lista_invasores) == 0 and (nivel == 1) :
                        Imagen_Disparo_Jugador = "2_proyectil.png"
                        Disparo_enemigo -= 600
                        Velocidad +=3
                        nivel += 1
                        Asteroides -= 150
                        Iniciar_nivel()
                        
                        
                        
                        
                #Se incrementa el nivel cuando la lista de invasores es igual a 0

                                
                elif len(lista_invasores) == 0 and (nivel == 2) :
                        Imagen_Disparo_Jugador = "3_proyectil.png"
                        Disparo_enemigo -= 400
                        Velocidad +=1
                        nivel += 1
                        Asteroides -= 150
                        Iniciar_nivel()
                        
                else:
                        Imagen_Disparo_Jugador = "proyectil_v2.png"
                        Disparo_enemigo = 1600
                        Velocidad = 5
                        nivel = 1
                        Asteroides = 500
                        lista_invasores = []
                        Win()
                       
                                
                
                juego.blit(Texto_Pantalla,(20,20))
                
                pygame.display.update()

        

        
Ventana.protocol("WM_DELETE_WINDOW",Cerrar)

######################### se define los botones de salida y jugar de la pantalla de inicio###############################
B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Nombre_Jugador, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop() #Despliega la ventana y ejecuta el loop principal que controla el juego
