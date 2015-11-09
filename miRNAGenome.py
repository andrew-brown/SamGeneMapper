class miRNACoordinate(object):

    def __init__(self, path):
        self.genome = []
        
        reader = open(path, 'r')
        text = reader.read()
        genes = text.split('\n')
        
        for gene in genes:
            if len(gene) > 0 and not str(gene)[0] == '#':
                gene_data = gene.split('\t')
                
                m = miRNA(gene_data[0], gene_data[2], gene_data[3], \
                          gene_data[4], gene_data[6], gene_data[8])
                          
                self.genome.append(m)
                
        reader.close()
                
    def get_miRNA_ById(self, miRNAId):
        miRNAs = list(filter(lambda x: x.identifiers.id == miRNAId))
        
        return miRNAs
        
    def get_miRNA_ByCoordinates(self, chromosome, start, end):
        miRNAs = list(filter(lambda x: chromosome == x.chromosome and \
                                       int(start) >= int(x.start) and \
                                       int(end) <= int(x.end)))
                                       
        return miRNAs
        
    def get_miRNA_ByName(self, name):
        miRNAs = list(filter(lambda x: x.identifiers.name == name))
        
        return miRNAs
        
    def get_miRNA_ByAlias(self, alias):
        miRNAs = list(filter(lambda x: x.identifiers.alias == alias))
        
        return miRNAs
                
class miRNA(object):
    
    def __init__(self, chromosome, miRNAType, start, \
                 end, strand, identifiers):
        self.chromosome = chromosome
        self.miRNAType = miRNAType(miRNAType)
        self.start = int(start)
        self.end = int(end)
        self.strand = strand
        self.identifiers = miRNAIdentifiers(identifiers)
        
    def __json__(self):
        return { 'chromosome': self.chromosome, \
                 'miRNAType': self.miRNAType, \
                 'start': self.start, \
                 'end': self.end, \
                 'strand': self.strand, \
                 'identifiers': self.identifiers }
        

class miRNAType(object):
    
    def __init__(self, miRNAType):
        if miRNAType == 'miRNA_primary_transcript':
            self.miRNAType = 'primary'
        else:
            self.miRNAType = 'mature'
            
    def __json__(self):
        return { 'miRNAType': self.miRNAType }
            
            
class miRNAIdentifiers(object):
    
    def __init__(self, identifiers):
        ids = identifiers.split(';')
        
        self.id = ids[0].split('=')[1]
        self.alias = ids[1].split('=')[1]
        self.name = ids[2].split('=')[1]
        
        if len(ids):
            self.derrivedFrom = ids[3]
            
    def __json__(self):
        return { 'id': self.id, \
                 'alias': self.alias, \
                 'name': self.name }