import datetime
import os

class Logger(object):
    
    def __init__(self, output_dir):
        today = datetime.datetime.now()
        str_today = today.strftime('%Y%m%d_%H%m')
        
        self.writer = open(os.path.join(output_dir, (str_today + '.log')), 'w')
        
    def __del__(self):
        self.writer.close()
        
    def logError(self, errorMessage):
        self.writer.write('ERROR: ' + errorMessage + '\n')
        
    def logOutput(self, outputMessage):
        self.writer.write('OUTPUT: ' + outputMessage + '\n')