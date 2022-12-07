import  operator

#global dictionary to be filled by round robin algorithim
ArivalTime = {}
BurstTime = {}
FinishTime = {}
StartTime = {}
processNum = 0
def getnextkey(dict,key):#returns next key in dictionary
     temp = list(dict)
     try:
         res = temp[temp.index(key) + 1]
     except (ValueError, IndexError):
            res = None
     return res
def RoundRoubinAlgo():
    global processNum

    processNum = int(input("please enter the number of process\n"))
    quantumTime = int(input("enter quantum time\n"))
    if processNum <= 0:
        return print("process number is incorrect must be above 0")
    if quantumTime <= 0:
        return print("quantum time is incorrect must be above 0")
    print("enter arrival time and burst time for each process respectivly \n")
    for i in range(processNum):
        ArivalTime[f"P{i + 1}"] = int(input())
        BurstTime[f"P{i + 1}"] = int(input())
    tempBurstTime = BurstTime.copy() #since we need Burst time for calculations we need the original copy to be safe
    # push first element to the ready queuee
    ready_queue = ["P1"]
    # steps couunter that keep track of process quantum time movement
    steps = ArivalTime.get(ready_queue[0])
    while len(ready_queue) > 0:
        workingProcess = ready_queue.pop(0)
        # if process ended its burst time (done working)
        if tempBurstTime.get(workingProcess) == "end":
            continue

        if workingProcess not in StartTime:
            StartTime[workingProcess] = steps #save starting time for each process

        # hold next process if
        nextProcess = getnextkey(ArivalTime, workingProcess)

        if tempBurstTime.get(workingProcess) == quantumTime:
            steps += quantumTime #increment my steps
            tempBurstTime[workingProcess] = "end" # process finished excuting
            FinishTime[workingProcess] = steps

            if nextProcess not in ready_queue and nextProcess != None:
                ready_queue.append(getnextkey(ArivalTime, workingProcess))

        elif tempBurstTime.get(workingProcess) < quantumTime:
            steps += tempBurstTime[workingProcess]
            tempBurstTime[workingProcess] = "end" # process finished excuting
            FinishTime[workingProcess] = steps
            if nextProcess not in ready_queue and nextProcess != None:
                ready_queue.append(getnextkey(ArivalTime, workingProcess))
        else: # processNum > 0
            steps += quantumTime  # increment my steps
            tempBurstTime[workingProcess] -= quantumTime  # decrement the burst

            # iterate at all proces that there arival time is <= steps and add them if they didnt exist in ready queue
            #and dont add the current process in order add it after other process has benn added
            for key in ArivalTime.keys():
                if ArivalTime[key] <= steps and tempBurstTime[key] != "end" and key != workingProcess:
                    if key not in ready_queue:
                        ready_queue.append(key)
            ready_queue.append(workingProcess)
def caculations():
    if processNum <= 0:
        exit()
    arivalValues = ArivalTime.values()
    burstValues  = BurstTime.values()
    finishValues = FinishTime.values()
    startValues  = StartTime.values()

    turnAroundTime = list(map(operator.sub, finishValues, arivalValues))
    print(f"avarege turn around time = {float(sum(turnAroundTime)/processNum)}")

    waitingdTime = list(map(operator.sub, turnAroundTime, burstValues))
    print(f"avarege waiting time = {float(sum(waitingdTime) / processNum)}")

    responseTime = list(map(operator.sub, startValues, arivalValues))
    print(f"avarege response time = {float(sum(responseTime) / processNum)}")

#project run
RoundRoubinAlgo()
caculations()