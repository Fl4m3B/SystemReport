'''
Cameron Ingle
NSSA 221 Sec. 5
Prof. A
10/4/2024
SCRIPT 02
'''


from datetime import date
import os
import distro
import platform
import shutil
import socket
import subprocess
import sys


RED = "\033[31m"    #For terminal formatting
GREEN = "\033[32m"  #For terminal formatting
RESET = "\033[0m"   #For terminal formatting


log = open( '/home/cvi3132_system_report.log', 'a' )	#Open log file with write permissions


def log_and_term( info ):	#New print function that writes to terminal and log file
    sys.__stdout__.write( info )
    log.write( info )
    #sys.__stdout__.flush()
    


print = log_and_term	#Re-define the print function to use log_and_term


def find_gateway(): #Helper function to find Default Gateway
    meta = subprocess.run( ["ip", "r"], capture_output = True, text = True )
   
    parse = meta.stdout.strip().split( "\n" )
    for piece in parse:
        if "default via" in piece:
            gateway = piece.split()[2]
            return gateway
    
    return None


def find_netmask( interface ):	#Find the netmask by using ifconfig, search through output to find netmask on given interface
    meta = subprocess.check_output( ['ifconfig', interface] ).decode()
    
    fullparse = meta.split( '\n' )
    
    for line in fullparse:
        if 'netmask' in line:
            return line.split( ' ' )[-4]


def find_dns():	#Find DNS servers by parsing through the output in /etc/resolv.conf
    serverlist = []
    
    with open( '/etc/resolv.conf', 'r' ) as f:
        for line in f:
            if line.startswith('nameserver'):
                server = line.split()[1]
                serverlist.append( server )
    
    return serverlist
  
  
def find_device_info():	#Find and print the hostname and domain
    print( GREEN + '\nDevice Information' + RESET )
    
    hostname = socket.gethostname().split( '.' )[0]
    domain = os.popen( 'hostname --domain' ).read().strip()
    
    print( '\nHostname:\t\t\t' + hostname )
    print( '\nDomain:\t\t\t\t' + domain )


def find_network_info():	#Find network information using helper functions and socket module
    print( GREEN + '\nNetwork Information' + RESET )
    
    hostname = socket.gethostname()
    ip_ad = socket.gethostbyname( hostname )
    def_gate = find_gateway()
    netmask = find_netmask( 'ens33' )
    dns_servers = find_dns()
    
    print( '\nIP Address:\t\t\t' + ip_ad )
    print( '\nGateway\t\t\t\t' + def_gate )
    print( '\nNetwork Mask\t\t\t' + netmask )
    print( '\nDNS1:\t\t\t\t' + dns_servers[0] )
    #print( '\nDNS2:\t\t\t\t' + dns_servers[1] )
    
    
def find_os_info():	#Use os module and distro to find OS information
    print( GREEN + '\nOS Information' + RESET )
    
    os_details = os.uname()
    os_cur = os_details.sysname
    os_ver = distro.version()
    os_kern_ver = os_details.release
    
    print( '\nOperating System:\t\t' + os_cur )
    print( '\nOperating Version:\t\t' + os_ver )
    print( '\nKernel Version\t\t\t' + os_kern_ver )
    
    
def find_storage_info():	#Make use of shutil to find disk information, convert to GB, and print results
    print( GREEN + '\nStorage Information' + RESET )
    
    total, used, avail = shutil.disk_usage( '/' )
    
    totalgbf = str( total / ( 1024 ** 3 ) )
    availgbf = str( avail / ( 1024 ** 3 ) )
    totalgb = totalgbf.split( '.' )[0]
    availgb = availgbf.split( '.' )[0] 
    
    print( '\nHard Drive Capacity:\t\t' + totalgb + 'G' )
    print( '\nAvailable Space\t\t\t' + availgb + 'G' )
    
    
def find_proccessor_info():	#Make use of the /proc/cpuinfo file to find processor information
    print( GREEN + '\nProcessor Information' + RESET )
    
    all = []
    cores = 0
    processors = 0
    
    with open( '/proc/cpuinfo', 'r' ) as f:
        for line in f:
            if line.startswith( 'model name' ):
                model = line.split( ':' )[1].strip()
                all.append( model )
            elif line.startswith( 'processor' ):
                processors += 1
                
    cores = len( all )
    
    print( '\nCPU Model:\t\t\t' + all[0] )
    print( '\nNumber of processors\t\t' + str( processors ) )
    print( '\nNumber of cores\t\t\t' + str( cores ) )
    
    
def find_memory_info():	#Parse through output from free -h to retrieve memory information
    print( GREEN + '\nMemory Information' + RESET )
    
    meta = subprocess.check_output( ['free', '-h'] ).decode()
    
    pre_parse = meta.split('\n')
    full_parse = pre_parse[1].split()
    
    total_ram = full_parse[1]
    available_ram = full_parse[3]
    
    print( '\nTotal RAM\t\t\t' + total_ram )
    print( '\nAvailable RAM\t\t\t' + available_ram + '\n' )
    
    
def main():
    os.system( 'clear' )	#Clear terminal
    
    today = str( date.today() )	#Get today's date
    print( RED + '\t\tSystem Report - ' + today + RESET )
    
    find_device_info()
    find_network_info()
    find_os_info()		#Run functions to find all information
    find_storage_info()
    find_proccessor_info()
    find_memory_info()

    log.close()			#Close log file
    exit()			#Exit program


main()

