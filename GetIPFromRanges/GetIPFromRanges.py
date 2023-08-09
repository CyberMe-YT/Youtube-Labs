import csv
import sys
import ipaddress
newiplist = []
def write_to_text(file_path,finaliplist):
    with open(file_path, 'w') as file:
        for item in finaliplist:
            file.write(str(item) + ","+ "\n")
def get_ip_from_range(ip):
    """IP address in CSV is listed as a range example: 192.168.1.1-192.168.1.20 and we need it to add each value in between to newiplist """
    # Split IP into two addresses 
    ipsplit = ip.split('-')
    # Assign var to each IP 
    startip = ipsplit[0]
    endip = ipsplit[1]
    # Get prefix
    p = startip.split('.')
    del p[3]
    ipprefix = '.'.join(p)+'.'
    # Get list of numbers in range
    s = startip.split('.')[3]
    e = endip.split('.')[3]
    for i in range (int(s),int(e)+1):
        newiplist.append(ipprefix + str(i))
def get_ip_from_subnet(ip):
    """IP address in CSV listed as /31 needed to be captured and added to list"""
    first_ip = ''
    last_ip = ''
    try:
        network = ipaddress.IPv4Network(ip, strict=False)
        first_ip = str(network.network_address + 1)
        last_ip = str (network.broadcast_address - 1)
        newiplist.append(first_ip)
        newiplist.append(last_ip)
    except ValueError as e:
        print(f"Error: {e}")
        return None, None
def get_ip_from_csv():
    with open(r"C:\temp\YT-GetIPFromRanges\IpRanges.csv", mode = 'r')as file:
        csv_reader = csv.reader(file)
        iplist = []
        for line in csv_reader:
            iplist = iplist + line
        return iplist
def create_new_ip_list(oldiplist):        
    for ip in oldiplist:
        if "-" in ip:
            get_ip_from_range(ip)
        if "/" in ip:
            get_ip_from_subnet(ip)
        if "-" not in ip and "/" not in ip:
            newiplist.append(ip)
    return newiplist
def main():
    oldiplist = get_ip_from_csv()
    finaliplist = create_new_ip_list(oldiplist)
    write_to_text(r'C:\temp\YT-GetIPFromRanges\finallist.csv',finaliplist)
if __name__ == "__main__":
        # Call the main function
        main()