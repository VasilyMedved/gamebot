# Imports 
import cv2 as cv2
import numpy as np 
# from matplotlib import pyplot as plt
import pyautogui as pag
import time
import timeit


# Helpers

def match(screenshot, template):
	'''
	Purpose: searches if particular targetImg is presented on sourceImg using OpenCV template matching 
	https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#template-matching
	https://stackoverflow.com/questions/9709631/how-do-i-use-opencv-matchtemplate
	'''
	#read screenshots
	screenshot = cv2.imread(screenshot)
	template = cv2.imread(template)

	# obtain center of template and center of screenshot
	w, h = template.shape[0],template.shape[1]
	centerY = screenshot.shape[0] // 2
	centerX = screenshot.shape[1] // 2
	
	# magic here
	res = cv2.matchTemplate(screenshot,template, cv2.TM_CCOEFF_NORMED)
	min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
	print('Match rate:',round(max_val,2))
	if max_val > 0.9:
		targetX = max_loc[0]
		targetY = max_loc[1]
		matchX = targetX - centerX
		matchY = targetY - centerY
		print(f'TargetXY:{targetX}:{targetY}, MatchXY:{matchX}:{matchY}')
		return (matchX, matchY)
	else:
		#return zero relative coordinates if not matched
		return (0,0)


def compare_frames(imgOne, imgTwo):
	'''
	Purpose: compares two screenshots, if they the are the same which may indicate that bot stuck
	https://stackoverflow.com/questions/51288756/how-do-i-calculate-the-percentage-of-difference-between-two-images-using-python
	Returns persentage of image difference:
		up to 100 for completely different image
		~ 1 - 2 persents for similar
		0.0 for identical images
	Images must be the same size
	'''
	persentage = None

	try:
		res = cv2.absdiff(cv2.imread(imgOne),cv2.imread(imgTwo))
		res = res.astype(np.uint8)
		persentage = (np.count_nonzero(res) * 100) / res.size
	except Exception as e:
		print(str(e))
	return round(persentage,2)


def take_screenshot(name):
	img = pag.screenshot()
	img.save(name)
	return name
	'''
	takes screenshots
	saves screenshot with a given name on disk
	'''

class Bot:
	def move_mouse(target):
		print('Mouse moves to '+ str(target) + 'relative to center')
		pag.moveRel(target[0],target[1],1)

	def interact():
		pag.keyDown('e')
		time.sleep(3)
		pag.keyUp('e')

	def mine(interval):
		pag.press('g')
		pag.click(clicks=interval, interval=0.2, button='left')

	def forward(duration):
		pag.keyDown('w',duration)
		pag.keyUp('w')

	def left():
		pag.press('a')

	def right():
		pag.press('d')

	def around():
		self.right()
		self.forward(1)
		self.left()

	def back():
		pag.press('s')

	def jump():
		pag.keyDown('space')		
		time.sleep(2)
		pag.keyUp('space')

	def scanner(toggle):
		if toggle == 'on':
			pag.keyDown('f')
		else:
			pag.keyUp('f')

# print(compare_frames('current.png','current+1.png'))

# Main loop
pag.FAILSAFE = False
templates = {
	'stone':'stone.png',
	'e_bar':'e_bar.png',
	'low_health':'low_health.png',
	'resource':'resource.png'
}
bot = Bot
i = 0
while True:
	
	# Search stone routine
	# enable scaner mode and look for match
	bot.scanner('on') 
	screenshot = take_screenshot('current.png')
	target = match(screenshot,templates['stone'])
	bot.move_mouse(target)
	if target == (0,0) and i < 10:
		print('target not found, must search')
		bot.move_mouse([-320,0])
		i += 1
	else:
		i = 0
		bot.scanner('off')
		bot.forward(3)
		screenshot = take_screenshot('current.png')
		target = match(screenshot, templates['e_bar'])
		if target != (0,0):
			bot.interact()
			bot.jump()
	# if match found mouse moved to it
	#look for e_bar which indicates that stone found
	'''
		time.wait(2)
		print('Now try to interact')
		bot.forward(2)
	'''
	#	print('found resource')
	#bot.scanner('off')
	#stamp = take_screenshot(f'{target}_screen.png')
	'''
	bot.forward(5)
	screenshot = take_screenshot('current.png')
	bot.forward(1)
	screenshot1 = take_screenshot('current+1.png')
	not_stuck = compare_frames(screenshot,screenshot1)
	print('stuck posibility:',not_stuck)
	if not_stuck < 80:
		bot.jump()
	'''