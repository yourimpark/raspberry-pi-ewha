import RPi.GPIO as GPIO
import datetime
import time
from datetime import timedelta
import pygame.mixer
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#LED_PORT_NUMBER
green_1 = 16
yellow_1 = 20
red_1 = 21

green_2 = 13
yellow_2 = 19
red_2 = 26

green_3 = 17
yellow_3 = 27
red_3 = 22

sound_button = 24

#setup external I/O
GPIO.setup(green_1, GPIO.OUT)
GPIO.setup(yellow_1, GPIO.OUT)
GPIO.setup(red_1, GPIO.OUT)

GPIO.setup(green_2, GPIO.OUT)
GPIO.setup(yellow_2, GPIO.OUT)
GPIO.setup(red_2, GPIO.OUT)

GPIO.setup(green_3, GPIO.OUT)
GPIO.setup(yellow_3, GPIO.OUT)
GPIO.setup(red_3, GPIO.OUT)

GPIO.setup(sound_button, GPIO.IN)

#list of food
register_list= {}
slot = [0,0,0] #For checking if the slot is full or not
day_list = [None, None, None]
 
onul =  datetime.date.today()
sound_flag=0

def led_on(green,yellow,red,day):
	global onul
	global sound_flag
	asd = onul - day
	day_count = asd.days

	if(day_count < -2):
		GPIO.output(green,GPIO.HIGH)
		GPIO.output(yellow,GPIO.LOW)
		GPIO.output(red,GPIO.LOW)	
		
	elif(day_count >= -2 and day_count <=-1):
		GPIO.output(yellow, GPIO.HIGH)
		GPIO.output(red, GPIO.LOW)
		GPIO.output(green, GPIO.LOW)
		
	else:
		GPIO.output(red,GPIO.HIGH)
		GPIO.output(yellow,GPIO.LOW)
		GPIO.output(green,GPIO.LOW)
		
		sound_flag=True
                return

def led_off(green,yellow,red):
	GPIO.output(green,GPIO.LOW)
        GPIO.output(yellow,GPIO.LOW)
        GPIO.output(red,GPIO.LOW)
	

def register():
	reg_name = raw_input('what food do you want to register?: ')
	reg_date = raw_input('what is the expiration date?(ex) 2014-03-22): ')
	yesorno = raw_input("name: "+reg_name +" / "+"date:" +reg_date+" is that true?")	
	if(yesorno == 'y'):		
		day = datetime.date(int(reg_date.split('-')[0]),int(reg_date.split('-')[1]),int(reg_date.split('-')[2])) 		
		#print(register_list["milk"])
		slot_index=-1
		if(slot[0] ==0):
			led_on(green_1,yellow_1,red_1,day)
			day_list[0] = day
			slot[0] =1
			slot_index = 0
		elif(slot[1]==0):
			led_on(green_2,yellow_2,red_2,day)
			day_list[1] = day
			slot[1] =1
			slot_index= 1
		elif(slot[2]==0):
			led_on(green_3,yellow_3,red_3,day)
			day_list[2] = day
			slot[2]=1
			slot_index= 2

		register_list[reg_name] = slot_index

	else:
		register()


def delete():
	delete_name = raw_input('what food do you want to delete?')

	if(register_list[delete_name]==0):
		led_off(green_1, yellow_1, red_1)
		slot[0] = 0
		day_list[0] = None
	elif(register_list[delete_name]==1):
		led_off(green_2, yellow_2, red_2)
		slot[1] = 0
		day_list[1] = None
	elif(register_list[delete_name]==2):
		led_off(green_3, yellow_3, red_3)
		slot[2] = 0
		day_list[2] = None
	
	register_list.pop(delete_name)

#increase date

def passday():
	global onul
	
	plusDay = timedelta(days=1)
	neil = onul + plusDay
	
	onul = neil
	
	
	if(slot[0]==1):
		led_on(green_1, yellow_1, red_1, day_list[0])
	if(slot[1]==1):
		led_on(green_2, yellow_2, red_2, day_list[1])
	if(slot[2]==1):
		led_on(green_3, yellow_3, red_3, day_list[2])
	


def makesound():
	pygame.mixer.init(48000, -16, 1, 1024)

	sound = pygame.mixer.Sound("/home/pi/python_games/match5.wav")
	channelA = pygame.mixer.Channel(1)
	channelA.play(sound, loops=-1)
	print("Press the RED BUTTON to stop the sound")

	sleep(2.0)
	
def stopsound():
	isReleased = True

	while True:
		inputValue = GPIO.input(sound_button)
		
		if(inputValue == True and isReleased == True):
			pygame.mixer.stop()
			isReleased = False
			break

		if(inputValue == False and isReleased == False):
			isReleased = True

		time.sleep(.01)

		
#main

while True:
	print("")
	print("")
	print("Today is: "+ str(onul)+"***")
	print("=================================")
	print(" >>>>EXPIRATION DATE MANAGER<<<<")
	print("--- 1. register")
	print("--- 2. delete")
	print("--- 3. tomorrow is comming~~~ ")
	print("--- 4. exit")
	print("=================================")
	print("************FOOD LIST************")
	print("***Food name : Expiration date***")
	
	for key, value in register_list.items() :
		print(key+ ' : ' +str(day_list[value])) 

	menu_select = raw_input('Input Menu Number: ')
	
	if(menu_select == '1'):
		register()

	elif(menu_select == '2'):
		delete()

	elif(menu_select == '3'):
		passday()

	elif(menu_select == '4'):
		led_off(green_1,yellow_1,red_1)
		led_off(green_2,yellow_2,red_2)
		led_off(green_3,yellow_3,red_3)
		break
	else:
		print("error: Wrong menu number")

	if(sound_flag == True):
		makesound()
		stopsound()
		sound_flag = False

	#makesound()
	#stopsound()


