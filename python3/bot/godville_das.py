#! /usr/bin/env python3
import os
import time
from selenium import webdriver
#<get identity>
print('===============Start_bot===============')
f = open('passwd')
a = f.read()
r = a.replace("\n", "")
username = r.split(':')[0]
passwd = r.split(':')[1]
f.close()
#</get identity>
browser = webdriver.Firefox()
browser.get('https://godville.net')
#######################################################
#login
browser.find_element_by_id('username').send_keys(username)
time.sleep (2)
browser.find_element_by_id('password').send_keys(passwd)
time.sleep (2)
browser.find_element_by_css_selector('input[name="commit"]').click()
time.sleep (1)
while browser.find_element_by_css_selector('h2.block_title').text != 'Герой':
	print('Wait to start...')
	time.sleep (3)

#######################################################
#Variable
prot = 'Противник'
global find_enemy
#Monster
def mob():
	monster = browser.find_element_by_css_selector('div.block_content > div > div.line > div.l_capt').text
	return monster

#HP
def hp():
	hp = browser.find_element_by_css_selector('#hk_health > div.l_val').text
	return int(hp.split(' /')[0])

#Prana charge
def prana_charge():
	pran_charge = browser.find_element_by_css_selector('span.acc_val').text
	return pran_charge
#Prana
def prana():
	prana_find = browser.find_element_by_css_selector('div.gp_val')
	prana_percent = str(prana_find.text)
	prana_count = prana_percent.split("%")[0]
	return int(prana_count)

def if_hero_with_mob():
	while mob() == prot:
		print("Stil wait...")
		time.sleep (2)

def god_battle_voice():
	try:
		browser.find_element_by_id('godvoice').send_keys('бей')
		print("Hit!")
		time.sleep (1)
		browser.find_element_by_id('voice_submit').click()
	except:
		print("Oops, not now... wait!")



def try_find_enemy():
	try:
		find_enemy = browser.find_element_by_css_selector('#o_info > div.block_h > h2.block_title').text
		return find_enemy
	except:
		find_enemy = " "
		return find_enemy



def arena():
#'Отправить на арену'
#no batton and have time until arena
#browser.find_element_by_css_selector('div.arena_msg').text
	if "Арена откроется" in browser.find_element_by_css_selector('div.arena_msg').text:
		print(browser.find_element_by_css_selector('div.arena_msg').text)
		time.sleep (1)
		print("Arena is not avaliable. We must exit! bye!")
		exit(0)
	elif "Отправить на арену" in browser.find_element_by_css_selector('a.no_link.to_arena').text:
		print('Start_arena')
		browser.find_element_by_css_selector('a.no_link.to_arena').click()
		time.sleep (2)
		alert = browser.switch_to_alert()
		time.sleep (2)
		alert.accept()
		time.sleep (1)
		try:
			alert.accept()
		except:
			pass
		
		time.sleep (3)

#		def try_find_enemy():
#			try:
#				find_enemy = browser.find_element_by_css_selector('#o_info > div.block_h > h2.block_title').text
#				return find_enemy
#			except:
#				find_enemy = " "
#				return find_enemy


		while try_find_enemy() != prot and prana() >= 4:
			print('Wait enemy in arena...')
			time.sleep (5)
		else:
			print("Enemy is come! Arena begin!")
			time_process_battle_shout()


def time_process_battle_shout():
	old_battle_log = ' '
	while prana() >= 4:
		if browser.find_element_by_css_selector('#m_fight_log > div.block_h > h2.block_title').text != old_battle_log:
			print('Attak enemy!')
			god_battle_voice()
			old_battle_log = browser.find_element_by_css_selector('#m_fight_log > div.block_h > h2.block_title').text
		else:
			print("Stil_old_battle_time")
			time.sleep (2)

def resurection():
	print('Us hero die?')
	if hp() == 0:
		print('Us hero is die=( Fix it!')
		browser.find_element_by_xpath("//a[contains(text(),'Воскресить')]").click()


def ii():
	global pr
	global mob_prot
	global summ
	if prana() >= 55:
		pr = 1
	else:
		pr = 0

	if prana() <= 10:
		print("Prana is over. Bye!")
		exit(0)

	if mob() == prot:
		mob_prot = 1
	else:
		mob_prot = 0


	summ = int(pr + mob_prot)
	return

print("Mob_type:", mob())
print("HP:", hp())
print("Prana_charge:", prana_charge())
print("Prana:", prana())
######################################################
##Script_body
#II
resurection()
time.sleep (1)
ii()
print("summ:", summ)
print("========")
while summ >= 0:
	ii()
	print("while is begin")
	print(pr)
	print(mob_prot)
	if pr == 1 and mob_prot == 0:
		print("Call arena")
		arena()
	
	if pr == 1 and mob_prot == 1:
		print("if hero in distance and with mob: def if hero with mob")
		if_hero_with_mob()

	if pr == 0 and mob_prot <= 1:
		print("Break")
		break
		
	time.sleep (20)

print("It's done and we exit=)")
######################################################
#Quit
time.sleep (5)
browser.quit()
print('===============Stop_bot===============')
