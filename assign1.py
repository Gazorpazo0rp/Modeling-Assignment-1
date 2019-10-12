class client(object):
    
    waitTime = None
    privilege = None

    def __init__(self, arriv, serv):
        self.arrivalTime = arriv
        self.serviceTime = serv
        


import numpy as np
#returns 0 for normal and 1 for Vip
def VIP():
    
    #Change after randomization
    return 0

def update(currTimeStep,peopleIterator,people,vipQueue,normalQueue):
    exitChecker=False
    while( not exitChecker):
        if(people[peopleIterator].arrivalTime<= currTimeStep):
            vipRandomizer=0
            if(len(normalQueue)<1):
                #if the normal queue is empty, force the randomizer towards the normal queue
                vipRandomizer=0
            else:
                vipRandomizer=VIP()
            #now insert into the corresponding queue
            if(vipRandomizer):
                vipQueue.append(peopleIterator)
            else:
                normalQueue.append(peopleIterator)
            peopleIterator+=1
        else:
            exitChecker=True
    return

#gets Daily clients sorted by arrival time and returns list 

def getPeople():
    people=[]
    dummyTime=0
    while( dummyTime<360 ):
        people.append()



    return people

def getServiceTime():
    pass
def serve(currTime,vipQueue,normalQueue):
    if(len(vipQueue)!=0):
        servingNow=vipQueue.pop()
        currTime+=servingNow.serviceTime
        return True
    elif(len(normalQueue)!=0):
        servingNow=normalQueue.pop()
        currTime+=servingNow.serviceTime
        return True
    return False

def sortClients():
    pass
def main():
    print("Hi \n Input Number of tests,service time mean and mean time between client arrivals consequtively please")
    n=input()
    s=input()
    a=input()
    people=[]
    peopleIterator=0
    currTimeStep=people[peopleIterator].arrivalTime
    #all customers
    normalQueue=[]
    vipQueue=[]
    people= getPeople()
    # all customers iterator
    peopleIterator=0
    while (peopleIterator<len(people) and  len(normalQueue) !=0 and len(vipQueue)!=0 ):
        update(currTimeStep,peopleIterator,people,vipQueue,normalQueue)
        successfullService=serve(currTimeStep,vipQueue,normalQueue)
        if(not successfullService):
            currTimeStep=people[peopleIterator].arrivalTime
        

main()

    





