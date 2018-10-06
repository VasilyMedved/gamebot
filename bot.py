# Imports 
import cv2
import numpy as np 
# from matplotlib import pyplot as plt
import pyautogui as pag
import time


# Helpers
def match (template, threshold):
	'''
	Purpose: searches if particular targetImg is presented on sourceImg using OpenCV template matching 
	https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#template-matching
	https://stackoverflow.com/questions/9709631/how-do-i-use-opencv-matchtemplate
	'''
	#setup
	global screen
	method = cv2.TM_CCOEFF_NORMED

	#read screenshots
	image = pag.screenshot()
	screenshot = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
	template = cv2.imread(template)
	match = ()
	# obtain center of template 
	template_center = (template.shape[0] // 2, template.shape[1] // 2)	
	# actual image recognition
	res = cv2.matchTemplate(screenshot, template, method)
	min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
	if max_val > threshold:
		# match is coordinates of precise center of matching template
		match = ((max_loc[0] + template_center[0]) - screen['center_x'],
				((max_loc[1] + template_center[1]) - screen['center_y']))
		return match 
	else:
		return None


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


class Bot:
	def move_mouse(target,duration = 0.5):
		print('Mouse moves to '+ str(target) + 'relative to center')
		pag.moveRel(target[0],target[1],duration)

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

# setup
pag.FAILSAFE = False
screen = {
'w' : pag.size()[0],
'h' : pag.size()[1],
'center_x' : pag.size()[0] // 2,
'center_y' : pag.size()[1] // 2}

print(screen)
templates = {
	'stone':'stone.png',
	'e_bar':'e_bar.png',
	'low_health':'low_health.png',
	'resource':'resource.png'
}
# Main loop
bot = Bot
while True:	
	# Search stone routine
	# enable scaner mode and look for match
	bot.scanner('on') 
	target = match(templates['stone'],0.9)
	if target == None:
		print('target not found, must search')
		bot.move_mouse([-(screen['w']//10),0],0.2)
	else: 
		print ('target:',target)
		bot.move_mouse(target,0.9)
		bot.forward(1)
		#look for e_bar which indicates that stone found
		bot.scanner('off')		
		target = match(templates['e_bar'],0.8)
		if target != None:
			bot.interact()
			bot.jump()
		else:
			bot.forward(0.5)
			
			#if bot.stuck_check() < 80:
			#	bot.jump()
	# if match found mouse moved to it
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
	if not_stuck < 80:
		bot.jump()
	'''