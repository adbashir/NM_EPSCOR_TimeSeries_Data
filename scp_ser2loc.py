# this script download 
# modified from : http://www.blog.pythonlibrary.org/2012/10/26/python-101-how-to-move-files-between-servers/
# "path2image" is the column header with links if you have downloaded it from grafana , Can be changed in csv file with all the links 

#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import sys
import paramiko
 
class SSHConnection(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False
 
        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))
 
        self.transport.connect(username=username, password=password)
 
    #----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True
 
    #----------------------------------------------------------------------
    def get(self, remote_path, local_path=None):
        """
        Copies a file from the remote host to the local host.
        """
        self._openSFTPConnection()        
        self.sftp.get(remote_path, local_path)        
 
    #----------------------------------------------------------------------
    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)
 
    #----------------------------------------------------------------------
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()

        
if __name__ == "__main__":
    host = "veyron.cs.unm.edu"
    # fill these three variables 
   ##############################################
    username = "your cs username"
    pw = "your account pwd"
    df = pd.read_csv('file with images' links')
   ##############################################                  
    list = []
    for index, link in df.iterrows():
 
        origin = df.iloc[index]['path2image']
        dst = 'local host folder' + df.iloc[index]['Time']
 
        ssh = SSHConnection(host, username, pw)
        ssh.get(origin,dst)
        ssh.close()

