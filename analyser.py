import re
from collections import Counter
import sys

# Matches failed SSH logins in both sshd formats:
#"Failed password for root from."
#"Failed password for invalid user admin from"

#(?:invalid user )? optional; present when the username doesn't exist.
#Non-capturing, so it's matched and discarded.
#(?P<user>\w+) the username tried (letters, digits, underscore)
#(?P<ip_address>[\d.]+)  source IP: a run of digits and dots (IPv4 only)

# Lines that don't fit the whole pattern are skipped, including noise,
# "Invalid user X from" lines (to avoid double-counting) and broken lines.

if len(sys.argv) > 1:
    log_path = sys.argv[1]
else:
    print("Not enough arguments, usage: python3 analyser.py <logfile>")
    sys.exit(1) #ends the script, 0 means good, everything else is failure, so 1 shows error

pattern = r"Failed password for (?:invalid user )?(?P<user>\w+) from (?P<ip_address>[\d.]+)"
alert_threshold = 5

ip_usernames = {}
lines_processed = 0
total_failures = 0

try: 
    with open(log_path, "r") as file:
        
        for line in file:
            match = re.search(pattern, line) 
            lines_processed += 1
            if match:
                
                total_failures += 1
                
                ip = match.group("ip_address")
                username = match.group("user")
            
                if ip not in ip_usernames:
                    ip_usernames[ip] = [username]
                else :
                    ip_usernames[ip].append(username)
                    
#OSError handles all file exceptions                    
except OSError as e: 
    print(f"Cannot access/find file: {log_path}: {e.strerror}") #e is the generic error specifying which file error 'string error'
    sys.exit(1)

total_ip = len(ip_usernames)

print(f"Lines Processed: {lines_processed}")  
print(f"Failed logins: {total_failures} from {total_ip} source IPs.")  

# Report IPs at or above the alert threshold, most failures first.
# sorted() orders the (ip, usernames) pairs by list length (item[1]), reverse=True
# puts the highest first. Counter tallies each username, and most_common() returns
# them highest count first, e.g. root (4), admin (2).
# Repeated attempts on one account suggest brute force; many names suggest probing.
for ip, usernames in sorted(ip_usernames.items(), key=lambda item: len(item[1]), reverse=True):
    if len(usernames) >= alert_threshold:
        user_counts = Counter(usernames) #creates tally list of every user eg. root (3) admin(1)
        parts = []
        for user, count in user_counts.most_common(): #part of Counter, return pairs from highest to lowest
            parts.append(f"{user} ({count})")
        print(f"ALERT: {ip} {len(usernames)} failed attempts. users: {', '.join(parts)}")   