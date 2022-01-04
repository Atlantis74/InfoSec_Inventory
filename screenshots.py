from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from time import sleep

#  sudo python3 -m pip install selenium
#  brew install chromedriver


capture_location="capture/" # Don't forget the / to force the Folder.

targets_file_all="targets_all.txt"
targets_file_http="targets_http.txt"
targets_file_https="targets_https.txt"
targets_file_domains="targets_domains.txt"


def site_screenshot(target_url,time_wait,capture_file_name):
    
    # For Selenium (working on Mac M1 with Chromium)
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
    options.headless = False   # Put to True to hide the Window
    chrome_driver_binary = "./chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    try:
        driver.get(target_url)
        
        driver.maximize_window()
        
        #get window size
        s = driver.get_window_size()
        #obtain browser height and width
        w = driver.execute_script('return document.body.parentNode.scrollWidth')
        h = driver.execute_script('return document.body.parentNode.scrollHeight')
        #set to new window size
        driver.set_window_size(w, h)
        #obtain screenshot of page within body tag
        driver.find_element_by_tag_name('body').screenshot(capture_location+"_"+capture_file_name+".png")
        driver.set_window_size(s['width'], s['height'])
        sleep(time_wait)
        
        # Capture
        print(capture_location+"_"+target_url+capture_file_name+".png")
        driver.get_screenshot_as_file(capture_location+"_"+capture_file_name+".png")    
        print("... "+capture_file_name+" done.")
    except WebDriverException:
        print("... page down")
        sleep(1)
    driver.quit


# Parse the HTTP file Line by Line for ScreenShots (Webpage port 80)
with open(targets_file_http, 'r') as f: # r for READ
    lines = f.readlines()
    #print(lines)
    count = 0
    for line in lines:
        count += 1
        url = line.strip() # strip to only read the line without /n and not as array (striplines())
    #
        target_url="http://"+url
        site_screenshot(target_url,5,url+"_HTTP")
        print("... End of HTTP capture " + url)

# Parse the HTTPS file Line by Line to prepare the SSL Qualys Cert check 
# (it takes time and must be launch before screenshot)
with open(targets_file_https, 'r') as f: # r for READ
    lines = f.readlines()
    #print(lines)
    count = 0
    for line in lines:
        count += 1
        url = line.strip() # strip to only read the line without /n and not as array (striplines())
        print("The URL is :"+url)
        
        # Call for Qualys - if not cached it triggers a long query
        target_url="https://www.ssllabs.com/ssltest/analyze.html?d="+url
        site_screenshot(target_url,8,url+"_QUALYS")
        print("... End of loop Qualys for : "+url)
        
    print("Sleep 60") # Long sleep to allow Qualys to generate the Cert report.
    sleep(60)
    print("End of the Qualys activation")

# Parse the HTTPS file Line by Line for ScreenShots (Webpage and qualys)
with open(targets_file_https, 'r') as f: # r for READ
    lines = f.readlines()
    #print(lines)
    count = 0
    for line in lines:
        count += 1
        url = line.strip() # strip to only read the line without /n and not as array (striplines())
        
         # Call for Qualys result - previously called
        target_url="https://"+url
        time_wait=5
        capture_name="_HTTPS"
        target_url="https://"+url
        site_screenshot(target_url,5,url+"_HTTPS")
        
        # Call for Qualys result - previously called
        target_url="https://www.ssllabs.com/ssltest/analyze.html?d="+url
        site_screenshot(target_url,5,"_QUALYS")
        
    print("End of HTTPS and QUALYS capture")



# Parse the DOMAIN file line by line to query some important web tools.
with open(targets_file_domains, 'r') as f: # r for READ
    lines = f.readlines()
    #print(lines)
    count = 0
    for line in lines:
        count += 1
        domain = line.strip() # strip to only read the line without /n and not as array (striplines())
        print("The current domain is : "+domain)
    #
        # Call for URLScan
        target_url="https://urlscan.io/search/#"+domain
        site_screenshot(target_url,8,domain+"_URLScan")
    #
        # Call for Shodan 
        target_url="https://www.shodan.io/search?query="+domain
        site_screenshot(target_url,7,domain+"_Shodan")
    #
        # Call for MxToolbox 
        target_url="https://mxtoolbox.com/emailhealth/"+domain+"/"
        #site_screenshot(target_url,15,domain+"_MXToolbox")
    #   
        # Call for Spyse - Domain
        target_url="https://spyse.com/search?target=domain&query="+domain
        site_screenshot(target_url,15,domain+"_Spyse_Domain")
        # Call for Spyse - Certificate SLL
        target_url="https://spyse.com/search?target=cert&query="+domain
        site_screenshot(target_url,15,domain+"_Spyse_Cert")
    #
        # Call for Censys 
        target_url="https://search.censys.io/certificates?q="+domain
        site_screenshot(target_url,15,domain+"_Censys_Cert")
    #
        # Call for Hardenize - if not cached it triggers a long query
        target_url="https://www.hardenize.com/report/"+domain
        time_wait=35
        site_screenshot(target_url,35,domain+"_Hardenize")
        
        print("... End of loop Hardenize, Spyse, Shodand, MxToolbox .... for : "+domain)       
    print("Well done for domains")
    print("End of the Hardenize, Spyce, Shodan, MxToolbox list, ... ")



print("End of Script")
