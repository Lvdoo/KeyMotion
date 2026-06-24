import pygame
import time

pygame.mixer.init()
pygame.mixer.set_num_channels(16)

sounds = {
    "DO1": pygame.mixer.Sound("sounds/Do1.wav"),
    "RE1": pygame.mixer.Sound("sounds/Re1.wav"),
    "MI1": pygame.mixer.Sound("sounds/Mi1.wav"),
    "FA1": pygame.mixer.Sound("sounds/Fa1.wav"),
    "SOL1": pygame.mixer.Sound("sounds/Sol1.wav"),
    "LA1": pygame.mixer.Sound("sounds/La1.wav"),
    "SI1": pygame.mixer.Sound("sounds/Si1.wav"),
    "DO2": pygame.mixer.Sound("sounds/Do2.wav"),
    "RE2": pygame.mixer.Sound("sounds/Re2.wav"),
    "MI2": pygame.mixer.Sound("sounds/Mi2.wav"),
    "FA2": pygame.mixer.Sound("sounds/Fa2.wav"),
    "SOL2": pygame.mixer.Sound("sounds/Sol2.wav"),
    "LA2": pygame.mixer.Sound("sounds/La2.wav"),
    "SI2": pygame.mixer.Sound("sounds/Si2.wav"),
    "DO3": pygame.mixer.Sound("sounds/Do3.wav"),
    "RE3": pygame.mixer.Sound("sounds/Re3.wav"),
    "MI3": pygame.mixer.Sound("sounds/Mi3.wav"),
    "FA3": pygame.mixer.Sound("sounds/Fa3.wav"),
    "SOL3": pygame.mixer.Sound("sounds/Sol3.wav"),
    "LA3": pygame.mixer.Sound("sounds/La3.wav"),
    "SI3": pygame.mixer.Sound("sounds/Si3.wav"),
    "DO4": pygame.mixer.Sound("sounds/Do4.wav")
}

for sound in sounds.values() : 
    sound.set_volume(0.25)

current_key = {}
current_channel = {}
timer = {}
fingers = ["thumb", "index", "middle", "ring", "pinky"]

for finger in fingers :
        current_key[finger] = None
        current_channel[finger] = None
        timer[finger] = None

def start_sound(finger, pressed_key):
    """
    Starts playing the sound corresponding to the pressed key.

    Args:
        finger (str):
            Name of the finger that pressed the key.
        pressed_key (dict):
            Dictionary mapping each finger to the key it has pressed.

    Returns:
        None
    """

    global current_key, current_channel, timer

    if pressed_key[finger] in sounds:
        current_channel[finger] = pygame.mixer.Sound.play(sounds[pressed_key[finger]])
        current_key[finger] = pressed_key[finger]
        timer[finger] = time.time()


def fade_sound(finger):
    """
    Gradually stops the sound currently played by a finger.

    Args:
        finger (str):
            Name of the finger whose sound must be stopped.

    Returns:
        None
    """

    global current_key, current_channel, timer
    
    if current_channel[finger] is not None:
        current_channel[finger].fadeout(700)

    current_key[finger] = None
    current_channel[finger] = None
    timer[finger] = None

def update_sound(keys, pressed_key):
    """
    Updates the sound playback according to the fingers' positions and pressed keys.

    Args:
        keys (dict):
            Dictionary mapping each finger to the key it is currently touching.
        pressed_key (dict):
            Dictionary mapping each finger to the key it has just pressed.

    Returns:
        None
    """
    
    global current_key, current_channel, fingers, timer

    for finger in fingers :
        if pressed_key[finger] is not None and current_key[finger] is None :
            start_sound(finger, pressed_key)
        if current_key[finger] is not None and time.time() - timer[finger] > 2:
            fade_sound(finger)

        if keys[finger] is None and current_key[finger] is not None:
            fade_sound(finger)