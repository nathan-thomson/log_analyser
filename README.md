# SSH Log Analyser

A command line tool that scans linux SSH authentication logs for brute-force attempts and reports the source IPs responsible.

## Features

- Detects failed SSH password logins, including attempts against usernames that dont exist on the system.
- Groups failures by source IP and shows which usernames, and how many times, each IP tried.
- Raises alert for any IP at or above a selected threshold (5), most active first.
- Skips unrelated lines without crashing.
- Exits with clear error if log file not found/cant be read.

## Usage

python3 analyser.py <logfile>

Example, using the included sample log: 

python3 analyser.py samples/sample_auth.py

## Example output

Lines Processed: 32
Failed logins: 20 from 5 source IPs.
ALERT: 203.0.113.45 8 failed attempts. users: root (4), admin (2), test (1), oracle (1)
ALERT: 198.51.100.23 5 failed attempts. users: root (3), ubuntu (2)

## How it works

The tool reads the log one line at a time. A regular expression matches sshd's "Failed password" messages and extracts the username and source IP. Failures are grouped by IP, and any IP with at least the threshold number of failures is reported, sorted by number of attempts.

## Testing

`samples/sample_auth.log` is a hand-written log covering attackers above, at
and below the threshold, a legitimate user who mistypes once, unrelated
system noise and malformed lines. The expected results were worked out by hand
before writing any code, and are in `samples/sample_auth_expected.md`.

## Design decisions

- **"Invalid user X from IP" lines are not counted.** sshd writes this line
  alongside the "Failed password for invalid user X" line for the same
  attempt (same process ID, IP and port), so counting both would double-count.
- **The IP pattern is `[\d.]+`.** It accepts any run of digits and dots rather
  than strictly validating the address. That's sufficient because sshd always
  writes a valid address here, and it keeps the pattern readable.
- **Usernames are shown with counts.** Many attempts on one account suggests
  a targeted brute force; many different names suggests probing for valid
  accounts.

## Limitations

- No time window yet.
- IPv4 only, IPv6 not matched as of yet.
- Attacker who disconects before entering password is not counted yet.

## Roadmap

- Time-window detection (e.g. 5 failures within 2 minutes)
- Alerting on a successful login that follows repeated failures
- Detection of password spraying (one IP trying many usernames)
- Configurable options via command-line flags
- JSON output for use by other tools
- Automated tests with pytest