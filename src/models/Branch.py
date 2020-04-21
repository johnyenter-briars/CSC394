class Branch(object):

    def __init__(self, branchTuple):
        super().__init__()
        self._BranchID = branchTuple[0]
        self._StudentID = branchTuple[1]
        self._ProjectID = branchTuple[2]
        self._BranchDesc = branchTuple[3]
        self._Resolved = branchTuple[4]
        self._Weight = branchTuple[5]
        self._StudentList = []

    def getBranchId(self):
        return self._BranchID

    def getStudentId(self):
        return self._StudentID

    def getProjectID(self):
        return self._ProjectID

    def getBranchDesc(self):
        return self._BranchDesc

    def getResolved(self):
        return self._Resolved
    
    def getWeight(self):
        return self._Weight

    def addStudent(self, student):
        self._StudentList.append(student)

    