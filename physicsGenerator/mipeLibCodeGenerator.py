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
    s = "Param " + param + "(" + str(val) + ");"
    return s

def genParamAudioCode(param, input):
    s = param + " = " + input + ";"
    return s


##############################
####    MATERIAL ELEMENTS
##############################

#######################################
####       Ground Module: Fixed Position
#######################################

def genGroundCode(name, initPos):

    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_ground(" + name + ");"

    return struct, init, eq


#######################################
####       Mass Module: Inertial Point
#######################################

def genMassCode(name, m_param, initPos, initPosR):

    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(initPos) + ", " + str(initPosR) + ");"
    eq = "compute_mass(" + name + ", " + m_param + ");"

    return struct, init, eq


############################################
####       Gravity Mass Module: w/ downward force
############################################
def genMassGravityCode(name, m_param, grav, initPos, initPosR):

    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(initPos) + ", " + str(initPosR) + ");"
    eq = "compute_mass(" + name + ", " + m_param + ", gravity = " + grav + ");"

    return struct, init, eq


#######################################
####       Cel Module: Integrated oscillator
#######################################
def genOscCode(name, M, K, Z, initPos, initPosR):

    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(initPos) + ", " + str(initPosR) + ");"
    eq = "compute_osc(" + name + ", " + M + ", " + K + ", " + Z + ");"

    return struct, init, eq


def genOscGravityCode(name, M, K, Z, grav, initPos, initPosR):

    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(initPos) + ", " + str(initPosR) + ");"
    eq = "compute_osc(" + name + ", " + M + ", " + K + ", " + Z + ", gravity = " + grav + ");"

    return struct, init, eq

#######################################
####       String Module: Integrated String
#######################################
def genStringCode(name, len, M, K, Z, initPos):

    struct = "Data " + name + "(3, " + str(int(len)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_string(" + name + ", " + M + ", " + K + ", " + Z + ");"

    return struct, init, eq

#######################################
####       String Module: Integrated String
#######################################
def genStiffStringCode(name, len, M, K, K2, Z, initPos):

    struct = "Data " + name + "(3, " + str(int(len)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_stiff_string(" + name + ", " + M + ", " + K + ", " + K2 + ", " + Z + ");"

    return struct, init, eq

def genChainCode(name, len, M, K, Z, initPos):

    struct = "Data " + name + "(3, " + str(int(len)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_chain(" + name + ", " + M + ", " + K + ", " + Z + ");"

    return struct, init, eq


def genMeshCode(name, length, width, M, K, Z, initPos):
    struct = "Data " + name + "(3, " + str(int(length)*int(width)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_mesh(" + name + ", " + str(length) \
         + ", " + str(width) + ", " + M + ", " + K + ", " + Z + ");"
    return struct, init, eq


def genClosedMeshCode(name, length, width, M, K, Z, initPos):
    struct = "Data " + name + "(3, " + str(int(length)*int(width)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_closed_mesh(" + name + ", " + str(length) \
         + ", " + str(width) + ", " + M + ", " + K + ", " + Z + ");"
    return struct, init, eq


def genCornerMeshCode(name, length, width, M, K, Z, initPos):
    struct = "Data " + name + "(3, " + str(int(length)*int(width)) + ");"
    init = "init_multiple_masses(" + name + ", " + str(initPos) + ", " + str(initPos) + ");"
    eq = "compute_corner_mesh(" + name + ", " + str(length) \
         + ", " + str(width) + ", " + M + ", " + K + ", " + Z + ");"
    return struct, init, eq

##############################
####    INTERACTION ELEMENTS
##############################

#######################################
####       Spring Module: Linear Spring
#######################################

def genSpringCode(name, connect1, connect2, K):

    s = "compute_spring(" + connect1 + ", " + connect2 + ", " \
        + K + ");"
    return s


def genDamperCode(name, connect1, connect2, Z):

    s = "compute_damper(" + connect1 + ", " + connect2 + ", " \
        + Z + ");"
    return s


def genSpringDamperCode(name, connect1, connect2, K, Z):

    s = "compute_spring_damper(" + connect1 + ", " + connect2 + ", " \
        + K + ", " + Z + ");"
    return s


def genSpringDamperCode_NL2(name, connect1, connect2, K, Q, Z):

    s = "compute_spring_damper_nl2(" + connect1 + ", " + connect2 + ", " \
        + K + ", " + Q + ", " + Z + ");"
    return s


def genSpringDamperCode_NL3(name, connect1, connect2, K, Q, Z):

    s = "compute_spring_damper_nl3(" + connect1 + ", " + connect2 + ", " \
        + K + ", " + Q + ", " + Z + ");"
    return s


def genContactCode(name, connect1, connect2, K, Z, thresh):

    s = "compute_contact(" + connect1 + ", " + connect2 + ", " \
        + K + ", " + Z + ", " + thresh + ");"
    return s


def genNLBowCode(name, connect1, connect2, Z, scale):
    s = "compute_nlBow(" + connect1 + ", " + connect2 + ", " \
        + Z + ", " + scale + ");"
    return s


def genNLPluckCode(name, connect1, connect2, K, scale):
    s = "compute_nlPluck(" + connect1 + ", " + connect2 + ", " \
        + K + ", " + scale + ");"
    return s


def genStringProxyCode(proxy, connect1, pos):
    struct = "Data " + proxy + "(3);"
    init = "init_mat(" + proxy + ", 0, 0);"
    s1 = "set_proxy_pos_string("+ proxy + ", " + connect1 + ", " + str(pos) + ");"
    s2 = "apply_proxy_frc_string(" + proxy + ", " + connect1 + ", " + str(pos) + ");"
    return struct, init, s1, s2


def genMeshProxyCode(proxy, connect1, pos_arg, length, width):

    pos = pos_arg.split(':')

    struct = "Data " + proxy + "(3);"
    init = "init_mat(" + proxy + ", 0, 0);"
    s1 = "set_proxy_pos_mesh(" + proxy + ", " + connect1 + ", " + str(length) + ", " + str(width) \
         + ", " + str(pos[0]) + ", " + str(pos[1]) + ");"
    s2 = "apply_proxy_frc_mesh(" + proxy + ", " + connect1 + ", " + str(length) + ", " + str(width) \
         + ", " + str(pos[0]) + ", " + str(pos[1]) + ");"
    return struct, init, s1, s2


##############################
####    INPUT/OUTPUT ELEMENTS
##############################

def genForceInputCode(f_dest, in_channel):
    s = "apply_input_force(" + f_dest + ", " + in_channel + ");"
    return s


def genPosInputCode(name, in_channel, inputPos):
    struct = "Data " + name + "(3);"
    init = "init_mat(" + name + ", " + str(inputPos) + ", " + str(inputPos) + ");"
    algo = "update_input_pos(" + name + ", " + in_channel + ");"
    return struct, init, algo


def genPosOutputCode(x_out, out_channel):
    s = out_channel + " =  " + "get_pos(" + x_out + ");"
    return s


def genForceOutputCode(f_out, out_channel):
    s = out_channel + " =  " + "get_frc(" + f_out + ");"
    return s




