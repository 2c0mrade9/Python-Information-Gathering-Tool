import os, time, io, sys, re
from tld import get_tld
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

#function to print out the usage
def printUsage():
    # print out how to use the programe
    print ("""
    Usage:
      python file.py [options]
            option 1 - project name<br>
            option 2 - host address (http://www.mywebsite.com)
            option 3 - information gathering style [Ping (p) or Host (h)]
            option 4 to 7 - nmap options [-F; -T4 -F, -T4 -A -v, -O]
            
      Example of Sample Commands
      python info_gathering.py help --> (_this displays the usage information_)
      (__*help options*__ _h_, _-h_, _--h_, _help_, _-help_, _--help_)
      python info_gathering.py newproject
      
      python info_gathering.py first-project http://www.mywebsite.com h -F -v
         """)

def lineBreak(symbol, multiply):
    print(symbol * multiply)

#First of all we want to save our entire Info Gathering Project in a separate folder
#create a directory
def create_dir(directory):
    #check if the directory already exists
    if not os.path.exists(directory):
        os.makedirs(directory)

#write a simple file
def write_file(path, data):
    #path: where you want to save the file
    #data: the data that you want to save
    f = open(path, 'w')
    f.write(data)
    f.close()

#first set a root folder to use
ROOT_DIR = 'pentesting'

#create the root folder if it does not exist
create_dir(ROOT_DIR)

#get the top level domain name of the url submitted
def get_domain_name(url):
    #fetch the top level domain name
    domain_name = get_tld(url)
    #return the domain name
    return domain_name

#get the ip address of the url as submitted by the user
def get_ip_address(url):

    #check if the user supplied it in the command line
    if len(sys.argv) > 3:
        user_response = sys.argv[3]
    else:
        #ask the user what command to use
        user_response = str(input("What command do you want to run? Ping (p) or Host (h): "))

    #check if the user submitted h as response
    if user_response == 'h':
        #run a system command
        command = "host " + url
    #check if the user submitted p as response
    elif user_response == 'p':
        #run a system command
        command = "ping " + url
    else:
        lineBreak("-", 70)
        print("You have selected a wrong input\n")
        #call the function again
        get_ip_address(url)
        
    #print out information to the screen
    print("[*] Fetching the ip adddress of the website...")
        
    try:
        #fetch the results
        process = os.popen(command)
        results = str(process.read())
        
        #place a marker for host results
        if user_response == 'h':
            marker = results.find('has address') + 11
            #get the results
            return results[marker:].splitlines()[0]
        #place a marker for ping results
        else:
            marker = results.find('statistics for') + 14
            result = results[marker:].splitlines()[0]
            #return the results
            return result.replace(':', '')
    except:
        pass
        

#run an nmap command
#[options]: what options are are you dmanding from the user
#[ip]: the ipaddres gotten from get_ip_address(url)
def get_nmap(ip):
    #ask the user for the options to use
    options = ''
    
    if len(sys.argv) > 4:
        options = re.sub('[\',[\]]','', str(sys.argv[4:7]))
    else:
        #get the user response
        user_response = str(input("What nmap options do you wish to use? Default (d) Help (h) "))
        
        #check if the user needs help
        if user_response == 'h':
            print("-" * 70)
            print("""
    [***]These are the various options that are available to you [***]
    SCAN TECHNIQUES:
       -F: Fast Scans
       -sU: UDP Scan
       -sN/sF/sX: TCP Null, FIN, and Xmas scans
       -sO: IP protocol scan
       -b <FTP relay host>: FTP bounce scan
    PORT SPECIFICATION AND SCAN ORDERS
       -p <port ranges>: Only scan specified ports
           Eg: -p22; -p1-65535;
       -r: Scan ports consecutively - don't randomize
    SERVICE / VERSION DETECTION:
       -sV: Probe open ports to determine service / version info
    OS DETECTION:
       -O: Enable OS detection
    OTHER SCANS
       -A: Enable OS detection, version detection, script scanning, and traceroute
       (This option is very cool to use)

    DEFAULT OPTIONS
       -T4 -A -v
           """)
            print("-" * 70)
            get_nmap(ip)
        #check if the user wants to go for the default options
        elif user_response == 'd':
            options = "-T4 -A -v"
        else:
            options = user_response
        
    print("[*] Running NMAP scan on the website... [***]: nmap " + options + " " + ip)

    #run the command
    command = "nmap " + options + " " + ip
    #fetch the results
    process = os.popen(command)
    results = str(process.read())

    return results
  
  #fetch the robots file on the website
def get_robots(url):
    results = ''
    
    if url.endswith('/'):
        path = url
    else:
        path = url + '/'

    try:
        link = path + "robots.txt"
        f = urlopen(link)
        data = io.TextIOWrapper(f, encoding='utf-8')
        #return req
        results = data.read()
        return results
    except HTTPError as e:
        return "Error code: ", e.code
    except URLError as e:
        results = "Reason: ", e.reason
    else:
        return ""

#run a whois command on the website
def get_whois(url):
    #set a command to use
    command = "whois " + url
    #fetch the results
    process = os.popen(command)
    results = str(process.read())

    return results

#gather the information
#[name]: The name of the project
#[url]: The url that we want to query
def gather_info(name, url):
    #start calculating the time
    print("[*] Scanning Started at ", time.strftime("%I:%M:%S %p"))

    #try to fetch the top level domain name
    try:
        #set a time for the begining of the process
        print("[*] Fetching the top level domain name of ", url)
        domain_name = get_domain_name(url)
    except:
        #print out error message
        printUsage()
        sys.exit(1)
    print("Done!\n")
       
    ip_address = get_ip_address(domain_name)
    print("Done!\n")

    #run an nmap scan against the target
    nmap = get_nmap(ip_address)
    print("Done!\n")

    print("[*] Fetching the robots.txt file on the website...")
    robots = get_robots(url)
    print("Done!\n")
    
    print("[*] Fetching the whois information...")
    whois = get_whois(domain_name)
    print("Done!\n")

    lineBreak("*", 70)
    print("[*] CREATING REPORTS")
    
    #create a report
    create_report(name, url, domain_name, ip_address, nmap, robots, whois)

#function to create the report
def create_report(name, full_url, domain_name, ip_address, nmap, robots, whois):
    project_path = ROOT_DIR + '/' + name

    lineBreak("*", 70)
    print("[*] Creating Project Folder: ", name)
    create_dir(project_path)

    print("[*] Creating additional files for storing the information fetched")
    write_file(project_path + '/full_url.txt', full_url)
    write_file(project_path + '/ip_address.txt', "The IP address of " + full_url + " is: \n" + ip_address)
    write_file(project_path + '/domain_name.txt', "Top level domain name: \n" + domain_name)
    write_file(project_path + '/nmap.txt', nmap)
    write_file(project_path + '/robots.txt', robots)
    write_file(project_path + '/whois.txt', whois)

    print("[*] Scanning Completed at ", time.strftime("%I:%M:%S %p"))
    print("[*] Host Name Scanning completed")
    lineBreak("-", 70)
    print("[*] Host Name Scanning completed")
    
    lineBreak("*", 70)

#main function to call
def main_call():
    #print out some trash info... hahahaha
    lineBreak("*", 70)
    print("[*] Emmallen Networks Scanner")
    print("""[*] Scan a web host for the following information:
  Top Level Domain Name, IP Address, NMAP Scan for Open Ports and Services,
  Whois Information and Download the robots.txt file.""")
    lineBreak("*", 70)

    #help list names
    help_list = ['h', '-h', '--h', 'help', '-help', '--help']
    
    try:
        #check if the user provided a name using the command line interface
        if len(sys.argv) > 1:
            #check the very first variable if its help or -help
            if sys.argv[1] in help_list:
                #print out the help window
                printUsage()
                #close the session
                sys.exit(1)
            else:
                project_name = sys.argv[1]
        else:
            #get the name of the project
            project_name = input("Please enter the project name: ")
        
        #confirm the string length of the user input
        if len(project_name) < 3:
            lineBreak("-", 70)
            print("PLEASE THE PROJECT NAME SHOULD BE AT LEAST 3 CHARACTERS")
            print(" "*5," restarting the process...")
            lineBreak("-", 70)
            main_call()

        #check if the user provided a website address in the command line interface
        if len(sys.argv) > 2:
            project_url = sys.argv[2]
        else:    
            #get the url to fetch the information from
            project_url = input("Please enter the web address of the website: ")

        lineBreak("-", 70)
        #star gathering the information
        gather_info(project_name, project_url)

    #print error if the user cancels the process
    except KeyboardInterrupt:
        lineBreak("-", 70)
        print("[*] You interrupted the process by pressing CTRL + C")
        sys.exit(1)

#run the code
main_call();
