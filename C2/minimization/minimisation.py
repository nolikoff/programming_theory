
def create_minimization(program_f, arguments_count):

    program = []
    data_move_comands = []
    result_comands = []
    
    # read comands of program f
    file = open(program_f)
    program = file.read().split("\n")
    comands_count = len(program)
    file.close()
    
    
    start_register = arguments_count + 3
    
    
    # add comand T to move data for f on coorect start register
    for i in range(0, arguments_count+2):
            data_move_comands += ["T("+ str(i) + "," + str(start_register+i) + ")"]
    
    result_comands += data_move_comands
    
    
    for i, comand in enumerate(program):
        comand = comand.replace(" ", "")
        
        if comand[0] in "ZS":
            # move register in interval accroding f start register
            regis = int(comand[2:-1])
            new_regis = regis + start_register
            program[i] = comand[:2] + str(new_regis) + comand[-1]
                
        if comand[0] == "T":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding f start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_register
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_register
            program[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + comand[-1]
                
        if comand[0] == "J":
            cmnd = comand[2:-1].split(",")
            # move register in interval accroding f start register
            regis1 = int(cmnd[0])
            new_regis1 = regis1 + start_register
            regis2 = int(cmnd[1])
            new_regis2 = regis2 + start_register
                
            cmd = int(cmnd[2])
            # if number of comand is zero or over f's comand number
            # change it on number of next comand
            if (cmd == 0) or (cmd > comands_count):
                cmd = len(data_move_comands) + comands_count + 1
            # else change comand number according to current comands count 
            else:
                cmd = len(data_move_comands) + cmd
                
            program[i] = comand[:2] + str(new_regis1) + "," + str(new_regis2) + \
                                                                                     "," + str(cmd) + comand[-1]
            
    result_comands += program
    

    # check if root is found
    result_comands += [f"J({arguments_count+2},{start_register}," + \
                                       f"{len(data_move_comands) + comands_count+4})"]
    
    # end of program
    result_comands += [f"S({arguments_count+1})"]
    result_comands += ["J(0,0,1)"]
    result_comands += [f"T({arguments_count+1},0)"]
    
    
    # write minimization program
    superpos_file = open("minimization.urm", "w")
    for comand in result_comands:
        superpos_file.write(comand + "\n")
    superpos_file.close()
    print("minimization program was created")
                
        
if __name__ == "__main__":
    program = "f.urm"
    arguments_count = 2
    create_minimization(program, arguments_count)