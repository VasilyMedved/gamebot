# Imports 
import cv2 as cv2
import numpy as np 
# from matplotlib import pyplot as plt
import pyautogui
import time
import timeit


# Helpers

def locate_target(screenshot, target_bitmap):
	'''
	Purpose: searches if particular targetImg is presented on sourceImg using OpenCV template matching 
	https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#template-matching
	https://stackoverflow.com/questions/9709631/how-do-i-use-opencv-matchtemplate
	'''
	screenshot = cv2.imread(screenshot)
	target_bitmap = cv2.imread(target_bitmap)
	w, h = target_bitmap.shape[0],target_bitmap.shape[1]
	centerY = screenshot.shape[0] // 2
	centerX = screenshot.shape[1] // 2
	duration = 2
	#
	res = cv2.matchTemplate(screenshot,target_bitmap, cv2.TM_CCOEFF_NORMED)
	min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
	print('Probabiluty:',max_val)
	if max_val > 0.9:
		targetX = max_loc[0]
		targetY = max_loc[1]
		matchX = targetX - centerX
		matchY = targetY - centerY
		print(f'TargetXY:{targetX}:{targetY}, MatchXY:{matchX}:{matchY}')
		return (matchX, matchY)
	else:
		#return zero relative coordinates if nothing found
		return (0,0)


def compare_frames(imgOne, imgTwo):
	'''
	Purpose: compares two screenshots (to make sure that bot reaached destination so picture not changes anymore)
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
	return persentage


def take_screenshot(name):
	img = pyautogui.screenshot()
	img.save(name)
	return name
	'''
	takes screenshots
	saves screenshot with a given name on disk
	'''

def move_mouse(target):
	print('Log - Mouse should move to '+ str(target) + 'relative to center of screen')
	#wpyautogui.moveTo(960,540)
	pyautogui.moveRel(target[0],target[1],1)

class Bot:
	def forward():
		pyautogui.press('w')

	def left():
		pyautogui.press('a')

	def right():
		pyautogui.press('d')

	def around():
		pass

	def back():
		pyautogui.press('s')

	def jump():
		pyautogui.press('space')		
#screenshot = 'screenshot_pass.png'

'''
screenshot = 'current.png'
template = 'target.png'
target = locate_target(screenshot,template)
print(target)
move_mouse(target)
'''

time.sleep(2)
while True:
	pyautogui.keyDown('f')
	time.sleep(0.5)
	screenshot = take_screenshot('current.png')
	template = 'target.png'
	target = locate_target(screenshot,template)
	pyautogui.keyUp('f')
	#stamp = take_screenshot(f'{target}_screen.png')
	move_mouse(target)
	pyautogui.keyDown('w',5)
	#time.sleep(5)
	pyautogui.keyUp('w')
