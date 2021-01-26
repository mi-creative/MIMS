######################################################
#           File: phyMdlCodeParser.py                                                       #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Read an input phyMdl file and generate the codebox     #
#         code for use inside gen, then save it to an output file     #
######################################################

import sys
import pprint
import numpy as np


pp = pprint.PrettyPrinter(indent=4)

NEW_ROUTING = False


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

class Physics2Faust():

    def __init__(self, parent=None):

        # Dictionary of all material physical modules
        self.matModuleDict = {"mass" : [],
                           "osc" : [],
                           "ground" : [],
                           "posInput": []}

        # Dictionary with name and index of all Mat modules
        self.matModuleMap = {}
        # Indexed parameters
        self.indexedParams = []
        # Dictionary of all interaction physical modules
        self.linkModuleDict = {"spring" : [],
                               "collision" : [],
                               "nlBow": [],
                               "nlPluck" : []}
        
        # The M point(lines) and L point (columns) matrix
        dim = (1,1)
        self.routingMatrix = np.zeros(dim)

        # labels of the output masses (positions are routed to output)
        self.outputMasses = []
        self.outputs = 0

        # Error state
        self.error = 0

        self.destFolder = ""
        self.generatedCode =""

        self.inNames = []
        self.inputs = 0

        self.frcInputs = []


    def getPosFromMatId(self, matId, delayed = False):
        offset = 0
        if delayed:
            offset = 1
        for mat in self.matModuleDict["mass"]:
            if mat[0] == matId:
                return mat[2 + offset]
        for mat in self.matModuleDict["osc"]:
            if mat[0] == matId:
                return mat[4 + offset]
        for mat in (self.matModuleDict["ground"] or self.matModuleDict["posInput"]):
            if mat[0] == matId:
                return mat[1]
        return 0


    ########################################################
    ####       phyMdl file parsing
    ####        read through the model file, ignoring comments, etc.
    ########################################################

    def parseModel(self, modelDescr):

        error = 0
        error_msg =""

        print("About to enter model generation...")

        compList = modelDescr.split("\n")

        # First parsing: order of material points.
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
                        self.indexedParams.append([l[0][1:], l[2]])

                    if l[1] == "audioParam":
                        self.indexedParams.append([l[0][1:], l[2]])

                    if l[1] == "ground":
                        self.matModuleDict["ground"].append([l[0], l[2]])

                    if l[1] == "mass":
                        if (len(l) == 5) or (len(l) == 8):
                            self.matModuleDict["mass"].append([l[0], l[2], l[3], l[4]])
                        else:
                            error = -1
                            error_msg = "Can't allocate mass module (wrong number of parameters)"
                            break
                    if l[1] == "osc":
                        if (len(l) == 7) or (len(l) == 10):
                            self.matModuleDict["osc"].append([l[0], l[2], l[3], l[4], l[5] , l[6]])
                        else:
                            error = -2
                            error_msg = "Can't allocate osc module (wrong number of parameters)"
                            break

                    ## Currently, all springs, dampers or springDampers generate "springs" in Faust

                    if l[1] == "spring" or l[1] == "springDamper":
                        if (len(l) == 6):
                            self.linkModuleDict["spring"].append([l[0], l[2], l[3], l[4], l[5]])
                        elif (len(l) == 5):
                            self.linkModuleDict["spring"].append([l[0], l[2], l[3], l[4], 0])
                        else:
                            error = -10
                            error_msg = "Issue allocating spring type module (wrong number of parameters)"
                            break
                    if l[1] == "damper":
                        if len(l) == 5:
                            self.linkModuleDict["spring"].append([l[0], l[2], l[3], 0, l[4]])
                        else:
                            error = -11
                            error_msg = "Issue allocating damper type module (wrong number of parameters)"
                            break

                    if l[1] == "contact":
                        if len(l) == 7:
                            self.linkModuleDict["collision"].append([l[0], l[2], l[3], l[4], l[5], l[6]])
                        else:
                            error = -12
                            error_msg = "Issue allocating contact type module (wrong number of parameters)"
                            break

                    if l[1] == "nlBow":
                        if (len(l) == 6):
                            self.linkModuleDict["nlBow"].append([l[0], l[2], l[3], l[4], l[5]])
                        else:
                            error = -13
                            error_msg = "Issue allocating nlBow type module (wrong number of parameters)"
                            break

                    if l[1] == "nlPluck":
                        if (len(l) == 6):
                            self.linkModuleDict["nlPluck"].append([l[0], l[2], l[3], l[4], l[5]])
                        else:
                            error = -14
                            error_msg = "Issue allocating nlPluck type module (wrong number of parameters)"
                            break

                    if l[1] == "posOutput":
                        if (len(l) == 3):
                            self.outputMasses.append(l[2])
                            self.outputs += 1
                        else:
                            error = -15
                            error_msg = "Issue allocating position output (wrong number of parameters)"
                            break
                    if l[1] == "posInput":
                        if (len(l) == 3):
                            self.matModuleDict["posInput"].append([l[0], l[2]])
                            self.inputs += 1
                            self.inNames.append(l[0][1:])
                        else:
                            error = -16
                            error_msg = "Issue allocating position input (wrong number of parameters)"
                            break

                    if l[1] == "frcInput":
                        if (len(l) == 3):
                            self.frcInputs.append([l[0][1:], l[2]])
                        else:
                            error = -17
                            error_msg = "Issue allocating force input (wrong number of parameters)"
                            break

                    if l[1] == "nlSpring" or l[1] == "nlSpring2" or l[1] == "nlSpring3":
                        error = -18
                        error_msg = "Non-linear springs are not yet available in FAUST"
                        break
                    if l[1] == "frcOutput":
                        error = -19
                        error_msg = "Force output is not yet available in FAUST"
                        break

        if error:
            return error, error_msg

        pp.pprint(self.matModuleDict)
        pp.pprint(self.linkModuleDict)

        # Build the map between module identifiers and index in the Mat table
        index = 0
        for mat in self.matModuleDict["ground"]:
            self.matModuleMap[mat[0]] = index
            index+=1
        for mat in self.matModuleDict["mass"]:
            self.matModuleMap[mat[0]] = index
            index+=1
        for mat in self.matModuleDict["osc"]:
            self.matModuleMap[mat[0]] = index
            index+=1
        for mat in self.matModuleDict["posInput"]:
            self.matModuleMap[mat[0]] = index
            index+=1

        # If any force inputs, find the index of the concerned Mats
        # in this method, the module name in the frcInputs is switched to the index
        for frcList in self.frcInputs:
            for name, index in self.matModuleMap.items():
                if name == frcList[1]:
                    frcList[1] = index

        matDim = len(self.matModuleDict["ground"])\
                 + len(self.matModuleDict["mass"])\
                 + len(self.matModuleDict["osc"])\
                 + len(self.matModuleDict["posInput"])

        linkDim = len(self.linkModuleDict["spring"])\
                  + len(self.linkModuleDict["collision"])\
                  + len(self.linkModuleDict["nlBow"])\
                  + len(self.linkModuleDict["nlPluck"])

        dim = (matDim,linkDim * 2)
        self.matRoutingMatrix = np.zeros(dim)

        print(self.matModuleMap)

        matrixIndex = 0
        for link in self.linkModuleDict["spring"]:
            self.matRoutingMatrix[self.matModuleMap[link[1]],2*matrixIndex] = 1
            self.matRoutingMatrix[self.matModuleMap[link[2]],2*matrixIndex+1] = 1
            matrixIndex += 1
        for link in self.linkModuleDict["collision"]:
            self.matRoutingMatrix[self.matModuleMap[link[1]],2*matrixIndex] = 1
            self.matRoutingMatrix[self.matModuleMap[link[2]],2*matrixIndex+1] = 1
            matrixIndex += 1
        for link in self.linkModuleDict["nlBow"]:
            self.matRoutingMatrix[self.matModuleMap[link[1]],2*matrixIndex] = 1
            self.matRoutingMatrix[self.matModuleMap[link[2]],2*matrixIndex+1] = 1
            matrixIndex += 1
        for link in self.linkModuleDict["nlPluck"]:
            self.matRoutingMatrix[self.matModuleMap[link[1]],2*matrixIndex] = 1
            self.matRoutingMatrix[self.matModuleMap[link[2]],2*matrixIndex+1] = 1
            matrixIndex += 1

        print("Mat Routing Matrix:")
        print(self.matRoutingMatrix)

        return self.generateFaustCode()


    def generateFaustCode(self, debug_mode = False):
        nb_links = int(np.size(self.matRoutingMatrix, 1) // 2)
        nb_mats = int(np.size(self.matRoutingMatrix, 0))
        nbOut = len(self.outputMasses)

        matString = ""
        index = 0
        for grndL in self.matModuleDict["ground"]:
            matString += "mi.ground(" + grndL[1] + ")"
            index += 1
            if index < nb_mats:
                matString += ',\n'
        for massL in self.matModuleDict["mass"]:
            matString += "mi.mass(" + massL[1] + ", 0, " + massL[2]  + ", " + massL[3] + ")"
            index += 1
            if index < nb_mats:
                matString += ',\n'
        for oscL in self.matModuleDict["osc"]:
            matString += "mi.oscil(" + oscL[1] + ", " + oscL[2]  + ", " + oscL[3] + ", 0, " + oscL[4]  + ", " + oscL[5] + ")"
            index += 1
            if index < nb_mats:
                matString += ',\n'
        for posInL in self.matModuleDict["posInput"]:
            matString += "mi.posInput(" + posInL[1] + ")"
            index += 1
            if index < nb_mats:
                matString += ',\n'

        if debug_mode:
            print(matString)

        linkString = ""
        index = 0
        for linkL in self.linkModuleDict["spring"]:
            linkString += "mi.springDamper(" + linkL[3] + "," + linkL[4]  \
                          + ", " + str(self.getPosFromMatId(linkL[1],True)) \
                          + ", " + str(self.getPosFromMatId(linkL[2],True)) + ")"
            index += 1
            if index < nb_links:
                linkString += ',\n'
        for linkL in self.linkModuleDict["collision"]:
            linkString += "mi.collision(" + linkL[3] + "," + linkL[4] + "," + linkL[5]  \
                          + ", " + str(self.getPosFromMatId(linkL[1],True)) \
                          + ", " + str(self.getPosFromMatId(linkL[2],True)) + ")"
            index += 1
            if index < nb_links:
                linkString += ',\n'
        for linkL in self.linkModuleDict["nlBow"]:
            linkString += "mi.nlBow(" + linkL[3] + "," + linkL[4] + ", 0" \
                          + ", " + str(self.getPosFromMatId(linkL[1],True)) \
                          + ", " + str(self.getPosFromMatId(linkL[2],True)) + ")"
            index += 1
            if index < nb_links:
                linkString += ',\n'
        for linkL in self.linkModuleDict["nlPluck"]:
            linkString += "mi.nlPluck(" + linkL[3] + "," + linkL[4] + ", 0" \
                          + ", " + str(self.getPosFromMatId(linkL[1],True)) \
                          + ", " + str(self.getPosFromMatId(linkL[2],True)) + ")"
            index += 1
            if index < nb_links:
                linkString += ',\n'

        if debug_mode:
            print(linkString)

        s =''
        s += """import("stdfaust.lib");\n"""


        paramString =""
        for param in self.indexedParams:
            paramString += param[0] + " = " + param[1] + ";\n"
        paramString += "\n"

        for input in self.inNames:
            s += input + " = 0; \t//write a specific position input signal operation here\n"
        s += "\n\n"

        for frc in self.frcInputs:
            s += frc[0] + " = 0; \t//write a specific force input signal operation here\n"
        s += "\n\n"


        s += "OutGain = 0.5;"
        s += "\n\n"

        s += paramString
        s += "model = (RoutingLinkToMass: \n" + matString + " :\nRoutingMassToLink : \n" + linkString + ", \
        par(i, " + str(nbOut) + ",_)\n)~par(i, " + str(2 * nb_links) + ", _): \
        par(i, " + str(2 * nb_links) + ",!), par(i,  " + str(nbOut) + ", _)\n"

        s += "with{\n"

        if NEW_ROUTING:
            s += self.generateRoutingFunctions_NEW()
        else:
            s += self.generateRoutingFunctions_OLD()

        s += '\n};\n'

        s += "process = "

        first = True
        for i in range(0, len(self.inNames)):
            if first:
                s += self.inNames[i]
                first = False
            else:
                s += ", " + self.inNames[i]

        for i in range(0, len(self.frcInputs)):
            if first:
                s += self.frcInputs[i][0]
                first = False
            else:
                s += ", " + self.frcInputs[i][0]

        if not first:
            s += ":"

        s += " model"

        if not self.outputs:
            s += ";"
        else :
            audioOutChannels=""
            for i in range (0, self.outputs):
                audioOutChannels += "*(OutGain)"
                if i < (self.outputs -1):
                    audioOutChannels += ", "

            s += ": " + audioOutChannels + ";"

        if debug_mode:
            print(s)
        return 0, s


    def generateRoutingFunctions_OLD(self):

        s = ""

        nb_links = int(np.size(self.matRoutingMatrix, 1) // 2)
        nb_mats = int(np.size(self.matRoutingMatrix, 0))

        # Generate Link to Mat Routing Function
        s += "RoutingLinkToMass("
        for i in range (0,nb_links-1):
            s+= "l"+str(i)+"_f1,"
            s+= "l"+str(i)+"_f2,"
        s += "l" + str(nb_links-1) + "_f1,"
        s += "l" + str(nb_links - 1) + "_f2"

        for i in range (0, len(self.inNames)):
            s += ", p_" + self.inNames[i]

        for i in range (0, len(self.frcInputs)):
            s += ", f_" + self.frcInputs[i][0]

        s += ") = "

        inCpt = 0


        for i in range(0, nb_mats):
            routed_forces = ""
            add = 0
            # check if there is a force input for this module
            for frc in self.frcInputs:
                if frc[1] == i:
                    if add:
                        routed_forces += "+"
                    routed_forces += "f_" + frc[0]
                    add = 1
            # check for active links to route
            for j in range(0, 2 * nb_links):
                if(self.matRoutingMatrix[i][j]) == 1:
                    if add:
                        routed_forces += "+"
                    routed_forces += "l" + str(j//2) + "_f" + str((j%2)+1)
                    add = 1
            if (routed_forces) == "":
                s += "0" #9""!"
            else:
                s += routed_forces
            if i >= nb_mats - len(self.matModuleDict["posInput"]):
                s += ", " + "p_" + self.inNames[inCpt]
                inCpt += 1
            if i < nb_mats-1:
                s += ", "
            else:
                s += ";"

        # If the last Mat was not connected to anything...
        if s.endswith(", ;"):
            s = s.replace(", ;", ";")

        # Generate Mat to Link Routing Function
        s += '\n'
        s += "RoutingMassToLink("
        for i in range (0,nb_mats-1):
            s+= "m"+str(i)+","
        s += "m" + str(nb_mats-1) + ") = "

        for i in range(0, 2 * nb_links):
            for j in range(0, nb_mats):
                if(self.matRoutingMatrix[j][i]) == 1:
                    if i < 2*nb_links-1:
                        s += "m" + str(j) + ", "
                    else:
                        s += "m" + str(j) +","

        # Need to add audio out here !
        for i, mass in enumerate(self.outputMasses):
            if i < len(self.outputMasses) - 1:
                s += "m"+str(self.matModuleMap[mass]) + ","
            else:
                s += "m"+str(self.matModuleMap[mass]) + ";"

        return s


    def generateRoutingFunctions_NEW(self):
        s = ""

        nb_links = int(np.size(self.matRoutingMatrix, 1) // 2)
        nb_mats = int(np.size(self.matRoutingMatrix, 0))

        # for i in range (0, len(self.inNames)):
        #     s += ", p_" + self.inNames[i]
        #
        # for i in range (0, len(self.frcInputs)):
        #     s += ", f_" + self.frcInputs[i][0]

        link2mass = ""
        mass2link = ""

        for cur_ptL in range(0, nb_links * 2):
            for cur_ptM in range(0, nb_mats):

                if self.matRoutingMatrix[cur_ptM][cur_ptL]:
                    link2mass += ", " + str(cur_ptL+1) + "," + str(cur_ptM+1)
                    mass2link += ", " + str(cur_ptM + 1) + "," + str(cur_ptL + 1)

        pos_out = ""
        # Need to add audio out here !
        for i, mass in enumerate(self.outputMasses):
            if i < len(self.outputMasses):
                pos_out += ", " + str(self.matModuleMap[mass]+1) + "," + str(nb_links*2 + 1 + i)


        
        s += "RoutingLinkToMass = "
        s += "route(" + str(nb_links * 2) + ", " + str(nb_mats) + link2mass + ");\n"

        s += "RoutingMassToLink = "
        s += "route(" + str(nb_mats) + ", " + str(nb_links * 2 + len(self.outputMasses)) + mass2link + pos_out + ");\n"

        print(s)

        return s


        # Generate Link to Mat Routing Function
        s += "RoutingLinkToMass("
        for i in range (0,nb_links-1):
            s+= "l"+str(i)+"_f1,"
            s+= "l"+str(i)+"_f2,"
        s += "l" + str(nb_links-1) + "_f1,"
        s += "l" + str(nb_links - 1) + "_f2"

        for i in range (0, len(self.inNames)):
            s += ", p_" + self.inNames[i]

        for i in range (0, len(self.frcInputs)):
            s += ", f_" + self.frcInputs[i][0]

        s += ") = "

        inCpt = 0


        for i in range(0, nb_mats):
            routed_forces = ""
            add = 0
            # check if there is a force input for this module
            for frc in self.frcInputs:
                if frc[1] == i:
                    if add:
                        routed_forces += "+"
                    routed_forces += "f_" + frc[0]
                    add = 1
            # check for active links to route
            for j in range(0, 2 * nb_links):
                if(self.matRoutingMatrix[i][j]) == 1:
                    if add:
                        routed_forces += "+"
                    routed_forces += "l" + str(j//2) + "_f" + str((j%2)+1)
                    add = 1
            if (routed_forces) == "":
                s += "0" #9""!"
            else:
                s += routed_forces
            if i >= nb_mats - len(self.matModuleDict["posInput"]):
                s += ", " + "p_" + self.inNames[inCpt]
                inCpt += 1
            if i < nb_mats-1:
                s += ", "
            else:
                s += ";"

        # If the last Mat was not connected to anything...
        if s.endswith(", ;"):
            s = s.replace(", ;", ";")

        # Generate Mat to Link Routing Function
        s += '\n'
        s += "RoutingMassToLink("
        for i in range (0,nb_mats-1):
            s+= "m"+str(i)+","
        s += "m" + str(nb_mats-1) + ") = "

        for i in range(0, 2 * nb_links):
            for j in range(0, nb_mats):
                if(self.matRoutingMatrix[j][i]) == 1:
                    if i < 2*nb_links-1:
                        s += "m" + str(j) + ", "
                    else:
                        s += "m" + str(j) +","

        # Need to add audio out here !
        for i, mass in enumerate(self.outputMasses):
            if i < len(self.outputMasses) - 1:
                s += "m"+str(self.matModuleMap[mass]) + ","
            else:
                s += "m"+str(self.matModuleMap[mass]) + ";"

        return s


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Not enough arguments, use: python physics2Faust [mdl file] [dsp file]")
    else:
        mdl_file = sys.argv[1]
        dsp_file = sys.argv[2]

        mdlcode = ""
        dspcode = ""

        with open(mdl_file, "rt") as file:
            phyGen = Physics2Faust()
            mdlcode = file.read()
            dspcode = phyGen.parseModel(mdlcode)[1]

        with open(dsp_file, "wt") as file:
            file.write(dspcode)
        print("Created the following FAUST file: " + dsp_file)
