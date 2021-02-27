
def create_superposition(programs, arguments_count):
    programs_count = len(programs)

    programs_list = []
    comand_counts= []
    max_registers = []
    
    for i, program in enumerate(programs):
        
        # read comands of program
        file = open(program)
        comands = file.read().split("\n")
        programs_list += [comands]
        comand_counts += [len(comands)]
        file.close()
        
        
        # find all used registers for all comands of program
        registers = []
        for comand in comands:
            comand = comand.replace(" ", "")
            if comand[0] in "ZS":
                registers += [int(comand[2:-1])]
            if comand[0] == "T":
                cmnd = comand[2:-1].split(",")
                registers += [int(cmnd[1])]
        
        # add to registers count of arguments
        registers += [programs_count-1] if i == 0 else [arguments_count]
        
        # find max for used register and number of argument
        max_registers += [max(registers)]
    
    
    # start register for first program is 0
    start_registers = [0]
    
    for i in range(1, programs_count):
        # start register for current program is sum of start register and
        # max used register for previous program increased by one
        start_registers += [start_registers[i-1] + max_registers[i-1] + 1]
        
    
    # add comand T to move data on coorect start register
    data_move_comands = []
    for i in range(1, programs_count):
        comands = programs_list[i]
        for j in range(0, arguments_count+1):
            data_move_comands += ["T("+ str(j) + "," + str(start_registers[i]+j) + ")"]
    
    
    current_comands_count = (arguments_count+1) * (programs_count - 1)
    
    
    # move command registers to correct intervals for all subprograms
    for i in range(1, programs_count):
        comands = programs_list[i]
        
        for j, comand in enumerate(comands):
            comand = comand.replace(" ", "")
            if comand[0] in "ZS":
                # move register in interval accroding start register
                regis = int(comand[2:-1])
                new_regis = regis + start_registers[i]
                comands[j] = comand[:2] + str(new_regis) + comand[-1]
                
            if comand[0] == "T":
                cmnd = comand[2:-1].split(",")
                # move register in interval accroding start register
                regis1 = int(cmnd[0])
                new_regis1 = regis1 + start_registers[i]
                regis2 = int(cmnd[1])
                new_regis2 = regis2 + start_registers[i]
                comands[j] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + comand[-1]
                
            if comand[0] == "J":
                cmnd = comand[2:-1].split(",")
                # move register in interval accroding start register
                regis1 = int(cmnd[0])
                new_regis1 = regis1 + start_registers[i]
                regis2 = int(cmnd[1])
                new_regis2 = regis2 + start_registers[i]
                
                cmd = int(cmnd[2])
                # if number of comand is zero or over program's comand number
                # change it on number of next comand
                if (cmd == 0) or (cmd > comand_counts[i]):
                    cmd = current_comands_count + comand_counts[i] + 1
                # else change comand number according to current comands count 
                else:
                    cmd = current_comands_count + cmd
                
                comands[j] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + \
                                                                                     "," + str(cmd) + comand[-1]
        current_comands_count += comand_counts[i]


    # add comand T to move result data on first registers
    result_data_move_comands = []
    for i in range(1, programs_count):
        result_data_move_comands += ["T("+ str(start_registers[i]) + "," + str(i) + ")"]
        
        
    current_comands_count += programs_count - 1
    
    
    # change comand number for f program because of last performing
    comands = programs_list[0]
    for j, comand in enumerate(comands):
            comand = comand.replace(" ", "")

            if comand[0] == "J":
                cmd = int(comand[-2])
                # if number of comand is over program's comand number change it on zero
                if cmd > comand_counts[0]:
                    cmd = 0
                # else change comand number according to current comands count 
                elif cmd != 0:
                    cmd = current_comands_count + cmd
                
                comands[j] = comand[:6] + str(cmd) + comand[-1]
    
    
    result_comands = data_move_comands
    for i in range(1, programs_count):
        result_comands += programs_list[i]
    result_comands += result_data_move_comands
    result_comands += programs_list[0]
    
    # write superposition program
    superpos_file = open("superposition.urm", "w")
    for comand in result_comands:
        superpos_file.write(comand + "\n")
    superpos_file.close()
    print("superposition program was created")
                
        
if __name__ == "__main__":
    programs = ["f.urm", "g1.urm", "g2.urm", "g3.urm"]
    arguments_count = 2
    create_superposition(programs, arguments_count)