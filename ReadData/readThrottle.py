import pygame
pygame.init()


def main():

    joysticks = []
    clock = pygame.time.Clock()
    keepPlaying = True

    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize them all (-1 means loop forever)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print ("Detected joystick '" + joysticks[-1].get_name(),"'")

    while keepPlaying:
        clock.tick(60)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print ("Received event 'Quit', exiting.")
                    keepPlaying = False

                #wheel staff
                elif event.type == pygame.JOYAXISMOTION:
                    if (event.axis == 2):
                        with open('current_throttle.txt', 'w') as file:
                            file.write(str(event.value))




main()
pygame.quit()
