# Import libraries pygame, opencv2, and others we'll be using for this application
import pygame, cv2, os, random, transferstyle

# Instantiate the dirname variable so that we can load relative paths
dirname = os.path.dirname(__file__)

# Initialize all imported PyGame modules 
pygame.init()

# (Disabled for now) Make mouse on screen invisible so that we can use a hand cursor instead
# pygame.mouse.set_visible( False )

# Create a display surface for the game
display = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN, display=0)

# Set the SU_Background_Color which will determine the background color of the application
SU_Background_Color = (255,255,255)

# Retrieve the width and height of the pygame surface for later sizing use
display_Width, display_Height = pygame.display.get_surface().get_size()

# (Disabled for now) Instantiate variable hand_Image and set it equal to a loaded hand.png image
# hand_Image = pygame.image.load(os.path.join(dirname,"hand.png"))

# (Disabled for now) # Create function to update cursor position
# def cursor_position_Render():
    
#     # Instantiate cursor_center variable and set it equal to the pygame.mouse position
#     cursor_center = pygame.mouse.get_pos()

#     # Render hand_Image at cursor_center position using blit
#     display.blit(hand_Image, cursor_center)

# (Disabled for now) # Create function to render the UI options to the screen, which are the photo and video buttons
# def UI_Render(color, x, y):

#     # The color parameter is either "light" or "dark"

#     # Instantiate the video_Button variable and set it equal to the loaded button_dark image
#     video_Button = pygame.image.load(os.path.join(dirname,"examples/button_" + color +".png"))

#     # Render the video_Button to the screen using the pygame.blit function
#     pygame.blit(video_Button, xy)

#     # Get Rect for video_Button for collision detection events
#     video_Button = video_Button.get_rect(x,y)

#     # Return video_Button Rect
#     return video_Button

# Create function to execute style transfer on the current_Photo
def style_Transfer_Save(currentStyle):
    class Opts:
        def __init__(self, checkpoint_dir, in_path, out_path):
            self.checkpoint_dir = checkpoint_dir
            self.in_path = in_path
            self.out_path = out_path

    if currentStyle == "roda1":
        opts = Opts("trained/" + currentStyle, "cv2Captures/currentPhoto.jpg", "cv2Translations")


    else:
        opts = Opts("trained/" + currentStyle + ".ckpt", "cv2Captures/currentPhoto.jpg", "cv2Translations")

    transferstyle.main(opts)

# Create function to render the current photo to the screen
def currentPhoto_Render():
    # Call the capture_Camera function to get the latest image from the camera feed and save it to a local file
    capture_Camera()

    # Instantiate current_Photo variable and set it equal to the image saved by the capture_Camera function
    current_Photo = pygame.image.load(os.path.join(dirname,"cv2Captures/currentPhoto.jpg"))
    
    # Render the latest image to the screen by using the pygame.blit function, with the x and y position as arguments
    display.blit(current_Photo, (100, 100))

# Create function to write text with a string, xy tuple coordinate, color, font size, and font.
def write_Text(string, xy, color, size, font):

    # Instantiate the variable font and set it equal to a loaded font with the font parameter as the file name in the fonts folder.
    font = pygame.font.Font(os.path.join(dirname,'fonts/' + font + '.ttf'), size)
    
    # Instantiate the variable text and set it equal to a rendered image with the string and colors
    text = font.render(string, True, color, SU_Background_Color) 

    # Render the text
    display.blit(text, xy)

# Create function to retrieve and render the style choices
def styleCards_Render(collide_index):

    # Fill the screen with the SU branded light blue color
    display.fill(SU_Background_Color)

    # Load and display SU logo
    SU_Logo = pygame.image.load(os.path.join(dirname,"examples/style/sulogo_png.png"))
    display.blit(SU_Logo, (835,300))

    # Instantiate variable styles and set it equal to a list of the JPG names for each of the available style options
    styles = ["la_muse", "rain_princess", "scream", "roda1", "udnie", "wave", "wreck"]

    # Instantiate thumbnail_Rectangles variable and set it equal to an empty list, which we will append the rectangles of each thumbnail to for use in detecting mouse collision with it
    thumbnail_Rectangles = []

    # Write above the cards "Select a style!"
    write_Text("Select a style!", (800, display_Height-440), (236,102,41), 60, "MinionPro-Regular")

    # Write above the images the title "Artistic Style Transfer using Neural Networks"
    write_Text("Artistic Style Transfer using Neural Networks", (450, 20), (228,22,141), 60, "MinionPro-Regular")

    # Create a for loop and enumerate the styles list
    for index, thumbnail in enumerate(styles):

        # Load images with the file path to the thumb nails and the .jpg file type added to file name
        thumbnail_image = pygame.image.load(os.path.join(dirname,"examples/style/thumbs/" + thumbnail + ".jpg"))
        
        # Calculate spacing between images with padding on the end
        space_Between = (display_Width-(len(styles)*thumbnail_image.get_size()[0]))/(len(styles)+1)

        # Instantiate the variables thumbnail_x and thumbnail_y
        # thumbnail_x is equal to 1+ the index of the thumbnail in the list to create spacing on the left multipllied by the available space between, added to the cumulative space being taken by each tumbnail so far
        thumbnail_x = space_Between*(index+1)+thumbnail_image.get_size()[0]*index
        # thumbnail_y is equal to the height of th thumbnail divided by two, subtracted from the height of the screen
        thumbnail_y = display_Height-thumbnail_image.get_size()[1]/2

        # Check if the current thumbnail index is equal to the collide_index passed for collisions detected, if so, add height to the thumbnail_y
        if index == collide_index:
            thumbnail_y -= thumbnail_image.get_size()[1]/3

        # Draw images to screen using blit function
        display.blit(thumbnail_image, (thumbnail_x,thumbnail_y))

        # Instantiate the variable thumbnail_Rectangle and set it equal to a created rectangle equal to the dimensions of the style thumbnail and in the same location and append it to the thumbnail_Rectangles list
        thumbnail_Rectangle = thumbnail_image.get_rect(x=thumbnail_x, y=thumbnail_y)

        # Append the thumbnail_Rectangle to the list thumbnail_Rectangles
        thumbnail_Rectangles.append(thumbnail_Rectangle)

    # Call the style_Transfer_Save function with the currentStyle parameter being the collide_index matched to the style list
    if collide_index>-1:
        style_Transfer_Save(styles[collide_index])
        styled_image = pygame.image.load(os.path.join(dirname,"cv2Translations/currentPhoto.jpg"))
        display.blit(styled_image, (1150,100))

    # Return the list of thumbnail_Rectangles so that they can be used for collision detection event triggers in the main While loop
    return thumbnail_Rectangles

# Create function to scale an image 
def scale_Image(scale_percent, image):

    # Instantiate variablew width and height by creating an int that is the current image widths and heights multiplied by the scala_percent input
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    
    # Instantiate variable resized which is the resized image
    resized = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

    # Save new image as local file "currentPhoto.jpg" for retreival by rendering functions
    cv2.imwrite("cv2Captures/currentPhoto.jpg",resized)

# Create function that captures an image from the current video feed and saves it to a local file
def capture_Camera():

    # Call the read function and instantiate the success and image variables
    success, image = camera_feed.read()

    # Check is success is true, meaning the webcam connection is successful
    if success == True:

        # Call scale_Image function to save a larger version of the camera feed to a local file
        scale_Image(1,image)

    # Print that we were unable to connect to the webcam
    else:
        print("Unable to connect to webcam. Please check that a webcam is attached to or plugged into this computer, and not being used aleady by video conferencing software like Skype/Zoom.")

# Create function that renders the main game screen
def mainScreen_Render():

    # Fill the screen with the SU branded light blue color
    display.fill(SU_Background_Color)

    # (Disabled for now) Call the cursor_position_Render function to draw the hand image to the current cursor position
    # cursor_position_Render()

    # Call the styleCards_Render function to show the style choices on the screen, and set the variable styleCards_Rectangles equal to the list of rectangles it returns. Set collide_index to -1 to indicate no cards are being collided with.
    styleCards_Rectangles = styleCards_Render(collide_index=-1)

    # Return the list of styleCards_Rectangles to be used for collission detection
    return styleCards_Rectangles

# Instantiate global variable camera_feed with VideoCapture variable set to 0 denoting the choice of camera from an index of available webcams
camera_feed = cv2.VideoCapture(0)

# Call render function to draw the main screen before the event listening initiates and set it equal to the styleCards_Boundaries to be used for collission detection in the main While loop
styleCards_Boundaries = mainScreen_Render()

# Instantiate GamePlaying variable as True to allow game loop to run
GamePlaying = True

# Instantiate variable total_Downtime
total_Downtime = 0

# Game loop that continues as long as GamePlaying == True
while GamePlaying:

    # Instantiate timedelta variable and set it equal to the time elapsed between the last clock tick and this one. Divid by 1000 to convert from milliseconds to seconds
    timedelta = pygame.time.Clock().tick(60)/1000

    # (Disabled for now) Call the cursor_position_Render function to draw the hand image to the current cursor position
    # cursor_position_Render()

    # Get all active events in PyGame that have occured since the last loop
    for event in pygame.event.get():

        # Create a for loop to iterate over the list styleCards_Boundaries
        for index, boundary in enumerate(styleCards_Boundaries):

            # Check if the mouse position is collidiing with the boundary (which is a pygame.Rect)
            if boundary.collidepoint(pygame.mouse.get_pos()):

                # Call the styleCards_Render function to move the selected style up, with the index of the card that has been collided with
                styleCards_Render(collide_index=index)

        # Check if an event is equal to pygame.KEYDOWN, which is triggered by clicking a keyboard key
        if event.type == pygame.KEYDOWN:

            # Check if the key is an Escape key
            if event.key == 27:

                # Set GamePlaying variable to False to stop game loop on next loop
                GamePlaying = False

        # Check if an event is equal to pygame.QUIT, which is triggered by the corner X button
        if event.type == pygame.QUIT:

            # Set GamePlaying variable to False to stop game loop on next loop
            GamePlaying = False
            
            # Terminate the nearest loop which is the "for event" loop
            break

    else:
        total_Downtime += timedelta
        if total_Downtime > 3:
            styleCards_Render(collide_index=random.randint(0,6))
            total_Downtime = 0

    # Call the currentPhoto_Render function to display the current photo on the screen during every event loop
    currentPhoto_Render()

    # Update pygame.display with newest information (render cycle)
    pygame.display.flip()
            
# Close display for PyGame
pygame.display.quit()