#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilas
from pilas.simbolos import *
from pilas.escena import Base
from pilas.actores import Bomba

#_________________________________________________________________________________________________________________________________________________#


class Menu(Base):
    """Esta clase representa el menu principal del juego"""

    def __init__(self):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)

    def iniciar(self):
        """En esta funcion se definen variables de la clase y se crea el actor Menu"""
        self.fondo = pilas.fondos.Noche()
        self.crear_menu()
        
    def crear_menu(self):
        """Esta funcion crea un menu de opciones en base a cuatro funciones"""
        def iniciar_juego(): # inicia el juego
            pilas.cambiar_escena(Juego())            
        def ayuda_iniciar(): # ejecuta la ayuda
            pilas.cambiar_escena(Ayuda())            
        def salir_del_juego(): # sale del juego
            pilas.terminar()

        self.menu = pilas.actores.Menu([("Iniciar Juego", iniciar_juego),
                                        ("Ayuda", ayuda_iniciar),
                                        ("Salir", salir_del_juego),
                                        ])
#_________________________________________________________________________________________________________________________________________________#



#_________________________________________________________________________________________________________________________________________________#

class Ayuda(Base):
    """Ejecuta la Ayuda del juego (como se juega)"""
    def __init__(self):
        Base.__init__(self)
        """Esta es la funcion inicial del programa"""
    def iniciar(self):
        """Crea las variables de la clase"""
        self.fondo = pilas.fondos.Noche()
        self.texto = pilas.actores.Texto("""
Lo unico que debes saber de este juego es
que para ganar hay que romper todas las
cajas, para esto cuentas con 1 barra la
cual tu mueves pulsando las teclas A y D,
y una bomba que va a ir eliminando las
cajas a medida que transcurra el juego!!
        """)
        self.texto.x, self.texto.y = 30, 250
        self.crear_menu()

    def crear_menu(self):
        """crea otro menu para volver al principal"""
        def atras(): # Vuelve al menu principal
            pilas.cambiar_escena(Menu())
        self.menu2=pilas.actores.Menu([("Atras" , atras)])
        self.menu2.x = -250
        self.menu2.y = -200
        
        
class BombaConMovimiento(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)

        self.circulo = pilas.fisica.Circulo(x, y, 12, restitucion=1, friccion=0, amortiguacion=0, sin_rotacion=True)
        self.imitar(self.circulo)

        self._empujar()

    def _empujar(self):
        self.dx = 1
        self.dy = 1
        self.circulo.impulsar(self.dx * 10, self.dy * 10)
        
        
#_________________________________________________________________________________________________________________________________________________#
                                   
class Barra(pilas.actores.Actor):

    print "PRESIONE LAS TECLAS A Y D PARA MOVER LA BARRA"
    def __init__(self, imagenapasar, x):
        pilas.actores.Actor.__init__(self,imagen=imagenapasar, x=x, y=-220)
        self.aprender(self.MoverseConWSAD)
        
    class MoverseConWSAD(pilas.habilidades.Habilidad):
        '''Hace que un actor se pueda mover con las teclas:
        
        W --> arriba
        S --> abajo
        A --> izquierda
        D --> derecha
        
        Facilita el uso de un segundo mando, muy usado en juegos multiplayer'''

        def __init__(self, receptor):
            pilas.habilidades.Habilidad.__init__(self, receptor)
            self.w = False
            self.s = False
            self.a = False
            self.d = False
            pilas.eventos.actualizar.conectar(self.pulsa_tecla)
            pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_la_tecla)
            pilas.eventos.suelta_tecla.conectar(self.cuando_suelta_la_tecla)
            
        def pulsa_tecla(self, evento):
            velocidad = 5

            if self.a:
                self.receptor.x -= velocidad
            elif self.d:
                self.receptor.x += velocidad
                
            #if self.w:
                self.receptor.y += velocidad
            #elif self.s:
                self.receptor.y -= velocidad
                
        def cuando_pulsa_la_tecla(self, evento):
            self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, True)

        def cuando_suelta_la_tecla(self, evento):
            self.procesar_cambio_de_estado_en_la_tecla(evento.codigo, False)
                
        def procesar_cambio_de_estado_en_la_tecla(self, codigo, estado):
            mapa = {
                w: 'w',
                s: 's',
                a: 'a',
                d: 'd',
            }

            if mapa.has_key(codigo):
                setattr(self, mapa[codigo], estado)
                
#_________________________________________________________________________________________________________________________________________________#

class Perdiste(Base):
    """Esta clase representa el menu principal del juego"""

    def __init__(self):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)

    def iniciar(self):
        """En esta funcion se definen variables de la clase y se crea el actor Menu"""
        self.fondo = pilas.fondos.Tarde()
        self.texto = pilas.actores.Texto("Perdiste, intentalo de nuevo")
#_________________________________________________________________________________________________________________________________________________#        
class Ganaste(Base):
    """Esta clase representa el menu principal del juego"""

    def __init__(self):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)

    def iniciar(self):
        """En esta funcion se definen variables de la clase y se crea el actor Menu"""
        self.fondo = pilas.fondos.Tarde()
        self.texto = pilas.actores.Texto("Ganaste!!!")
        
class Juego(Base):   
    def __init__(self):
        """Esta es la funcion inicial del programa"""
        Base.__init__(self)
        self.contadordemuertes = 0
    def toca_lateral(self, evento):
        if self.bomba.y <= -225:
            print "Moriste, intentalo de nuevo"
            self.bomba.eliminar()
            self.barra1.eliminar()
            self.barra2.eliminar()
            self.barra3.eliminar()
            self.barra4.eliminar()
            pilas.cambiar_escena(Perdiste())
            
    def iniciar(self):           
        
#________________________________________________________________________________________________________________________________________________#
        self.bomba = BombaConMovimiento(y=-219)
        self.bomba.escala = (0.5)
        pilas.atajos.definir_gravedad(0, 0)
        self.barra1 = Barra("Cuad1.jpeg", 1)
        self.barra2 = Barra("Cuad2.jpeg", 22)
        self.barra3 = Barra("Cuad3.jpeg", -20)
        self.barra4 = Barra("Cuad4.jpeg", 43)
        self.barra1.aprender(pilas.habilidades.SeMantieneEnPantalla)
        self.barra2.aprender(pilas.habilidades.SeMantieneEnPantalla)
        self.barra3.aprender(pilas.habilidades.SeMantieneEnPantalla)
        self.barra4.aprender(pilas.habilidades.SeMantieneEnPantalla)
        self.barra = [self.barra1, self.barra2, self.barra3, self.barra4]
        def cuando_colisionan_1(pelota, jugador): # colision entre pelota y jugador 1
            print "La barra toco a la pelota"
            pelota.y += 1
            pelota.circulo.impulsar(pelota.dx * 4, pelota.dy * 5)        
        def cuando_colisionan_2(pelota, jugador): # colision entre pelota y jugador 1
            print "La barra toco a la pelota"
            pelota.y += 1
            pelota.circulo.impulsar(pelota.dx * 5, pelota.dy * 5)
        def cuando_colisionan_3(pelota, jugador): # colision entre pelota y jugador 1
            print "La barra toco a la pelota"
            pelota.y += 1
            pelota.circulo.impulsar(pelota.dx * -5, pelota.dy * 5)
        def cuando_colisionan_4(pelota, jugador): # colision entre pelota y jugador 1
            print "La barra toco a la pelota"
            pelota.y += 1
            pelota.circulo.impulsar(pelota.dx * -4, pelota.dy * 5)
        
        pilas.escena_actual().colisiones.agregar(self.bomba, self.barra2, cuando_colisionan_1)
        pilas.escena_actual().colisiones.agregar(self.bomba, self.barra4, cuando_colisionan_2)    
        pilas.escena_actual().colisiones.agregar(self.bomba, self.barra1, cuando_colisionan_3)
        pilas.escena_actual().colisiones.agregar(self.bomba, self.barra3, cuando_colisionan_4)
        pilas.eventos.actualizar.conectar(self.toca_lateral)
        
        


        caja01 = pilas.actores.Caja(y=192,x=0) 
        caja02 = pilas.actores.Caja(y=192,x=52)
        caja03 = pilas.actores.Caja(y=192,x=104)
        caja04 = pilas.actores.Caja(y=192,x=156)
        caja05 = pilas.actores.Caja(y=192,x=208)
        caja06 = pilas.actores.Caja(y=192,x=260)
        caja07 = pilas.actores.Caja(y=192,x=-52)
        caja08 = pilas.actores.Caja(y=192,x=-104)
        caja09 = pilas.actores.Caja(y=192,x=-156)
        caja10 = pilas.actores.Caja(y=192,x=-208)
        caja11 = pilas.actores.Caja(y=192,x=-260)
        caja12 = pilas.actores.Caja(y=140,x=-260)
        caja13 = pilas.actores.Caja(y=140,x=-208)
        caja14 = pilas.actores.Caja(y=140,x=-156)
        caja15 = pilas.actores.Caja(y=140,x=-104)
        caja16 = pilas.actores.Caja(y=140,x=-52)
        caja17 = pilas.actores.Caja(y=140,x=0)
        caja18 = pilas.actores.Caja(y=140,x=52)
        caja19 = pilas.actores.Caja(y=140,x=104)
        caja20 = pilas.actores.Caja(y=140,x=156)
        caja21 = pilas.actores.Caja(y=140,x=208)
        caja22 = pilas.actores.Caja(y=140,x=260)
        cajas = [caja01, caja02, caja03, caja04, caja05, caja06, caja07, caja08, caja09, caja10, caja11, caja12, caja13, caja14, caja15, caja16, caja17, caja18, caja19, caja20, caja21, caja22]

        def colision(caja, bomba):
            ir = 1
            if(caja.x>bomba.x):
                ir = -1
            caja.eliminar()
            self.contadordemuertes += 1
            print "total de cajas muertas", self.contadordemuertes

    
            bomba.circulo.empujar(15,15)
            if self.contadordemuertes == 22:
                print "perdiste"
                '''self.bomba.eliminar()
                self.barra1.eliminar()
                self.barra2.eliminar()
                self.barra3.eliminar()
                self.barra4.eliminar()'''
                pilas.cambiar_escena(Ganaste()) 
        pilas.escena_actual().colisiones.agregar(cajas, self.bomba, colision)



#_________________________________________________________________________________________________________________________________________________#

pilas.iniciar()
pilas.cambiar_escena(Menu())
pilas.ejecutar()


