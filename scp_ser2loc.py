#!/usr/bin/env python
# coding: utf-8

# In[6]:


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

df = pd.read_csv('/home/dsvm/Desktop/nov_19/data/image_links.csv')
df.head(5)



 
if __name__ == "__main__":
    host = "sultana.cs.unm.edu"
    username = "adnan"
    pw = "P@ssw0rd!"
    
    list = []
    for index, link in df.iterrows():
 
        origin = df.iloc[index]['path2image']
        dst = '/home/dsvm/Desktop/nov_19/scripts/' + df.iloc[index]['Time']
 
        ssh = SSHConnection(host, username, pw)
        ssh.get(origin,dst)
        ssh.close()

