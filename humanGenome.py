class HumanGeneCoordinate(object):
    
    def __init__(self, path):
        self.genome = []

        reader = open(path, 'r')
        text = reader.read()
        genes = text.split('\n')
        
        for gene in genes:
            if len(gene) > 0 and not str(gene)[0] == '#':
                gene_data = gene.split('\t')

                g = HumanGene(gene_data[1], gene_data[2], gene_data[3], gene_data[4], \
                              gene_data[5], gene_data[6], gene_data[7], gene_data[8], \
                              gene_data[9], gene_data[10], gene_data[11], gene_data[12], \
                              gene_data[13], gene_data[14], gene_data[15])
                
                self.genome.append(g)
        
        reader.close()
            
    def get_genes_BySymbol(self, symbol):
        genes = list(filter(lambda x: symbol == x.name, self.genome))
        return genes
        
    def get_genes_ByCoordinates(self, chromosome, start, stop):
        genes = list(filter(lambda x: chromosome == x.chromosome and \
                                      int(start) >= int(x.txStart) and \
                                      int(stop) <= int(x.txEnd), self.genome))
        return genes
        
    def get_genes_ByGeneId(self, geneId):
        genes = list(filter(lambda x: geneId == x.geneId, self.genome))
        return genes
        
    def get_genes_ByCDSCoordinates(self, chromosome, start, stop):
        genes = list(filter(lambda x: chromosome == x.chromosome and \
                                       int(start) >= int(x.cdsStart) and \
                                       int(stop) <= int(x.cdsEnd), self.genome))
        return genes
    
class HumanGene(object):
    
    def __init__(self, geneId, chromosome, strand, txStart, txEnd, \
                 cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, score, \
                 name, cdsStartStat, cdsEndStat, exonFrames):
        self.chromosome = chromosome
        self.geneId = geneId
        self.strand = strand
        self.txStart = txStart
        self.txEnd = txEnd
        self.cdStart = cdsStart
        self.cdsEnd = cdsEnd
        self.exonCount = exonCount
        self.exonStarts = exonStarts
        self.exonEnds = exonEnds
        self.score = score
        self.name = name
        self.cdsStartStat = cdsStartStat
        self.cdsEndStat = cdsEndStat
        self.exonFrames = exonFrames