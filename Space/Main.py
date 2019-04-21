import tkinter
from tkinter import *
from tkinter import messagebox
import pygame,sys
from pygame import *
from random import randint
import winsound
import csv
#______________________Ventana Principal_____________________
Ventana = tkinter.Tk()
pygame.init()
Ventana.title ("Space Invaders") 
Ventana.wm_state('zoomed') 
Ventana.config(bg='black')
img = PhotoImage(file='Logo2.png')
Logo = Label(Ventana, image=img)
Logo.pack()
print (pygame.display.list_modes())

#_________________________Variables globales
ancho = 1366
alto = 768
lista_invasores = []


global marcador, nivel, Velocidad, Disparo_enemigo, Imagen_Disparo_Jugador, Asteroides, Num_x
nivel = 1
marcador = 0
Velocidad = 5
Disparo_enemigo = 1600
Asteroides = 600
Imagen_Disparo_Jugador = "proyectil_v2.png"
Num_x = 0

#______________________Funciones para cerrar el programa
def Cerrar():
        if messagebox.askokcancel("Salir", "¿Desea salir del juego?"):
            print ("Ha cerrado la ventana") 
            Ventana.destroy() 
def Salir():
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            Ventana.destroy()


#___________________________________________________________
class asteroide(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_asteroide = pygame.image.load ("enemiga2.png")
                self.imagen_asteroide = pygame.transform.scale(self.imagen_asteroide,(50,45))
                self.rect = self.imagen_asteroide.get_rect()
                global Num_x
                self.v_asteroide = 2
                self.rect.top = -75
                self.rect.left = Num_x
                self.aparicion_asteroide = 5
                self.lista_asteroide = []
                self.Num_x = 0
                print (self.rect.left)
                

        def comportamiento(self, tiempo):
                self.Rango()
                self.Rango_x()


        def Rango_x(self):
                global Num_x
                Num_x = (randint(0,1100))
                
                

        def Trayecto(self):
                self.rect.top = self.rect.top + self.v_asteroide

        def Rango(self):
                global Asteroides
                if (randint(0,Asteroides) == self.aparicion_asteroide):
                        x = self.rect.left
                        y = self.rect.top
                        self.aparicion(x,y)

        
                
                
        def aparicion(self,x,y):
                Aparicion = asteroide()
                self.lista_asteroide.append(Aparicion)
                 
                        

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_asteroide, self.rect)
        
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
                
                

        def Trayecto(self):
                if self.disparo_personaje == False:
                        self.rect.top = self.rect.top + self.v_disparo
                else:
                        self.rect.top = self.rect.top - self.v_disparo
                 
                        

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_proyectil, self.rect)
                
class Enemigos(pygame.sprite.Sprite):
        def __init__(self, posx, posy, distancia, imagen):
                pygame.sprite.Sprite.__init__(self)



                self.imagen_enemigo1 = pygame.image.load (imagen)
                self.imagen_enemigo1 = pygame.transform.scale(self.imagen_enemigo1,(80,80))
                
                self.lista_invasores = [self.imagen_enemigo1]
                self.posImagen = 0

                self.imag_invasor = self.lista_invasores[self.posImagen]
                self.rect = self.imag_invasor.get_rect()
                global Velocidad
                
                self.rect.top = posy
                self.rect.left = posx
                self.Rango_Disparo = 5
                self.Rango_Movimiento = 5
                self.lista_disparo1 = []
                

                self.derecha = True
                self.contador = 0
                self.Maximo_Descenso = self.rect.top + 15

                self.limite_derecha = posx + distancia
                self.limite_izquierda= posx - distancia

        def comportamiento(self, tiempo):
                self.Ataque()
                self.Movimientos()

        def Movimientos(self):
            if self.contador < 2:
                self.Mov_Lateral()
            else:
                self.Mov_Descenso()

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
        def Mov_Descenso(self):
            if  self.Maximo_Descenso == self.rect.top:
                self.contador = 0
                self.Maximo_Descenso = self.rect.top + 15
                
                
            else:
                self.rect.top += 1
        def Ataque(self):
                global Disparo_enemigo
                if (randint(0,Disparo_enemigo) == self.Rango_Disparo):
                        x = self.rect.centerx
                        y = self.rect.centery
                        self.Disparo_enemigo(x,y)

        
                
                
        def Disparo_enemigo(self,x,y):
                disparo = Proyectil(x,y,"proyectil_v3.png",False)
                self.lista_disparo1.append(disparo)
                
                


        def Dibujar (self, superficie):
                self.imag_invasor = self.lista_invasores[self.posImagen]
                superficie.blit (self.imag_invasor, self.rect)

class Nave_espacial(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.Nave = pygame.image.load("nave2.png")   #nave2.png
                self.Nave = pygame.transform.scale(self.Nave,(90,90))
                self.rect = self.Nave.get_rect()
                self.rect.centerx = 683
                self.rect.centery = 690
                self.velocidad_nave = 10
                self.negro = (0,0,0)
                #self.rect.x = self.rect.centerx 
                #self.rect.y = self.rect.centery
                self.lista_disparo = []
                print (self.rect)
        
        def Disparar (self,x,y):
                #x = 570
                #y = 500
                global Imagen_Disparo_Jugador
                disparo = Proyectil(x,y, Imagen_Disparo_Jugador,True)
                self.lista_disparo.append(disparo)
                 
        def Dibujar (self, superficie):
                superficie.blit (self.Nave, self.rect)
        
def Cargar_Enemigos():
        
    posx = 265
    for x in range(1,7):
        enemigo = Enemigos (posx,100,265,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 150


    posx = 265
    for x in range(1,7):
        enemigo = Enemigos (posx,0,265,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 150
        
    posx = 265
    for x in range(1,7):
        enemigo = Enemigos (posx,200,265,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 150
        
    posx = 265
    for x in range(1,7):
        enemigo = Enemigos (posx,400,265,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 150
        
    posx = 265
    for x in range(1,7):
        enemigo = Enemigos (posx,300,265,"enemiga2.png")
        lista_invasores.append(enemigo)
        posx = posx + 150    
        


        

class Nombre_Jugador():
        def __init__(self):
        
                
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
                valor=[self.dato.get()]
                list_Jugador = open ('Jugadores.csv','w')
                with list_Jugador:
                        writer = csv.writer(list_Jugador)
                        writer.writerow(valor)

def Win():
        WIN = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Texto_WIN= pygame.font.Font (None, 80)
        Texto = Texto_WIN.render("Ganó el juego" , 0,(51,159,17))

        Texto_Puntaje = pygame.font.Font (None, 80)
        Texto_P = Texto_Puntaje.render("Puntaje: " + str(marcador), 0,(51,159,17))

        Texto_indicacion = pygame.font.Font (None, 60)
        Texto_in = Texto_indicacion.render("Presione [s] para ir a la ventana principal ", 0,(51,159,17))
        

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        Ventana.deiconify()
                                        pygame.display.quit()
                                        pygame.quit()
                                        sys.exit()
                                                
                
                        
                                        
                                        
                        
                WIN.blit(Texto,(100,200))
                WIN.blit(Texto_P,(100,300))
                WIN.blit(Texto_in,(200,550))
                pygame.display.update()

def Game_Over():
        
        G_O = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Texto_G_O = pygame.font.Font (None, 80)
        Texto = Texto_G_O.render("GAME OVER" , 0,(51,159,17))

        Texto_Puntaje = pygame.font.Font (None, 80)
        Texto_P = Texto_Puntaje.render("Puntaje: " + str(marcador), 0,(51,159,17))

        Texto_indicacion = pygame.font.Font (None, 60)
        Texto_in = Texto_indicacion.render("Presione [s] para ir a la ventana principal ", 0,(51,159,17))
        

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        Ventana.deiconify()
                                        pygame.display.quit()
                                        pygame.quit()
                                        sys.exit()
                                                
                
                        
                                        
                                        
                        
                G_O.blit(Texto,(100,200))
                G_O.blit(Texto_P,(100,300))
                G_O.blit(Texto_in,(200,550))
                pygame.display.update()


        

def Iniciar_nivel():
        nivel_txt =str(nivel)
        Level = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Texto_nivel = pygame.font.Font (None, 80)
        Texto = Texto_nivel.render("Nivel: " + nivel_txt, 0,(51,159,17))
        Puntos = 0
        Texto_indicacion = pygame.font.Font (None, 60)
        Texto_in = Texto_indicacion.render("Presione [s] para empezar... ", 0,(51,159,17))

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        pygame.display.quit()
                                        Jugar()

                        
                Level.blit(Texto,(100,200))
                Level.blit(Texto_in,(200,550))
                pygame.display.update()


#            Se crea la pantalla del juego y se minimiza la ventana del menu, se da una resolucion a la pantalla del juego
#            se carga la imagen de la nave, se le da su posicionamiento y se carga la cancion del juego
def Jugar():
        Cont = 1
        Nombre = Nombre_Jugador()
        Ventana.withdraw()
        juego = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        reloj = pygame.time.Clock()
        pygame.mixer.music.load("Cancion. verificar peso.mpeg")
        pygame.mixer.music.play(3)
        Jugador = Nave_espacial()
        jugando = True
        #Enemig = Enemigos(100,100)
        Enemig = Cargar_Enemigos()
        AST = asteroide()
        
        global nivel, Velocidad, Disparo_enemigo, Imagen_Disparo_Jugador
        
        while True:
                tiempo = pygame.time.get_ticks()/1000
                #Se define el color de fondo, tiempo, posicion de la imagen de nave
                juego.fill(Jugador.negro)
                
                keys = pygame.key.get_pressed()
               # juego.blit(Jugador.Nave,(Jugador.posx,Jugador.posy))
                reloj.tick(60)
                #proyectil_juego.Trayecto()
                # Se define los eventos para los movimientos derecha, izquierda, arriba, abajo de la nave
                # y las coordenadas limites para que no se salga de la ventana
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if jugando == True:
                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                                x = Jugador.rect.centerx
                                                y = Jugador.rect.centery
                                                Jugador.Disparar(x,y)
                                                print ("disparo")
                                        
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


                
                              
                Jugador.Dibujar(juego)
                

                if len(Jugador.lista_disparo) > 0:
                    for x in Jugador.lista_disparo:
                        x.Dibujar(juego)
                        x.Trayecto()
                        if x.rect.top < -20:
                            Jugador.lista_disparo.remove(x)
                        else:
                            for enemigo in lista_invasores:
                                if x.rect.colliderect(enemigo.rect):
                                        

                                        lista_invasores.remove(enemigo)
                                        Jugador.lista_disparo.remove(x)
                                        global marcador
                                        marcador += 10
                                        print (marcador)
                                        
                AST.comportamiento(tiempo)
                                        
                if len(AST.lista_asteroide) > 0:
                                 for x in AST.lista_asteroide:
                                         x.Dibujar(juego)
                                         x.Trayecto()
                     
                    
                
                if len(lista_invasores) > 0:
                    for enemigo in lista_invasores:
                        enemigo.comportamiento(tiempo)
                        enemigo.Dibujar(juego)

                        if enemigo.rect.colliderect(Jugador.rect):
                                pygame.display.quit()
                                Game_Over()
                        
                        
                        if len(enemigo.lista_disparo1) > 0:
                                 for x in enemigo.lista_disparo1:
                                         x.Dibujar(juego)
                                         x.Trayecto()
                                         if x.rect.colliderect(Jugador.rect):
                                                 pygame.display.quit()
                                                 Game_Over()
                                                 
                                         if x.rect.top > 900:
                                                 enemigo.lista_disparo1.remove(x)
                
                                 
                elif len(lista_invasores) == 0 and (nivel == 1) :
                        Imagen_Disparo_Jugador = "2_proyectil.png"
                        Disparo_enemigo -= 600
                        Velocidad +=3
                        nivel += 1
                        Iniciar_nivel()
                        
                        
                        

                                 
                elif len(lista_invasores) == 0 and (nivel == 2) :
                        print ("Hola")
                        Imagen_Disparo_Jugador = "3_proyectil.png"
                        Disparo_enemigo -= 600
                        Velocidad +=3
                        nivel += 1
                        Iniciar_nivel()
                else:
                        Win()
                       
                                
                        
                
                pygame.display.update()

        

        
Ventana.protocol("WM_DELETE_WINDOW",Cerrar)

######################### se define los botones de salida y jugar de la pantalla de inicio###############################
B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Nombre_Jugador, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop() #Despliega la ventana y ejecuta el loop principal que controla el juego
