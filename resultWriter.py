import os
import json

import pdb

class ResultWriter(object):
    
    def __init__(self, output_dir, outputFile):
        output_dir = os.path.join(output_dir, 'object')
        self.output_file = os.path.join(output_dir, outputFile)
        
    def writeSamMapToFile(self, mappedReads, unmappedReads):
        map_read_file = self.output_file + '.reads'
        writer = open(map_read_file, 'w')
        
        for read in mappedReads:
            
            pdb.set_trace()            
            
            serializedData = json.dumps(read, cls = Encoder)
            writer.write(serializedData + '\n')
            
        writer.close()          
        unmapped_read_file = self.output_file + '.unmappedReads'
        writer = open(unmapped_read_file, 'w') 
        
        for read in unmappedReads:
            serializedData = json.dumps(read, cls = Encoder)
            writer.write(serializedData + '\n')
            
        writer.close()         
        
    def writeFreqMapToFile(self, freqMap):
        freq_file = self.output_file + '.freq'
        writer = open(freq_file, 'w')
        
        for freqCount in freqMap:
            result = 'Gene|' + freqCount.geneId + '\t' + 'Name|' + \
                     freqCount.geneName + '\t' + 'Count|' + str(freqCount.freq)
            writer.write(result + '\n')
            
        writer.close()
        
        
class Encoder(json.JSONEncoder):
        
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        
        return json.JSONEncoder.default(self, obj)