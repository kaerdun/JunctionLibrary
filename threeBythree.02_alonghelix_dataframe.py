#!/usr/bin/env python

# Author: Sarah Denny, Stanford University 

# Provides modular tools for making a helix-junction
# helix DNA library

# This function calls dependent functions to make the subset of
# final library that is all three by three junctions and less


##### IMPORT #####
import numpy as np
import os
import sys
import pandas as pd

# load custom libraries

import globalvars
parameters = globalvars.Parameters()
from hjh.helix import Helix
from hjh.junction import Junction
import create_library_dataframe

##### MODULE #####
"""
SETUP
set working directory, create filename to save all subsequent
sequences to.
Initialize count.
"""
#wd = os.path.join(os.getcwd(), 'libraries') # working directory
wd = parameters.wd

# check if working directory exists and if not, creates it
if not os.path.exists(wd):
    os.mkdir(wd)
    
# initialize file
filename = os.path.join(wd, 'all3x3junctionsNB.02_alonghelix.txt')
print 'saving to %s'%filename
f = open(filename, 'w')

filename2 = os.path.join(wd, 'all3x3junctionsNB.02_alonghelix_characterization.txt')
print 'saving to %s'%filename
f2 = open(filename2, 'w')
# initalize log file
logfile = open(os.path.join(wd, '%s.log'%os.path.splitext(filename)[0]), 'w')

# initialize counts
count = 1
#initialize dataframe
df = pd.DataFrame(columns = ['Sequence', 'Junction Topology','Loop', 'Receptor', 'HelixContext', 'Junction Sequence',
            'HelixSequence', 'HelixLength1', 'Helixlength2','Junctionlength', 'Totallength']) 
#add header
df.to_csv(f2, sep='\t')

"""
JUNCTIONS IN ALL 20 POSITIONS
Save subset of junctions located in 'along' set. Also do different loop for all of these.
"""
# save one helix context, many junctions, in many different locations
print 'Doing 20 different positions of subset of junctions'
receptorName = 'R1'
loopNames     = ['goodLoop', 'badLoop']
cutOffNumber = 24

# Do Bulges in rigid context
junctionMotifs = [('B1',), ('B2',)]
helixName = 'rigid'
for junctionMotif in junctionMotifs:
    junction = Junction(junctionMotif)
    
    # take subset of junctions if greater than cutoff number
    if junction.howManyPossibilities() > cutOffNumber:
        subsetIndex = np.around(np.linspace(0, junction.howManyPossibilities()-1, cutOffNumber)).astype(int)
        junction.sequences = junction.sequences[subsetIndex]
        
    # save all different loops
    for loopName in loopNames:
        helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
        count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f,f2, logfile, count)

# Do single mismatch, double mismatch, 1x3 junction in WC context   
junctionMotifs = [('M',), ('M', 'B1', 'B1'), ('B2', 'B2', 'M')]
helixName = 'rigid'
for junctionMotif in junctionMotifs:
    junction = Junction(junctionMotif)
    
    # take subset of junctions if greater than cutoff number
    if junction.howManyPossibilities() > cutOffNumber:
        subsetIndex = np.around(np.linspace(0, junction.howManyPossibilities()-1, cutOffNumber)).astype(int)
        junction.sequences = junction.sequences[subsetIndex]
        
    # save all different loops
    for loopName in loopNames:
        helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
        count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f,f2, logfile, count)

"""
Do double mismatches in context of rigid helix
"""
helixName = 'rigid'
junctionMotif = ('M', 'M')
junction = Junction(junctionMotif)

# take subset of junctions if greater than cutoff number
if junction.howManyPossibilities() > cutOffNumber:
    subsetIndex = np.around(np.linspace(0, junction.howManyPossibilities()-1, cutOffNumber)).astype(int)
    junction.sequences = junction.sequences[subsetIndex]

# save all different loops
for loopName in loopNames:
    helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
    count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f,f2, logfile, count)

"""
But also do a subset of double mismatches that are all GU wobbles in WC context
"""
helixName = 'wc'
junctionMotif = ('M', 'M')
junction = Junction(junctionMotif)

# append GU wobble sequences
wobbleSequences = [('GU', 'GU'), ('GG', 'UU'), ('UU', 'GG'), ('UG', 'UG')]
junction.sequences = np.array(wobbleSequences, dtype=junction.sequences.dtype)

# save all different loops
for loopName in loopNames:
    helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
    count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f, f2,logfile, count)

"""
But also do a subset of single mismatches that are all GU wobbles in WC context
"""
helixName = 'wc'
junctionMotif = ('M',)
junction = Junction(junctionMotif)

# append GU wobble sequences
wobbleSequences = [('G', 'U'), ('U', 'G')]
junction.sequences = np.array(wobbleSequences, dtype=junction.sequences.dtype)

# save all different loops
for loopName in loopNames:
    helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
    count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f,f2, logfile, count)

"""
Also do more junctions in the WC context
"""
# Do  1x3 junction in WC context   
junctionMotifs = [('M', 'B1', 'B1'), ('B2', 'B2', 'M')]
helixName = 'wc'
for junctionMotif in junctionMotifs:
    junction = Junction(junctionMotif)
    
    # take subset of junctions if greater than cutoff number
    if junction.howManyPossibilities() > cutOffNumber:
        subsetIndex = np.around(np.linspace(0, junction.howManyPossibilities()-1, cutOffNumber)).astype(int)
        junction.sequences = junction.sequences[subsetIndex]
        
    # save all different loops
    for loopName in loopNames:
        helices = Helix(parameters.helixDict[helixName], junction.length).alongHelix()
        count = create_library_dataframe.saveSet(junction, helices, helixName, receptorName, loopName, f,f2, logfile, count)


# close
f2.close()
f.close()
logfile.close()
