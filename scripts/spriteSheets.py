import pygame

def cutSurf(surface,pos,cutSize):
    cuttedSurf = pygame.Surface(cutSize)
    cuttedSurf.blit(surface,pos)

    return cuttedSurf

def spriteSheet(surface,cellSize):
    surfSize = surface.get_size()
    cellsx = surfSize[0]//cellSize[0]
    cellsy = surfSize[1]//cellSize[1]
    
    cellSurfs = []
    

    
    for celly in range(cellsy):
        for cellx in range(cellsx):
            cellSurf = pygame.Surface((cellSize[0],cellSize[1]))
            cellSurf.blit(surface,(-cellx*cellSize[0],-celly*cellSize[1]))

            cellSurfs.append(cellSurf)

    return cellSurfs
