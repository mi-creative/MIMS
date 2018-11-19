######################################################
#           File: phyMdlCodeParser.py                                                       #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Read an input phyMdl file and generate the codebox     #
#         code for use inside gen, then save it to an output file     #
######################################################

## Use the library version or direct macro code generation (TODO: compare efficiency)

LIB_VERSION = True

# import physicsGenerator.phyMdlCodeGenerator as phyMdlCodeGenerator
if(LIB_VERSION == True):
    import physicsGenerator.mipeLibCodeGenerator as phyMdlCodeGenerator
else:
    import physicsGenerator.phyMdlCodeGenerator as phyMdlCodeGenerator

import physicsGenerator.phyMdlDspObjGenerator as phyMdlDspObjGenerator

import sys



########################################################
####       Error check function: do we have enough parameters?
########################################################
def errorCheck(mdlList, nbParams):
    if (len(mdlList) < nbParams):
        print("Error: Not enough parameters for  module: " + str(l))
        print("Leaving!")
        return 1
    else:
        return 0


class PhysicsGenParser():

    def __init__(self, parent=None):

        # list holders for generate DSP Code
        self.structCode = []
        self.initCode = []
        self.matSimCode = []
        self.interactSimCode = []
        self.motionCode = []

        # Error state
        self.error = 0

        # List of all material points
        self.matList = []

        self.destFolder = ""
        self.motionBufferName = "motion"

        self.userBufferList = []

        self.generatedCode =""
        self.inputs = 0
        self.outputs = 0

    def writeGenericMotionData(self, mat_name):
        self.motionCode.append(
            self.motionBufferName + ".poke(" + mat_name[1:] + "_X, " + str(len(self.matList)) + ", 0);\n")


    def writeSpecificMotionData(self, mat_name, motion_name, xpos, ypos):
        self.motionCode.append(
            motion_name + ".poke(" + mat_name[1:] + "_X, " + str(len(self.matList)) + ", 0);\n")
        self.motionCode.append(
            motion_name + ".poke(" + str(xpos) + ", " + str(len(self.matList)) + ", 1);\n")
        self.motionCode.append(
            motion_name + ".poke(" + str(ypos) + ", " + str(len(self.matList)) + ", 2);\n")

    def addMotionBufferToList(self, buffer_name):
        if buffer_name not in self.userBufferList:
            self.userBufferList.append(buffer_name)

    def declareBufferList(self):
        for buffer in self.userBufferList:
            self.generatedCode += "Buffer " + buffer + ";\n"

    def writeMotionData(self, mList):
        cpt = 0
        s = ""
        while len(mList) > 0:
            name = mList.pop()
            s += self.motionBufferName + ".poke(" + name[1:] + "_X, " + str(cpt) + ");\n"
            cpt = cpt +1

        print("all OK")
        return s


    ########################################################
    ####       phyMdl file parsing
    ####        read through the model file, ignoring comments, etc.
    ########################################################

    def parseModel(self, modelDescr, includeMotionData):
        # dest = open(genCodePath,'w')

        error = 0

        self.motionCode.clear()

        print("About to enter model generation...")

        compList = modelDescr.split("\n")

        for line in compList:
            if  line.startswith('#') == True :
                pass
            else :
                rCom = line.rsplit('#')
                l = rCom[0].rsplit()
                #####################################################
                ###      Generate gendsp code from the model information
                #####################################################
                if(len(l) > 2):
                    if l[1] == "param":
                        # Note : changed order for param. Remove @ from parameter name
                        self.structCode.append(phyMdlCodeGenerator.genParamCode(l[0][1:], l[2]))

                    if l[1] == "ground":
                        if (len(l)== 3):     # if no explicit motion data is specified
                            header, body = phyMdlCodeGenerator.genGroundCode(l[0], l[2])
                            self.initCode.append(header)
                            self.matSimCode.append(body)
                            self.writeGenericMotionData(l[0])
                            self.matList.append(l[0])
                        elif (len(l) == 6): # if specific position data is supplied
                            header, body = phyMdlCodeGenerator.genGroundCode(l[0], l[2])
                            self.initCode.append(header)
                            self.matSimCode.append(body)
                            self.writeSpecificMotionData(l[0], str(l[3]), l[4], l[5])
                            self.addMotionBufferToList(str(l[3]))
                            self.matList.append(l[0])
                        else:
                            print("Error: Wrong number of parameters for  module: " + str(l))

                        # error = errorCheck(l, 5)
                        # header, body = phyMdlCodeGenerator.genGroundCode(l[0], l[2])
                        # self.initCode.append(header)
                        # self.matSimCode.append(body)
                        # self.writeSingleMotionData(l[0], l[3], l[4])
                        # #self.initCode.append(phyMdlCodeGenerator.genGroundCode(l[0], l[2]))
                        # self.matList.append(l[0])

                    if l[1] == "mass":
                        if (len(l)== 5):     # if no explicit motion data is specified
                            header, body = phyMdlCodeGenerator.genMassCode(l[0], l[2], l[3], l[4])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeGenericMotionData(l[0])
                            self.matList.append(l[0])
                        elif (len(l) == 8): # if specific position data is supplied
                            header, body = phyMdlCodeGenerator.genMassCode(l[0], l[2], l[3], l[4])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeSpecificMotionData(l[0], str(l[5]), l[6], l[7])
                            self.addMotionBufferToList(str(l[5]))
                            self.matList.append(l[0])
                        else:
                            print("Error: Wrong number of parameters for  module: " + str(l))

                        # error = errorCheck(l, 7)
                        # if (error == 0):
                        #     header, body =  phyMdlCodeGenerator.genMassCode(l[0], l[2], l[3], l[4])
                        #     self.structCode.append(header)
                        #     self.matSimCode.append(body)
                        #     self.writeSingleMotionData(l[0], l[5], l[6])
                        #     self.matList.append(l[0])
                        # else:
                        #     break

                    if l[1] == "massG":
                        if (len(l)== 6):     # if no explicit motion data is specified
                            header, body = phyMdlCodeGenerator.genMassGravityCode(l[0], l[2], l[3], l[4], l[5])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeGenericMotionData(l[0])
                            self.matList.append(l[0])
                        elif (len(l) == 9): # if specific position data is supplied
                            header, body = phyMdlCodeGenerator.genMassGravityCode(l[0], l[2], l[3], l[4], l[5])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeSpecificMotionData(l[0], str(l[6]), l[7], l[8])
                            self.addMotionBufferToList(str(l[6]))
                            self.matList.append(l[0])
                        else:
                            print("Error: Wrong number of parameters for  module: " + str(l))
                        # error = errorCheck(l, 6)
                        # if (error == 0):
                        #     header, body =  phyMdlCodeGenerator.genMassGravityCode(l[0], l[2], l[3], l[4],l[5])
                        #     self.structCode.append(header)
                        #     self.matSimCode.append(body)
                        #     self.writeSingleMotionData(l[0], l[5], l[6])
                        #     self.matList.append(l[0])
                        # else:
                        #     break

                    if l[1] == "osc":
                        if (len(l)== 7):     # if no explicit motion data is specified
                            header, body = phyMdlCodeGenerator.genCelCode(l[0], l[2], l[3], l[4], l[5], l[6])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeGenericMotionData(l[0])
                            self.matList.append(l[0])
                        elif (len(l) == 10): # if specific position data is supplied
                            header, body = phyMdlCodeGenerator.genCelCode(l[0], l[2], l[3], l[4], l[5], l[6])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.writeSpecificMotionData(l[0], str(l[7]), l[8], l[9])
                            self.addMotionBufferToList(str(l[7]))
                            self.matList.append(l[0])
                        else:
                            print("Error: Wrong number of parameters for  module: " + str(l))

                        # error = errorCheck(l, 9)
                        # if (error == 0):
                        #     header, body =  phyMdlCodeGenerator.genCelCode(l[0], l[2], l[3], l[4], l[5], l[6])
                        #     self.structCode.append(header)
                        #     self.matSimCode.append(body)
                        #     self.writeSingleMotionData(l[0], l[7], l[8])
                        #     self.matList.append(l[0])
                        # else:
                        #     break

                    if l[1] == "spring":
                        error = errorCheck(l, 6)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genSpringCode(l[0], l[2], l[3], l[4], l[5])
                            self.interactSimCode.append(body)
                        else:
                            break

                    if l[1] == "detent":
                        error = errorCheck(l, 7)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genDetentCode(l[0], l[2], l[3], l[4], l[5], l[6])
                            self.interactSimCode.append(body)
                        else:
                            break

                    if l[1] == "nlBow":
                        error = errorCheck(l, 6)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genNLBowCode(l[0], l[2], l[3], l[4], l[5])
                            self.interactSimCode.append(body)
                        else:
                            break

                    if l[1] == "nlPluck":
                        error = errorCheck(l, 6)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genNLPluckCode(l[0], l[2], l[3], l[4], l[5])
                            self.interactSimCode.append(body)
                        else:
                            break

                    if l[1] == "nlSpring":
                        error = errorCheck(l, 7)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genNLSpringCode(l[0], l[2], l[3], l[4], l[5], l[6])
                            self.interactSimCode.append(body)
                        else:
                            break

                    if l[1] == "posInput":
                        error = errorCheck(l, 3)
                        if (error == 0):
                            header, body  =  phyMdlCodeGenerator.genPosInputCode(l[0], l[2])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.inputs += 1
                        else:
                            break

                    if l[1] == "frcInput":
                        error = errorCheck(l, 3)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genForceInputCode(l[0], l[2])
                            self.interactSimCode.append(body)
                            self.inputs += 1
                        else:
                            break

                    if l[1] == "posOutput":
                        error = errorCheck(l, 3)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genPosOutputCode(l[0], l[2])
                            self.interactSimCode.append(body)
                            self.outputs += 1
                        else:
                            break

                    if l[1] == "frcOutput":
                        error = errorCheck(l, 3)
                        if (error == 0):
                            body =  phyMdlCodeGenerator.genForceOutputCode(l[0], l[2])
                            self.initCode.append(body)
                            self.outputs += 1
                        else:
                            break

        ########################################################
        ####       Write the generated code to the output destination,
        ####        respecting order (structures, declarations, simcode)
        ########################################################

        if(LIB_VERSION):
            self.generatedCode += 'require(\\"mipe-lib\\");\n'

        if (includeMotionData == 1):
            self.generatedCode += "Buffer " + self.motionBufferName + ";\n"

        self.declareBufferList()

        if (error == 0):
            while len(self.structCode) > 0:
                tmp = self.structCode.pop()
                self.generatedCode += tmp
            while len(self.initCode) > 0:
                tmp = self.initCode.pop()
                self.generatedCode += tmp
            while len(self.matSimCode) > 0:
                tmp = self.matSimCode.pop()
                self.generatedCode += tmp
            while len(self.interactSimCode) > 0:
                tmp = self.interactSimCode.pop()
                self.generatedCode += tmp

            if (includeMotionData):
                while len(self.motionCode) > 0:
                    self.generatedCode += self.motionCode.pop()

            print(self.generatedCode)

        print("all OK")

    def createDspObj(self, targetPath):
        self.generatedCode = self.generatedCode.replace('\n', '\\r\\n')
        phyMdlDspObjGenerator.generateDspObj(targetPath, self.generatedCode, self.inputs, self.outputs)

