# InfoSec Inventory and Screenshots

When you deal with hundreds of IP and domain names, you can call many websites related to Infosec and do screen captures to organize and illustrate your findings.
Based on
1. Python 3
2. Nmap
3. Selenium

# Setup 

(I'm on Mac M1)

- Install chromium ( https://www.chromium.org/getting-involved/download-chromium )or adapt the config to your config ( chrome, chromium, brave, firefox, ... ) 
- Install NMap ( https://nmap.org/download.html )
- Install Python3 ( https://www.python.org/downloads/ ) and its libs ( Selenium, nmap, ... )
- Download the chromedrive related to your browser (https://chromedriver.chromium.org/downloads )

/ sudo python3 -m pip install selenium

/ brew install chromedriver

# 1. Start with domain name, list of IP and url in a file

"targets_all.txt"

Be clean in your file. I don't handle errors.

Supported today:
- www.test.com - subdomains (not urls)
- 1.1.1.1 - ipv4
- 10.0.10.0/24 - subnets
- example.com - domain

Unsupported:
- ipv6
- urls  (would be great)

# 2. With NMAP, scan your IP ranges and make basic reseaches
Based on your "target_all.txt" file :
- identify subdomains
- extract domains and do research on Shodan, Spyse, Hardenize, UrlScan, ...
- identify IP (alive and not responding)
- identify web services


# 3. Filter your findings by categories and take Screenshots

By generating specific "target_XXX.txt" files you can run queries.

- http - screenshot
- https - screenshot + Qualys SSL check
- bad protocols - rdp, telnet, ftp
- web file transfers
- web email related - imap, pop3, smtp, ... track with MxToolbox
- ...

# 4. Idealy create a basic report in MsWord with all that sh!t.
