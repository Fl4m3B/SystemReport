from datetime import date
import os
import distro
import platform
import logging
import shutil
import socket
import subprocess
import sys


RED = "\033[31m"    #For terminal formatting
GREEN = "\033[32m"  #For terminal formatting
RESET = "\033[0m"   #For terminal formatting

#Set a logger
logger = logging.getLogger(__name__)
logger.setLevel( logging.INFO )

#Add a file handler for file output
file_handler = logging.FileHandler( "report.log" )
file_handler.setLevel( logging.INFO )
logger.addHandler( file_handler )
logger.porpagate = False

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
    logger.info( GREEN + '\nDevice Information' + RESET )

    hostname = socket.gethostname().split( '.' )[0]
    domain = os.popen( 'hostname --domain' ).read().strip()
    
    print( 'Hostname:\t\t\t' + hostname )
    logger.info( 'Hostname:\t\t\t' + hostname )
    print( 'Domain:\t\t\t\t' + domain )
    logger.info( 'Domain:\t\t\t\t' + domain )


def find_network_info():	#Find network information using helper functions and socket module
    print( GREEN + 'Network Information' + RESET )
    logger.info( GREEN + 'Network Information' + RESET )
    
    hostname = socket.gethostname()
    ip_ad = socket.gethostbyname( hostname )
    def_gate = find_gateway()
    netmask = find_netmask( 'ens33' )
    dns_servers = find_dns()
    
    print( 'IP Address:\t\t\t' + ip_ad )
    logger.info( 'IP Address:\t\t\t' + ip_ad )
    print( 'Gateway\t\t\t\t' + def_gate )
    logger.info( 'Gateway\t\t\t\t' + def_gate )
    print( 'Network Mask\t\t\t' + netmask )
    logger.info( 'Network Mask\t\t\t' + netmask )
    print( 'DNS1:\t\t\t\t' + dns_servers[0] )
    logger.info( 'DNS1:\t\t\t\t' + dns_servers[0] )
    
def find_os_info():	#Use os module and distro to find OS information
    print( GREEN + 'OS Information' + RESET )
    logger.info( GREEN + 'OS Information' + RESET )

    os_details = os.uname()
    os_cur = os_details.sysname
    os_ver = distro.version()
    os_kern_ver = os_details.release
    
    print( 'Operating System:\t\t' + os_cur )
    logger.info( 'Operating System:\t\t' + os_cur )
    print( 'Operating Version:\t\t' + os_ver )
    logger.info( 'Operating Version:\t\t' + os_ver )
    print( 'Kernel Version\t\t\t' + os_kern_ver )
    logger.info( 'Kernel Version\t\t\t' + os_kern_ver )
    
def find_storage_info():	#Make use of shutil to find disk information, convert to GB, and print results
    print( GREEN + 'Storage Information' + RESET )
    logger.info( GREEN + 'Storage Information' + RESET )

    total, used, avail = shutil.disk_usage( '/' )
    
    totalgbf = str( total / ( 1024 ** 3 ) )
    availgbf = str( avail / ( 1024 ** 3 ) )
    totalgb = totalgbf.split( '.' )[0]
    availgb = availgbf.split( '.' )[0] 
    
    print( 'Hard Drive Capacity:\t\t' + totalgb + 'G' )
    logger.info( 'Hard Drive Capacity:\t\t' + totalgb + 'G' )
    print( 'Available Space\t\t\t' + availgb + 'G' )
    logger.info( 'Available Space\t\t\t' + availgb + 'G' )
    
def find_proccessor_info():	#Make use of the /proc/cpuinfo file to find processor information
    print( GREEN + 'Processor Information' + RESET )
    logger.info( GREEN + 'Processor Information' + RESET )

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
    
    print( 'CPU Model:\t\t\t' + all[0] )
    logger.info( 'CPU Model:\t\t\t' + all[0] )
    print( 'Number of processors\t\t' + str( processors ) )
    logger.info( 'Number of processors\t\t' + str( processors ) )
    print( 'Number of cores\t\t\t' + str( cores ) )
    logger.info( 'Number of cores\t\t\t' + str( cores ) )
    
def find_memory_info():	#Parse through output from free -h to retrieve memory information
    print( GREEN + 'Memory Information' + RESET )
    logger.info( GREEN + 'Memory Information' + RESET )

    meta = subprocess.check_output( ['free', '-h'] ).decode()
    
    pre_parse = meta.split('\n')
    full_parse = pre_parse[1].split()
    
    total_ram = full_parse[1]
    available_ram = full_parse[3]
    
    print( 'Total RAM\t\t\t' + total_ram )
    logger.info( 'Total RAM\t\t\t' + total_ram )

    print( 'Available RAM\t\t\t' + available_ram + '\n' )
    logger.info( 'Available RAM\t\t\t' + available_ram + '\n' )
    
    
def main():
    os.system( 'clear' )	#Clear terminal
    
    today = str( date.today() )	#Get today's date
    print( RED + '\t\tSystem Report - ' + today + RESET )
    logger.info( RED + '\t\tSystem Report - ' + today + RESET )

    find_device_info()
    find_network_info()
    find_os_info()		#Run functions to find all information
    find_storage_info()
    find_proccessor_info()
    find_memory_info()

    exit()			#Exit program


main()

