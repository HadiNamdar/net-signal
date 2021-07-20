import os
import re
import fnmatch
import time as tm
from datetime import datetime, timezone
import speedtest
sp = speedtest.Speedtest()

# Checking the existing .txt files in the directory to find the last number
ROOT = './'
files = fnmatch.filter((f for f in os.listdir(ROOT)), 'data*.txt')
if not files:
    num = ''
elif len(files) == 1:
    num = '(1)'
else:
    files.remove('data.txt')
    num = '(%i)' % (int(re.search(r'\(([0-9]+)\)', max(files)).group(1))+1)

# Defining the headers of the table's columns and the template for printing data
Headers = ["id","Download Speed (Mb/s)", "Upload Speed (Mb/s)", "Ping Value (ms)", "Start Time (UTC)", "End Time (UTC)", "Date (UTC)"]
template = '{:<4}   {:^21}   {:^19}   {:^15}   {:^16}   {:^14}   {:^10}'

# Creating a new numbered .txt file and writing the table headers in it
with open('data%s.txt' % num, 'w') as f:
    f.write(template.format(*Headers))
    f.write('\n')
    f.write(template.replace(':',':-').format('', '','','','','',''))
    f.write('\n')
f.close()


print(template.format(*Headers))  # Showing the headers on the shell
print(template.replace(':',':-').format('', '','','','','',''))  # Printing dashed line under the headers
print("To stop the algorithm press CTRL + C",end='\r')  # Showing a command of how to stop the program (the next line will replace this line)

# main function

def main():
    n = 1
    try:
        while True:

            st = tm.strftime("%H:%M:%S", tm.gmtime()) # Store the starting time (UTC) of the calculation (to store the local time use "tm.localtime()" instead of "tm.gmtime()")
            ds = sp.download()/1024/1024 # Calculating the download speed and converting to Mb/s
            us = sp.upload()/1024/1024 # Calculating the upload speed and converting to Mb/s
            ping = sp.results.ping # Calculating the ping
            et = tm.strftime("%H:%M:%S", tm.gmtime()) # Store the finishing time (UTC) of the calculation
            Data = [str(f'{n}'), str(f'{ds:.2f}'), str(f'{us:.2f}'), str(f'{ping:.2f}'), st, et, datetime.now(timezone.utc).strftime("%d/%m/%Y")] #

            # Writing Data in the .txt file
            with open('data%s.txt' % num, 'a') as f:
                f.write(template.format(*Data))
                f.write('\n')
            f.close()
            n = n+1

            print(template.format(*Data))  # Showing the Data on the shell
            print("To stop the algorithm press CTRL + C",end='\r')  # Showing a command of how to stop the program (the next line will replace this line)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

print("FINISH!!                                      ")