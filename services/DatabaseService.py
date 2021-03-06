import sqlite3
from models.Student import Student
from models.Teacher import Teacher
from models.Project import Project
from models.UserCredentials import UserCredentials
from models.Branch import Branch
from models.Award import Award
from services.FlattenerService import BranchFlattener
from models.Files import Files
from models.Task import Task
from models.Chat import Chat
from models.TaskReview import TaskReview
from models.Goal import Goal
from models.Apple import Apple
from models.MessageNotifications import MessageNotifications
import os

DATABASE_PATH = 'database_files/Grove.db'

class DatabaseService(object):

    def __init__(self):
        super().__init__()
        self._db = None
        self.set_db()

    def set_db(self):
        self._db = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        
    def get_db(self):
        return self._db

    def getValidAppleTypes(self):
        return [Apple(tuple) for tuple in self._db.execute("select * from AppleType;").fetchall()] 

    def getUserCredentials(self):
        return [UserCredentials(tuple) for tuple in self._db.execute("select * from UserCredentials;").fetchall()] 

    def getStudents(self):
        return [Student(tuple) for tuple in self._db.execute("select * from Student;").fetchall()] 
    
    def getTeachers(self):
        return [Teacher(tuple) for tuple in self._db.execute("select * from Teacher;").fetchall()]

    def getStudentProject(self, StudentID):
         return [Project(tuple) for tuple in 
                self._db.execute("""select * from Project where ProjectID = 
                (select ProjectID from Student where StudentID = {id});""".format(id=StudentID))
                .fetchall()][0]

    def getStudent(self, StudentID):
        return [Student(tuple) for tuple in self._db.execute(
                """select * from Student where StudentID={id};""".format(id=StudentID)).fetchall()][0]

    def getTeacher(self, TeacherID):
        return [Teacher(tuple) for tuple in self._db.execute(
                """select * from Teacher where TeacherID={id};""".format(id=TeacherID)).fetchall()][0]
    
    def getBranchesForProject(self, ProjectID):
        return BranchFlattener(
                self._db.execute("""select * from Branch where ProjectID={id};"""
                .format(id=ProjectID)).fetchall()).flatten()
    
    def getBranchesForStudent(self, StudentID):
        return BranchFlattener(
                self._db.execute("""select * from Branch where StudentID={id};"""
                .format(id=StudentID)).fetchall()).flatten()

    def getTask(self, TaskID):
        return [Task(tuple) for tuple in self._db.execute("""
        select * from Task where TaskID={id};"""
        .format(id=TaskID)).fetchall()][0]

    def getTasksForBranch(self, BranchID, ProjectID):
        return [Task(tuple) for tuple in self._db.execute("""
                    select * from Task where BranchID={bid} and ProjectID={pid};"""
                    .format(bid=BranchID, pid=ProjectID)).fetchall()]
    
    def getTasksForProject(self, ProjectID):
        return [Task(tuple) for tuple in self._db.execute("""
                    select * from Task where ProjectID={pid};"""
                    .format(pid=ProjectID)).fetchall()]

    def getAwardsForStudent(self, StudentID):
        return [Award(tuple) for tuple in self._db.execute(
            """select * from Award where StudentID={id};""".format(id=StudentID)).fetchall()]
    
    def getTasksForStudent(self, StudentID):
        return [Task(tuple) for tuple in self._db.execute(
            """select * from Task where StudentID={id};""".format(id=StudentID)).fetchall()]

    def getProjectsForTeacher(self, TeacherID):
        return [Project(tuple) for tuple in self._db.execute("""
                    select * from Project where TeacherID={id};"""
                    .format(id=TeacherID)).fetchall()]

    def getClassList(self, TeacherID):
        return [Student(tuple) for tuple in self._db.execute(
                """select * from Student where TeacherID={id};""".format(id=TeacherID)).fetchall()]

    def getProject(self, ProjectID):
        return [Project(tuple) for tuple in self._db.execute("""
            select * from Project where ProjectID={id}"""
            .format(id=ProjectID)).fetchall()][0]

    def getStudentsOnProject(self, ProjectID):
        return [Student(tuple) for tuple in self._db.execute("""
            select * from Student where ProjectID={id}"""
            .format(id=ProjectID)).fetchall()]

    def getProjects(self):
        return [Project(tuple) for tuple in self._db.execute("select * from Project").fetchall()]

    def insertAward(self,StudentID:int,AppleType:str,ProjectName:str,DateAwarded:str):
        try:
            self._db.execute("""insert into Award("StudentID", "apple_type", "ProjectName", "DateAwarded")
                                values({id}, "{type}", "{name}", "{date}");"""
                                .format(id=StudentID,type=AppleType,name=ProjectName,date=DateAwarded))
            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def addMessage(self, UserName, TaskID, TimeStmp, MessageString, StudentID):
        self._db.execute(""" INSERT INTO Chat
            (UserName, TaskID, TimeStmp, MessageString) VALUES (?, ?, ?, ?)""", (UserName, TaskID, TimeStmp, MessageString))
        self._db.commit()
        ProjectID = self.getTask(TaskID).getProjectID()
        students = self.getStudentsOnProject(ProjectID)
        for student in students:
            if student.getStudentID() != StudentID:
                self._db.execute(""" INSERT INTO MessageNotifications
                (MessageContent, TaskID, Viewed, StudentID) VALUES (?, ?, ?, ?)""", (MessageString, TaskID, 0, student.getStudentID()))
                self._db.commit()

    def removeNotification(self, NotificationID):
        try:
            self._db.execute(""" DELETE FROM MessageNotifications
            WHERE NotificationID = ?""", (NotificationID,))
            self._db.commit()
            
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def getNotifications(self, StudentID, TaskID):
        try:
            return [MessageNotifications(tuple) for tuple in self._db.execute("""
                    select * from MessageNotifications where TaskID={tid} and StudentID={sid};"""
                    .format(tid=TaskID, sid=StudentID)).fetchall()]
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def getChatForTask(self, TaskID):
        return [Chat(tuple) for tuple in self._db.execute(
                """select * from Chat where TaskID={id};""".format(id=TaskID)).fetchall()]

    def getGoalForProject(self, ProjectID):
        return [Goal(tuple) for tuple in self._db.execute("""
        select * from ProjectGoal where ProjectID = {id}"""
        .format(id=ProjectID)).fetchall()][0]

    def getFilesForTask(self, TaskID):
        return [Files(tuple) for tuple in self._db.execute(
                """select * from Files where TaskID={id};""".format(id=TaskID)).fetchall()]

    def addFile(self, TaskID, FileName, FileType):
        try:
            self._db.execute(""" INSERT INTO Files
            (TaskID, FileName, FileType) VALUES (?, ?, ?)""", (TaskID, FileName, FileType))
            self._db.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def removeFile(self, FileName):
        try:
            self._db.execute(""" DELETE FROM Files
            WHERE FileName = ?""", (FileName,))
            self._db.commit()
            
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
            
    def insertNewStudent(self, FirstName:str, LastName:str, TeacherID:int, ProjectID: int, PermissionLevel:str):
        try:
            self._db.execute("""insert into Student(FirstName, LastName, TeacherID, 
                                ProjectID, RoleType) 
                                values("{fname}", "{lname}", {teachID}, {projID}, "{permLvl}");"""
                                .format(fname=FirstName, lname=LastName, teachID=TeacherID,
                                        projID=ProjectID, permLvl=PermissionLevel))
            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def insertNewTask(self, BranchID: int, StudentID: int, ProjectID: int, TaskDesc: str, TaskWeight: int):
        try:
            self._db.execute("""insert into Task
                                (BranchID, StudentID, ProjectID, TaskDescription, Resolved, Weight)
                                values({bID}, {sID}, {pID}, "{tDesc}", 0, "{tWght}");"""
                                .format(bID=BranchID, sID=StudentID, pID=ProjectID, tDesc=TaskDesc, tWght=TaskWeight))
            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def insertTaskReview(self, TaskID: int):
        try:
            self._db.execute("""insert into TaskReview
                                (TaskID, Resolved, Rating)
                                values({tID}, 0, 0);"""
                                .format(tID=TaskID))
            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def markTaskResolved(self, TaskID: int, Rating: int):
        try:
            self._db.execute("""UPDATE TaskReview
                                SET Resolved = 1, Rating = {Rating}
                                WHERE TaskID = {tID}"""
                                .format(tID=TaskID, Rating=Rating))

            self._db.execute("""UPDATE Task
                                SET Resolved = 1
                                WHERE TaskID = {tID}"""
                                .format(tID=TaskID, Rating=Rating))

            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def getTasksToBeReviewed(self):
        return [TaskReview(tuple) for tuple in self._db.execute("select * from TaskReview").fetchall()]

    def getTaskReviewedStatus(self, TaskID: int):
        return [TaskReview(tuple) for tuple in self._db.execute(
            """select * from TaskReview where TaskID={id};""".format(id=TaskID)).fetchall()]

    def updateAwardedApples(self, StudentID: int):
        self._db.execute("""UPDATE Student SET ApplesAwarded = ApplesAwarded + 1 WHERE StudentID = {StudentID}""".format(StudentID=StudentID))
        self._db.commit()

    def updateTaskCreation(self, StudentID: int):
        self._db.execute("""UPDATE Student SET FirstTask = 1 WHERE StudentID = {StudentID}""".format(StudentID=StudentID))
        self._db.commit()

    def updateGrowthStatus(self, ProjectID, GrowthStatus: str):
        try:
            self._db.execute("""UPDATE Project
                                SET GrowthStatus = '{gStatus}'
                                WHERE ProjectID = {pID}"""
                                .format(gStatus=GrowthStatus, pID=ProjectID))

            self._db.commit()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        
    def getTaskReviewsForProject(self, ProjectID: int):
        return [TaskReview(tuple) for tuple in self._db.execute(
            """select * from Taskreview where taskid in 
            (select TaskID from Task where ProjectID = {projID});"""
            .format(projID=ProjectID))]

    def close_connection(self, exception):
        self._db.close()
        