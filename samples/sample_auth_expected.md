Line 1: NOISE - CRON
Line 2: Success - 192.0.2.25 - deploy publickey
Line 3: FAIL - 203.0.113.45 - root (password)
Line 4: FAIL - 203.0.113.45 - admin (invalid user)
Line 5: FAIL - 192.0.2.10 - nathan (password)
Line 6: SUCCESS - 192.0.2.10 - nathan (password)
Line 7: FAIL - 198.51.100.23 - root (password)
Line 8: FAIL - 203.0.113.45 - root (password)
Line 9: PART OF LINE 10 - same PID, IP and port; not counted separately
Line 10: FAIL - 203.0.113.99 - pi (invalid user, invalid password)
Line 11: FAIL - 198.51.100.23 - ubuntu (invalid user)
Line 12: FAIL - 203.0.113.45 - test (invalid user, invalid password)
Line 13: NOISE - CRON
Line 14: FAIL - 203.0.113.99 - pi (invalid user, invalid password)
Line 15: FAIL - 203.0.113.45 - root (invalid password)
Line 16: FAIL - 198.51.100.23 - root (invalid password)
Line 17: PART OF LINE 18 - same PID, IP and port; not counted separately
Line 18: FAIL - 198.51.100.7 - guest (invalid user, invalid password)
Line 19: FAIL - 203.0.113.45 - admin (invalid user, invalid password)
Line 20: FAIL - 203.0.113.99 - pi (invalid user, invalid password)
Line 21: FAIL - 198.51.100.23 - ubuntu (invalid user, invalid pass)
Line 22: SUCCESS - 192.0.2.10 - nathan (publickey)
Line 23: FAIL - 203.0.113.45 - oracle (invalid user, invalid password)
Line 24: NOISE - connection closed
Line 25: FAIL - 198.51.100.7 - guest (invalid user, invalid password)
Line 26: NOISE - Invalid log
Line 27: FAIL - 198.51.100.23 - root (invalid password)
Line 28: NOISE - SYS
Line 29: FAIL - 203.0.113.99 - pi (invalid user, password)
Line 30: FAIL - 203.0.113.45 - root (invalid password)
Line 31: NOISE - Invalid log
Line 32: NOISE - connection closed

3 Success - (192.0.2.25, 192.0.2.10, 192.0.2.10)
203.0.113.45 - Line 3, 4, 8, 12, 15, 19, 23, 30
192.0.2.10 - Line 5
198.51.100.23 - Line 7, 11, 16, 21, 27
203.0.113.99 - Line 9 & 10 (1 attempt), 14, 20, 29
198.51.100.7 - Line 17 & 18 (1 attempt), 25

SUMMARY

32 Lines
20 Failed attempts from 5 unique IP
203.0.113.45 - 8 failed - root, admin, test, oracle - should alert at 5
192.0.2.10 - 1 failed - nathan
198.51.100.23 - 5 failed - root, ubuntu - should alert at 5
203.0.113.99 - 4 failed - pi
198.51.100.7 - 2 failed - guest

Decision: "Invalid user X from IP" lines are not counted. sshd logs them
alongside the "Failed password for invalid user X" line for the same attempt
(same PID, IP and port), so counting both would double-count. Only
"Failed password" lines are counted as failed attempts.

