import os
import zipfile

from seleniumwire import webdriver
global driver
PROXY_HOST = ''  # rotating proxies ONLY!
PROXY_PORT = 8000
PROXY_USER = ''
PROXY_PASS = ''

runewild_mule_username = ""

path_to_chromedriver = ""

API_KEY = "" # your 2captcha api key to solve captchas with

data_sitekey = '6LclzxMUAAAAAJkbpofiE95kkDC3xgNRJHPPRi32' # **don't change**

from selenium.webdriver.support.ui import Select

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(
        path_to_chromedriver,
        chrome_options=chrome_options)
    return driver
import time


driver = get_chromedriver(use_proxy=False)

driver.get('https://roatpkz.com/vote/?continue=true&voteusername=' + runewild_mule_username)

script = """function getElementByXpath(path) { 
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

const rlocus = '//*[@id="wrapper"]/section/div/div[1]/div/a[1]'
const rspslist = "/html/body/div/section/div/div[1]/div/a[2]"
const moparscape = "/html/body/div/section/div/div[1]/div/a[3]"
const tophunnid = "/html/body/div/section/div/div[1]/div/a[4]"
const rspshunnid = "/html/body/div/section/div/div[1]/div/a[5]"


const rlocusurl = getElementByXpath('//*[@id="wrapper"]/section/div/div[1]/div/a[1]').getAttribute("href")
const rspslisturl = getElementByXpath(rspslist).getAttribute("href")
const moparscapeurl = getElementByXpath(moparscape).getAttribute("href")

const ret = rlocusurl + "|" + rspslisturl + "|" + moparscapeurl

return ret""" # inject a script into the roatpkz vote hub page to grab all
			  # the links so we don't have to actually go through any menus


response = driver.execute_script(script)
response = response.split('|')

runelocus = response[0]
rspslist = response[1]
moparscape = response[2]
print(response)



import time

import requests
status = "Waiting for a new Google Chrome developer instance..."
print(status)

driver.get(rspslist)
status = "Waiting for Google ReCaptchaV3 to load..."
print(status)
time.sleep(1)

status = "Sending Google ReCaptchaV3 captcha to 2captcha for solving."
print(status)


page_url = driver.current_url
u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
r1 = requests.get(u1)
rid = r1.json().get("request")

status = "Sent Google ReCaptchaV3 captcha to 2captcha for solving. Request #" + rid
print(status)

u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
time.sleep(1)
status = "Waiting for a 2captcha worker to solve the captcha."
print(status)

while True:
    r2 = requests.get(u2)
    #print(r2.json())
    if r2.json().get("status") == 1:
        form_token = r2.json().get("request")
        break
    time.sleep(1)



status = "Captcha solved, injecting pre-solved ReCaptchaV3 token: " + form_token
print(status)

js_token_write = f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'
driver.execute_script(js_token_write)

driver.execute_script("document.getElementById('g-recaptcha-response').value = '" + form_token + "';")

status = "Bypassing time countdown and anti-botted captcha check."
print(status)
time.sleep(1.3)

btn_script = """
const response_token = '""" + form_token + """'
console.log("response token is " + response_token)
await VisioList.ajax('https://www.rsps-list.com/plugins/ReCaptcha/ajax_base.php', 'POST', { token: response_token }).then(response => {
					
			document.getElementById('g-recaptcha-response').value = response.token;
			vote_button.dataset.recaptcha = true;	
			doVote();
			console.log("returning " + response_token)
						
		}).catch(error => {
			//window.location = link;
			console.log(error);
		});


		return response_token"""
response = driver.execute_script(btn_script)
status = "Button activated, custom RSPS-List response token: " + response
print(status)

time.sleep(3)

print("Submitting...")

submitbutton = driver.find_element_by_xpath('/html/body/main/section[2]/div/div[2]/div/div/div/form/div[2]/div[1]')



time.sleep(0.5)
submitbutton.click()
time.sleep(4)
#driver.get('https://roatpkz.com/vote/?continue=true&voteusername=RTX3080')

#time.sleep(2)


# Start Moparscape Vote

#/html/body/main/div/section/div[2]/strong/div[1]/div/form/button[1]
driver.get(moparscape)


status = "Waiting for Google ReCaptchaV3 to load..."
print(status)
time.sleep(1)

status = "Sending Google ReCaptchaV3 captcha to 2captcha for solving."
print(status)


page_url = "https://www.moparscape.org/rsps-list/server/roatpkz"
u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={page_url}&json=1&invisible=1"
r1 = requests.get(u1)
#print(r1.json())
rid = r1.json().get("request")

status = "Sent Google ReCaptchaV3 captcha to 2captcha for solving. Request #" + rid
print(status)

u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
time.sleep(1)
status = "Waiting for a 2captcha worker to solve the captcha."
print(status)

while True:
    r2 = requests.get(u2)
    #print(r2.json())
    if r2.json().get("status") == 1:
        form_token = r2.json().get("request")
        break
    time.sleep(1)



status = "Captcha solved, injecting pre-solved ReCaptchaV3 token: " + form_token
print(status)

js_token_write = f'document.getElementById("g-recaptcha-response").innerHTML="{form_token}";'
driver.execute_script(js_token_write)

driver.execute_script("document.getElementById('g-recaptcha-response').value = '" + form_token + "';")

time.sleep(1.5)
print("Done, submitting...")


submitbutton = driver.find_element_by_xpath('/html/body/main/div/section/div[2]/strong/div[1]/div/form/button[1]')




submitbutton.click()
time.sleep(4)
driver.get('https://roatpkz.com/vote/?continue=true&voteusername=' + runewild_mule_username)



import os
from mimetypes import guess_extension




from urllib.parse import urlparse

def download_assets(requests, # https://stackoverflow.com/questions/49627458/python-selenium-download-images-jpeg-png-or-pdf-using-chromedriver
							  # 02/2020 bypass anti-bot countdown on runelocus
                   asset_dir="temp",
                   default_fname="unnamed",
                   exts=[".png", ".jpeg", ".jpg", ".svg", ".gif", ".pdf", ".bmp", ".webp", ".ico"],
                   append_ext=False):
    asset_list = {}
    for req_idx, request in enumerate(requests):
        # request.headers
        # request.response.body is the raw response body in bytes
        if request is None or request.response is None or request.response.headers is None or 'Content-Type' not in request.response.headers:
            continue
            
        ext = guess_extension(request.response.headers['Content-Type'].split(';')[0].strip())
        if ext is None or ext == "" or ext not in exts:
            #Don't know the file extention, or not in the whitelist
            continue
        parsed_url = urlparse(request.url)
        
        if skip:
            continue
        
        frelpath = parsed_url.path.strip()
        if frelpath == "":
            timestamp = str(datetime.datetime.now().replace(microsecond=0).isoformat())
            frelpath = f"{default_fname}_{req_idx}_{timestamp}{ext}"
        elif frelpath.endswith("\\") or frelpath.endswith("/"):
            timestamp = str(datetime.datetime.now().replace(microsecond=0).isoformat())
            frelpath = frelpath + f"{default_fname}_{req_idx}_{timestamp}{ext}"
        elif append_ext and not frelpath.endswith(ext):
            frelpath = frelpath + f"_{default_fname}{ext}" #Missing file extension but may not be a problem
        if frelpath.startswith("\\") or frelpath.startswith("/"):
            frelpath = frelpath[1:]
        
        fpath = os.path.join(asset_dir, parsed_url.netloc, frelpath)
        if os.path.isfile(fpath):
            continue
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        
        if "vote-captcha" in fpath:
        	fpath = "temp/captcha.png"
        	print(f"Downloading {request.url} to {fpath}")
        	asset_list[fpath] = request.url
	        try:
	            with open(fpath, "wb") as file:
	                file.write(request.response.body)
	        except:
	            print(f"Cannot download {request.url} to {fpath}")
    return asset_list





asset_dir = "temp"





#driver.close()



	#submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')








def continuefinal(driver):
	#global root
	#root.quit()
	submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
	print("Submitting...")
	submitbutton.click()
	print("Completed the vote.")
	return True










def selectfive(driver):

	while True:
		time.sleep(0.3)
		selectionbox = driver.find_elements_by_xpath('/html/body/section/div[2]/div/div/div[2]/form/center/div[2]/div/div[3]/select[2]')[0]

		submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
		select = Select(selectionbox)
		select.select_by_visible_text('5 items')
		break
	continuefinal(driver)


def selectthree(driver):

	while True:
			time.sleep(0.3)
			selectionbox = driver.find_elements_by_xpath('/html/body/section/div[2]/div/div/div[2]/form/center/div[2]/div/div[3]/select[2]')[0]

			submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
			select = Select(selectionbox)
			select.select_by_visible_text('3 items')
			break
	continuefinal(driver)

def selectfour(driver):


	while True:
			time.sleep(0.3)
			selectionbox = driver.find_elements_by_xpath('/html/body/section/div[2]/div/div/div[2]/form/center/div[2]/div/div[3]/select[2]')[0]

			submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
			select = Select(selectionbox)
			select.select_by_visible_text('4 items')
			break
	continuefinal(driver)



def selecttwo(driver):

	while True:
			time.sleep(0.3)
			selectionbox = driver.find_elements_by_xpath('/html/body/section/div[2]/div/div/div[2]/form/center/div[2]/div/div[3]/select[2]')[0]

			submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
			select = Select(selectionbox)
			select.select_by_visible_text('2 items')
			break
	continuefinal(driver)


def selectone(driver):


	while True:
			time.sleep(0.3)
			selectionbox = driver.find_elements_by_xpath('/html/body/section/div[2]/div/div/div[2]/form/center/div[2]/div/div[3]/select[2]')[0]

			submitbutton = driver.find_element_by_xpath('//*[@id="submitbutton"]')
			select = Select(selectionbox)
			select.select_by_visible_text('1 item')
			break
	continuefinal(driver)


def runrunelocus(name, url, alwaysretry = True):
	#driver = webdriver.Chrome(r'C:\Users\Admin\.wdm\drivers\chromedriver\win32\89.0.4389.23\chromedriver.exe')#,seleniumwire_options=options) 

	'''


	root = tk.Tk()
	root.geometry("400x400")

	canvas = Canvas(root, width=800, height=400)
	canvas.pack()
	'''

	#imagetest = PhotoImage(file="temp/captcha.png")
	import matplotlib.pyplot as plt
	import matplotlib.image as mpimg
	#driver = webdriver.Chrome(r'C:\Users\Admin\.wdm\drivers\chromedriver\win32\89.0.4389.23\chromedriver.exe')#,seleniumwire_options=options) 



	from twocaptcha import TwoCaptcha

	global done
	done = alwaysretry
	while done:

		time.sleep(0.5)
		try:
			driver.close()
		except:
			pass
		driver = get_chromedriver()
		driver.get(url)#'https://www.runewild.com/vote/?site=1&name=' + name)
		print("Waiting for captcha...")
		time.sleep(3)
		download_assets(driver.requests, asset_dir=asset_dir)
		time.sleep(3)
		config = {
		    		'apiKey':           API_KEY,
		    		'recaptchaTimeout':  45
			    }
		solver = TwoCaptcha(**config)
		print("Waiting for 2captcha worker")
		try:
			result = solver.normal('temp/captcha.png', textInstructions="How many video game objects are shown over the handwashing image? (1 to 5, objects can overlap)", minLength = "1", maxLength = "1", numeric="1")
			
		except:
			print("error solving captcha (bad worker), retrying")
			continue
		id = result['captchaId']
		print("result: ", result)

		result = result['code']
		if len(result) > 1 or int(result) > 5:
			print("failed, trying again")
			solver.report(id, False)
		result = int(result)
		if result == 1:
			selectone(driver)
		elif result == 2:
			selecttwo(driver)
		elif result == 3:
			selectthree(driver)
		elif result == 4:
			selectfour(driver)
		elif result == 5:
			selectfive(driver)
		else:
			print("result ",result," doesnt make sense")
			continue
		time.sleep(1)
		if "You did not pass the anti-robot check." in driver.page_source:
			print("failed, trying again")
			solver.report(id, False)
		else:
			print("Verified the vote.")
			break






driver.close()
runrunelocus(runewild_mule_username,runelocus,True)



print("Voted on all three websites, claiming vote on roatpkz...")

try:
	driver.close()
except:
	pass

from selenium import webdriver
driver = get_chromedriver()

driver.get('https://roatpkz.com/vote/?continue=true&voteusername=' + runewild_mule_username)



submitbutton = driver.find_element_by_xpath('/html/body/div[1]/section/div/div[1]/div/div[2]/a/button') # claim vote button, votes need to be claimed on roatpkz for some reason

submitbutton.click()

driver.close()

print("Voted on all websites and claimed the vote.")