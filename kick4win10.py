import ctypes
import sys
import subprocess
import ConfigParser


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # suspend the 8021x.exe process
    parser = ConfigParser.ConfigParser()
    parser.read("config.ini")
    tgtbit = parser.get("System", "version")
    tgtprocess = parser.get("Processes", "process")

    tmp = subprocess.Popen(
        "tasklist|findstr 8021x.exe",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    pid = (str(tmp.stdout.readlines()[0]).split())[1]

    if tgtbit == "64":
        subprocess.Popen("PStools/pssuspend64.exe %s" % pid)
    if tgtbit == "32":
        subprocess.Popen("PStools/pssuspend.exe %s" % pid)

    # restart VMware NAT service
    tgtservice = parser.get("Services", "service")
    subprocess.Popen('sc start "%s"' % tgtservice)
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, "", None, 1)
