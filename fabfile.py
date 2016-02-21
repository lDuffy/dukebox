__author__ = 'centralstation'

from fabric.api import *


env.hosts = ['188.166.57.42']
env.user = 'root'
env.key_filename = 'liams.pem'
code_dir = '/var/www/dukebox/'


def deploy():
    with cd(code_dir):
        run("source bin/activate")
        run("git pull origin master")
        run("./setupdatabase.sh")
        run("sudo service apache2 restart")
