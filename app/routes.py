from flask import Flask, request, render_template
import requests 
from json2html import *
import json 
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, root_path=dir_path)


sts = 'https://healthycanadians.gc.ca/recall-alert-rappel-avis'

@app.route('/recent', methods=['GET'])
@app.route('/recent/<string:lang>', methods=['GET'])
def recent(lang=None):
	
	sred = '/en'
	if lang == 'fr':
		srend = '/fr'
	
	st = sts + '/api/recent' + sred 
	
	rsj = requests.get(st)
	
	todos = json.loads(rsj.content)
	
	for k in todos['results']:
		print('----------------------------------------------')
		print('----------------------------------------------')
		print(k)
		for key,v in enumerate(todos['results'][k]):
			print('----------------------------------------------')
			print(v['recallId'])
			print(v['title'])
			print(v['category'])
			print(v['url'])
			print(v['date_published'])
			print('----------------------------------------------')
		print('----------------------------------------------')
		print('----------------------------------------------')
		
	#rsh = json2html.convert(json = rsj.content.decode('ascii'))
	#return rsh 
	
	return render_template('recent.html', 
							all = todos['results']['ALL'], 
							cps = todos['results']['CPS'], 
							health = todos['results']['HEALTH'], 
							food = todos['results']['FOOD'],
							vehicle = todos['results']['VEHICLE'])
	
@app.route('/api/<int:id>',methods=['GET'])
@app.route('/api/<int:id>/<string:lang>',methods=['GET'])
def recall(id, lang=None):
	
	
	sred = '/en'
	if lang == 'fr':
		srend = '/fr'
	
	
	st = sts + '/api/' + str(id) + sred

	
	rsj = requests.get(st)
	
	rsh = json2html.convert(json = rsj.content.decode('utf-8'))
	
	return rsh
	
@app.route('/')
def form():
	return render_template('form.html')

@app.route('/', methods=['POST'])
def form_post():

	srst = sts + '/api/search?search=' 
	srend = ''
	
	print('----------------------------------------------')
	print('----------------------------------------------')
	fr = request.form.get('french')
	if fr:
		print("We love french")
		srend = srend + '&lang=fr'
	else:
		print("We love English")
		srend = srend + '&lang=en'
		
	rcount = request.form.get('rcount')
	if rcount:
		print("User wants to change result count")
		srend = srend + '&lim=' + str(rcount)
	else:
		print("We will use default value of 5 for result count")
		srend = srend + '&lim=5'
		
	scount = request.form.get('scount')
	if scount:
		srend = srend + '&off=' + str(scount)
	else:
		srend = srend + '&off=0'
		

	cats = request.form.get('cats')
	if cats:
		if cats.lower() == 'vehicle':
			srend = srend + '&cat=2'
		elif cats.lower()  == 'food':
			srend = srend + '&cat=1'
		elif cats.lower()  == 'health':
			srend = srend + '&cat=3'
		elif cats.lower()  == 'cps':
			srend = srend + '&cat=4'
		
	# no cat flag means search is for all 

	
	text = request.form['text']
	processed_text = text.upper().replace(' ','')
	
	st = srst + processed_text + srend
	
	rsj = requests.get(st)
	
	rsh = json2html.convert(json = rsj.content.decode('ascii'))
	
	return rsh