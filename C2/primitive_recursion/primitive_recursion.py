
def create_primitive_recursion(program_f, program_g, arguments_count):

    programs = {}
    comand_counts = {}
    data_move_comands = {"f": [], "g": []}
    result_comands = []
    
    # read comands of program f
    file = open(program_f)
    programs["f"] = file.read().split("\n")
    comand_counts["f"] = len(programs["f"])
    file.close()
    
    # read comands of program g
    file = open(program_g)
    programs["g"] = file.read().split("\n")
    comand_counts["g"] = len(programs["g"])
    file.close()
    
        
    # find all used registers for all comands of program f
    registers = []
    comands = programs["f"]
    for comand in comands:
        comand = comand.replace(" ", "")
        if comand[0] in "ZS":
            registers += [int(comand[2:-1])]
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            registers += [int(cmnd[1])]
        
    # find max for used register and number of argument
    max_register = max(registers+[arguments_count])
    
    
    # start register for f is number arguments of f plus 1
    # start register for g is start register for f plus max used register for f plus 1
    start_registers = {"f": arguments_count+2, "g": arguments_count+2+max_register+1}

    # star part comand
    result_comands += ["J(0,0,4)"]
    # end part comands
    result_comands += [f"T({start_registers['g']},0)"]
    result_comands += ["J(0,0,0)"]
    current_comands_count = 3
    
    
    # add comand T to move data for f on coorect start register
    for i in range(0, arguments_count+1):
            data_move_comands["f"] += ["T("+ str(i) + "," + str(start_registers["f"]+i) + ")"]
    
    result_comands += data_move_comands["f"]
    current_comands_count += arguments_count + 1
    
    
    comands = programs["f"]
    for i, comand in enumerate(comands):
        comand = comand.replace(" ", "")
        
        if comand[0] in "ZS":
            # move register in interval accroding f start register
            regis = int(comand[2:-1])
            new_regis = regis + start_registers["f"]
            comands[i] = comand[:2] + str(new_regis) + comand[-1]
                
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding f start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_registers["f"]
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_registers["f"]
            comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + comand[-1]
                
        if comand[0] == "J":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding f start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_registers["f"]
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_registers["f"]
                
            cmd = int(cmnd[2])
            # if number of comand is zero or over f's comand number
            # change it on number of next comand
            if (cmd == 0) or (cmd > comand_counts["f"]):
                cmd = current_comands_count + comand_counts["f"] + 1
            # else change comand number according to current comands count 
            else:
                cmd = current_comands_count + cmd
                
            comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + \
                                                                                     "," + str(cmd) + comand[-1]
            
    result_comands += comands
    current_comands_count += comand_counts["f"]


    # check recursion for continue
    result_comands += [f"T({start_registers['f']},{start_registers['g']})"]
    result_comands += [f"J({arguments_count+1},{start_registers['g']+arguments_count+1},2)"]
    current_comands_count += 2
    check_comand = current_comands_count
    
    # add comand T to move data for g on coorect start register
    for i in range(1, arguments_count+1):
            data_move_comands["g"] += ["T("+ str(i) + "," + str(start_registers["g"]+i) + ")"]
    data_move_comands["g"] += [f"T({start_registers['g']},{start_registers['g']+arguments_count+2})"]
    data_move_comands["g"] += [f"T(0,{start_registers['g']})"]
    
    
    result_comands += data_move_comands["g"]
    current_comands_count += arguments_count + 2
    
    
    comands = programs["g"]
    for i, comand in enumerate(comands):
        comand = comand.replace(" ", "")
        
        if comand[0] in "ZS":
            # move register in interval accroding g start register
            regis = int(comand[2:-1])
            new_regis = regis + start_registers["g"]
            comands[i] = comand[:2] + str(new_regis) + comand[-1]
                
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding g start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_registers["g"]
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_registers["g"]
            comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + comand[-1]
                
        if comand[0] == "J":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding g start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_registers["g"]
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_registers["g"]
                
            cmd = int(cmnd[2])
            # if number of comand is zero or over g's comand number
            # change it on number of next comand
            if (cmd == 0) or (cmd > comand_counts["g"]):
                cmd = current_comands_count + comand_counts["g"] + 1
            # else change comand number according to current comands count 
            else:
                cmd = current_comands_count + cmd
                
            comands[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + \
                                                                                     "," + str(cmd) + comand[-1]
    result_comands += comands
    current_comands_count += comand_counts["g"]
    
    result_comands += [f"S({start_registers['g']+arguments_count+1})"]
    result_comands += [f"J(0,0,{check_comand})"]
    current_comands_count += 2
    
    
    # write primitive recursion program
    superpos_file = open("primitive_recursion.urm", "w")
    for comand in result_comands:
        superpos_file.write(comand + "\n")
    superpos_file.close()
    print("primitive recursion program was created")
                
        
if __name__ == "__main__":
    programs = ["f.urm", "g.urm"]
    arguments_count = 3
    create_primitive_recursion(programs[0], programs[1], arguments_count)