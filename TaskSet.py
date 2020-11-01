from Task import Task 
import datetime

class TaskSet:
    active=""
    name=""
    version=0
    taskList=[]
    dateCreated=""
    checkBoxList=[]
    checkBoxVarList=[]

    

    def generateUpdatePackage(self):
        taskSetString= (
            "TS " + self.active + " " + self.dateCreated + " " + str(self.version) + " " + self.name 
            + self.taskListString() + "\n" +"ET" )
    
        return taskSetString
 
    def viewTaskSet(self):
        return (self.generateUpdatePackage())

    def viewTaskDetails(self):
        counter=1
        for i in (self.taskList):
            print(str(counter) + " " + str(i.weight) + " " + str(i.position) +  " " + i.description)
            counter=counter+1
            
    
    def taskListString(self):
        returnString=""
        
        for i in self.taskList:
            if i:
                returnString=returnString+"\n"
            returnString=returnString+i.getDetails()
        return returnString

    def saveToFile(self, fileName):
        f = open(fileName, "w")
        f.write(self.generateUpdatePackage())
        f.close()

    def addNewVersionToFile(self, fileName):
    
        self.dateCreated=datetime.date.today().strftime("%d%m%Y")
        f = open(fileName, "r")
        contents= f.read()
        f.close()   
        
        contents=contents.replace("TS Y", "TS N")


        f = open(fileName, "w")
        f.write(contents + "\n" + self.generateUpdatePackage())
        f.close()    
    
    def isActive(self):
        if self.active=="Y":
            return True
            
    def getPointsPerWeight(self):
        totalWeight=0
        
        for i in self.taskList:
            totalWeight=totalWeight+int(i.weight)
        
        return 100/totalWeight

               
    def createCheckBoxVarListStorageString(self):
        storageString=""
        for i in self.checkBoxVarList:
            storageString=storageString+str(i.get())
        
        return storageString

    def createinitCheckBoxVarListStorageString(self):
        storageString=""
        for i in self.checkBoxVarList:
            storageString=storageString+"0"
        
        return storageString    
    
    
    def getTotalPointsForDay(self):
        counter=0
        points = 0
                
        
        for i in self.checkBoxVarList:          
            if(i.get()==1):
                points=points+(self.getPointsPerWeight() * int(self.taskList[counter].weight))
                
            counter=counter+1
            
        return (int(round(points)))
        
    def getVersionAndName(self):
        return str(self.version) + " " + self.name
        
    def isDifferent(self, otherTaskSet):
        changed=False
        #compare contents if size is same (check for changed description or weight
        for f, b in zip(self.taskList, otherTaskSet.taskList):
            if(f.description!=b.description):
                changed=True
                break
            else:
                if(f.weight!=b.weight):
                    changed=True
                    break
        #check if lists have same number of items, if not flag as changed
        if(len(self.taskList)!=len(otherTaskSet.taskList)):
            changed=True
        
        return changed
        
    def convertToSortedString(self, string):
        self.taskList.sort(key=lambda x: (int(x.weight), int(x.position)), reverse=True)
        
        weightList=[]
        postList=[]
        
        for i in (self.taskList):
            weightList.append(int(i.weight))
            postList.append(int(i.position))
        
        
        z = zip (weightList, postList)
        zsorted=sorted(z, key=lambda x: (weightList, postList), reverse=True)
        weightList, postList = zip(*zsorted)
     
        sortedString=""
        for i in postList:
            sortedString=sortedString+string[i]

        return sortedString        
        
        
    def convertToOriginalString(self, sortedString):
        postList=[]
        for i in (self.taskList):
            postList.append(int(i.position))
        
        unsortedString=""
        counter=0

        
        while counter<len(postList):
            
            index=postList.index(counter)
            unsortedString=unsortedString+sortedString[index]
            
            counter=counter+1
            
        return unsortedString

        
            

