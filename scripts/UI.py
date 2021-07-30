import pygame, sys, math
import random as rd
from pygame.locals import *

pygame.init()

UIfont = pygame.font.Font('assets/font/menu.ttf',30)

class cubeTrans():
    def __init__(self,disp_1,disp_2,dispSize):
        self.poses = []
        self.cellSize = 100
        xCells = dispSize[0]//8
        yCells = dispSize[1]//8

        self.disp1 = disp_1
        self.disp2 = disp_2
        
        self.dispSize = dispSize

        self.transEvent = {'start':True,'end':False}

        for ycell in range(8):
            for xcell in range(8):
                self.poses.append([xcell*xCells,ycell*yCells])

        self.transEnd = False

        self.rects = []

    def main(self,disp):
        if self.transEnd == False:
            if self.transEvent['start'] == True:
                disp.blit(self.disp1,(0,0))

                indexPos = rd.randint(0,len(self.poses)-1)
                self.rects.append(pygame.Rect(self.poses[indexPos][0],self.poses[indexPos][1],self.cellSize+1,self.cellSize+1))
                self.poses.pop(indexPos)
            


                if len(self.poses) < 1:
                    self.transEvent = {'start':False,'end':True}
            elif self.transEvent['end'] == True:
                disp.blit(self.disp2,(0,0))
                delIndex = rd.randint(0,len(self.rects)-1)
                self.rects.pop(delIndex)
                if len(self.rects) < 1:
                    self.transEnd = True
                    
            for rect in self.rects:
                pygame.draw.rect(disp,(105,105,105),rect)
        else:
            disp.blit(self.disp2,(0,0))


class button():
    def __init__(self,pos,image,prsImg):
        self.pos = pos

        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)

    def main(self,display,mr):
        if self.rect.colliderect(mr):
            pass

class mainMenu():
    def __init__(self,dispSize):
        self.disp = pygame.Surface(dispSize)
        self.disp.fill((0,0,0))

        self.dispSize = dispSize

        self.colorIndex = 0
        self.colors = [[254,0,0],[254,128,0],[254,254,0],[0,254,0],[0,200,200],[154,0,254],[198,0,222]]

        self.transition = False
        
        self.logoPos = [0,200]
        self.logo = pygame.image.load('assets/images/logo_big.png')
        self.rect = self.logo.get_rect(topleft=self.logoPos)

        self.press_space = UIfont.render('press SPACE to play',False,(255,255,255))
        self.press_spaceSize = self.press_space.get_size()

        
        self.press_z = UIfont.render('press Z to go to settings',False,(255,255,255))
        self.press_zSize = self.press_z.get_size()
        
    def main(self,display):
        #check

        #draw
        cCount = 0
        for col in self.colors[self.colorIndex]:
            if col == 0:
                cCount += 1

        if cCount == 3:#self.colors[self.colorIndex][self.colors[self.colorIndex].index(col)] = col
            self.colorIndex += 1
            
            if self.colorIndex > len(self.colors)-1:
                self.colorIndex = 0
                self.colors = [[254,0,0],[254,128,0],[254,254,0],[0,254,0],[	0,200,200],[154,0,254],[198,0,222]]
                
        for col in self.colors[self.colorIndex]:
            if col > 0:
                self.colors[self.colorIndex][self.colors[self.colorIndex].index(col)] = col - 2
                
                
                
        pygame.draw.rect(self.disp,self.colors[self.colorIndex],self.rect)
        self.disp.blit(self.logo,self.logoPos)

        self.disp.blit(self.press_space,(self.dispSize[0]//2-self.press_spaceSize[0]//2,600))#self.press_zSize
        self.disp.blit(self.press_z,(self.dispSize[0]//2-self.press_zSize[0]//2,650))

        display.blit(self.disp,(0,0))
        
