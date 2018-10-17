######################################################
#           File: phyMdlCodeGenerator.py                                               #
#           Author:     James Leonard                                                            #
#           Date:           23/03/2017                                                                  #
#         Methods for generating gendsp code for  the various     #
#         physical modules  used in the formalism                              #
######################################################

##############################
#### STRUCTURAL ELEMENTS
##############################

########################################################
####       Create a parameter that can be controlled from outside
########################################################
def genParamCode(param, val):
    s = "Param " + param + "(" + str(val) + ");\n"
    return s


##############################
####    MATERIAL ELEMENTS
##############################

#######################################
####       Ground Module: Fixed Position
#######################################
def genGroundCode(name, initPos):
    s = name[1:] + "_X = float(" + str(initPos) + ");\n"
    s += name[1:] + "_XR = float(" + str(initPos) + ");\n"
    return s


#######################################
####       Mass Module: Inertial Point
#######################################
def genMassCode(name, mass, initPos, initPosR):
    x = name[1:] + "_X"
    xr = name[1:] + "_XR"
    f = name[1:] + "_F"

    s = "History " + x + "(" + str(initPos) + ");\n"
    s += "History " + xr + "(" + str(initPosR) + ");\n"
    s += "History " + f + "(0.);\n"

    eq = "newPos = (" + f + ") / " + mass + " + 2 * " + x + " - " + xr + ";\n"
    eq += xr + " = fixdenorm(" + x + ");\n"
    eq += x + " = fixdenorm(newPos);\n"
    eq += f + " =  (0.);\n"

    return s, eq


############################################
####       Gravity Mass Module: w/ downward force
############################################
def genMassGravityCode(name, mass, initPos, initPosR, gravity):
    x = name[1:] + "_X"
    xr = name[1:] + "_XR"
    f = name[1:] + "_F"

    s = "History " + x + "(" + str(initPos) + ");\n"
    s += "History " + xr + "(" + str(initPosR) + ");\n"
    s += "History " + f + "(0.);\n"
    eq = "newPos = (" + f + " + (" + str(gravity) + ")) / " + mass + " + 2 * " + x + " - " + xr + ";\n"
    eq += xr + " = fixdenorm(" + x + ");\n"
    eq += x + " = fixdenorm(newPos);\n"
    eq += f + " =  (0.);\n"

    return s, eq


#######################################
####       Cel Module: Integrated oscillator
#######################################
def genCelCode(name, M, K, Z, initPos, initPosR):
    x = name[1:] + "_X"
    xr = name[1:] + "_XR"
    f = name[1:] + "_F"

    s = "History " + x + "(" + str(initPos) + ");\n"
    s += "History " + xr + "(" + str(initPosR) + ");\n"
    s += "History " + f + "(0.);\n"
    eq = "newPos = (" + f + ") / " + M + " + (2 - (" + K + "+" + Z + ")/ " + M + ") * " + x + " + (" + Z + "/" + M + " - 1) * " + xr + ";\n"
    eq += xr + " = fixdenorm(" + x + ");\n"
    eq += x + " = fixdenorm(newPos);\n"
    eq += f + " =  (0.);\n"

    return s, eq


##############################
####    INTERACTION ELEMENTS
##############################

#######################################
####       Spring Module: Linear Spring
#######################################
def genSpringCode(name, connect1, connect2, K, Z):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"
    x1r = connect1[1:] + "_XR"
    x2r = connect2[1:] + "_XR"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    s = "force = (" + str(K) + ") * (" + x1 + " - " + x2 + ") + (" + str(
        Z) + ") * ((" + x1 + "-" + x1r + ") - (" + x2 + "-" + x2r + ")) ;\n"
    s += f1 + " +=  -force;\n"
    s += f2 + "+= force;\n"

    return s


#######################################
####       NLSpring Module: Cubic Spring
#######################################
def genNLSpringCode(name, connect1, connect2, K, Q, Z):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"
    x1r = connect1[1:] + "_XR"
    x2r = connect2[1:] + "_XR"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    s = "dist = (" + x1 + " - " + x2 + " );\n"

    s += "force = (" + str(K) + ") * dist + ("
    s += str(Q) + ") * dist*dist*dist + ("
    s += str(Z) + ") * ((" + x1 + "-" + x1r + ") - (" + x2 + "-" + x2r + ")) ;\n"
    s += f1 + " +=  -force;\n"
    s += f2 + "+= force;\n"

    return s


###########################################
####       Detent Module: conditonal spring (perc)
###########################################
def genDetentCode(name, connect1, connect2, K, Z, S):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"
    x1r = connect1[1:] + "_XR"
    x2r = connect2[1:] + "_XR"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    s = "force = (" + str(K) + ") * (" + x1 + " - " + x2 + ") + (" + str(
        Z) + ") * ((" + x1 + "-" + x1r + ") - (" + x2 + "-" + x2r + ")) ;\n"
    s += "if((" + x1 + "-" + x2 + ") > (" + str(S) + "))  { force = 0.;}\n"
    s += f1 + " +=  -force;\n"
    s += f2 + "+= force;\n"

    return s


#######################################
####       NL Bow Module: Friction Interaction
#######################################
def genNLBowCode(name, connect1, connect2, Z, scale):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"
    x1r = connect1[1:] + "_XR"
    x2r = connect2[1:] + "_XR"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    low_thres = "(" + scale + " / 3.)"
    high_thres = scale

    dampZ = Z
    excZ = "(-" + Z + "/4.)"

    tipping_force = low_thres + " * " + dampZ

    s = "force = 0.;\n"
    s += "speed = ((" + x1 + "-" + x1r + ") - (" + x2 + "-" + x2r + "));\n"
    s += "if(abs(speed) < " + low_thres + ")  {\n"
    s += "force = " + str(dampZ) + " * speed ;\n"
    s += "}\n"
    s += "else if(abs(speed) < " + high_thres + ")  {\n"
    s += "if(speed > 0) {"
    s += "force = " + str(tipping_force) + " + " + str(excZ) + " * speed ;}\n"
    s += "else { force =  - " + str(tipping_force) + " + " + str(excZ) + " * speed ;}\n"
    s += "}\n"
    s += "else force = 0.;\n"
    s += f1 + " +=  -force;\n"
    s += f2 + "+= force;\n"

    return s


#########################################
####       NL Pluck Module: Plucking Interaction
#########################################
def genNLPluckCode(name, connect1, connect2, K, scale):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    low_thres = "(" + scale + " / 2.)"
    high_thres = scale

    pluckUp = K
    pluckDown = "(-" + K + ")"

    tipping_force = low_thres + " * " + pluckUp

    s = "force = 0.;\n"

    s += "deltapos = (" + x1 + " - " + x2 + ");\n"
    s += "if(abs(deltapos) < " + low_thres + ")  {\n"
    s += "force = " + str(pluckUp) + " * deltapos ;\n"
    s += "}\n"
    s += "else if(abs(deltapos) < " + high_thres + ")  {\n"
    s += "if(deltapos > 0) {"
    s += "force = " + str(tipping_force) + " + " + str(pluckDown) + " * deltapos ;}\n"
    s += "else { force =  - " + str(tipping_force) + " + " + str(pluckDown) + " * deltapos ;}\n"
    s += "}\n"
    s += "else force = 0.;\n"
    s += f1 + " +=  -force;\n"
    s += f2 + "+= force;\n"

    return s


##############################
####    INPUT/OUTPUT ELEMENTS
##############################

#######################################################
####        Force input: apply outside force to material element
#######################################################
def genForceInputCode(name, connect):
    in_channel = name[1:];
    f_dest = connect[1:] + "_F"

    s = f_dest + "+=  " + in_channel + ";\n"

    return s


#######################################################
####        Position input: input a position from outside world
#######################################################
def genPosInputCode(name, initPos):
    x = name[1:] + "_X"
    xr = name[1:] + "_XR"

    f = name[1:] + "_F"

    s = "History " + x + "(" + str(initPos) + ");\n"
    s += "History " + xr + "(" + str(initPos) + ");\n"
    s += "History " + f + "(0.);\n"

    eq = xr + " = " + x + ";\n"
    eq += x + " = " + name[1:] + ";\n"
    eq += f + " =  (0.);\n"

    return s, eq


#######################################################
####        Pos Output: get the position of a module (sound out)
#######################################################
def genPosOutputCode(name, connect):
    out_channel = name[1:];
    x_out = connect[1:] + "_X"
    s = out_channel + " =  " + x_out + ";\n"
    return s


#######################################################
####        Force Output: get the force of a module (sound out)
#######################################################
def genForceOutputCode(name, connect):
    out_channel = name[1:];
    f_out = connect[1:] + "_F"
    s = out_channel + " =  " + f_out + ";\n"
    return s


