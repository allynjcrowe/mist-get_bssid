mist-get_bssid
 
This script is used to retrieve information for an input file of MAC addresses of mist APs 
 from a specific site and export information on them to a CSV.

Information currently includes: 
   Name
   Name of the map the AP is located on (if it's on a map)
   MAC
   BSSIDs for active radios 
   LLDP name and port_id of the device it's connected to

Currently uses n+1 API calls where n is the number of  in the input file

Hacked together by Allyn Crowe, Principal Engineer, Nexum
allyn@nexuminc.com
https://www.nexuminc.com

CREDITS:
Mist Access Point – CSV: https://artofrf.com/2022/02/09/mist-access-point-csv/
Mist Use Case Basics: https://api-class.mist.com/use_cases/
