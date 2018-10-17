######################################################
#           File: phyMdlCodeParser.py                                                       #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Read an input phyMdl file and generate the codebox     #
#         code for use inside gen, then save it to an output file     #
######################################################


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

        # Error state
        self.error = 0

        # List of all material points
        self.matList = []

        self.destFolder = ""
        self.motionBufferName = "motion"

        self.generatedCode =""
        self.inputs = 0
        self.outputs = 0



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
                        self.initCode.append(phyMdlCodeGenerator.genGroundCode(l[0], l[2]))
                        self.matList.append(l[0])

                    if l[1] == "mass":
                        error = errorCheck(l, 5)
                        if (error == 0):
                            header, body =  phyMdlCodeGenerator.genMassCode(l[0], l[2], l[3], l[4])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.matList.append(l[0])
                        else:
                            break

                    if l[1] == "massG":
                        error = errorCheck(l, 6)
                        if (error == 0):
                            header, body =  phyMdlCodeGenerator.genMassGravityCode(l[0], l[2], l[3], l[4],l[5])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.matList.append(l[0])
                        else:
                            break

                    if l[1] == "osc":
                        error = errorCheck(l, 7)
                        if (error == 0):
                            header, body =  phyMdlCodeGenerator.genCelCode(l[0], l[2], l[3], l[4], l[5], l[6])
                            self.structCode.append(header)
                            self.matSimCode.append(body)
                            self.matList.append(l[0])
                        else:
                            break

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

        if (includeMotionData == 1):
            self.generatedCode += "Buffer " + self.motionBufferName + ";\n"

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
                self.generatedCode += self.writeMotionData(self.matList)

            print(self.generatedCode)

        print("all OK")

    def createDspObj(self, targetPath):
        self.generatedCode = self.generatedCode.replace('\n', '\\r\\n')
        phyMdlDspObjGenerator.generateDspObj(targetPath, self.generatedCode, self.inputs, self.outputs)

