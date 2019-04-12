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
winsound.PlaySound('Bonfire.mp3', winsound.SND_ASYNC)
print (pygame.display.list_modes())

ancho = 1366
alto = 768


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

class Nave_espacial(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.Nave = pygame.image.load("nave2.png")
                #self.Nave = pygame.transform.scale(self.Nave,(170,100))
                self.rect = self.Nave.get_rect()
                self.rect.centerx = ancho/2
                self.rect.centery = 690
                self.velocidad_nave = 17
                self.negro = (0,0,0)
                #self.rect.x = self.rect.centerx 
                #self.rect.y = self.rect.centery
                self.lista_disparo = []
                print (self.rect)
        def disparo (self,x,y):
                proyectil_1 = Proyectil(x,y)
                self.lista_disparo.append(proyectil_1)
                
        def Dibujar (self, superficie):
                superficie.blit (self.Nave, self.rect)


class Proyectil(pygame.sprite.Sprite):
        def __init__(self, posx, posy):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_proyectil = pygame.image.load ("proyectil.png")
                self.rect = self.imagen_proyectil.get_rect()
                self.v_disparo = 20
                self.rect.top = posy
                self.rect.left = posx
                

        def Trayecto(self):
                self.rect.top = self.rect.top - self.v_disparo

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_proyectil, self.rect)
                
class Enemigos(pygame.sprite.Sprite):
        def __init__(self, posx, posy):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_enemigo = pygame.image.load ("enemiga.png")
                self.rect = self.imagen_enemigo.get_rect()
                self.imagen_enemigo = pygame.transform.scale(self.imagen_enemigo,(100,90))
                self.lista_d = []
                self.Velocidad = 20
                self.rect.top = posy
                self.rect.left = posx


        def Dibujar (self, superficie):
                superficie.blit (self.imagen_enemigo, self.rect)
                
        

#            Se crea la pantalla del juego y se minimiza la ventana del menu, se da una resolucion a la pantalla del juego
#            se carga la imagen de la nave, se le da su posicionamiento y se carga la cancion del juego
def Jugar():
        Ventana.withdraw()
        juego = pygame.display.set_mode((1366, 768),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        reloj = pygame.time.Clock()
        #pygame.mixer.music.load("Cancion. verificar peso.mpeg")
        #pygame.mixer.music.play(3)
        #proyectil_juego = Proyectil(ancho, alto)
        Jugador = Nave_espacial()
        jugando = True
        vely = 0
        invasor = Enemigos(100,100)
        while True:
                # Se define el color de fond, tiempo, posicion de la imagen de nave
                juego.fill(Jugador.negro)  
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
                                        if event.key == pygame.K_LEFT:
                                                if Jugador.rect.left > -76:
                                                        Jugador.rect.left -= Jugador.velocidad_nave
                                        elif event.key == pygame.K_RIGHT:
                                                if Jugador.rect.right < 1176:
                                                        Jugador.rect.right += Jugador.velocidad_nave
                                        elif event.key == pygame.K_UP:
                                                if Jugador.rect.centery > -76:
                                                        Jugador.rect.centery -= 10
                                        elif event.key == pygame.K_DOWN:
                                                #if Jugador.rect.centery < 563:
                                                if Jugador.rect.centery < 690:
                                                        Jugador.rect.centery += 10
                                        elif event.key == pygame.K_SPACE:
                                                x,y = Jugador.rect.center  
                                                Jugador.disparo(x,y)
                                                print ("disparo")
                                               
                          
                
                Jugador.Dibujar(juego)
                invasor.Dibujar(juego)
                #proyectil_juego.Dibujar(juego)
                if len(Jugador.lista_disparo) > 0:
                        for x in Jugador.lista_disparo:
                                x.Dibujar(juego)
                                x.Trayecto()

                                if x.rect.top < 100:
                                        Jugador.lista_disparo.remove(x)
                pygame.display.update()

        

        
Ventana.protocol("WM_DELETE_WINDOW",Cerrar)

######################### se define los botones de salida y jugar de la pantalla de inicio###############################
B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Jugar, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop() #Despliega la ventana y ejecuta el loop principal que controla el juego
