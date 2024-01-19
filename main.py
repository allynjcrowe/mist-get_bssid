#!/usr/bin/python3
#
# main.py
#
# This script is used to retrieve information for an input file of MAC addresses of mist APs 
#   from a specific site and export information on them to a CSV.
#
# Information currently includes: 
#   Name
#   Name of the map the AP is located on (if it's on a map)
#   MAC
#   BSSIDs for active radios 
#   LLDP name and port_id of the device it's connected to
#
# Currently uses n+1 API calls where n is the number of  in the input file
#
# Hacked together by Allyn Crowe, Principal Engineer, Nexum
# allyn@nexuminc.com
# https://www.nexuminc.com
#
# CREDITS:
# Mist Access Point – CSV: https://artofrf.com/2022/02/09/mist-access-point-csv/
# Mist Use Case Basics: https://api-class.mist.com/use_cases/

from datetime import datetime
from dotenv import dotenv_values
from mist_client import *
import sys,csv

### Set Variables
#get mist info from .env file
mist_secrets = dotenv_values(".env")

#mist site ID to get the APs for
mist_site_id = mist_secrets['mist_site_id']
mist_org_id = mist_secrets['mist_org_id']

#file to use for import
input_file = 'input.csv'

# Convert CSV file to JSON object.
def csv_to_dict(filename):
    csv_rows = []
    with open(filename,mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([ {title[i]: row[title[i]] for i in range(len(title))} ])
    return csv_rows

def get_site_maps(mist_session):
    map_info = mist_session.get(mist_secrets['api_base_url'].format('/api/v1/sites/') + mist_site_id +'/maps')
    #API Error
    if map_info == False:
        print('API call failed')
        sys.exit(1)
    else:
        #Iterate Map Info to associate mapid to name
        map_list = {}
        for i in map_info:
            map_list[i['id']] = i['name']
    return map_list

def get_ap_bssid(ap_stats):
        radio_data = {}
        radio_24 = ap_stats.get('radio_stat',{}).get('band_24',{}).get('mac','')
        if (radio_24 != ''):
                radio_24  = radio_24 + '-' + radio_24[-2:-1] + 'f'
        else:
            pass
        radio_5 = ap_stats.get('radio_stat',{}).get('band_5',{}).get('mac','')
        if (radio_5 != ''):
            radio_5 = radio_5 + '-' + radio_5[-2:-1] + 'f'
        else:
            pass
        radio_6 = ap_stats.get('radio_stat',{}).get('band_6',{}).get('mac','')
        if (radio_6 != ''):
            radio_6 = radio_6 + '-' + radio_6[-2:-1] + 'f'
        else:
            pass
        radio_data = {"band_24":radio_24,"band_5":radio_5,"band_6":radio_6}

        return radio_data

def get_ap_list():
   # Check for required variables
    if mist_secrets['mist_api_token'] == '':
        print('Please provide your Mist API token as mist_api_token in .env')
        sys.exit(1)
    elif mist_secrets['mist_org_id'] == '':
        print('Please provide your Mist Organization UUID as mist_org_id in .env')
        sys.exit(1)

    #set runtime variable
    operation_time = datetime.now()

    # Establish Mist session
    mist = MistSession(mist_secrets['mist_api_token'])

    print("Retrieve List of Mist Site Maps")
    map_data = get_site_maps(mist)

    #Read input csv file
    inventory = csv_to_dict(input_file)

    #open output csv file
    with open('output/ap_list-' + operation_time.strftime("%Y%m%d-%H%M%S") + '.csv', 'a+') as csvfile:
        output_file = csv.writer(csvfile)
        header_row = ['HostName','Location','MAC','2.4 GHz BSSID','5 GHz BSSID','6 GHz BSSID','Switch Name','Switch Port']

        output_file.writerow(header_row)

        #iterate over AP list
        for ap in inventory:
            #If the AP is disconnected we won't get any BSSID data so skip over it
            if (ap['Status'] == 'Disconnected'):
                pass
            #The AP shows connected so get it's data
            else:
                #convert mac to non-delimited
                mac = (ap['MAC Address']).replace(':', '')

                #get AP stats
                ap_stats = mist.get(mist_secrets['api_base_url'].format('/api/v1/sites/') + mist_site_id +'/stats/devices/00000000-0000-0000-1000-'+ mac)
                #API Error
                if ap_stats == False:
                    print('API call failed')
                    sys.exit(1)
                else:
                    #Iterate Radios to BSSIDs
                    ap_bssid = get_ap_bssid(ap_stats)

                    #get name of map AP is on
                    ap_map = map_data.get(ap_stats.get('map_id'),'Not on Map')

                    output_row = (ap['Name'],ap_map,mac,ap_bssid.get('band_24',''),ap_bssid.get('band_5',''),ap_bssid.get('band_6',''),ap_stats.get('lldp_stat').get('system_name'),ap_stats.get('lldp_stat').get('port_id'))
                    output_file.writerow(output_row)

if __name__ == "__main__":
   get_ap_list()
