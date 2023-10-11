import pygame
from pygame.locals import *

#const ======================================================
H = 11
screen_width = 1300
screen_height = 1000
image_size = (900,900)
dots = image_size[0] / H

#initial =====================================================
pygame.init()
pygame.display.set_caption("Transparent Button Example")
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont("Serif", 50)


button_clear = (1000, 50,400,70)
button_fp  =   ( 900,130,400,70)
button_fp0 =   (1000,210,400,70)
button_fp1 =   (1000,290,400,70)
button_fp2 =   (1000,370,400,70)
button_ac  =   ( 900,450,400,70)
button_ac1 =   (1000,530,400,70)
button_ac2 =   (1000,610,400,70)
button_ac3 =   (1000,690,400,70)

rect_clear = pygame.Rect(*button_clear)
txt_clear = font.render("Clear", True, (0, 0, 0))

txt_fp = font.render("Fill-Pattern", True, (0, 0, 0))

rect_fp0 = pygame.Rect(*button_fp0)
txt_fp0 = font.render("Separate", True, (0, 0, 0))

rect_fp1 = pygame.Rect(*button_fp1)
txt_fp1 = font.render("All-Fill", True, (0, 0, 0))

rect_fp2 = pygame.Rect(*button_fp2)
txt_fp2 = font.render("Checked-Fill", True, (0, 0, 0))

txt_ac = font.render("Actions", True, (0, 0, 0))

rect_ac1 = pygame.Rect(*button_ac1)
txt_ac1 = font.render("Move", True, (0, 0, 0))

rect_ac2 = pygame.Rect(*button_ac2)
txt_ac2 = font.render("Build", True, (0, 0, 0))

rect_ac3 = pygame.Rect(*button_ac3)
txt_ac3 = font.render("Break", True, (0, 0, 0))

#func ========================================================
def click_field(p):
    return 0 <= p[0] < 900 and 0 <= p[1] < 900

def click_clear(p):
    return button_clear[0] <= p[0] < button_clear[0] + button_clear[2] and button_clear[1] <= p[1] < button_clear[1] + button_clear[3]

def click_fp0(p):
    return button_fp0[0] <= p[0] < button_fp0[0] + button_fp0[2] and button_fp0[1] <= p[1] < button_fp0[1] + button_fp0[3]

def click_fp1(p):
    return button_fp1[0] <= p[0] < button_fp1[0] + button_fp1[2] and button_fp1[1] <= p[1] < button_fp1[1] + button_fp1[3]

def click_fp2(p):
    return button_fp2[0] <= p[0] < button_fp2[0] + button_fp2[2] and button_fp2[1] <= p[1] < button_fp2[1] + button_fp2[3]

def click_ac1(p):
    return button_ac1[0] <= p[0] < button_ac1[0] + button_ac1[2] and button_ac1[1] <= p[1] < button_ac1[1] + button_ac1[3]

def click_ac2(p):
    return button_ac2[0] <= p[0] < button_ac2[0] + button_ac2[2] and button_ac2[1] <= p[1] < button_ac2[1] + button_ac2[3]

def click_ac3(p):
    return button_ac3[0] <= p[0] < button_ac3[0] + button_ac3[2] and button_ac3[1] <= p[1] < button_ac3[1] + button_ac3[3]

Select_image = pygame.transform.scale(pygame.image.load(r"img\select.png").convert_alpha(), (dots, dots))
choice_image = pygame.transform.scale(pygame.image.load(r"img\choice.png").convert_alpha(), (60, 60))

past_mouse_position = (-1,-1)
Selected_Rect = []
running = True

fill_pattern = 1    # 0 : Non-Fill 1 : All-Fill 2 : check-Fill
Actions_pattern = 1 # 1 ; Move 2 : Build 3 : Break

Selecting_Rect = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    try:
        Field_image = pygame.transform.scale(pygame.image.load(r"Field_Data\visualized_wall_territories.png.png"), image_size)
    except:
        None
    Field_image.set_alpha(90)
    screen.fill((200, 200, 200))
    screen.blit(Field_image,(0,0))

    pygame.draw.rect(screen, (255, 0, 0), rect_clear)
    screen.blit(txt_clear, (button_clear[0], button_clear[1] + 5))
    
    screen.blit(txt_fp,    (button_fp[0],    button_fp[1] + 5))

    pygame.draw.rect(screen, (255, 0, 0), rect_fp0)
    screen.blit(txt_fp0, (button_fp0[0], button_fp0[1] + 5))
    pygame.draw.rect(screen, (255, 0, 0), rect_fp1)
    screen.blit(txt_fp1, (button_fp1[0], button_fp1[1] + 5))
    pygame.draw.rect(screen, (255, 0, 0), rect_fp2)
    screen.blit(txt_fp2, (button_fp2[0], button_fp2[1] + 5))

    if fill_pattern == 0:
        screen.blit(choice_image, (button_fp0[0] - 60, button_fp0[1] + 5))
    elif fill_pattern == 1:
        screen.blit(choice_image, (button_fp1[0] - 60, button_fp1[1] + 5))
    elif fill_pattern == 2:
        screen.blit(choice_image, (button_fp2[0] - 60, button_fp2[1] + 5))

    screen.blit(txt_ac, (button_ac[0], button_ac[1] + 5))

    pygame.draw.rect(screen, (255, 0, 0), rect_ac1)
    screen.blit(txt_ac1, (button_ac1[0], button_ac1[1] + 5))
    pygame.draw.rect(screen, (255, 0, 0), rect_ac2)
    screen.blit(txt_ac2, (button_ac2[0], button_ac2[1] + 5))
    pygame.draw.rect(screen, (255, 0, 0), rect_ac3)
    screen.blit(txt_ac3, (button_ac3[0], button_ac3[1] + 5))

    if Actions_pattern == 1:
        screen.blit(choice_image, (button_ac1[0] - 60, button_ac1[1] + 5))
    elif Actions_pattern == 2:
        screen.blit(choice_image, (button_ac2[0] - 60, button_ac2[1] + 5))
    elif Actions_pattern == 3:
        screen.blit(choice_image, (button_ac3[0] - 60, button_ac3[1] + 5))

    for Rect_ in Selected_Rect:
        screen.blit(Select_image, (Rect_[0] * dots,Rect_[1] * dots))

    for Rect_ in Selecting_Rect:
        screen.blit(Select_image, (Rect_[0] * dots,Rect_[1] * dots))

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()

        if click_clear(mouse_position):
            Selected_Rect = []
            Selecting_Rect = []
        elif click_fp0(mouse_position):
            fill_pattern = 0
        elif click_fp1(mouse_position):
            fill_pattern = 1
        elif click_fp2(mouse_position):
            fill_pattern = 2
        elif click_ac1(mouse_position):
            Actions_pattern = 1
        elif click_ac2(mouse_position):
            Actions_pattern = 2
        elif click_ac3(mouse_position):
            Actions_pattern = 3
        elif click_field(mouse_position):
            if mouse_position == past_mouse_position:
                None
            else:
                past_mouse_position = mouse_position
                p = (int(mouse_position[0]//dots), int(mouse_position[1]//dots))
                if p in Selecting_Rect:
                    Selecting_Rect.remove(p)
                else:
                    Selecting_Rect.append(p)
                if len(Selecting_Rect) == 2:
                    max_x = max(Selecting_Rect[0][0], Selecting_Rect[1][0])
                    min_x = min(Selecting_Rect[0][0], Selecting_Rect[1][0])
                    max_y = max(Selecting_Rect[0][1], Selecting_Rect[1][1])
                    min_y = min(Selecting_Rect[0][1], Selecting_Rect[1][1])
                    if fill_pattern == 0:
                        for k in Selecting_Rect:
                            if not ((k[0], k[1]) in Selected_Rect):
                                Selected_Rect.append((k[0], k[1]))
                    if fill_pattern == 1:
                        for i in range(min_y, max_y + 1):
                            for j in range(min_x, max_x + 1):
                                if not ((j, i) in Selected_Rect):
                                    Selected_Rect.append((j, i))
                    if fill_pattern == 2:
                        for i in range(min_y, max_y + 1):
                            for j in range(min_x, max_x + 1):
                                if not (((i - Selecting_Rect[0][0]) + (j - Selecting_Rect[0][1])) % 2):
                                    if not ((j, i) in Selected_Rect):
                                        Selected_Rect.append((j, i))
                    Selecting_Rect = []
                # print(mouse_position)
                print(p[0], p[1])
        else:
            None

    pygame.display.flip()

pygame.quit()