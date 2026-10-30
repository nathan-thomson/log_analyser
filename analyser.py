import re

# Matches failed SSH logins in both sshd formats:
#   "Failed password for root from."
#   "Failed password for invalid user admin from"
#
#   (?:invalid user )?      optional; present when the username doesn't exist.
#                           Non-capturing, so it's matched and discarded.
#   (?P<user>\w+)           the username tried (letters, digits, underscore)
#   (?P<ip_address>[\d.]+)  source IP: a run of digits and dots (IPv4 only)
#
# Lines that don't fit the whole pattern are skipped, including noise,
# "Invalid user X from" lines (to avoid double-counting) and broken lines.

pattern = r"Failed password for (?:invalid user )?(?P<user>\w+) from (?P<ip_address>[\d.]+)"


with open("samples/sample_auth.log", "r") as file:
    
    for line in file:
        match = re.search(pattern, line) #searches for "Failed password", user and ip
        
        if match:
            print(match.group("user"), match.group("ip_address"))  
        