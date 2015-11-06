from humanGenome import *
from samReader import *
from configuration import *
import os
import copy_reg
import types
import threading

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else: 
        return getattr, (m.im_self, m.im_func.func_name)
        
copy_reg.pickle(types.MethodType, _pickle_method)


class SAMConverter(object):
    
    def __init__(self, input_path, logger):
        config = Configuration()
        
        self.logger = logger
        self.logger.logOutput('Reading gene coordinate reference into memory.')
        
        genomeRef = HumanGeneCoordinate(os.path.join(config.getDataDirectory(), \
                                  'hg38_gene_map.txt'))

        self.samFile = SamFile(input_path)
        self.genomeRef = genomeRef
        self.genomeRef
        self.samMap = []
        self.freqMap = []
        
        self.mtReads = []
        self.unmappedReads = []
        
    def mapReadsMT(self):
        threads = []
        self.logger.logOutput('Opening multithreaded pool for mapping.')
        reads = self.samFile.getReads()

        for read in reads:
            t = threading.Thread(target = self.asyncMapRead, args = \
                (read, self.samMap, self.genomeRef,))
            threads.append(t)
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()
            
        return
        
    def asyncMapRead(self, samRead, samMap, genomeRef):
        self.logger.logOutput('Mapping read: ' + samRead.qName)              
        result = genomeRef.get_genes_ByCoordinates(samRead.rName, \
                                                   samRead.pos, \
                                                   samRead.endPos)
        
        if len(result) > 0:
            s = SAMMap(samRead, result)
            self.mtReads.append(s)
        else:
            self.unmappedReads.append(samRead)
            
    def countFrequenciesMT(self, resultArray):
        threads = []
        self.logger.logOutput('Determining unique genes in reads.')
        uniqueIds = self.getUniqueGeneNamesAsync(resultArray)
        self.logger.logOutput(str(len(uniqueIds)) + ' unique genes found.')
        
        for uniqueId in uniqueIds:
            t = threading.Thread(target = self.getFrequencyAsync, args = \
                (self.samMap, uniqueId, self.genomeRef,))
            threads.append(t)
            
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()
            
        self.logger.logOutput('Frequency count complete.')
            
        return            
       
    def getFrequencyAsync(self, resultArray, geneId, genomeRef):
        frequency = list(filter(lambda x: geneId == x.genomeRef[0].geneId, \
                                    resultArray))        
        gene_name = genomeRef.get_genes_ByGeneId(geneId)[0].name
        fm = FreqMap(len(frequency), geneId, gene_name)
        
        self.freqMap.append(fm)
        
    def getUniqueGeneNamesAsync(self, resultArray):
        geneIds = []

        for ra in resultArray:
            geneId = ra.genomeRef[0].geneId
            geneIds.append(geneId)
            
        uniqueIds = set(geneIds)
        
        return uniqueIds
    
    def mapReads(self):
        samReads = self.samFile.getReads()
        
        for samRead in samReads:
            result = self.genomeRef.get_genes_ByCoordinates(samRead.rName, \
                                                            samRead.pos, \
                                                            samRead.endPos)
            
            if len(result) > 0:                                        
                s = SAMMap(samRead, result)                
                self.samMap.append(s)
            
    def countFrequencies(self):
        self.logger.logOutput('Determining unique genes in reads.')
        uniqueIds = self.getUniqueGeneNames()
        self.logger.logOutput(str(len(uniqueIds)) + ' unique genes found.')

        for uniqueId in uniqueIds:
            self.logger.logOutput('Counting occurrences of: ' + str(uniqueId) + '.')
            frequency = list(filter(lambda x: uniqueId == x.genomeRef[0].geneId, \
                                        self.samMap))
            gene_name = self.genomeRef.get_genes_ByGeneId(uniqueId)[0].name
            fm = FreqMap(len(frequency), uniqueId, gene_name)
            
            self.freqMap.append(fm)
        
        self.logger.logOutput('Frequency count complete.')
        return self.freqMap
        
    def getUniqueGeneNames(self):
        geneIds = []
        
        for sm in self.samMap:
            geneId = sm.genomeRef[0].geneId            
            geneIds.append(geneId)

        uniqueIds = set(geneIds)
        
        return uniqueIds 
           

class SAMMap(object):
    
    def __init__(self, samRead, genomeRef):
        self.samRead = samRead
        self.genomeRef = genomeRef
        
        
class FreqMap(object):
    
    def __init__(self, freq, geneId, geneName):
        self.freq = freq
        self.geneId = geneId
        self.geneName = geneName