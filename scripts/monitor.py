import os, time
print("CPU load:", os.getloadavg())
print("Disk usage:")
os.system("df -h")
