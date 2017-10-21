#login using post

from selenium import webdriver
br=webdriver.Chrome('/Applications/chromedriver')
br.get("https://www.facebook.com/login")
email=br.find_element_by_name("email")
email.send_keys('youremail')
pas=br.find_element_by_name("pass")
pas.send_keys('yourpassword')
l_button=br.find_element_by_name("login")
l_button.click()
