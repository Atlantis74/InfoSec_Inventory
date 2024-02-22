from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from time import sleep

#  sudo python3 -m pip install selenium
#  brew install chromedriver
#  or go to https://chromedriver.chromium.org/downloads
#  install chromium https://www.google.com/intl/en/chrome/canary/ 

capture_location="./capture/" # Don't forget the / ate the end to force the Folder.

targets_file_all="targets_ip.txt"
targets_file_http="targets_http.txt"
targets_file_https="targets_https.txt"
targets_file_domains="targets_domains.txt"
search_subdomaines="No"
take_screenshoots="No" # This is lighter, but remove interesting findings



# By domain, collect the DNS information (Hosts, MX, CNAME, Dname, TXT, SPF, DMARK ... )
# By domain check the domain to the different engines.
# By domain, list subdomains (Yes/NO)
# By host discovered, check the IP (to merge) similar site IP together
# By host discovered, check if the host is behind Cloudflare or Akamai
# By host, check if the host is behind a reverse proxy 
# Create a list of "targets" with domain, IP, url, status(alive,proxied,notresponding,blacklist)
# By host, check if the host is a 'Microsoft Office 365 service" is yes, exclude the host of the 'alive' list
# By host in "targets" we ping and define the open ports ( Shodan, NMap, ...) to be sure the host is 'alive'
# If host common port is/are open or ping we can consider the host 'alive'
# Updat the list "targets" with openports
# By alive host take screenshot of websites (80 and 443, but also RDP etc)
# By alive host for HTTPS check the certificate status
# By alive host determine the technologie in place ( and do a security scan in relation - wordress, joomla, drupa, RDP, ... )

def site_screenshot(target_url,time_wait,capture_file_name):
    
    # For Selenium (working on Mac M1 with Chromium)
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"
    options.headless = False   # Put to True to hide the Window
    chrome_driver_binary = "./chromedriver.exe"
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
    
#     shodan.io             v
#     mxtoolbox.com         v
#     wigle.net
#     grep.app
#     app.binaryedge.io
#     onyphe.io
#     viz.greynoise.io
#     censys.io             v
#     hunter.io
#     fofa.info
#     zoomeye.org
#     leakix.net
#     intelx.io
#     app.netlas.io
#     searchcode.com
#     urlscan.io            v
#     publicwww.com
#     fullhunt.io
#     socradar.io
#     binaryedge.io
#     tivre.rocks
#     crt.sh
#     vulners.com
#     pulsedive.com
#     spice.com             RIP
#     hardenize.com         v
    

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
        
        print("... End of loop for Tools .... for : "+domain)       
    print("Well done for domains")
    print("End of the Tools sections ")



print("End of Script")
