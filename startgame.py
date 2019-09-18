import pygame
import os, random, time
import cv2
import transferstyle
dirname = os.path.dirname(__file__)

def createText(x,y):
    font = pygame.font.Font(os.path.join(dirname,'fonts/MinionPro-Regular.ttf'), 70)
    text = font.render('Fast Style Transfer Tool', True, (255,255,255), (155,155,155)) 
    screen.blit(text, (x, y))

def takeImage():
    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:    # frame captured without any errors
        # cv2.namedWindow("cam-test",cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("cam-test",img)
        # cv2.waitKey(0)
        # cv2.destroyWindow("cam-test")
        cv2.imwrite("cv2Captures/filename.jpg",img) #save image

class Opts:
  def __init__(self, checkpoint_dir, in_path, out_path):
    self.checkpoint_dir = checkpoint_dir
    self.in_path = in_path
    self.out_path = out_path

pygame.init()
print('Starting Pygame')
GameOn = True
screen = pygame.display.set_mode(size=(1080,920))
print('Filling Screen')
screen.fill((155,155,155))
createText(175,50)
displayed = False
while GameOn:
    pygame.display.flip()
    if displayed == False:
        takeImage()
        faceimg = pygame.image.load(os.path.join(dirname,"cv2Captures/filename.jpg"))
        screen.blit(faceimg, (225,150))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOn = False
        if event.type == pygame.KEYDOWN:
            print('This key number is: ', event.key)
            # Escape Key
            if event.key == 27:
                GameOn = False
            # P Key
            if event.key == 112:
                displayed = True
                takeImage()
                faceimg = pygame.image.load(os.path.join(dirname,"cv2Captures/filename.jpg"))
                screen.blit(faceimg, (225,150))
                opts = Opts("trained/roda1", "cv2Captures/filename.jpg", "cv2Translations")
                transferstyle.main(opts)
                print('It ends')
                faceimg2 = pygame.image.load(os.path.join(dirname,"cv2Translations/filename.jpg"))
                print(faceimg2)
                screen.blit(faceimg2, (225,150))
pygame.display.quit()