# Main game file
#importing necessary
import pygame
import copy
import tkinter as tk
from tkinter import *
import sys
import time
from random import randint
from obj import Object
from obj import Triangle
from obj import Circle
from obj import Square
from obj import Rectangle
from a_star import A_star
class Treasure:
    def __init__(self,tip):
        self.tip=tip
        
        if self.tip=='diamond':
            self.img=pygame.image.load('../Images/diamond.png')
        elif self.tip=='safir':
            self.img=pygame.image.load('../Images/safir.png')
        elif self.tip=='opal':
            self.img=pygame.image.load('../Images/opal.png')
            
    def print_at_coord(self,screen,x,y):
        screen.blit(self.img,(x,y))
        
class MyPyGame(object):
    def __init__(self):
        #define grid
        self.Glist={}
        
        #initialising pygame
        
        pygame.display.init()
        
        #defining the colours in the RGB(red,green,blue) system
        self.green=(0,190,0)
        self.red=(200,0,0)
        self.blue=(63,72,204)
        self.white=(255,255,255)
        self.yellow=(254,216,1)
        self.black=(0,0,0)
        #defining the screen dimensions
        self.display_width=1266
        self.display_height=650
        #defining the screen
        self.screen = pygame.display.set_mode((self.display_width,self.display_height))
        #naming the window
        pygame.display.set_caption('Space Hunter')
        #uploading the background image
        self.background=pygame.image.load('../Images/space.jpg')
        #blit the image on the screen
        self.screen.blit(self.background,(0,0))
        #setting fps
        self.FPS=10
        self.clock=pygame.time.Clock()
        #updateting pygame window
        pygame.display.update()

    def runIntroWindow(self):

        exitWindow=False
        while not exitWindow:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            startimg=pygame.image.load('../Images/start.png')
            startimg1=pygame.image.load('../Images/start1.png')
            quitimg=pygame.image.load('../Images/quit.png')
            quitimg1=pygame.image.load('../Images/quit1.png')
            self.message_display("Welcome to Space Hunter!")
            self.message_display1("Set the timer, pick what you want to find and how you want to sort them :)")
            self.button(400,350,startimg1,startimg,"play")
            self.button(760,350,quitimg1,quitimg,"quit")
        pygame.display.update()
    def update(self):
        pygame.display.update()
    
    def find_best_obj(self,start):
        minim=10000
        
        find_list={}
        for i in self.good_list:
            distance=self.cost(start,i.get_coord())
            price=i.get_price()
            find_list[i]=distance
            if (find_list[i]/price)<minim:
                minim=(find_list[i]/price)
                position=i.get_coord()
                x=i
        return(position)
    def cost(self,start,goal):
        
        dx=abs(start[0]-goal[0])
        dy=abs(goal[1]-start[1])
        D=abs(dx-dy)
        E=min(dx,dy)
        return ( round( (((E*14)+(D*10))/30),0) )
        
        

    def search(self,start,end,Glist):
        
        exitGame=False
        pos_x=self.start_point_x
        pos_y=self.start_point_y
        self.de_occupy_grid(pos_x,pos_y)

        
        for i in range(end[0]-30,end[0]+30,30):
                for j in range(end[1]-30,end[1]+30,30):
                    self.de_occupy_grid(i,j)
        a=A_star(end,start,Glist)
        self.path=a.solve()
        first_x,first_y=self.path[0]
        

        while not exitGame:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            for x,y in self.path:
                if x>first_x and y>first_y:
                    #direction='down_right'
                    ship=pygame.transform.rotate(self.ship,225)
                elif x>first_x and y==first_y:
                    #direction=='right'
                    ship=pygame.transform.rotate(self.ship,270)
                elif x>first_x and y<first_y:
                    #direction='up_right'
                    ship=pygame.transform.rotate(self.ship,315)
                elif x==first_x and y<first_y:
                    ship=self.ship
                elif x==first_x and y==first_y:
                    ship=self.ship
                elif x==first_x and y>first_y:
                    #direction='down'
                    ship=pygame.transform.rotate(self.ship,180)
                elif x<first_x and y>first_y:
                    #direction='down_left'
                    ship=pygame.transform.rotate(self.ship,135)
                if x<first_x and y==first_y:
                    #direction='left'
                    ship=pygame.transform.rotate(self.ship,90)
                if x<first_x and y<first_y:
                    #direction='up_left'
                    ship=pygame.transform.rotate(self.ship,45)
                self.t_current=time.time()
                
                if (self.t_current-self.t1)>self.seconds:
                    self.breakloop=1
                    exitGame=True
                    break
                self.screen.blit(self.held_image,(0,0))
                first_x=x
                first_y=y
                for i in self.objects:
                    i.print_obj()
                    self.message_display_price(str(i.get_price()),i.get_x(),i.get_y())
                for i in self.obstacles:
                    i.print_obj()
                pos_x=x
                pos_y=y
                self.screen.blit(ship,(pos_x,pos_y))
                pygame.display.update()
                self.clock.tick(self.FPS)
            
            for i in self.good_list:
                if end==i.get_coord(): 
                    x=i
            self.good_list.remove(x)
            self.objects.remove(x)
            self.sort_list.append(x)
            if self.breakloop==1:
                self.sort_list.remove(x)
            exitGame=True
        pygame.display.update()
    def obj_to_found(self,Alist):
        ok=1
        self.good_list=[]
        self.minutes=float(user_input[0])
        self.seconds=float(user_input[1])
        self.seconds=self.seconds+(self.minutes*60)
        self.sort_type=user_input[9]
        self.sort_order=user_input[8]
        red_i=user_input[6]
        blue_i=user_input[5]
        green_i=user_input[7]
        square_i=user_input[3]
        rect_i=user_input[4]
        tri_i=user_input[2]
        

        for i in self.objects:
            
            if i.get_colour()==self.red and (red_i)==1:
                ok=0
            if i.get_colour()==self.blue and (blue_i)==1:
                ok=0
            if i.get_colour()==self.green and (green_i)==1:
                ok=0
            if i.get_shape()=='T' and (tri_i)==1:
                ok=0
            if i.get_shape()=='R' and (rect_i)==1:
                ok=0
            if i.get_shape()=='S' and (square_i)==1:
                ok=0
            if ok==0:
                self.good_list.append(i)
            ok=1
        return (self.good_list)
    
    def shapeSortValue(self,shape):
        if type(shape) == Triangle:
            shapeType = 0
        elif type(shape) == Square:
            shapeType = 1
        elif type(shape) == Rectangle:
            shapeType = 2

        return shapeType

    def colourSortValue(self,shape):
        if shape.strColour == "green":
            colourType = 0
        elif shape.strColour == "blue":
            colourType = 1
        elif shape.strColour == "red":
            colourType = 2

        return colourType

    def bubble(self,objList, sortVar, orderVar):
        """
        This function takes 3 arguments.
        1: A list of shape objects.
        2: A variable for selecting whether to sort by shape or colour.
        3: A variable for selecting whether to sort in decending of ascending order.

        The functions sorts the list and then displays the objects on screen in the chosen sorted order.
        """

        checkCount = 0
    
        for i in range(len(objList)):

            swapCount = 0
        
            for item in objList:

                # Gives each item a numeric value for colour and shape to allow them to be compared easily.
                itemVal = self.shapeSortValue(item)
                colourVal = self.colourSortValue(item)
                itemIndex = objList.index(item)
                itemPrice = item.price
                checkCount += 1

                if orderVar == "Descending":
                    if sortVar == "Shape":
                        try:
                            if itemVal > self.shapeSortValue(objList[itemIndex+1]):
                                # If item is greater than the next item in the list, swap them.
                                objList[itemIndex] = objList[itemIndex+1]
                                objList[itemIndex+1] = item
                                swapCount+=1
                            elif itemVal == self.shapeSortValue(objList[itemIndex+1]):
                                # If item is equal to the next item, compare the price of each item.
                                if itemPrice < objList[itemIndex+1].price:
                                    objList[itemIndex] = objList[itemIndex+1]
                                    objList[itemIndex+1] = item
                                    swapCount+=1
                            else:
                                continue
            
                    # When reached end of list.
                        except:
                            pass
                            #print("Line complete")
                    
                    elif sortVar == "Colour":
                        try:
                            if colourVal > self.colourSortValue(objList[itemIndex+1]):
                                objList[itemIndex] = objList[itemIndex+1]
                                objList[itemIndex+1] = item
                                swapCount+=1
                            elif colourVal == self.colourSortValue(objList[itemIndex+1]):
                                if itemPrice < objList[itemIndex+1].price:
                                    objList[itemIndex] = objList[itemIndex+1]
                                    objList[itemIndex+1] = item
                                    swapCount+=1
                            else:
                                continue
                    
                        # When reached end of list.
                        except:
                            pass
                            #print("Line complete")
                    else:
                        raise ValueError("sortVar must be either \"Colour\" or \"Shape\"")

                elif orderVar == "Ascending":
                    if sortVar == "Shape":
                        try:
                            if itemVal < self.shapeSortValue(objList[itemIndex+1]):
                                objList[itemIndex] = objList[itemIndex+1]
                                objList[itemIndex+1] = item
                                swapCount+=1
                            elif itemVal == self.shapeSortValue(objList[itemIndex+1]):
                                if itemPrice > objList[itemIndex+1].price:
                                        objList[itemIndex] = objList[itemIndex+1]
                                        objList[itemIndex+1] = item
                                        swapCount+=1
                            else:
                                continue
                
                        # When reached end of list.
                        except:
                            pass
                            #print("Line complete")
                        
                    elif sortVar == "Colour":
                        try:
                            if colourVal < self.colourSortValue(objList[itemIndex+1]):
                                objList[itemIndex] = objList[itemIndex+1]
                                objList[itemIndex+1] = item
                                swapCount+=1
                            elif colourVal == self.colourSortValue(objList[itemIndex+1]):
                                if itemPrice > objList[itemIndex+1].price:
                                    objList[itemIndex] = objList[itemIndex+1]
                                    objList[itemIndex+1] = item
                                    swapCount+=1
                            else:
                                continue
                        
                        # When reached end of list.
                        except:
                            pass
                                         
                    else:
                        raise ValueError("sortVar must be either \"Colour\" or \"Shape\"")
                else:
                    raise ValueError("orderVar must be either \"Descending\" or \"Ascending\"")

            if swapCount == 0:
                break

        exitGame=False
        self.screen.blit(self.held_image,(0,0))
        first_x=30
        first_y=30
        while not exitGame:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            x=30
            y=30
            self.keep_coord=[]
            self.opal_list=[]
            self.diamond_list=[]
            self.safir_list=[]
            for i in objList:
                self.keep_coord.append((x,y))
                if x>=self.display_width:
                    y=y+60
                
                i.print_obj_sort(x,y)
                self.message_display_price(str(i.get_price()),x,y)
                x=x+90
            self.open_shapes(objList)

            pygame.display.update()
    def open_shapes(self,obj_to_open):
        exitGame=False
        self.obj_to_open=obj_to_open
        self.screen.blit(self.held_image,(0,0))
        while not exitGame:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()            
            self.redkey=pygame.image.load('../Images/redkey.png')
            self.redkey1=pygame.image.load('../Images/redkey1.png')
            self.bluekey=pygame.image.load('../Images/bluekey.png')
            self.bluekey1=pygame.image.load('../Images/bluekey1.png')
            self.greenkey=pygame.image.load('../Images/greenkey.png')
            self.greenkey1=pygame.image.load('../Images/greenkey1.png')
                            
            m=30
            n=480
            for i in self.opal_list:
                i.print_at_coord(self.screen,m,n)
                m=m+55
            m=30
            n=530
            for i in self.safir_list:
                i.print_at_coord(self.screen,m,n)
                m=m+55
            m=30
            n=580
            
            for i in self.diamond_list:
                i.print_at_coord(self.screen,m,n )
                m=m+55

            i=30
            j=390
            for x in self.green_keys:
                self.key_buttons(i,j,self.greenkey,self.greenkey1,'green')
                i=i+90
            for x in self.red_keys:
                self.key_buttons(i,j,self.redkey,self.redkey1,'red')
                i=i+90
            for x in self.blue_keys:
                self.key_buttons(i,j,self.bluekey,self.bluekey1,'blue')
                i=i+90
                
            x,y= self.keep_coord[0]
            for i in self.obj_to_open:
                i.print_obj_sort(x,y)
                self.message_display_price(str(i.get_price()),x,y)
                x=x+90
            if self.green_keys==[] and self.blue_keys==[] and self.red_keys==[]:
                qT=pygame.image.load('../Images/qT.png')
                qT1=pygame.image.load('../Images/qT1.png')
                self.button((self.display_width/2)-100,(self.display_height/2)+50,qT1,qT,"quit")
            
            pygame.display.update()
    def key_buttons(self,x,y,img,img1,colour):
        colourkey=colour
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
##        print('green keys= '+str(self.green_keys))
##        print('red keys= '+str(self.red_keys))
##        print('blue keys= '+str(self.blue_keys))
        if x+57>=mouse[0]>=x and y+50>=mouse[1]>y:
            self.screen.blit(img1,(x,y))
            if click[0]and colourkey=='green':
                self.green_keys.remove(self.green_keys[len(self.green_keys)-1])
                self.move_key(x,y,'green')
            elif click[0]and colourkey=='red':
                self.red_keys.remove(self.red_keys[len(self.red_keys)-1])
                self.move_key(x,y,'red')
            elif click[0]and colourkey=='blue':
                self.blue_keys.remove(self.blue_keys[len(self.blue_keys)-1])
                self.move_key(x,y,'blue')
        else:
            self.screen.blit(img,(x,y))
        
    def move_key(self,x1,y1,colour):

        
        colourkey=colour
        lead_x=x1
        lead_y=y1
        x_avoid=x1
        prev_x=x1
        prev_y=y1
        occupied_x=[]
        occupied_y=[]
        
        exitGame=False        
        while not exitGame:
            self.screen.blit(self.held_image,(0,0))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        if lead_x>90  :
                            prev_x=lead_x
                            prev_y=lead_y
                            lead_x=lead_x-90
                    if event.key==pygame.K_RIGHT:
                        if lead_x<self.display_width-100  :
                            prev_x=lead_x
                            prev_y=lead_y
                            lead_x=lead_x+90
                    if event.key==pygame.K_UP:
                        if lead_y>90  :
                            prev_x=lead_x
                            prev_y=lead_y
                            lead_y=lead_y-90
                    if event.key==pygame.K_DOWN:
                        if lead_y<self.display_height-160 :
                            prev_x=lead_x
                            prev_y=lead_y
                            lead_y=lead_y+90
                              
        
            q=30
            w=390
            occupied_y.append(w)
##            print('green keys= '+str(self.green_keys))
##            print('red keys= '+str(self.red_keys))
##            print('blue keys= '+str(self.blue_keys))
            if q==x_avoid:
                q=q+90              
            for x in self.green_keys:
                if q==x_avoid:
                    q=q+90 
                self.screen.blit(self.greenkey,(q,w))
                occupied_x.append(q)
                q=q+90
            
            for x in self.red_keys:
                if q==x_avoid:
                    q=q+90 
                self.screen.blit(self.redkey,(q,w))
                occupied_x.append(q)
                q=q+90
                
            for x in self.blue_keys:
                if q==x_avoid:
                    q=q+90 
                self.screen.blit(self.bluekey,(q,w))
                occupied_x.append(q)
                q=q+90
                
            x,y= self.keep_coord[0]

            if (lead_x in occupied_x)and (lead_y in occupied_y):
                lead_x=prev_x
                lead_y=prev_y
                
            occupied_x=[]
            occupied_y=[]
            change=0
            for i in self.obj_to_open:
                i.print_obj_sort(x,y)
                if (lead_x == x )and(lead_y == y)and colourkey==i.get_strColour():
                    c=i.get_colour()
                    z=i
                    change=1
                    self.obj_to_open.remove(i)
                self.message_display_price(str(i.get_price()),x,y)
                x=x+90
           
            if change==1:
                
                nr=z.get_price()
                if c==self.green and colourkey=='green':
                    while nr>0:
                        t=Treasure('opal')
                        self.opal_list.append(t)
                        nr=nr-1
                if c==self.red  and colourkey=='red':
                    while nr>0:
                        t=Treasure('safir')
                        self.safir_list.append(t)
                        nr=nr-1
                if c==self.blue  and colourkey=='blue':
                    while nr>0:
                        t=Treasure('diamond')
                        self.diamond_list.append(t)
                        nr=nr-1
                
                                  
                self.open_shapes(self.obj_to_open)
            
            if colourkey=='green':
                self.screen.blit(self.greenkey,(lead_x,lead_y))
            if colourkey=='red':
                self.screen.blit(self.redkey,(lead_x,lead_y))
            if colourkey=='blue':
                self.screen.blit(self.bluekey,(lead_x,lead_y))

            
            pygame.display.update()
            
    def end_search(self):
        exitGame=False
        self.screen.blit(self.held_image,(0,0))
        while not exitGame:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            sort=pygame.image.load('../Images/sort_img.png')
            sort1=pygame.image.load('../Images/sort1_img.png')
            self.button((self.display_width/2)-100,(self.display_height/2)-50,sort1,sort,"sort")
            pygame.display.update()  
    def game(self,x,y):
        self.sort_list=[]
        exitGame=False
        self.t1=time.time()
        while not exitGame:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            self.start_point_x=x+30
            self.start_point_y=y+15
            self.ship=pygame.image.load('../Images/ship.png')
            self.random_object_generator(10)
            self.good_list=self.obj_to_found(self.objects)            
            self.start_pos=(self.start_point_x,self.start_point_y)
            #call the search function
            self.breakloop=0
            while self.good_list:
                current_to_be_found=self.find_best_obj((self.start_pos))
                self.search((self.start_pos),(current_to_be_found),self.Glist)
                if self.breakloop==1:
                    break
                self.start_pos=current_to_be_found
        
            exitGame=True
        self.end_search()
    def create_grid(self):
        nri=0
        nrj=0
        for i in range(30,self.display_width-30,30):
            nri=nri+1
            for j in range(30,self.display_height-30,30):
                self.Glist[(i,j)]=True
                nrj=nrj+1

        return(self.Glist)
    def occupy_grid(self,x,y):
        self.Glist[(x,y)]=False
        return (self.Glist)
    def de_occupy_grid(self,x,y):
        self.Glist[(x,y)]=True
        return (self.Glist)
    def random_object_generator(self,nr):
        self.objects=[]
        self.obstacles=[]
        self.Glist=self.create_grid()
        rand_obst=randint(2,3)
        while rand_obst!=0:
        
            rand_dimension=randint(45,60)

            i=randint(0,len(self.Glist)-1)

            pos=list(self.Glist)[i]

            rand_x=pos[0]
            rand_y=pos[1]
            ok=1
            #checking if the position is available
            for x in range(rand_x-60,rand_x+61,30):
                for y in range(rand_y-60,rand_y+61,30):
                    if  (x,y)in self.Glist and self.Glist[(x,y)]==True:
                        pass
                    else:
                        ok=0
            if ok:
                for x in range(rand_x-60,rand_x+61,30):
                    for y in range(rand_y-60,rand_y+61,30):
                        self.Glist=self.occupy_grid(x,y)
                ob4=Circle(rand_x,rand_y,rand_dimension,self.screen,self.yellow)
                rand_obst=rand_obst-1
                self.obstacles.append(ob4)

                
        self.green_keys=[]
        self.red_keys=[]
        self.blue_keys=[]

        while nr>0:
                
                
                rand_shape=randint(1,3)
                rand_colour=randint(1,3)
                colours={1:self.red,2:self.blue,3:self.green}
                
                condition_for_red=0
                condition_for_blue=0
                condition_for_green=0
                condition_exist=0
                if rand_colour==1:#red
                    price=randint(4,6)
                    x=randint(1,100)
                    if x>60:
                        condition_for_red=1
                elif rand_colour==2:#blue
                    price=randint(7,9)
                    x=randint(1,100)
                    if x>70:
                        condition_for_blue=1
                elif rand_colour==3:#green
                    price=randint(1,3)
                    x=randint(1,100)
                    if x>50:
                        condition_for_green=1
                    
                j=randint(0,len(self.Glist)-1)
                pos=list(self.Glist)[j]
                rand_x=pos[0]
                rand_y=pos[1]
                if rand_shape==1:
                    ok=1
                    for x in range(rand_x,rand_x+31,30):
                        for y in range(rand_y,rand_y+31,30):
                            if  (x,y)in self.Glist and self.Glist[(x,y)]==True:
                                pass
                            else:
                                ok=0
                    if ok:
                        for x in range(rand_x,rand_x+31,30):
                            for y in range(rand_y,rand_y+31,30):
                                self.Glist=self.occupy_grid(x,y)
                        ob1=Square(rand_x,rand_y,price,45,self.screen,colours[rand_colour])
                        condition_exist=1
                        
                        self.objects.append(ob1)
                        nr=nr-1
                elif rand_shape==2:
                    ok=1
                    for x in range(rand_x,rand_x+31,30):
                        for y in range(rand_y,rand_y+31,30):
                            
                            if  (x,y)in self.Glist and self.Glist[(x,y)]==True:
                                pass
                            else:
                                ok=0
                                
                    if ok:
                        for x in range(rand_x,rand_x+31,30):
                            for y in range(rand_y,rand_y+31,30):
                                self.Glist=self.occupy_grid(x,y)
                        ob2=Triangle(rand_x,rand_y,price,45,self.screen,colours[rand_colour])
                        condition_exist=1

                        self.objects.append(ob2)
                        nr=nr-1
                elif rand_shape==3:
                    ok=1
                    for x in range(rand_x,rand_x+31,30):
                        for y in range(rand_y,rand_y+31,30):
                            if  (x,y)in self.Glist and self.Glist[(x,y)]==True:
                                pass
                            else:
                                ok=0
                    if ok:
                        for x in range(rand_x,rand_x+31,30):
                            for y in range(rand_y,rand_y+31,30):
                                self.Glist=self.occupy_grid(x,y)
                        ob3=Rectangle(rand_x,rand_y,price,45,self.screen,colours[rand_colour])
                        condition_exist=1

                        self.objects.append(ob3)
                        nr=nr-1
                if condition_exist and condition_for_red:
                    self.red_keys.append('key')
                if condition_exist and condition_for_blue:
                    self.blue_keys.append('key')
                if condition_exist and condition_for_green:
                    self.green_keys.append('key')
    
        pygame.display.update()


    def button(self,x,y,img1,img,action=None):
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if x+150>=mouse[0]>=x and y+80>=mouse[1]>y:
            self.screen.blit(img1,(x,y))
            if click[0]==1 and action!=None:
                if action=="play":
                    root=tk.Tk()
                    g=Gui(root)
                    root.mainloop()
                    
                elif action=="quit":
                    pygame.quit()
                    quit()
                elif action=="spawn":
                    
                    self.game(x,y)
                elif action=='sort':
                    self.bubble(self.sort_list,self.sort_type,self.sort_order)
                    
                
        else:
            self.screen.blit(img,(x,y))

    def text_objects(self,text,font):
        textSurface=font.render(text,True,self.white)
        return textSurface,textSurface.get_rect()
    def message_display(self,text):
        pygame.font.init()
        self.largeText=pygame.font.Font('freesansbold.ttf',40)
        TextSurf,TextRect=self.text_objects(text,self.largeText)
        TextRect.center=((self.display_width/2),((self.display_height/2)-100))
        self.screen.blit(TextSurf,TextRect)
        pygame.display.update()
    def message_display1(self,text):
        pygame.font.init()
        self.largeText=pygame.font.Font('freesansbold.ttf',30)
        TextSurf,TextRect=self.text_objects(text,self.largeText)
        TextRect.center=((self.display_width/2),(self.display_height/2))
        self.screen.blit(TextSurf,TextRect)
        pygame.display.update()
    def message_display_price(self,text,x,y):
        pygame.font.init()
        self.largeText=pygame.font.Font('freesansbold.ttf',20)
        TextSurf,TextRect=self.text_objects(text,self.largeText)
        TextRect.center=((x+15),(y+15))
        self.screen.blit(TextSurf,TextRect)
        
    def spawn_ship(self):
        
            exitW=False
            while not exitW:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        quit()
                self.background=pygame.image.load('../Images/space.jpg')
                self.held_image=self.background
                self.screen.blit(self.background,(0,0))
                spawn=pygame.image.load('../Images/spawn.png')
                spawn1=pygame.image.load('../Images/spawn1.png')
                self.button(330,135,spawn1,spawn,"spawn")
                self.button(810,135,spawn1,spawn,"spawn")
                self.button(330,405,spawn1,spawn,"spawn")
                self.button(810,405,spawn1,spawn,"spawn")
                pygame.display.update()

class Gui():
    def __init__(self, root):
        self.root = root
        root.title('Space Hunter')
        root.wm_title("Space Hunter")

        self.mpg=MyPyGame()
        
        title_frame=Frame(self.root)
        textbox_frame=Frame(self.root)
        time_frame=Frame(self.root)
        time_frame1=Frame(self.root)
        checkboxframe=Frame(self.root)
        optionframe=Frame(self.root)
        startframe=Frame(self.root)

        checkbox_frame1=Frame(checkboxframe)
        checkbox_frame2=Frame(checkboxframe)
        option_frame1=Frame(optionframe)
        option_frame2=Frame(optionframe)

        
        title_frame.pack(side=TOP)
        textbox_frame.pack(side=TOP)
        time_frame.pack(side=TOP)
        time_frame1.pack(side=TOP)
        checkboxframe.pack(side=TOP)
        optionframe.pack(side=TOP)
        startframe.pack(side=TOP)
        
        checkbox_frame1.pack(side=LEFT)
        checkbox_frame2.pack(side=LEFT)
        option_frame1.pack(side=LEFT)
        option_frame2.pack(side=LEFT)

        
        L1 = Label(title_frame, text="Choose what to search for and how much time is it given ")
        L1.pack(side=TOP)
        L2 = Label(textbox_frame,text='Time')
        L2.pack(side=LEFT)
        L3 = Label(time_frame,text='Minutes:')
        L3.pack(side=LEFT)
        L4 = Label(time_frame1,text='Seconds:')
        L4.pack(side=LEFT)

        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.CheckVar3 = IntVar()
        self.CheckVar4 = IntVar()
        self.CheckVar5 = IntVar()
        self.CheckVar6 = IntVar()

        L5=Label(checkbox_frame1,text='Shapes to be found:')
        L5.pack(side=TOP)

        C1 = Checkbutton(checkbox_frame1, text = "Triangles", variable = self.CheckVar1, onvalue = 1, offvalue = 0, height=3,  width = 20)
        C2 = Checkbutton(checkbox_frame1, text = "Squares", variable = self.CheckVar2, onvalue = 1, offvalue = 0, height=3,  width = 20)
        C3 = Checkbutton(checkbox_frame1, text = "Rectangles", variable = self.CheckVar3, onvalue = 1, offvalue = 0, height=3,  width = 20)

        # Start button.
        buttonStart = Button(startframe, text="START", command=lambda a=self.mpg: self.getTextBoxInput(), background = "green", width=20)
        buttonStart.pack(side=LEFT)

        # Set up shape select drop down menu.
        labelShapeSelect = Label(option_frame1, text="Sort by: ")
        labelShapeSelect.pack(side=TOP)

        self.shapeVar = StringVar()
        self.shapeVar.set("Shape")
        shapeSelect = OptionMenu(option_frame1, self.shapeVar, "Shape", "Colour")
        shapeSelect.config(width=35)
        shapeSelect.pack(side = TOP)

        labelSortAorD = Label(option_frame2, text="Sort in order of: ")
        labelSortAorD.pack()

        self.sortVar = StringVar()
        self.sortVar.set("Ascending")
        sortAorD = OptionMenu(option_frame2, self.sortVar, "Ascending", "Descending")
        sortAorD.config(width=35)
        sortAorD.pack(side = TOP)

       
        
        L6=Label(checkbox_frame2,text='Colours to be found:')
        L6.pack(side=TOP)
        
        C4 = Checkbutton(checkbox_frame2, text = "Blue", variable = self.CheckVar4, onvalue = 1, offvalue = 0, height=3,  width = 20)
        C5 = Checkbutton(checkbox_frame2, text = "Red", variable = self.CheckVar5, onvalue = 1, offvalue = 0, height=3,  width = 20)
        C6 = Checkbutton(checkbox_frame2, text = "Green", variable = self.CheckVar6, onvalue = 1, offvalue = 0, height=3,  width = 20)
        
        C1.pack(side=TOP)
        C2.pack(side=TOP)
        C3.pack(side=TOP)
        C4.pack(side=TOP)
        C5.pack(side=TOP)
        C6.pack(side=TOP)
        
        self.minutes=Entry(time_frame,bd=3)
        self.seconds=Entry(time_frame1,bd=3)
        self.minutes.pack(side=LEFT,expand=True,fill=BOTH)
        self.seconds.pack(side=LEFT,expand=True,fill=BOTH)
       
    def getTextBoxInput(self):
        '''Takes all inputs from input window. Calls CheckInput and passes all inputs.'''
        inputs=self.minutes.get()
        inputs2=self.seconds.get()
        TriInput=self.CheckVar1.get()
        SquareInput=self.CheckVar2.get()
        RectInput=self.CheckVar3.get()
        BlueInput=self.CheckVar4.get()
        RedInput=self.CheckVar5.get()
        GreenInput=self.CheckVar6.get()
        SortInput=self.sortVar.get()
        ShapeInput=self.shapeVar.get()
        if inputs == "":
            inputs = 0
        if inputs2 == "":
            inputs2 = 0
        self.CheckInput(inputs,inputs2,TriInput,SquareInput,RectInput,BlueInput,RedInput,GreenInput,SortInput,ShapeInput)
    def CheckInput(self,minutes,sec,TriInput,SquareInput,RectInput,BlueInput,RedInput,GreenInput,SortInput,ShapeInput ):
        '''Takes 11 inputs, converts the time inputs into int,defines global variable with
        all input values within it. Makes sure that it is a maximum time value of 6 minutes.
        Calls CheckCheckBox function if valid time inputs, else prints to console.'''
        try:
            IntMins=float(minutes)
            IntSec=float(sec)
            global user_input
            user_input= (IntMins,IntSec,TriInput,SquareInput,RectInput,BlueInput,RedInput,GreenInput,SortInput,ShapeInput)

            if IntMins<0:
                messagebox.showerror('Error','Must be positive')

            elif IntMins >6:
                messagebox.showerror('Error','Searching seconds maximum is 6 minutes')

            else:
                
                if IntMins == 6:
                    if IntSec > 0 or IntSec < 0:
                            messagebox.showerror('Error','Searching seconds has to be be equal to 0')
                    else:
                        self.CheckCheckBox()

                elif IntSec<0 or IntSec>60:
                    messagebox.showerror('Error','Seconds must be between 0-60')
                else:
                    self.CheckCheckBox()

        except ValueError:
            messagebox.showerror('Error','Wrong Input')
    
    def CheckCheckBox(self):
        '''Loops through all the checkbox values, if none of them are ticked then tells user to tick one.
           Otherwise launches the game.'''
        i = 2
        BoxesTorF = False
        while BoxesTorF == False and i <=7:
            if user_input[i] == 1:
                BoxesTorF = True

            i = i+1

        if BoxesTorF == False:
            messagebox.showerror('Error','Please tick at least one box ')
            
        else:
            self.root.withdraw()
            self.mpg.spawn_ship()
             

def main():
    pgame=MyPyGame()
    pgame.runIntroWindow()
if __name__=='__main__':
    sys.exit(main())
