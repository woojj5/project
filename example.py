from flask import Flask, jsonify
from flask import render_template, request, send_file, url_for
#from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
#from selenium import webdriver
import  time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/')
def getInfo() :
	return render_template('index.html')

@app.route('/result',methods = ['POST','GET'])
def result():
	if request.method == 'POST':
		userid = request.form['username']
		userpw =request.form['password']
		from selenium import webdriver
		from selenium.webdriver.support import expected_conditions as EC
		from selenium.common.exceptions import NoAlertPresentException, TimeoutException, UnexpectedAlertPresentException, NoSuchElementException

		import time
		import getpass
		from bs4 import BeautifulSoup
		import pandas as pd
		import numpy as np


		user = getpass.getuser()
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('disable-gpu')
		driver = webdriver.Chrome(r'C:\Users\{}.\Downloads\chromedriver_win32\chromedriver.exe'.format(user), chrome_options=options)
		driver.implicitly_wait(5)
		driver.get('http://wis.hufs.ac.kr/src08/jsp/index.jsp')
		driver.find_element_by_name('user_id').send_keys(userid)
		driver.find_element_by_name('password').send_keys(userpw)
		driver.execute_script('onLogin()')
		time.sleep(10)
		if(driver.current_url == "https://wis.hufs.ac.kr/src08/jsp/login/ValidPw.jsp?userId=jK1g2xT8Qtrs6jOiLz9u%2Bg%3D%3D&d=null&msg=%20&reurl=&REGNO=&ERPID=" + userid):
			driver.execute_script('javascript:f_chgPwNext()')
			cnt = 0
			while(cnt == 0):
				try: 
					driver.switch_to.alert().dismiss()
					break
				except NoAlertPresentException as e: 
					pass
					break
				except UnexpectedAlertPresentException as e: cnt+=1
		
		driver.switch_to.default_content()
		driver.switch_to.frame('left')
		driver.find_element_by_xpath('/html/body/div/div[2]/div')
		driver.switch_to.frame('MenuFrame')
		driver.find_element_by_xpath('/html/body/div/a[4]').click()
		driver.find_element_by_xpath('//*[@id="div23"]/a[2]').click()
		driver.execute_script("return fnWisMLog('/src08/jsp/grade/GRADE1030L_Main.jsp?tab_lang=K|성적취득현황')")
		
		driver.switch_to.default_content()
		driver.switch_to.frame('left')
		name_source = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr/td/div[2]/table/tbody/tr[2]/td')
		user_name = name_source.text[2:] # user name
		major_source = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr/td/div[2]/table/tbody/tr[3]/td')
		major_source2 = major_source.text[5:].split('\n')
		user_college = major_source2[0]
		user_major = major_source2[1]
		
		choose = 0
		
		time.sleep(1)
		driver.switch_to.default_content()
		driver.switch_to.frame(driver.find_element_by_name('body'))
		driver.switch_to.frame(driver.find_element_by_name('top'))
		user_majors = driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr/td')
		
		if "\n" in user_majors.text :# 이중.부전공 선택한 사람
			if user_sub == "부전공" :choose = 1
			elif user_sub == "전공심화(부전공)" :choose = 2
			elif user_sub == "이중전공" :choose = 3
			else : choose = 0 # 이중.부전공 미선택자

		if choose != 0 : # 이중.부전공 선택자인경우
			user_sub_major = user_majors.text.split(']')[-1][1:]
			user_sub = (user_majors.text.split('[')[2]).split(']')[0]
		else : # 이중.부전공 미선택자인경우
			user_sub = None
			user_sub_major = None
		lista = ["1전공", "이중전공", "2전공", "실외", "교양", "부전공", "교직", "자선", "총취득"]
		time.sleep(1)
		
		driver.switch_to.default_content()
		driver.switch_to.frame(driver.find_element_by_name('body'))
		driver.switch_to.frame(driver.find_element_by_name('top'))
		driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[2]')
		
		html = driver.page_source
		bs = BeautifulSoup(html, 'html.parser')
		tags = bs.findAll('td')
		id2  = 0
		count = 9
		
		user_grade = []
		for tag in tags :
			user_grade.append(tag.text)
		user_grade = user_grade[1:10]
		user_grade = list(map(int,user_grade))

		df = pd.DataFrame(data = np.array([user_grade]),columns=lista)
		df.to_csv("user_grade.csv", mode='w', encoding='utf-8-sig')
		
	
		#driver.save_screenshot("score.png")
		return jsonify({"학부": str(user_college),
						" 학과 ": str(user_major),
						" 선택학부 ": str(user_sub) ,
						" 부전공/이중전공  ": str(user_sub_major)})
		#send_file('score.png', mimetype= 'image/png')
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

