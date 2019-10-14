import pygame
import os, random, time, glob
import cv2
import transferstyle
import PIL
from PIL import Image
dirname = os.path.dirname(__file__)

def createText(x,y):
    font = pygame.font.Font(os.path.join(dirname,'fonts/MinionPro-Regular.ttf'), 70)
    text = font.render('Fast Style Transfer Tool', True, (255,255,255), (155,155,155)) 
    screen.blit(text, (x, y))

def renderStyleThumbnails(my_styles):
    thumbnails = my_styles
    for index, thumbnail in enumerate(thumbnails):
        thumbnail_style = pygame.image.load(os.path.join(dirname,"examples/style/thumbs/" + thumbnail + ".jpg"))
        IMAGE_SMALL = pygame.transform.scale(thumbnail_style, (150, 300))
        the_thumb = screen.blit(IMAGE_SMALL, (200*index+25,600))
        thumbnail_images.append(the_thumb)

def takeImage(scalar):
    s, img = cam.read()
    if s:    # frame captured without any errors
        # print('Original Dimensions : ',img.shape) 
        scale_percent = scalar # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # print('Resized Dimensions : ', resized.shape)

        # cv2.namedWindow("cam-test",cv2.WINDOW_AUTOSIZE)
        # cv2.imshow("cam-test",img)
        # cv2.waitKey(0)
        # cv2.destroyWindow("cam-test")
        cv2.imwrite("cv2Captures/currentPhoto.jpg",resized) #save image

def doit():
    transferstyle.main(opts)
    createdImages.append("createdImage" + str(len(createdImages)))
    os.rename("cv2Translations/currentPhoto.jpg", "cv2Translations/" + next(reversed(createdImages)) + ".jpg")
    faceimg2 = pygame.image.load(os.path.join(dirname,"cv2Translations/" + next(reversed(createdImages)) + ".jpg"))
    screen.blit(faceimg2, (625,150))
    # input_scalar = input_scalar+10

class Opts:
  def __init__(self, checkpoint_dir, in_path, out_path):
    self.checkpoint_dir = checkpoint_dir
    self.in_path = in_path
    self.out_path = out_path

pygame.init()
GameOn = True
thumbnail_images = []
screen = pygame.display.set_mode(size=(1200,920))
screen.fill((155,155,155))
createText(175,50)
styles = ["la_muse", "rain_princess", "scream", "udnie", "wave", "wreck"]
renderStyleThumbnails(styles)
displayed = False
# initialize the camera
cam = cv2.VideoCapture(0)   # 0 -> index of camera
if not cam.isOpened():
    raise Exception("Could not open video device")
# Clear old images
filelist1 = glob.glob(os.path.join(dirname, "cv2Translations/*.jpg"))
filelist2 = glob.glob(os.path.join(dirname, "cv2Captures/*.jpg"))
for f in filelist1:
    os.remove(f)
for f in filelist2:
    os.remove(f)
# Set camera resolution, smaller resolution is faster and may yeild different kinds of results from the GAN generator
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
input_scalar = 70
createdImages = []
currentStyle = styles[0]
while GameOn:
    pygame.display.flip()
    # if input_scalar > 200:
        # GameOn = False
    if displayed == False:
        takeImage(input_scalar)
        faceimg = pygame.image.load(os.path.join(dirname,"cv2Captures/currentPhoto.jpg"))
        screen.blit(faceimg, (25,150))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOn = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            x, y = event.pos
            print("mouse down")
            for index, thumbnail in enumerate(thumbnail_images):
                if thumbnail.collidepoint(x,y):
                    currentStyle = styles[index]
                    print(styles[index])
                # if thumbnail.get_rect().collidepoint(x, y):
        if event.type == pygame.KEYDOWN:
            print('This key number is: ', event.key)
            # Escape Key
            if event.key == 27:
                GameOn = False
            # P Key
            if event.key == 112:
                # displayed = False
                doit()
                # takeImage()
                # faceimg = pygame.image.load(os.path.join(dirname,"cv2Captures/currentPhoto.jpg"))
                # screen.blit(faceimg, (25,150))
    #Select one of the above styles to use
    opts = Opts("trained/" + currentStyle + ".ckpt", "cv2Captures/currentPhoto.jpg", "cv2Translations")
pygame.display.quit()
cam.release()