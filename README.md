# mist-get_bssid
 
This script is used to retrieve information for an input file of MAC addresses of mist APs from a specific site and export information on them to a CSV. The current input format expected is the export from the mist portal inventory page (again for a site).

Information currently includes: 
- Name
- Name of the map the AP is located on (if it's on a map)
- MAC
- BSSIDs for active radios 
- LLDP name and port_id of the device it's connected to

Currently uses n+1 API calls where n is the number of  in the input file

Hacked together by Allyn Crowe, Principal Engineer, Nexum  
allyn@nexuminc.com  
https://www.nexuminc.com  

# CREDITS:
Mist Access Point – CSV: https://artofrf.com/2022/02/09/mist-access-point-csv/  
Mist Use Case Basics: https://api-class.mist.com/use_cases/

## DISCLAIMER: I am not a programmer, I'm a network engineer. All config/script/code samples are from my test environments. Use them at your risk. They are provided as is without any warranty or assurance they will even work. Always test in a non-production environment before using it in production.
