# Information-Gathering
This script helps you as a hacker to gather information very easy and really quick...

This file contains 5 fucntions fro the information gathering<br>
def   1. domain_name<br>
      2. ip address<br>
      3. nmap<br>
      4. robots file download<br>
      5. whois information<br>
You must supply a valid domain name

#USAGE 
Usage:<br>
      python file.py [options]<br> 
      option 1 - project name<br>
      option 2 - host address (http://www.mywebsite.com) -> should be a valid address<br>
      option 3 - information gathering style [Ping (p) or Host (h)]<br>
      option 4 - nmap options [-F; -T4 -F, -T4 -A -v, -O] --> Any valid one nmap options apply<br>
      
      Simple Command
      python filename full_website_address
      
      Example:
      python info_gathering.py first-project http://www.mywebsite.com h -F
