######################################################
#           File: phyMdlCodeParser.py                                                       #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Read an input phyMdl file and generate the codebox     #
#         code for use inside gen, then save it to an output file     #
######################################################

import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)


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
                           "ground" : [] }

        # Dictionary with name and index of all Mat modules
        self.matModuleMap = {}

        # Indexed parameters
        self.indexedParams = []

        # Dictionary of all interaction physical modules
        self.linkModuleDict = {"spring" : [],
                               "collision" : [] }
        
        # The M point(lines) and L point (columns) matrix
        dim = (1,1)
        self.routingMatrix = np.zeros(dim)

        # Param and Init Val lists: do we need this, depending on code gen?
        # self.massValues = []
        # self.massPos = []
        # self.massPosR = []
        # self.stiffvalues = []
        # self.dampValues = []

        # labels of the output masses (positions are routed to output)
        self.outputMasses = []

        # Error state
        self.error = 0

        self.destFolder = ""
        self.generatedCode =""
        self.inputs = 0
        self.outputs = 0


    ########################################################
    ####       phyMdl file parsing
    ####        read through the model file, ignoring comments, etc.
    ########################################################

    def parseModel(self, modelDescr):
        # dest = open(genCodePath,'w')

        error = 0

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

                    if l[1] == "ground":
                        self.matModuleDict["ground"].append([l[0], l[2]])

                    if l[1] == "mass":
                        error = errorCheck(l, 5)
                        if (error == 0):
                            self.matModuleDict["mass"].append([l[0], l[2], l[3], l[4]])
                            # self.massValues.append(l[2])
                            # self.massPos.append(l[3])
                            # self.massPosR.append(l[4])
                        else:
                            break
                    if l[1] == "osc":
                        error = errorCheck(l, 7)
                        if (error == 0):
                            self.matModuleDict["osc"].append([l[0], l[2], l[3], l[4], l[5] , l[6]])
                        else:
                            break

                    if l[1] == "spring":
                        error = errorCheck(l, 6)
                        if (error == 0):
                            self.linkModuleDict["spring"].append([l[0], l[2], l[3], l[4], l[5]])
                            # self.stiffvalues.append(l[4])
                            # self.dampValues.append(l[5])
                        else:
                            break
                    if l[1] == "detent":
                        error = errorCheck(l, 7)
                        if (error == 0):
                            self.linkModuleDict["collision"].append([l[0], l[2], l[3], l[4], l[5], l[6]])
                        else:
                            break

                    if l[1] == "posOutput":
                        error = errorCheck(l, 3)
                        if (error == 0):
                            self.outputMasses.append(l[2])
                        else:
                            break

        pp.pprint(self.matModuleDict)
        pp.pprint(self.linkModuleDict)

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


        matDim = len(self.matModuleDict["ground"]) + len(self.matModuleDict["mass"])+ len(self.matModuleDict["osc"])
        linkDim = len(self.linkModuleDict["spring"])+ len(self.linkModuleDict["collision"])

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

        print("Mat Routing Matrix:")
        print(self.matRoutingMatrix)

        return self.generateFaustCode()


    def generateFaustCode(self, debug_mode = False):
        nbLinks = int(np.size(self.matRoutingMatrix, 1) // 2)
        nbMats = int(np.size(self.matRoutingMatrix, 0))
        nbOut = len(self.outputMasses)

        matString = ""
        index = 0
        for grndL in self.matModuleDict["ground"]:
            matString += "ground(" + grndL[1] + ")"
            index += 1
            if index < nbMats:
                matString += ',\n'
        for massL in self.matModuleDict["mass"]:
            matString += "mass(" + massL[1] + "," + massL[2]  + ", " + massL[3] + ")"
            index += 1
            if index < nbMats:
                matString += ',\n'
        for oscL in self.matModuleDict["osc"]:
            matString += "osc(" + oscL[1] + "," + oscL[2]  + ", " + oscL[3] + "," + oscL[4]  + ", " + oscL[5] + ")"
            index += 1
            if index < nbMats:
                matString += ',\n'

        if debug_mode:
            print(matString)

        linkString = ""
        index = 0
        for linkL in self.linkModuleDict["spring"]:
            linkString += "spring(" + linkL[3] + "," + linkL[4]  + ")"
            index += 1
            if index < nbLinks:
                linkString += ',\n'
        for linkL in self.linkModuleDict["collision"]:
            linkString += "collision(" + linkL[3] + "," + linkL[4] + "," + linkL[5]  + ")"
            index += 1
            if index < nbLinks:
                linkString += ',\n'

        if debug_mode:
            print(linkString)

        paramString =""
        for param in self.indexedParams:
            paramString += param[0] + " = " + param[1] + ";\n"
        paramString += "\n"

        s = paramString
        s += "model = (RoutingLinkToMass : \n" + matString + " :\nRoutingMassToLink : \n" + linkString + ", \
        par(i, " + str(nbOut) + ",_))~par(i, " + str(2 * nbLinks) + ", _): \
        par(i, " + str(2 * nbLinks) + ",!), par(i,  " + str(nbOut) + ", _)\n"

        s += "with{\n"

        # Generate Link to Mat Routing Function
        s += "RoutingLinkToMass("
        for i in range (0,nbLinks-1):
            s+= "l"+str(i)+"_f1,"
            s+= "l"+str(i)+"_f2,"
        s += "l" + str(nbLinks-1) + "_f1,"
        s += "l" + str(nbLinks-1) + "_f2) = "

        for i in range(0, nbMats):
            add = 0
            for j in range(0, 2 * nbLinks):
                if(self.matRoutingMatrix[i][j]) == 1:
                    if add:
                        s += "+"
                    s += "l" + str(j//2) + "_f" + str((j%2)+1)
                    add = 1
            if i < nbMats-1:
                s += ", "
            else:
                s += ";"

        # Generate Mat to Link Routing Function
        s += '\n'
        s += "RoutingMassToLink("
        for i in range (0,nbMats-1):
            s+= "m"+str(i)+","
        s += "m" + str(nbLinks) + ") = "

        for i in range(0, 2 * nbLinks):
            for j in range(0, nbMats):
                if(self.matRoutingMatrix[j][i]) == 1:
                    if i < 2*nbLinks-1:
                        s += "m" + str(j) + ", "
                    else:
                        s += "m" + str(j) +","

        # Need to add audio out here !
        for i, mass in enumerate(self.outputMasses):
            if i < len(self.outputMasses) - 1:
                s += "m"+str(self.matModuleMap[mass]) + ","
            else:
                s += "m"+str(self.matModuleMap[mass]) + ";"

        s += '\n'
        s += "};\nprocess = model: *(0.5), *(0.5);"

        if debug_mode:
            print(s)
        return s


    # def generateRoutingLinkToMass_V1(self):
    #
    #     nbLinks =int(np.size(self.matRoutingMatrix,1) //2)
    #     nbMats = int(np.size(self.matRoutingMatrix, 0))
    #
    #     nbOut = len(self.outputMasses)
    #
    #     s = "model = (RoutingLinkToMass : par(i,"+ str(nbMats) +", mass(m(i), x1(i),x2(i))):RoutingMassToLink :  \
    #     par(i,"+ str(nbLinks) + ",spring(k(i), z(i))), \
    #     par(i, " + str(nbOut) + ",_))~par(i, "+ str(2*nbLinks) +", _): \
    #     par(i, "+str(2*nbLinks)+",!), par(i,  "+ str(nbOut) +", _)\n"
    #
    #     s += "with{\n"
    #
    #     # Generate Link to Mat Routing Function
    #     s += "RoutingLinkToMass("
    #     for i in range (0,nbLinks-1):
    #         s+= "l"+str(i)+"_f1,"
    #         s+= "l"+str(i)+"_f2,"
    #     s += "l" + str(nbLinks-1) + "_f1,"
    #     s += "l" + str(nbLinks-1) + "_f2) = "
    #
    #     for i in range(0, nbMats):
    #         add = 0
    #         for j in range(0, 2 * nbLinks):
    #             if(self.matRoutingMatrix[i][j]) == 1:
    #                 if add:
    #                     s += "+"
    #                 s += "l" + str(j//2) + "_f" + str((j%2)+1)
    #                 add = 1
    #         if i < nbMats-1:
    #             s += ", "
    #         else:
    #             s += ";"
    #
    #     # Generate Mat to Link Routing Function
    #     s += '\n'
    #     s += "RoutingMassToLink("
    #     for i in range (0,nbMats-1):
    #         s+= "m"+str(i)+","
    #     s += "m" + str(nbLinks) + ") = "
    #
    #     for i in range(0, 2 * nbLinks):
    #         for j in range(0, nbMats):
    #             if(self.matRoutingMatrix[j][i]) == 1:
    #                 if i < 2*nbLinks-1:
    #                     s += "m" + str(j) + ", "
    #                 else:
    #                     s += "m" + str(j) +","
    #
    #     # Need to add audio out here !
    #     for i, mass in enumerate(self.outputMasses):
    #         if i < len(self.outputMasses) - 1:
    #             s += "m"+str(self.matModuleMap[mass]) + ","
    #         else:
    #             s += "m"+str(self.matModuleMap[mass]) + ";"
    #
    #     s += '\n'
    #
    #     s+= "m(n) = ba.take(n + 1, ("
    #     for i,mVal in enumerate(self.massValues):
    #         if i < len(self.massValues)-1:
    #             s += str(mVal) + ','
    #         else:
    #             s += str(mVal) + "));"
    #
    #     s += '\n'
    #     s+= "x1(n) = ba.take(n + 1, ("
    #     for i,xVal in enumerate(self.massPos):
    #         if i < len(self.massPos)-1:
    #             s += str(xVal) + ','
    #         else:
    #             s += str(xVal) + "));"
    #
    #     s += '\n'
    #     s+= "x2(n) = ba.take(n + 1, ("
    #     for i,xVal in enumerate(self.massPosR):
    #         if i < len(self.massPosR)-1:
    #             s += str(xVal) + ','
    #         else:
    #             s += str(xVal) + "));"
    #
    #     s += '\n'
    #     s+= "k(n) = ba.take(n + 1, ("
    #     for i,kVal in enumerate(self.stiffvalues):
    #         if i < len(self.stiffvalues)-1:
    #             s += str(kVal) + ','
    #         else:
    #             s += str(kVal) + "));"
    #
    #     s += '\n'
    #     s+= "z(n) = ba.take(n + 1, ("
    #     for i,zVal in enumerate(self.dampValues):
    #         if i < len(self.dampValues)-1:
    #             s += str(zVal) + ','
    #         else:
    #             s += str(zVal) + "));"
    #
    #     s += "};\nprocess = model: *(0.1), *(0.1);"
    #
    #     print(s)
        #print('Nb colunms: ' + str(np.size(self.matRoutingMatrix,1)))
        #print('Nb lines: ' + str(np.size(self.matRoutingMatrix, 0)))

