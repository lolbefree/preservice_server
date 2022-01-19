import subprocess, sys, re

p = subprocess.Popen(["powershell.exe", 
              "C:\AM\BAT\preservicecall\ps_attribute.ps1"], 
              stdout=subprocess.PIPE)
result = str(p.communicate()[0])

ip = (result[2:-5])
name = ip.index(".")
ip = (ip[:name])
