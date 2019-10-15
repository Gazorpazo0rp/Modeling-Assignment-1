class client(object):

    def __init__(self, arriv, serv):
        self.arrivalTime = arriv
        self.serviceTime = serv
        self.waitTime = 0
        self.privilege = 0
        
#    def setWait(self,time):
#        self.waitTime=time
#        
#    def setPriv(self,priv):
#        self.privilege=priv

import numpy as np

#reads user input and does some processing
def readInput():
    print("Hello, this program simulates a queueing system.\nto start simulation kindly enter the required parameters")
    print("Enter number of replications to run")
    n = int(input())
    print("Enter mean for the exponential distribution of arrival times")
    a = float(input()) * 60
    print("Enter mean for the exponential distribution of service time")
    s = float(input()) * 60
    return n, a, s

#returns the time between the arrival of two customers
def getInterArrivalTime(a):
    return np.random.exponential(a)

#returns the service time of a client
def getServiceTime(s):
    return np.random.exponential(s)

#gets Daily clients sorted by arrival time and returns list 
def getPeople(a, s):
    #a list to store all clients that are supposed to arrive during a whole day
    people=[]
    #a variable to keep track of time when generating customers, we initialize it with first client arrival time
    dummyTime=getInterArrivalTime(a)
    
    while( dummyTime<21600 ):
        people.append(client(dummyTime, getServiceTime(s)))
        dummyTime+=getInterArrivalTime(a)

    return people
#returns 0 for normal and 1 for Vip
def VIP():
    return np.random.randint(0, 2)

#
def update(currTimeStep,peopleIterator,people,vipQueue,vipCnt,normalQueue):
    exitChecker=False
    peopleNo=len(people)
    
    while( not exitChecker and peopleIterator < peopleNo):
        if(people[peopleIterator].arrivalTime<=currTimeStep):
            
            if(len(normalQueue)>0 and VIP()):
                #if the normal queue is not empty and the randomizer returns 1, then a vip customer is generated
                vipQueue.append(peopleIterator)
                people[peopleIterator].privilege=1
                vipCnt+=1
            else:
                normalQueue.append(peopleIterator)
                people[peopleIterator].privilege=0
                
            peopleIterator+=1
            
        else:
            exitChecker=True
    return currTimeStep, peopleIterator, vipCnt

#
def serve(currTime,vipQueue,normalQueue,people):
    if(len(vipQueue)!=0):
        servingNow=vipQueue.pop()
        people[servingNow].waitTime=currTime-people[servingNow].arrivalTime
        currTime+=people[servingNow].serviceTime
        return True, currTime
    
    elif(len(normalQueue)!=0):
        servingNow=normalQueue.pop()
        people[servingNow].waitTime=currTime-people[servingNow].arrivalTime
        currTime+=people[servingNow].serviceTime
        return True, currTime
    
    return False, currTime

#
def getRepStats(people,privPrice):
    privCnt = 0
    privWait = 0
    normWait = 0
    
    for j in people:
        if( j.privilege == 1):
            privWait+=j.waitTime
            privCnt+=1
        else:
            normWait+=j.waitTime
        
    if( privCnt == 0):
        privCnt = 1
        
    return privCnt*privPrice, privWait/privCnt, normWait/(len(people)-privCnt)

#returns calculated stats in minutes
def getFinalStats(n,sumAvgWaitTimePriv,sumAvgWaitTimeNorm):
    avgWaitTimePriv = sumAvgWaitTimePriv/n
    avgWaitTimeNorm = sumAvgWaitTimeNorm/n
    avgWaitTime = (avgWaitTimePriv+avgWaitTimeNorm)/2
    return avgWaitTimePriv/60, avgWaitTimeNorm/60, avgWaitTime/60

def main():
    n, a, s = readInput()
    if( n==0 or a==0 or s==0 ):
        print("Error")
        return 0
    
    privPrice=30
    profit = 0
    sumAvgWaitTimePriv = 0
    sumAvgWaitTimeNorm = 0
    
    #create replications loop
    for i in range(n):
        
        #get all customers for this replication
        people=getPeople(a,s)
        
        #number of clients
        peopleNo = len(people)
        
        #all customers iterator
        peopleIterator=0
        
        #initialize time with first arrival
        currTimeStep=people[peopleIterator].arrivalTime
        
        #create queues for the two types of customers
        normalQueue=[]
        vipQueue=[]
        vipCnt = 0
    
    
        while (peopleIterator<peopleNo or  len(normalQueue) !=0 or len(vipQueue)!=0 ):
            currTimeStep,peopleIterator,vipCnt=update(currTimeStep,peopleIterator,people,vipQueue,vipCnt,normalQueue)
            successfullService,currTimeStep=serve(currTimeStep,vipQueue,normalQueue,people)
            if(not successfullService):
                currTimeStep=people[peopleIterator].arrivalTime
                
        p, sPriv, sNorm = getRepStats(people,privPrice)
        profit+=p
        sumAvgWaitTimePriv+=sPriv
        sumAvgWaitTimeNorm+=sNorm
            
    totAvgWaitTimePriv, totAvgWaitTimeNorm, totAvgWaitTime = getFinalStats(n, sumAvgWaitTimePriv, sumAvgWaitTimeNorm)
    
    print(totAvgWaitTimePriv,totAvgWaitTimeNorm,totAvgWaitTime,profit)
main()

    





