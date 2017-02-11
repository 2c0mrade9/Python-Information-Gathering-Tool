import os, time, io
from tld import get_tld
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

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

#get the top level domain name of the url submitted
def get_domain_name(url):
    domain_name = get_tld(url)
    return domain_name

#get the ip address of the url as submitted by the user
def get_ip_address(url):
    #run a system command
    command = "host " + url
    #fetch the results
    process = os.popen(command)
    results = str(process.read())
    #place a marker 
    marker = results.find('has address') + 11
    #get the results
    return results[marker:].splitlines()[0]

#run an nmap command
#[options]: what options are are you demanding from the user
#[ip]: the ipaddres gotten from get_ip_address(url)
def get_nmap(options, ip):
    command = "nmap " + options + " " + ip
    #fetch the results
    process = os.popen(command)
    results = str(process.read())
  
  
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


#finally set a root folder to use
ROOT_DIR = 'pentesting'

#create the root folder if it does not exist
create_dir(ROOT_DIR)


#gather the information
#[name]: The name of the project
#[url]: The url that we want to query
def gather_info(name, url):
    #set a time for the begining of the process
    print("[*] Fetching the top level domain name of ", url)
    domain_name = get_domain_name(url)

    print("[*] Fetching the ip adddress of the website...")
    ip_address = get_ip_address(url)

    print("[*] Running NMAP scan of the website...")
    nmap = get_nmap('-F', ip_address)

    print("[*] Fetching the robots.txt file on the website...")
    robots = get_robots(url)
    #robots = 'hello i am here and you are there';
    
    print("[*] Fetching the whois information...")
    whois = get_whois(domain_name)

    print("*" * 70)
    print("[*] CREATING REPORTS")
    
    #create a report
    create_report(name, url, domain_name, ip_address, nmap, robots, whois)

#function to create the report
def create_report(name, full_url, domain_name, ip_address, nmap, robots, whois):
    project_path = ROOT_DIR + '/' + name

    print("*" * 70)
    print("[*] Creating the project folder for ", name, " Website")
    create_dir(project_path)

    print("[*] Creating additional files for storing the information fetched")
    write_file(project_path + '/full_url.txt', full_url)
    write_file(project_path + '/domain_name.txt', domain_name)
    write_file(project_path + '/nmap.txt', nmap)
    write_file(project_path + '/robots.txt', robots)
    write_file(project_path + '/whois.txt', whois)

    print("[*] Scanning Completed at ", time.strftime("%I:%M:%S %p"))
    print("[*] Website Scanning completed")
    print("*" * 70)

#main function to call
def main_call():
    #print out some trash info... hahahaha
    print("*" * 70)
    print("[*] Emmallen Networks Scanner")
    print("[*] Scanning started at ", time.strftime("%I:%M:%S %p"))

    #get the name of the project
    project_name = input("Please enter the project name: ")

    #get the url to fetch the information from
    project_url = input("Please enter the web address of the website: ")
    
    gather_info(project_name, project_url)


#run the code
main_call();

  
  
