from ConvertSAMToGeneFrequency import *
from configuration import *
from logger import *
import pickle
import os

import pdb

def save_object(obj, fileName, directory):
    with open(os.path.join(directory, fileName), 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
def clean_mt_objects(obj):
    cleanObj = []
    
    for o in obj:
        if o:
            cleanObj.append(o)
    
    return cleanObj

sam_file = os.environ['INPUT_FILE']
slots = os.environ['SLOTS']

config = Configuration()
log = Logger(config.getOutputDirectory())

converter = SAMConverter(os.path.join(config.getInputDirectory(), sam_file), log)

# Single Threaded --> Very Slow
#converter.mapReads()
#frequency_map = converter.countFrequencies()
#
#pdb.set_trace()
#
#save_object(converter.samMap, str(sam_file + '.read.obj'), config.getOutputDirectory())
#save_object(converter.freqMap, str(sam_file + '.freq..obj'), config.getOutputDirectory())

# Multi Threaded --> Pass in Number of Processors
#mtResults = converter.mapReadsMT(int(slots))
#mtResults = clean_mt_objects(mtResults)
converter.mapReadsMT()
pdb.set_trace()
converter.countFrequenciesMT(int(slots), mtResults)
mtFrequency = clean_mt_objects(mtFrequency)

#save_object(mtResults, str(sam_file + '.read.obj'), config.getOutputDirectory())
#save_object(mtFrequency, str(sam_file + '.freq..obj'), config.getOutputDirectory())

log.logOutput('Completed, objects saved to files.')

# Save and Inflate Binary objects
#o = [1, 2, 3, 4, 5]
# 
#save_object(o, '.test.obj', config.getOutputDirectory())
#q = pickle.load(open(os.path.join(config.getOutputDirectory(), '.test.obj'), 'rb'))