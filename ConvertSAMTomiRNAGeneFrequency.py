from miRNAGenome import *
from configuration import *
import types
import copy_reg
import os

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)
        
copy_reg.pickle(types.MethodType, _pickle_method)


class SAMmiRNAConverter(object):
    
    def __init__(self, samFile):
        config = Configuration()
        
        self.logger = logger
        self.logger.logOutput('Obtaining SAM map from memory')
        
        miRNARef = miRNACoordinate(os.path.join(config.getDataDirectory(), \
                                   'hsa.miRNA.hg38.txt'))        
        

        self.samFile = samFile
        self.samMap = []
        self.freqMap = []
        self.miRNARef = miRNARef
        
    def mapReads(self):
        samReads = self.samFile.getReads()
        
        for samRead in samReads:
            result = self.miRNARef.get_miRNA_ByCoordinates(samRead.rName, \
                                                           samRead.pos, \
                                                           samRead.endPos)
                                                           
            if len(results) > 0:
                s = SAMMapmiRNA(samRead, result)
                self.samMap.append(s)
                
    def countFrequencies(self):
        self.logger.logOutput('Determining unique miRNA in reads.')
        uniqueIds = self.getUniquemiRNAIds
        self.logger.logOutput(str(len(uniqueIds)) + ' unique miRNAs found.')
        
        for uniqueId in uniqueIds:
            self.logger.logOutput('Counting occurrences of: ' + str(uniqueId) + '.')
            frequency = list(filter(lambda x: uniqueId == \
                                    x.miRNARef[0].identifiers.id, self.samMap))
            miRNAName = self.miRNARef.get_miRNA_ById(uniqueId)[0].name
            fm = FreqMapmiRNA(len(frequency), uniqueId, miRNAName)
            
            self.freqMap.append(fm)
            
        self.logger.logOutput('miRNA frquency count complete.')
        return self.freqMap
            
        
    def getUniquemiRNAIds(self):
        miRNAIds = []
        
        for sm in self.samMap:
            miRNAId = sm.miRNARef[0].identifiers.id
            miRNAIds.append(miRNAId)
            
        uniqueIds = set(miRNAIds)
        
        return uniqueIds
                
                
class SAMMapmiRNA(object):
    
    def __init__(self, samRead, miRNARef):
        self.samRead = samRead
        self.miRNARef = miRNARef
        

class FreqMapmiRNA(object):
    
    def __init__(self, freq, miRNAId, miRNAName):
        self.freq = freq
        self.miRNAId = miRNAId
        self.miRNAName = miRNAName