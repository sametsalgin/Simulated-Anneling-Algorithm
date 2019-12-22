import sys
import math
import random

#job transition times
job_transition_times={\
    1:{2:12,3:10},\
    2:{1:4,3:8},\
    3:{1:6,2:10},\
    }
#machine job times 
machine_times={\
    1:{1:10,2:4,3:8},\
    2:{1:12,2:9,3:5},\
    }
#machine relationship with jobs dict.
machine_jobs={}
#machines first job array because first job hasn't got transition time
machine_first_job=[]
costs={}
machine_count=0
job_count=0
best_case={}
next_case={}
next_cost=0
best_cost=999
def main():
    max_iteration=input("max iteration count :")
    temperature=input("max temparature :")
    #integer control
    try:
        max_iteration=int(max_iteration)
        temperature=int(temperature)
    except:
        print("ERROR(control value)")
        exit()
    machine_count=len(machine_times)
    job_count=len(job_transition_times)
    
    min_temperature=0.5
    alfa=0.5

    simulating_anneling(int(max_iteration),int(temperature),min_temperature,alfa,machine_count,job_count)
    print("---------------------best case---------------------")
    print(best_case,best_cost)



def simulating_anneling(max_iteration,temperature,min_temperature,alfa,machine_count,job_count):
    #control temperature
    while temperature > min_temperature:
        iteration = 1 
        #control iteration size
        while iteration <= max_iteration:
            create_next_case(machine_count,job_count)
            global best_cost
            global next_cost
            global best_case
            global next_case
            if best_cost>next_cost:
                best_cost=next_cost
                best_case=next_case

            random_probablity=random.random()
            ap = acceptance_probability(best_cost, next_cost, temperature)
            #tries to find better probability
            if ap > random_probablity:
                best_cost=next_cost
                best_case=next_case
            print(next_case,next_cost)
            iteration=iteration+1
        temperature=temperature*alfa

def acceptance_probability(old_cost, new_cost, temperature):
    try:
        #calculate
        res = math.exp((old_cost - new_cost) / temperature) 
    except OverflowError:
        res = float('inf')
    return res

def create_next_case(machine_count,job_count):
    
    machine_list=list(range(1,machine_count+1))
    job_list=list(range(1,job_count+1))
    jobs=[]
    global machine_jobs
    global machine_first_job
    machine_jobs={}

    while True:
        #random select job and machine
        random_select_job=random.choice(job_list)
        random_select_machine=random.choice(machine_list)
        #a job cannot be selected more than once
        if random_select_job not in jobs:
            jobs.append(random_select_job)
            for i in range(1,machine_count+1):
                #which machine selected
                if random_select_machine==i:
                    machine_jobs.setdefault(i,[])
                    machine_jobs[i].append(random_select_job)
                    

        if len(jobs)==job_count:
            calculate_cost()
            return False

          
def calculate_cost():
    global machine_jobs
    machine_first_job=[]
    #find machine
    for machine in machine_jobs:
        #find job
        for one_job in machine_jobs[machine]:
            #is the first job of the machine
            if machine not in machine_first_job :
                #calculate cost
                try:
                    machine_first_job.append(machine)
                    costs[machine]=machine_times[machine][one_job]
                    previos_job_name=one_job
                except:
                    print("ERROR (check jobs or machines table)")
                    
                    exit()
            else:
                #calculate cost
                try:
                    temp_cost=costs[machine]
                    temp_cost +=machine_times[machine][one_job]+job_transition_times[previos_job_name][one_job]
                    costs[machine]=temp_cost
                    previos_job_name=one_job
                except:
                    print("ERROR (check jobs or machines table)")
                    

    max_cost=0
    #select max cost(time)
    for machine in machine_jobs:
        cost= costs[machine]
        if cost>max_cost:
            max_cost=cost
    
    
    global next_case
    next_case=machine_jobs
    global next_cost
    next_cost=max_cost
    


if __name__ == '__main__':
    main()
