import os
class Files(object):
    def __init__(self, filesTuple):
        super().__init__()
        self._FileID = filesTuple[0]
        self._TaskID = filesTuple[1]
        self._FileName = filesTuple[2]
        self._File = filesTuple[3]

    def getFileID(self):
        return self._FileID

    def getTaskID(self):
        return self._TaskID

    def getFileName(self):
        return self._FileName

    def getFile(self):
        fname = os.getcwd()+"/app/static/tmp/"+self._FileName
        print(fname)
        with open(fname, 'wb') as file:
            file.write(self._File)
        print("Stored blob data into: ", self._FileName, "\n")
        shortfname = '/static/tmp/'+self._FileName
        return shortfname
