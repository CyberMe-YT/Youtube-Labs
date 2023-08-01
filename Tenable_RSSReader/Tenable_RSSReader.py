
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import subprocess
def get_date_difference(published_date):
    """ Function used to get difference in days between published and today"""
    published_date = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %Z")
    current_date = datetime.now()
    date_difference = current_date - published_date
    days_difference = date_difference.days
    return days_difference
def create_jiratask(title,pubdate):
    powershell_script = """
    # Python variables
    # Jira API URL
    $apiUrl = "https://TYPE URL HERE/rest/api/2/issue/"
    # Jira credentials
    $username = "TYPE EMAIL HERE"
    $apiToken = "TYPE API KEY HERE"
    $base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${username}:${apiToken}")))
    # Request headers
    $headers = @{
        "Authorization" = "Basic $base64AuthInfo"
        "Content-Type" = "application/json"
    }
    # Request body - replace the fields with your desired values
    $body = @{
        "fields" = @{
            "project" = @{
                "key" = "ENTER PROJECT KEY HERE"
            }
            "summary" = "New Audit File Uploaded in Tenable"
            "description" = "New Audit File uploaded in last 30 days! "
            "issuetype" = @{
                "name" = "Task"
            }
        }
    } | ConvertTo-Json
    try {
        # Send POST request to create the task
        $response = Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Post -Body $body -Verbose
        # Display the response
        Write-Host "Task created successfully! Issue key: $($response.key)"
    }
    catch {
        Write-Host "Error creating the task: $($_.Exception.Message)"
    }
    """
    result = subprocess.run(["powershell", "-Command", powershell_script], capture_output=True, text=True)
    print(result.stdout)
def read_rss_feed(url):
    """ Function used to read RSS feed from tenable """
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        tree = ET.parse(response)
        root = tree.getroot()
        for item in root.iter('item'):
            title = item.find('title').text
            pubdate = item.find('pubDate').text
            if("DISA" in title):
                if("DISA IIS 10.0 Server" in title ):
                    days_difference = get_date_difference(pubdate)
                    if(days_difference < 30):
                        # Write to Jira 
                        create_jiratask(title,pubdate)
    except urllib.error.URLError as e:
        print("Error occured while reading the RSS feed",e)

feed_url = "https://www.tenable.com/audits/feeds?sort=updated"
read_rss_feed(feed_url)