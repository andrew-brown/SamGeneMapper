import os

class Configuration(object):

    def __init__(self):
        self.application_directory = r'/Users/m149505/Google Drive/Mayo/Development/Src/Python/SamGeneMapper'
        self.input_directory = os.path.join(self.application_directory, 'Input')
        self.data_directory = os.path.join(self.application_directory, 'Data')
        self.output_directory = os.path.join(self.application_directory, 'Output')
        
    def getApplicationDirectory(self):
        return self.application_directory
        
    def getInputDirectory(self):
        return self.input_directory
        
    def getDataDirectory(self):
        return self.data_directory
    
    def getOutputDirectory(self):
        return self.output_directory