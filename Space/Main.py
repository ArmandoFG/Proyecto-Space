import tkinter
from tkinter import *
from tkinter import messagebox
import pygame,sys
from pygame import *
from random import randint
import winsound


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
#lista_invasores = True

#______________________Funciones para cerrar el programa
def Cerrar():
        if messagebox.askokcancel("Salir", "¿Desea salir del juego?"):
            print ("Ha cerrado la ventana") 
            Ventana.destroy() 
def Salir():
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            Ventana.destroy()

def Inicio():
        global pausa
        pausa=True
        C_juego.destroy()
        Ventana.deiconify()

#___________________________________________________________-




class Proyectil(pygame.sprite.Sprite):
        def __init__(self,posx,posy, imagen, personaje):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_proyectil = pygame.image.load (imagen)
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
        def __init__(self, posx, posy):
                pygame.sprite.Sprite.__init__(self)



#_____________________________Fila 1_______________________

                self.imagen_enemigo1 = pygame.image.load ('enemiga.png')
                self.imagen_enemigo1 = pygame.transform.scale(self.imagen_enemigo1,(100,90))
                
                
                self.lista_invasores = [self.imagen_enemigo1]
                self.posImagen = 0

                self.imag_invasor = self.lista_invasores[self.posImagen]
                self.rect = self.imag_invasor.get_rect()
                self.Velocidad = 20
                self.rect.top = posy
                self.rect.left = posx
                self.Rango_Disparo = 5
                self.lista_disparo1 = []
                

        #def comportamiento(self, tiempo):
                
                #self.ataque()
                

        #def ataque(self):
                #if (randint(0,100) > self.Rango_Disparo):
                 #       self.Disparo_enemigo
        def Disparo_enemigo(self,x,y):
                disparo = Proyectil(x,y,"proyectil.png",False)
                self.lista_disparo1.append(disparo)
                
                


        def Dibujar (self, superficie):
                self.imag_invasor = self.lista_invasores[self.posImagen]
                superficie.blit (self.imag_invasor, self.rect)

class Nave_espacial(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.Nave = pygame.image.load("nave2.png")   #nave2.png
                #self.Nave = pygame.transform.scale(self.Nave,(170,100))
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
               # x = 570
                #y = 500
                disparo = Proyectil(x,y, "proyectil.png",True)
                self.lista_disparo.append(disparo)
                 
        def Dibujar (self, superficie):
                superficie.blit (self.Nave, self.rect)

        
                

# ________________________Fila 1 _____________________________
         
        

                                                          

#            Se crea la pantalla del juego y se minimiza la ventana del menu, se da una resolucion a la pantalla del juego
#            se carga la imagen de la nave, se le da su posicionamiento y se carga la cancion del juego
def Jugar():
        Ventana.withdraw()
        juego = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        reloj = pygame.time.Clock()
        #pygame.mixer.music.load("Cancion. verificar peso.mpeg")
        #pygame.mixer.music.play(3)
        #proyectil_juego = Proyectil()
        Jugador = Nave_espacial()
        jugando = True
        #vely = 0
        Enemig = Enemigos(100,100)
        
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
                        if Jugador.rect.left > -76:
                                Jugador.rect.left -= Jugador.velocidad_nave
                                if keys[K_UP]:
                                        if Jugador.rect.top > -75:
                                                Jugador.rect.top -= 10
                                elif keys[K_DOWN]:
                                        if Jugador.rect.top < 560:
                                                Jugador.rect.top += 10
                elif keys[K_RIGHT]:
                        if Jugador.rect.right < 1440:
                                Jugador.rect.right += Jugador.velocidad_nave
                                if keys[K_UP]:
                                        if Jugador.rect.top > -75:
                                                Jugador.rect.top -= 10
                                elif keys[K_DOWN]:
                                        if Jugador.rect.top < 560:
                                                Jugador.rect.top += 10
                elif keys[K_UP]:
                        if Jugador.rect.top > -75:
                                Jugador.rect.top -= 10
                elif keys[K_DOWN]:
                        if Jugador.rect.top < 560:
                                Jugador.rect.top += 10


                        
                if (randint(0,60) == Enemig.Rango_Disparo):
                        x = Enemig.rect.centerx
                        y = Enemig.rect.centery
                        Enemig.Disparo_enemigo(x,y)
                        print("disparo")

                #if Enemig.Rango_Disparo 
                
                              
                Jugador.Dibujar(juego)
                Enemig.Dibujar(juego)
                #Enemig.comportamiento(tiempo)
               # proyectil_juego.Dibujar(juego)
                if len(Jugador.lista_disparo) > 0:
                         for x in Jugador.lista_disparo:
                                 x.Dibujar(juego)
                                 x.Trayecto()
                                 if x.rect.top < -20:
                                         Jugador.lista_disparo.remove(x)
                if len(Enemig.lista_disparo1) > 0:
                         for x in Enemig.lista_disparo1:
                                 x.Dibujar(juego)
                                 x.Trayecto()
                                 if x.rect.top > 900:
                                         Enemig.lista_disparo1.remove(x)
                                 
                  
                
                pygame.display.update()

        

        
Ventana.protocol("WM_DELETE_WINDOW",Cerrar)

######################### se define los botones de salida y jugar de la pantalla de inicio###############################
B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Jugar, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop() #Despliega la ventana y ejecuta el loop principal que controla el juego
