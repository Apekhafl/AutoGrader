import subprocess

cmd = ['python3', "uploads/sum.py"]
output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=10)
print(output)
