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
        
def Jugar():
        Ventana.withdraw()
        juego = pygame.display.set_mode((1366, 768),pygame.FULLSCREEN)
        pygame.display.set_caption ("Space Invaders")
        Nave = pygame.image.load("nave2.png")
        posx = 400
        posy = 350
        reloj = pygame.time.Clock()

        velocidad_nave = 17
        negro = (0,0,0)
        #derecha = True

        while True:
                juego.fill(negro)
                juego.blit(Nave,(posx,posy))
                reloj.tick(20)

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        if posx > -76:
                                                posx -= velocidad_nave
                                if event.key == pygame.K_RIGHT:
                                        if posx < 1176:
                                                posx += velocidad_nave
                                if event.key == pygame.K_UP:
                                        if posy > -76:
                                                posy -= velocidad_nave
                                if event.key == pygame.K_DOWN:
                                        if posy < 563:
                                                posy += velocidad_nave
                                        
                
                


                pygame.display.update()

        

        
Ventana.protocol("WM_DELETE_WINDOW",Cerrar)

################################################################
B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Jugar, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop() #Despliega la ventana y ejecuta el loop principal que controla el juego
