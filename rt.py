import math as m
import numpy as np

def my_rotx(theta):
    matrix=([[1,0,0],[0,m.cos(theta),-m.sin(theta)],[0,m.sin(theta),m.cos(theta)]])
    matrix=np.round(matrix,decimals=5)
    return matrix

def my_roty(theta):
    matrix=[[m.cos(theta),0,m.sin(theta)],[0,1,0],[-m.sin(theta),0,m.cos(theta)]]
    matrix=np.round(matrix,decimals=5)
    return matrix

def my_rotz(theta):
    matrix=[[m.cos(theta),-m.sin(theta),0],[m.sin(theta),m.cos(theta),0],[0,0,1]]
    matrix=np.round(matrix,decimals=5)
    return matrix

def my_transl():
    x=int(input("Valor x:"))
    y=int(input("Valor y:"))
    z=int(input("Valor z:"))
    t=np.array([[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]])
    return t

def main():
    print("\n~~~~~~~~~~~~~")
    print("1) Rotacion X")
    print("2) Rotacion Y")
    print("3) Rotacion Z")
    print("4) Traslación")
    print("5) Termina")
    op=int(input("Operación : "))
    if op<1 or op>5: print("Opcion no válida")
    return op
    
    
g = 30
x = g *(0.01745329)
op=0
while op != 5:
    op=main()
    print("~~~~~~~~~~~~~")
    if op==1: print("\nROT EN X: \n",my_rotx(x))
    if op==2: print("\nROT EN Y: \n",my_roty(x))
    if op==3: print("\nROT EN Z: \n",my_rotz(x))
    if op==4: print(my_transl())


#def grados():
# G R A D O S
#g = -90
#x = g *(0.01745329)

# R A D I A N E S
#x = (m.pi) / 2
