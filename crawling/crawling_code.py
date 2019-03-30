# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 22:22:57 2019

@author: sehee
"""

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
binary = 'D:\\chromedriver.exe'
browser = webdriver.Chrome(binary)
browser.get("https://www.cardoc.co.kr/repair/after")
time.sleep(10)
image=[]
price=[]
text=[]
contents_cnt=1 
parts_cnt=1 
def car_doc(): # site join, crawling, parsing Function
    browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[1]/div/div/button/span[1]""").click() 
    time.sleep(10) 
    for i in range(1,8+1): # Choice which of car 
        browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div["""+str(i)+"""]/button""").click()
        time.sleep(5)         
        image=[]
        price=[]
        text=[]
        contents_cnt=1 
        parts_cnt=1
        
        for j in range(1,8+1): # Choice which of part for repair
            parts_path = 'd:\\KIA\\parts'+str(j)+'\\'
            os.mkdir( parts_path)                        
            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[3]/div["""+str(j)+"""]/button""").click()
            time.sleep(5)  
            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/button""").click()
            time.sleep(10)             
            more_view_button = 1
            
            for o in range(1, 3): # Specific page run
                if more_view_button==11:  # You can control how much you want 
                    button_finish=0 
                    while button_finish < 21:
                        for oo in range(1,10+1): 
                            oo1 = ( oo/10 + (button_finish+1) )*10
                            oo1 = int(oo1)
                            for bf in range(1, button_finish+1+1):
                                try:
                                    browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/div/button""").click()
                                    time.sleep(10)
                                except:
                                    break
                            try:
                                browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/ul/li["""+str(oo1)+"""]/div/div[1]/div/div""").click()
                                time.sleep(10)
                                html = browser.page_source 
                                time.sleep(10)
                                html = BeautifulSoup(html, "html.parser")                                 
                                time.sleep(10)
                                for idx, p in enumerate(html.find_all('div', class_='cd-cont'), 1 ): 
                                    x = p.get_text()
                                    price.append([ str(idx) + str('.')+ x ])        
                                for idx, t in enumerate( html.find_all('p', class_='cd-cont'),1 ):
                                    x = t.get_text()
                                    text.append([ str(idx) + str('.') + x.strip() ])
                                for idx, im in enumerate( html.find_all('img'),1 ): 
                                    if '.png' in im["src"]: # Png causes Error and That's no need.
                                        time.sleep(2)                            
                                        pass 
                                    else:
                                        image.append(im["src"]) 
                                        time.sleep(2)                                
                                final_path = parts_path+str(contents_cnt)+'\\'                                
                                save_image(final_path, image) # save_image Function
                                final_path2 = parts_path+'\\'+str(contents_cnt)
                                open_text(final_path2, price, text) # open_text Function
                                price=[]
                                text=[]
                                image = []
                            except:
                                pass
                                    
                            browser.get("https://www.cardoc.co.kr/repair/after")
                            time.sleep(10)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[1]/div/div/button/span[1]""").click() 
                            time.sleep(10)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div["""+str(i)+"""]/button""").click()
                            time.sleep(5)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[3]/div["""+str(j)+"""]/button""").click()
                            time.sleep(5)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/button""").click()
                            time.sleep(10)
                            contents_cnt+=1
                        button_finish +=1
                else:                    
                    for oo in range(1, 10+1): 
                        more_view_button+=1
                        try:
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[2]/div[2]/ul/li["""+str(oo)+"""]/div/div[1]/div/div""").click()
                            time.sleep(10)
                            html = browser.page_source 
                            time.sleep(10)
                            html = BeautifulSoup(html, "html.parser") 
                            time.sleep(10)
                            for idx, p in enumerate(html.find_all('div', class_='cd-cont'), 1 ): 
                                x = p.get_text()
                                price.append([ str(idx) + str('.')+ x ])
                            for idx, t in enumerate( html.find_all('p', class_='cd-cont'),1 ):
                                x = t.get_text()
                                text.append([ str(idx) + str('.') + x.strip() ])
                            for idx, im in enumerate( html.find_all('img'),1 ): 
                                if '.png' in im["src"]:
                                    time.sleep(2)                            
                                    pass 
                                else:
                                    image.append(im["src"]) 
                                    time.sleep(2)
                            final_path = parts_path+str(contents_cnt)+'\\'
                            save_image(final_path, image)
                            final_path2 = parts_path+'\\'+str(contents_cnt)
                            open_text(final_path2, price, text)
                            price=[]
                            text=[]
                            image = []
                            browser.get("https://www.cardoc.co.kr/repair/after")
                            time.sleep(10)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[1]/div/div/button/span[1]""").click() 
                            time.sleep(10) 
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div["""+str(i)+"""]/button""").click()
                            time.sleep(5)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[3]/div["""+str(j)+"""]/button""").click()
                            time.sleep(5)
                            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/button""").click()
                            time.sleep(10) 
                            contents_cnt+=1
                        except:
                            pass
            browser.get("https://www.cardoc.co.kr/repair/after")
            time.sleep(10)
            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div/div[1]/div/div/button/span[1]""").click() 
            time.sleep(10)            
            browser.find_element_by_xpath("""//*[@id="content"]/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div["""+str(i)+"""]/button""").click()
            time.sleep(5) 
            parts_cnt+=1
            contents_cnt=1
            
                                        
def save_image(path,image): 
    final_path = path
    os.mkdir(final_path)
    for idx, p in enumerate(image,1): 
        urllib.request.urlretrieve(p , final_path+str(idx)+".jpg")                    
        time.sleep(1)
    return print("save_image function complete!")

def open_text(path, price, text): 
    f =open(path+'.txt' , 'w', encoding='utf-8')
    for p in price: 
        f.write('%s' %(p) + '\n')        
    for t in text: 
        f.write('%s' %(t) + '\n')
    f.close() 
    return print("open_text function complete!")
car_doc()
browser.quit()  

