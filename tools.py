import os
import requests
import whois
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()
@tool
def scan_url(url: str)->str:
    """Scans a URL or domain using VirusTotal to check for malicious or suspicious flags.
    Use this when you find a URL in an email that needs security verification."""
    
    api_key= os.getenv("VIRUSTOTAL_API_KEY")
    #clean the domain so that virustotal or whois can get the only domain name without full url and can process it.
    #if we send full url to whois or virustotal it will not work, so we need to extract the domain name from the url.
    domain = url.split("//")[-1].split("/")[0].split("?")[0]
    
    url=f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers={"x-apikey": api_key}
    
    try:
        response= requests.get(url, headers=headers)
        if response.status_code==200:
            stats= response.json()['data']['attributes']['last_analysis_stats']
            return f"Security scan for {domain}: Malicious:{stats['malicious']}, Suspicious:{stats['suspicious']}"
        return f"VirusTotal has no record for {domain} (Status: {response.status_code}). This could be a very new and dangerous domain."
    except Exception as e:
        return f"Error connecting to VirusTotal:{str(e)}"

@tool   
def check_domain_age(url:str)->str:
    """Checks the registration age of a domain.
    Use this to see if a domain was recently created (a common sign of phishing).
    """
    try:
        domain= url.split("//")[-1].split("/")[0].split("?")[0]
        w= whois.whois(domain)
        creation_date=w.creation_date
        
        #WHOIS sometimes returns a list of dates, we need to get the first one
        if isinstance(creation_date, list):
            creation_date=creation_date[0]
            
        if creation_date:
            days_old= (datetime.now()- creation_date).days
            return f"The domain {domain} was created {days_old} days ago."
        return f"Could not determine the age of {domain}. Registration info is private."
    except Exception as e:
        return f"WHOIS check failed for {domain}. It might be an unregistered or invalid domain."
    
tools_list = [scan_url, check_domain_age]