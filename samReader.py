class SamFile(object):
    
    def __init__(self, path):
        self.reads = []

        reader = open(path, 'r')
        text = reader.read()
        reads = text.split('\n')
        
        for read in reads:
            if len(read) > 0 and not str(read)[0] == "@":
                read_data = str(read).split('\t')
                tags = []
                
                for x in range(11, len(read_data)):
                    tag = read_data[x].split(':')
                    t = SamTag(tag[0], tag[1], tag[2])
                    
                    tags.append(t)
                
                r = SamRead(read_data[0], read_data[1], read_data[2], \
                            read_data[3], read_data[4], read_data[5], \
                            read_data[6], read_data[7], read_data[8], \
                            read_data[9], read_data[10], tags)
                            
                self.reads.append(r)
        
        reader.close()
        
    def getReads(self):
        return self.reads
        

class SamRead(object):
    
    def __init__(self, qName, flag, rName, pos, mapq, cigar, mrnm, \
                 mpos, iSize, seq, qual, tags):
        self.qName = qName
        self.flag = flag
        self.rName = rName
        self.pos = pos
        self.mapq = mapq
        self.cigar = cigar
        self.mrnm = mrnm
        self.mpos = mpos
        self.iSize = iSize
        self.seq = seq
        self.qual = qual
        self.tags = tags
        self.endPos = (int(self.pos) + len(self.seq))

class SamTag(object):
    
    def __init__(self, tag, tag_type, value):
        self.tag = tag
        self.tag_type = tag_type
        self.value = value