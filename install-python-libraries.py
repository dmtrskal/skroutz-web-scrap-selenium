import subprocess
import sys

def library_install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
	
library_install("xlrd")
library_install("selenium")
library_install("progressbar2")