from bs4 import BeautifulSoup as bs
from firebase import Firebase
import requests, html5lib
import time
import unicodedata



while True:
	print "@@@@@@@@@@@@@@@@@@ new check @@@@@@@@@@@@@@@@@@@@"
	start_time = time.time()
	fire = Firebase('https://monitor-6d32c.firebaseio.com')
	item = fire.child('item').get()
	for link in item:
		folder = link.encode('ascii','ignore')
		link = fire.child('item').child(folder).child('url').get()

		text = ''

		#Input Link
		#link = raw_input("Type Link :")
		html = requests.get(link).text
		soup = bs(html, 'lxml')

		#nosize item
		sold = soup.find('a', class_='selected')
		if(sold != None):
			isSold = sold.get('data-sold-out')
		else:
			print("not eligible site")
			continue

		if(isSold == "false"):
			fire.child('item').child(folder).update({'stock' : True})
			print('In Stock :' + folder)
			# method1
			#Name = soup.find('select', id='s')
			#if(Name != None):
			#	nameText = Name.getText()
			

			# method2
			#for item in soup.findAll('select', id='s'):
			#    text = item.getText()

		else:
			fire.child('item').child(folder).update({'stock' : False})
		print("--- %s seconds ---" %(time.time() - start_time))

	time.sleep(60.0 - ((time.time() - start_time) % 60.0))