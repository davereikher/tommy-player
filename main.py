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
	#print(all_music_files[0])
	index = 0
	playing = 'nothing'
	all_music_files_deq = deque([])
	while True:
		time.sleep(0.3)
		if (not GPIO.input(4)): # Start playing, from a random piece or stop
			if playing != 'nothing':
				print("Stopping music")
				pygame.mixer.music.stop()
				playing = 'nothing'
				continue

			index = 0
			all_music_files_deq = deque(all_music_files)
			all_music_files_deq.rotate(random.randint(0, len(all_music_files) - 1))	
			print("DETECTED PLAY, index = %d. First song: %s" % (index, all_music_files_deq[0]))

			playing = 'music'
			pygame.mixer.music.load(all_music_files_deq[index])
			pygame.mixer.music.play()
		elif (not GPIO.input(17)): # Play white noise
			print("DETECTED STOP, index = %d" % index)
			if playing != 'nothing':
				print("Stopping noise")
				pygame.mixer.music.stop()
				playing = 'nothing'
				continue
			pygame.mixer.music.load(config.white_noise_file)
			pygame.mixer.music.set_volume(1)
			pygame.mixer.music.play()
			playing = 'noise'
		elif playing == 'music':
			if not pygame.mixer.music.get_busy():
				index += 1
				if index == len(all_music_files_deq):
					playing = 'nothing'
					index = 0
				else:
					pygame.mixer.music.load(all_music_files_deq[index])
					pygame.mixer.music.play()
		elif playing == 'noise':
			if not pygame.mixer.music.get_busy():
				print("Continuing noise")
#				pygame.mixer.music.load(config.white_noise_file)
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()


#  time.sleep(5)


