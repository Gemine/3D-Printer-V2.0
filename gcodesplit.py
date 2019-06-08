def split(Dir):
        sourcefile = Dir
        file1 = "Gcode/one.gcode"
        file2 = "Gcode/two.gcode"
        startcode = "Gcode/startcode.gcode"
        
        #data = f.readline()
        flag = 0
        f1 = open(file1, "w")
        f1.write("")
        f2 = open(file2, "w")
        f2.write("")
        f1.close
        f2.close
        f1 = open(file1, "a")
        f2 = open(file2, "a")
        
        f = open(startcode, "r")
        for x in f:
                f1.write(x)
                f2.write(x)
        f.close

        f = open(sourcefile, "r")
        for x in f:
                if x[0:2] == 'T0':
                        #switch to copy to file box1
                        flag = 1
                elif x[0:2] == 'T1':
                        #switch to copy to file box2
                        flag = 2
                elif x[0:2] == 'T2':
                        flag = 0
                else:
                        if flag == 1:
                                # copy to box 1
                                f1.write(x)
                                if x[0:4] == "G1 Z":
                                        f2.write(x)
                                #print(x)
                                #f1.close
                        elif flag == 2:
                                # copy to box2
                                #f2 = open(file2, "a")
                                f2.write(x)
                                if x[0:4] == "G1 Z":
                                        f1.write(x)
                                #f2.close
                        else:
                                pass
        f1.close
        f2.close
        f.close