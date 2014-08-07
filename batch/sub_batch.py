#!/usr/bin/env python

import getopt
import os
import sys
import glob
import math
import time
import subprocess

import shutil

def usage():
    print ' '
    print 'Usage: sub.py %s inputLocation [options]' % sys.argv[0]
    print '-u | --unsupervised: learning rate'
    print '-s | --supervised: learning rate'
    print '-n | --name: specify the data file name'
    print '-o | --output directory: specify output directory'
    print ' '

#default settings
UnsupervisedLearnRate=0.05
SupervisedLearnRate=0.0001
Name='test'
Output=''

Walltime=2
Memory=2
system=os.system
currentDir = os.getcwd()

t = time.localtime()
timestr = '%s_%s_%s_%s:%s:%s' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

try:
    # command line options
    shortopts = 'u:s:n:o:'
    longopts = ['UnsupervisedLearnRate=','SupervisedLearnRate=','Name=','Output=']
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
 
except getopt.GetoptError:
    print >> sys.stderr, 'ERROR: options unknown in %s' %sys.argv[1:]
    usage()
    sys.exit(1)

for o, a in opts:
    if o in('--UnsupervisedLearnRate', '-u'):
        UnsupervisedLearnRate = float(a)
    if o in('--SupervisedLearnRate', '-s'):
        SupervisedLearnRate = float(a)
    if o in('--Name', '-n'):
        Name = a
    if o in('--Output', '-o'):
        Output = a

#create submission shell script
if not os.path.exists('subs/'+Output):
    os.makedirs('subs/'+Output)
flname = 'subs/'+Output+'/'+Name+'_'+timestr+'.sh'

#shutil.copyfile(currentDir+"/../train", currentDir+"/../train_running")

with open(flname,'a') as file:
    fstr = 'hostname \n'
    file.write(fstr)
    fstr = 'cd '+currentDir+' \n'
    file.write(fstr)
    fstr = 'cd ..\n'
    file.write(fstr)
    #fstr = 'cp train train_running\n'
    #file.write(fstr)
    fstr = './train_running %s %s %s %s\n' % (UnsupervisedLearnRate,SupervisedLearnRate,Name,'/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_intput/'+Output)
    file.write(fstr)


ts = 'subs/'+Output+'/'+Name+'_'+timestr+'.sh'
w = 'walltime=0%s:00:00' % Walltime
m = 'mem=%sgb' % Memory
command = ['qsub -d . -l '+m+','+w+',naccesspolicy=shared -V -q hep -e '+currentDir+'/log/err.%s_%s' % (Name,timestr) + ' -o '+currentDir+'/log/log.%s_%s ' % (Name, timestr) + ts]
for c in command:
    print c
    time.sleep(1)
    os.system(c)
