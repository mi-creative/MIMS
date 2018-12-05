######################################################
#           File: phyMdlCodeParser.py                                                       #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Read an input phyMdl file and generate the codebox     #
#         code for use inside gen, then save it to an output file     #
######################################################

import pprint
import numpy as np


FAUST_LIB_HEADER: str = """ 
import("stdfaust.lib");

Fe = ma.SR;

impulsify = _ <: _,mem : - <: >(0)*_;

// integrated oscillator (mass-spring-ground system)
// m, k, z: mass, stiffness, damping (algorithmic values)
// x0, x1: initial position and delayed position
osc(m,k,z,x0,x1) = equation
with{
  A = 2-(k+z)/m;
  B = z/m-1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify)) + C*_;
	};
};

// punctual mass module
// m: mass (algorithmic value)
// x0, x1: initial position and delayed position
mass(m,x0,x1) = equation
with{
  A = 2;
  B = -1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify) + (x0 : impulsify)') + C*_;
	};
};

// punctual ground module
// x0: initial position
ground(x0) = equation
with{
  // could this term be removed or simlified? Need "unused" input force signal for routing scheme
  C = 0;
  equation = x 
	letrec{
		'x = x + (x0 : impulsify) + C*_;
	};
};

// spring
// k,z: stiffness and daming (algorithmic values)
spring(k,z,x1,x2) = k*(x2-x1) + z*((x2-x2')-(x1-x1')) <: _,_*(-1);

// nlPluck
// 1D non-linear picking Interaction algorithm
nlPluck(k,scale,x1,x2) = 
  select2(
    absdeltapos>scale,
    select2(
      absdeltapos>scale*0.5,
      k*deltapos,
      k*(ma.signum(deltapos)*scale*0.5-deltapos)),
    0) <: _,*(-1)
with{
  deltapos = x1 - x2;
  absdeltapos = abs(deltapos);
};

// nlBow
// 1D non-linear bowing Interaction algorithm 
nlBow(z,scale,x1,x2) = 
  select2(
    absspeed < (scale/3),
    select2(
      absspeed<scale,
      0,
      select2(
        speed>0,
        (scale/3)*z + (-z/4)*speed,
        (-scale/3)*z + (-z/4)*speed
        )
      ),
    z*speed) <: _,*(-1)
with{
  speed = (x1-x1r) - (x2-x2r);
  absspeed = abs(speed);
};

// collision
// k,z: stiffness and daming (algorithmic values)
// thres: position threshold for the collision to be active
collision(k,z,thres,x1,x2) = spring(k,z,x1,x2) : (select2(comp,0,_),select2(comp,0,_))
with{
  comp = (x2-x1)<thres;
};

posInput(init) = _,_ : !,_ :+(init : impulsify);
 
"""


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
                        if (len(l) == 5) or (len(l) == 8):
                            self.matModuleDict["mass"].append([l[0], l[2], l[3], l[4]])
                        else:
                            break
                    if l[1] == "osc":
                        if (len(l) == 7) or (len(l) == 10):
                            self.matModuleDict["osc"].append([l[0], l[2], l[3], l[4], l[5] , l[6]])
                        else:
                            break

                    if l[1] == "spring":
                        if (len(l) == 6):
                            self.linkModuleDict["spring"].append([l[0], l[2], l[3], l[4], l[5]])
                        else:
                            break
                    if l[1] == "detent":
                        if (len(l) == 7):
                            self.linkModuleDict["collision"].append([l[0], l[2], l[3], l[4], l[5], l[6]])
                        else:
                            break

                    if l[1] == "nlBow":
                        if (len(l) == 6):
                            self.linkModuleDict["nlBow"].append([l[0], l[2], l[3], l[4], l[5]])
                        else:
                            break

                    if l[1] == "nlPluck":
                        if (len(l) == 6):
                            self.linkModuleDict["nlPluck"].append([l[0], l[2], l[3], l[4], l[5]])
                        else:
                            break

                    if l[1] == "posOutput":
                        if (len(l) == 3):
                            self.outputMasses.append(l[2])
                        else:
                            break
                    if l[1] == "posInput":
                        if (len(l) == 3):
                            self.matModuleDict["posInput"].append([l[0], l[2]])
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
        for mat in self.matModuleDict["posInput"]:
            self.matModuleMap[mat[0]] = index
            index+=1


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
        for posInL in self.matModuleDict["posInput"]:
            matString += "posInput(" + posInL[1] + ")"
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
        for linkL in self.linkModuleDict["nlBow"]:
            linkString += "nlBow(" + linkL[3] + "," + linkL[4]  + ")"
            index += 1
            if index < nbLinks:
                linkString += ',\n'
        for linkL in self.linkModuleDict["nlPluck"]:
            linkString += "nlPluck(" + linkL[3] + "," + linkL[4]  + ")"
            index += 1
            if index < nbLinks:
                linkString += ',\n'

        if debug_mode:
            print(linkString)

        s =''
        s += FAUST_LIB_HEADER

        paramString =""
        for param in self.indexedParams:
            paramString += param[0] + " = " + param[1] + ";\n"
        paramString += "\n"

        extraSignalString =""
        for i in range (0, len(self.matModuleDict["posInput"])):
            extraSignalString += ", _"

        s += paramString
        s += "model = (RoutingLinkToMass" + extraSignalString + ": \n" + matString + " :\nRoutingMassToLink : \n" + linkString + ", \
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
