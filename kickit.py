import subprocess
import ConfigParser

# suspend the 8021x.exe process
parser = ConfigParser.ConfigParser()
parser.read("config.ini")
tgtbit = parser.get("System", "version")
tgtprocess = parser.get("Processes", "process")
tgtpath = parser.get("Tools", "path")

tmp = subprocess.Popen(
    "tasklist|findstr 8021x.exe",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
pid = (str(tmp.stdout.readlines()[0]).split())[1]

if tgtbit == "64":
    subprocess.Popen("%s/pssuspend64.exe %s" % (tgtpath, pid), shell=True)
if tgtbit == "32":
    subprocess.Popen("%s/pssuspend.exe %s" % (tgtpath, pid), shell=True)

# restart VMware NAT service
tgtservice = parser.get("Services", "service")
subprocess.Popen('sc start "%s"' % tgtservice, shell=True)
