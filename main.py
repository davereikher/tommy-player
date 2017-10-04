import os
from collections import deque
from glob import glob
import config
import time
import RPi.GPIO as GPIO
import pygame
import random

def get_all_mp3s(root_folder):
	result = [y for x in os.walk(root_folder) for y in glob(os.path.join(x[0], '*.mp3'))]
	return result

if __name__ == "__main__":
	all_music_files = get_all_mp3s(config.music_root_folder)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)

	pygame.mixer.init()
	index = 0
	playing = False
	all_music_files_deq = deque([])
	while True:
		if (not GPIO.input(4)): # Start playing, from a random piece
			index = 0
			pygame.mixer.music.stop()
			all_music_files_deq = deque(all_music_files)
			all_music_files_deq.rotate(random.randint(0, len(all_music_files) - 1))	

			playing = True
			pygame.mixer.music.load(all_music_files_deq[index])
			pygame.mixer.music.play()
		elif (not GPIO.input(17)): # Stop playing
			pygame.mixer.music.stop()
			playing = False
		elif playing:
			if not pygame.mixer.music.get_busy():
				index += 1
				if index == len(all_music_files_deq):
					playing = False
					index = 0
				else:
					pygame.mixer.music.load(all_music_files_deq[index])
					pygame.mixer.music.play()
		time.sleep(1)


