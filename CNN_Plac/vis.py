import pygame
import numpy as np


CELL_SIZE = 100  # px

imageScaler = np.array((CELL_SIZE, CELL_SIZE))
blankImage = pygame.transform.scale(
    pygame.image.load("./img/blank.png"), imageScaler
)
pondImage = pygame.transform.scale(
    pygame.image.load("./img/pond.png"), imageScaler
)
castleImage = pygame.transform.scale(
    pygame.image.load("./img/castle.png"), imageScaler
)
workerAImage = pygame.transform.scale(
    pygame.image.load("./img/worker_A.png"), imageScaler
)
workerBImage = pygame.transform.scale(
    pygame.image.load("./img/worker_B.png"), imageScaler
)
wallAImage = pygame.transform.scale(
    pygame.image.load("./img/rampart_A.png"), imageScaler
)
wallBImage = pygame.transform.scale(
    pygame.image.load("./img/rampart_B.png"), imageScaler
)
areaAImage = pygame.transform.scale(
    pygame.image.load("./img/area_A.png"), imageScaler
)
areaBImage = pygame.transform.scale(
    pygame.image.load("./img/area_B.png"), imageScaler
)
areaABImage = pygame.transform.scale(
    pygame.image.load("./img/area_AB.png"), imageScaler
)

def save(WS, fileName):
    pygame.image.save(WS, fileName)

def drawGrids(W, H, WS):
    for i in range(1, W):
        pygame.draw.line(
            WS,
            (0, 0, 0),
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, CELL_SIZE * H),
            1,
        )
    for i in range(1, H):
        pygame.draw.line(
            WS,
            (0, 0, 0),
            (0, i * CELL_SIZE),
            (CELL_SIZE * W, i * CELL_SIZE),
            1,
        )


def placeImage(WS, img, i, j):
    placement = (j * CELL_SIZE, i * CELL_SIZE)
    img = pygame.transform.scale(img, imageScaler)
    WS.blit(img, placement)

def captureField_struct(W, H, WS, field, field2, fileName):
    for i in range(H):
        for j in range(W):
            placeImage(WS, blankImage, i, j)

            if field[i][j] == 0:
                pass
            if field[i][j] == 1:
                placeImage(WS, pondImage, i, j)
            if field[i][j] == 2:
                placeImage(WS, castleImage, i, j)

            if field2[i][j] == 0:
                pass
            if field2[i][j] > 0:
                placeImage(WS, workerAImage, i, j)
            if field2[i][j] < 0:
                placeImage(WS, workerBImage, i, j)
    drawGrids(W, H, WS)

    save(WS, fileName)
    # pygame.image.save(WS, fileName + ".png")

def captureField_area(W, H, WS, field0, field, field2, fileName):
    for i in range(H):
        for j in range(W):
            placeImage(WS, blankImage, i, j)
            # print(field2[i][j], end=" ")

            if field[i][j] == 0:
                pass
            if field[i][j] == 1:
                placeImage(WS, wallAImage, i, j)
            if field[i][j] == 2:
                placeImage(WS, wallBImage, i, j)

            if field2[i][j] == 0:
                pass
            if field2[i][j] == 1:
                placeImage(WS, areaAImage, i, j)
            if field2[i][j] == 2:
                placeImage(WS, areaBImage, i, j)
            if field2[i][j] == 3:
                placeImage(WS, areaABImage, i, j)

            if field0[i][j] == 0:
                pass
            if field0[i][j] > 0:
                placeImage(WS, workerAImage, i, j)
            if field0[i][j] < 0:
                placeImage(WS, workerBImage, i, j)
        # print()
    drawGrids(W, H, WS)

    save(WS, fileName)
    # pygame.image.save(WS, fileName + ".png")

def captureField_all(W, H, WS, field, field2, field3, fileName):
    for i in range(H):
        for j in range(W):
            placeImage(WS, blankImage, i, j)
            # print(field[i][j], end=" ")

            if field3[i][j] == 0:
                pass
            if field3[i][j] == 1:
                placeImage(WS, wallAImage, i, j)
            if field3[i][j] == 2:
                placeImage(WS, wallBImage, i, j)

            # if field4[i][j] == 0:
            #     pass
            # if field4[i][j] == 1:
            #     placeImage(WS, areaAImage, i, j)
            # if field4[i][j] == 2:
            #     placeImage(WS, areaBImage, i, j)
            # if field4[i][j] == 3:
            #     placeImage(WS, areaABImage, i, j)

            if field[i][j] == 0:
                pass
            if field[i][j] == 1:
                placeImage(WS, pondImage, i, j)
            if field[i][j] == 2:
                placeImage(WS, castleImage, i, j)

            if field2[i][j] == 0:
                pass
            if field2[i][j] > 0:
                placeImage(WS, workerAImage, i, j)
            if field2[i][j] < 0:
                placeImage(WS, workerBImage, i, j)
        # print()
    drawGrids(W, H, WS)
    save(WS, fileName)
    # pygame.image.save(WS, fileName + ".png")

def main():
    # print("Image_Generating...", end = "     ")
    fieldPath = "./Field_Data/Field_Structures.txt"
    fieldPath2 = "./Field_Data/Field_Masons.txt"
    f = open(fieldPath,"r")
    field = eval(f.read())
    f2 = open(fieldPath2,"r")
    field2 = eval(f2.read())
    pygame.init()
    W = len(field[0])
    H = len(field)
    WS = pygame.display.set_mode((CELL_SIZE * W, CELL_SIZE * H))
    captureField_struct(W, H, WS, field, field2, 
                        fileName="./Field_Data/visualized_struct_masons.png")

    fieldPath3 = "./Field_Data/Field_Walls.txt"
    fieldPath4 = "./Field_Data/Field_Territories.txt"
    f3 = open(fieldPath3,"r")
    field3 = eval(f3.read())
    f4 = open(fieldPath4,"r")
    field4 = eval(f4.read())
    pygame.init()
    WS = pygame.display.set_mode((CELL_SIZE * W, CELL_SIZE * H))
    captureField_area(W, H, WS, field2, field3, field4, 
                      fileName="./Field_Data/visualized_wall_territories.png")
    pygame.init()
    WS = pygame.display.set_mode((CELL_SIZE * W, CELL_SIZE * H))
    captureField_all(W, H, WS, field, field2, field3, 
                      fileName="./Field_Data/visualized_all.png")
    # print("Finished", end = "")
# main()
