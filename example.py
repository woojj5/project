# -- coding: utf-8 --

from flask import Flask, jsonify
from flask import render_template, request, send_file, url_for
#from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
#from selenium import webdriver
import  time
import json
#import tkinter
#from tkinter import *
#from multiprocessing import Pool
#from app import application


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
#                from tkinter import messagebox
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
                options.add_argument("disable-gpu") 
                options.add_argument("disable-infobars")
                options.add_argument("--disable-extensions")
                prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
                options.add_experimental_option('prefs', prefs)
                
                driver = webdriver.Chrome("/home/ubuntu/project/chromedriver", chrome_options= options)
                #driver.implicitly_wait(3)
                #driver.implicitly_wait(1)
                driver.get('http://wis.hufs.ac.kr/src08/jsp/index.jsp')
                driver.find_element_by_name('user_id').send_keys(userid)
                driver.find_element_by_name('password').send_keys(userpw)
                driver.execute_script('onLogin()')
                #time.sleep(5)
                #driver.implicitly_wait(3)
                #driver.implicitly_wait(1)

                if(driver.current_url == "https://wis.hufs.ac.kr/src08/jsp/login/ValidPw.jsp?userId=jK1g2xT8Qtrs6jOiLz9u%2Bg%3D%3D&d=null&msg=%20&reurl=&REGNO=&ERPID=" + userid): # 로그인은 했으나 비밀번호 변경 알림이 뜨는 경우
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
                #elif (driver.current_url == "https://wis.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp") : # 비밀번호 틀린경우
                #    messagebox.showinfo()
                #    messagebox.showinfo(title="오류", message="아이디 혹은 비밀번호가 틀렸습니다")
                #elif(driver.current_url != "https://wis.hufs.ac.kr/src08/jsp/main.jsp?d=null") :
                else:
                    try : 
                        driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/button[2]').click()
                    except :
                        driver.close() # 팝업창 무시
                driver.switch_to.default_content()
                driver.switch_to.frame('left')
                driver.find_element_by_xpath('/html/body/div/div[2]/div')
                driver.switch_to.frame('MenuFrame')
                driver.find_element_by_xpath('/html/body/div/a[4]').click()
                driver.find_element_by_xpath('//*[@id="div23"]/a[2]').click()
                driver.execute_script("return fnWisMLog('/src08/jsp/grade/GRADE1030L_Main.jsp?tab_lang=K|성적취득현황')")
                driver.switch_to.default_content()
                driver.switch_to.frame('left')
                #ssn_source = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr/td/div[2]/table/tbody/tr[1]/td[2]')
                #use_ssn = ssn_source[4:6]
                #user_ssn = int(user_ssn) #user_ssn 새로 추가
                user_ssn = int(userid[2:4])
                name_source = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr/td/div[2]/table/tbody/tr[2]/td')
                user_name = name_source.text[2:] # user name
                major_source = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr/td/div[2]/table/tbody/tr[3]/td')
                major_source2 = major_source.text[5:].split('\n')
                user_college = major_source2[0]
                user_college = str(user_college) #user_college str화
                user_major = major_source2[1]
		
                choose = 0
		
                #driver.implicitly_wait(1)
                #time.sleep(1)
                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element_by_name('body'))
                driver.switch_to.frame(driver.find_element_by_name('top'))
                user_majors = driver.find_element_by_xpath('/html/body/div/form/div[2]/table/tbody/tr/td')

                if "전공심화(부전공)" in user_majors.text :
                    choose = 2
                elif "부전공" in user_majors.text :
                    choose = 1
                elif "이중전공" in user_majors.text :
                    choose = 3
                elif "1전공" in user_majors.text :
                    choose = 4
                else :
                    choose = 0
                #if '\n'  in user_majors.text :# 이중.부전공 선택한 사람
                #    if user_sub == "부전공" :choose = 1
                #    elif user_sub == "전공심화(부전공)" :choose = 2
                #    elif user_sub == "이중전공" :choose = 3
                #    else : choose = 0 # 이중.부전공 미선택자

                if choose != 4 : # 이중.부전공 선택자인경우
                    user_sub_major = user_majors.text.split(']')[-1][1:]
                    user_sub = (user_majors.text.split('[')[2]).split(']')[0]
                else : # 이중.부전공 미선택자인경우
                    user_sub = None
                    user_sub_major = None
                lista = ["1전공", "이중전공", "2전공", "실외", "교양", "부전공", "교직", "자선", "총취득"]
                #time.sleep(1)
		
                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element_by_name('body'))
                driver.switch_to.frame(driver.find_element_by_name('top'))
                driver.find_element_by_xpath('/html/body/div/form/div[1]/table/tbody/tr[2]')
		
                html = driver.page_source
                #bs = BeautifulSoup(html, 'html.parser')
                bs = BeautifulSoup(html, "lxml")
                tags = bs.findAll('td')
		
                user_grade = []
                for tag in tags :
                    user_grade.append(tag.text)
                user_grade = user_grade[1:10]
                user_grade = np.array(list(map(int,user_grade)))

                user_grade[7] += user_grade[2] + user_grade[3] + user_grade[6] # 2전공, 실외, 교직 카운트안함
                index = [2,3,6]
                user_grade = np.delete(user_grade,index)
                user_grade[2],user_grade[3] = user_grade[3],user_grade[2]

                requirement = connect_csv(user_college, user_ssn,choose) #여기서 왜 안들어갈까?
                requirement = np.delete(requirement, [0])
                remain = requirement - user_grade
                
                print(requirement.shape, user_grade.shape)

                credit = {'user':user_grade,'requirement':requirement, 'remain':remain}
                #print(credit)

#                df = pd.DataFrame(data = np.array([user_grade]),columns=lista)
#                df.to_csv("user_grade.csv", mode='w', encoding='utf-8-sig')#cp949
                user_college = str(user_college)
                user_major = str(user_major)
                user_sub = str(user_sub)
                user_sub_major = str(user_sub_major)
                #return jsonify({"학부": user_college," 학과 ": user_major," 선택학부 ": user_sub ," 부전공/이중전공  ": user_sub_major})
                #return json.dumps({"학부": user_college," 학과 ": user_major," 선택학부 ": user_sub ," 부전공/이중전공 ": user_sub_major,"잔여학점": remain}, ensure_ascii=False, indent=4)    
                remain = remain.tolist()
                driver.close()
                return json.dumps(remain, ensure_ascii=False, indent=4)
def connect_csv(user_college, user_ssn,choose) :
    import numpy as np
    import pandas as pd
    if user_ssn >= 19 and user_college == "바이오메디컬공학부":
        if choose == 1 : #부전공
            standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2019-_바이오메디컬공학부.csv'))
            return standard[1]
        elif choose == 2 : #부전공+전심
            standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2019-_바이오메디컬공학부.csv'))
            return standard[3]
        elif choose == 3 : #이중전공
            standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2019-_바이오메디컬공학부.csv'))
            return standard[0]
        elif choose == 4 : #전공심화
            standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2019-_바이오메디컬공학부.csv'))
            return standard[2]
    #csv와 비교 function
    else :
        if 8 <= user_ssn <= 14 :
            if user_college == "통번역대학" :
                if choose == 1 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_통번역대학.csv'))
                    return standard[1]
                elif choose == 2 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_통번역대학.csv'))
                    return standard[3]
                elif choose == 3 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_통번역대학.csv'))
                    return standard[0]
                elif choose == 4 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_통번역대학.csv'))
                    return standard[2]
                #csv와 비교 function 
            else :
                if choose == 1 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_외.csv'))
                    return standard[1]
                elif choose == 2 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_외.csv'))
                    return standard[3]
                elif choose == 3 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_외.csv'))
                    return standard[0]
                elif choose == 4 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2008-2014_외.csv'))
                    return standard[2]
                #csv와 비교 function
        elif user_ssn >= 15 :
            if user_college == "통번역대학" :
                if choose == 1 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_통번역대학.csv'))
                    return standard[1]
                elif choose == 2 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_통번역대학.csv'))
                    return standard[3]
                elif choose == 3 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_통번역대학.csv'))
                    return standard[0]
                elif choose == 4 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_통번역대학.csv'))
                    return standard[2]
                #csv와 비교 function
            elif user_college == "공과대학" :
                if choose == 1 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[1]
                elif choose == 2 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[3]
                elif choose == 3 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[0]
                elif choose == 4 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[2]
                #csv와 비교 function
            else :
                if choose == 1 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[1]
                elif choose == 2 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[3]
                elif choose == 3 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[0]
                elif choose == 4 :
                    standard = np.array(pd.read_csv('/home/ubuntu/project/excel/2015-_외.csv'))
                    return standard[2]
                #csv와 비교 function

#if __name__ == '__main__':
    #app.debug = False 
 #   pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
 #   pool.map(getInfo,result) 
    #app.run(host = '0.0.0.0', threaded = True, port = '8080')
    #app.run(host = '0.0.0.0',threaded = True)
