import csv
import math
import cluster_instances

def make_subsets(main, parts):
    subs = []
    for i in range(len(parts)):
        subs.append(merge_sets(main[parts[i][0]:parts[i][1]]))
    return subs

def set_partitions(num_parts):
    #makes list of tuples for evenly subsetting 
    #TODO: change partitions such that instead of a tuple indicating range for solvers, 
    #      it can be a list of specific solvers
    partitions = []
    last=0
    for i in range(num_parts):
        edge = math.ceil(solver_c/num_parts) * (i+1)
        if i == num_parts-1: #on last iter, extend edge to end
            partitions.append((last,solver_c+1))
            return partitions
        partitions.append((last,edge))
        last = edge
    return partitions

def evaluate_set(set, instance_parts):
    acc=0
    subset=[]
    for i in instance_parts:
        subset.append(set[i])
    for el in subset:
        if el < cutoff:
            solved_instances[set.index(el)]+=1
            acc+=1
    return acc
    
def merge_sets(set_of_sets):
    merged_set = []
    for i in range(instance_c):
        merged_set.append(cutoff)
    for set in set_of_sets:
        for i in range(instance_c):
            if set[i] < merged_set[i]:
                merged_set[i] = set[i]
    return merged_set

def find_subsets(data, subset_count):
    # set subset_count to 39 for individual solver performances
    
    sets = []   # 39 sets each with 380 measures
    for i in range(solver_c):
        sets.append([])
    for row in data:
        for el in range(len(row)-1):
            sets[el].append(float(row[el+1]))
    subsets = make_subsets(sets, set_partitions(subset_count))
    return subsets
    
if __name__ == '__main__':
    ##CONSTANTS##
    instance_c = 380
    solver_c = 39
    cutoff = 5000
    ##HYPER PARAMS##
    cluster_c = 12
    subset_c= 12
    ##
    print_results = True
    ##
    solved_instances = [0]*380 # tracks when an instance (denoted by index) is solved.
    instance_partitions = cluster_instances.main(cluster_c) 
    # denotes specific problem instances to evaluate for each subset of solvers 
    
    with open('aspeed-teton-SAT2018-39-solvers-10-parallel.csv', newline='') as f:
        next(f)
        reader = csv.reader(f)
        #####
        solver_sets = find_subsets(reader, subset_c)
        #####
        tot=0  
        for i in range(len(solved_instances)):
            if solved_instances[i]>0:
                tot+=1
        
        if (print_results):
            print("\n--RESULTS--\n")
            for i in range(len(solver_sets)):
                for e in range(len(instance_partitions)):
                    eval = evaluate_set(solver_sets[i], instance_partitions[e])
                    print("Solver Set " + str(i+1) + ", Problem Set "+ str(e+1) +": satisfied " + str(eval) + "/"+ str(len(instance_partitions[e])) +" instances (" + str(eval/len(instance_partitions[e])) + "%)")
            tot=0
            for i in range(len(solved_instances)):
                if solved_instances[i]>0:
                    tot+=1
            print("Total unique instances solved in this instance subset: " + str(tot) + "/380 (" + str(tot/380) + "%)")
        
        
        