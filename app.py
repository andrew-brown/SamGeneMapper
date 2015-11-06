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

pdb.set_trace()

converter.mapReadsMT()
pdb.set_trace()
converter.countFrequenciesMT(int(slots), mtResults)
mtFrequency = clean_mt_objects(mtFrequency)

#save_object(mtResults, str(sam_file + '.read.obj'), config.getOutputDirectory())
#save_object(mtFrequency, str(sam_file + '.freq..obj'), config.getOutputDirectory())

log.logOutput('Completed, objects saved to files.')