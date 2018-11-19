######################################################
#           File: mipeLibCodeGenerator.py                                               #
#           Author:     James Leonard                                                            #
#           Date:           14/11/2018                                                        #
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
    s += name[1:] + "_F = float(" + str(0) + ");\n"

    eq = "ground(" + name[1:] + "_X);\n"

    return s, eq


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

    eq = x + "," + xr + "," + f + " = mass("+ mass + "," + x + "," + xr + "," + f +");\n"

    return s, eq


############################################
####       Gravity Mass Module: w/ downward force
############################################
def genMassGravityCode(name, mass, gravity, initPos, initPosR):
    x = name[1:] + "_X"
    xr = name[1:] + "_XR"
    f = name[1:] + "_F"

    s = "History " + x + "(" + str(initPos) + ");\n"
    s += "History " + xr + "(" + str(initPosR) + ");\n"
    s += "History " + f + "(0.);\n"

    eq = x + "," + xr + "," + f + " = mass_gravity(" + mass + "," + str(gravity) + "," + x + "," + xr + "," + f + ");\n"

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

    eq = x + "," + xr + "," + f + " = osc(" + M + "," + K + "," + Z + "," + x + "," + xr + "," + f + ");\n"

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

    s = f1 + "," + f2 + " = spring_damper(" + K + "," + Z + "," \
        + x1 + "," + x1r + "," +  f1 + ","\
        + x2 + "," + x2r + ", " + f2 + ");\n"

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

    s = f1 + "," + f2 + " = nl_spring_damper(" + K + "," + Q + "," +Z + "," \
        + x1 + "," + x1r + "," +  f1 + ","\
        + x2 + "," + x2r + ", " + f2 + ");\n"

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

    s = f1 + "," + f2 + " = detent(" + K + "," + Z + "," + S + "," \
        + x1 + "," + x1r + "," +  f1 + ","\
        + x2 + "," + x2r + ", " + f2 + ");\n"

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

    s = f1 + "," + f2 + " = nlBow(" + Z + "," + scale + "," \
        + x1 + "," + x1r + "," +  f1 + ","\
        + x2 + "," + x2r + ", " + f2 + ");\n"

    return s


#########################################
####       NL Pluck Module: Plucking Interaction
#########################################

def genNLPluckCode(name, connect1, connect2, K, scale):
    x1 = connect1[1:] + "_X"
    x2 = connect2[1:] + "_X"

    f1 = connect1[1:] + "_F"
    f2 = connect2[1:] + "_F"

    s = f1 + "," + f2 + " = nlPluck(" + K + "," + scale + "," \
        + x1 + "," + f1 + "," \
        + x2 + ", " + f2 + ");\n"

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


