import paramiko
import time
import difflib
import re

# Device information
ip = '192.168.56.100'
username='python'
password='Huawei12#$'

# Define a function to obtain the current configurations.
def get_config(ip,username,password):
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,port=22,username=username,password=password)
    print(ip+' login succesfully')

    cli = ssh.invoke_shell()
    cli.send('N\n')
    time.sleep(0.5)
    cli.send('screen-length 0 temporary\n')
    time.sleep(0.5)
    cli.send('display cu\n')
    time.sleep(2)

    dis_cu = cli.recv(999999).decode()
    return (dis_cu)
    ssh_client.close()        

# Define the ssh_config function to write the script to the device.    
def ssh_config(file,ip,username,password):
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,port=22,username=username,password=password)
    print(ip+' login succesfully')
    
    cli = ssh.invoke_shell()
    cli.send('N\n')
    time.sleep(0.5)
    cli.send('screen-length 0 temporary\n')
    time.sleep(0.5)

    f = open(file,'r')
    config_list = f.readlines()
    for i in config_list:
        cli.send(i)
        time.sleep(0.5)

    dis_this = cli.recv(999999).decode()
    #print (dis_this)
    ssh.close()    

# Invoke get_config to assign a value to output.    
output = get_config(ip,username,password)
#print (output)

# Process data and use regular expressions to obtain only configurations.
config = re.findall(r'(<CE1>display cu[\d\D]+<CE1>$)',output)
#print (config)

# Save the configurations to local file1.
with open(r'D:\Config\file1','w') as f:
    f.writelines(config[0])

# Invoke ssh_config to write the netconf.txt configurations to the device.    
ssh_config('netconf.txt',ip,username,password)

# Read the configurations again and save them to local file2.
output = get_config(ip,username,password)
config = re.findall(r'(<CE1>display cu[\d\D]+<CE1>$)',output)

with open(r'D:\Config\file2','w') as f:
    f.writelines(config[0])

# Compare configurations.
d = difflib.HtmlDiff()

# Define a function to read files.
def read_file(filename):
    try:
        with open(filename,'r') as f:
            return f.readlines()
    except IOError:
        print('%s The file is not found.'% filename)
        sys.exit(1)

# Define the compare_files function to compare configurations and save the comparison as result.html.
def compare_files(file1,file2,out_file):
    file1_content = read_file(file1)
    file2_content = read_file(file2)
    d = difflib.HtmlDiff()
    result = d.make_file(file1_content,file2_content)    
    with open(r'D:\Config\result.html','w') as f:
        f.writelines(result)
    print ()

# Invoke compare_files.
#compare_files(FILE_ONE.txt,FILE_TWO.txt,RESULT..txt)    
