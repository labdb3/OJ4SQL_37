import os
import utils.config as config


def changePasswd(studentid, passwd):
    os.system('docker exec -u root -it {} sh -c "echo {}:{} | chpasswd"'.format(
        config.Learncase_JupyterHub_Docker_Name, studentid, passwd))


# run this function using root

import os
def cpFilesToAllUsers():
    users = ["/home/"+name for name in os.listdir("/home/")]
    for user in users:
        os.system("rm -rf {user}/commons && mkdir {user}/commons".format(user=user))
        os.system("cp -r /root/commons/ {user}/".format(user = user))
        os.system("chmod -R 777 {}/commons".format(user))


# cpFilesToAllUsers()

def read_data():
    # with open("数据库选课名单.csv", "r") as f:
    with open("copy.csv", "r") as f:
        lines = f.readlines()[1:]
        id_name = [line.strip().split(",")[:2] for line in lines]

    return id_name


def addusers(id_name):
    for id,name in id_name: 
        os.system("useradd -m {username} --badnames".format(username=id))
        os.system("echo '{passwd}\n{passwd}' | passwd {username}".format(passwd=id,username=id))

