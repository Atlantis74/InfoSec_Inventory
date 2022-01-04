# InfoSec Inventory and Screenshots

When you deal with hundreds of IP and domain names, you can call many websites related to Infosec and do screen captures to organize and illustrate your findings.
Based on
1. Python 3
2. Nmap
3. Selenium

# Setup (I'm on Mac M1)

Install chromium or adapt the config to your config ( chrome, chromium, brave, firefox, ... ) 
Install NMap
Install Python3 and its libs
command : sudo python3 -m pip install selenium
command : brew install chromedriver


# With NMAP Scan your ranges and make basic reseaches.
- identify subdomains
- extract domains and do research on Shodan, Spyse, Hardenize, UrlScan, ...
- identify IP (alive and not responding)
- identify web services


# Filter your findings by categories and take Screenshots
- http - screenshot
- https - screenshot + Qualys SSL check
- bad protocols - rdp, telnet, ftp
- web file transfers
- web email related - imap, pop3, smtp, ... track with MxToolbox
- ...

# Idealy create a basic report in MsWord with all that sh!t.
