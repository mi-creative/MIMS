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

import physicsGenerator.phyDict as phyDict


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
        
        self.struct_code = []
        self.param_code = []
        self.audio_param_code = []
        self.init_mass_code = []
        self.comp_mass_code = []
        self.comp_link_code = []
        self.comp_proxy_mass_code = []
        self.comp_proxy_link_code = []
        self.outputs_code = []
        
        self.motion_code = []

        # Error state
        self.error = 0

        # List of all material points
        self.mat_list = []

        # List of integrated objects that will require special treatment
        self.integ_list = []

        self.nb_proxies = 0

        self.destFolder = ""

        self.motionBufferName = "motion"
        self.userBufferList = []

        self.generated_code =""
        self.inputs = 0
        self.outputs = 0

    def writeGenericMotionData(self, mat_name):
        self.motion_code.append(self.motionBufferName + ".poke(get_pos("
                                + mat_name[1:] + "), " + str(len(self.mat_list))
                                + ", 0);\n")

    def writeGenericIntegratedMotionData(self, mat_name):
        s = "for(i = 0; i < channels("+ mat_name[1:] +"); i+=1){motion.poke(get_pos_at("
        s += mat_name[1:] + ", i), "+ str(len(self.mat_list)) + "+i , 0);}\n"
        self.motion_code.append(s)

    def writeSpecificMotionData(self, mat_name, motion_name, xpos, ypos):
        self.motion_code.append(motion_name + ".poke(get_pos("
                                + mat_name[1:] + "), " + str(len(self.mat_list))
                                + ", 0);\n")
        self.motion_code.append(motion_name + ".poke(" + str(xpos)
                                + ", " + str(len(self.mat_list))
                                + ", 1);\n")
        self.motion_code.append(motion_name + ".poke(" + str(ypos)
                                + ", " + str(len(self.mat_list))
                                + ", 2);\n")


    def addMotionBufferToList(self, buffer_name):
        if buffer_name not in self.userBufferList:
            self.userBufferList.append(buffer_name)

    def declareBufferList(self):
        for buffer in self.userBufferList:
            self.generated_code += "Buffer " + buffer + ";\n"


    def moduleName(self, mod_label):
        mod_label = mod_label[1:]
        if mod_label[0:2] == "in":
            try:
                ch_num = int(mod_label[2:])
                if 0 <(ch_num) < 99:
                    return "m_" + mod_label
            except:
                return mod_label
        else:
            return mod_label

    def checkForProxies(self, name):
        if name in self.integ_list:
            return 1
        else:
            return 0

    def addProxies(self, name, parameter):
        if name in self.integ_list:
            proxy = "proxy_" + str(self.nb_proxies)
            self.nb_proxies = self.nb_proxies + 1
            header, init, pMat, pInt = phyMdlCodeGenerator.genProxyCode(proxy, name, parameter)
            self.struct_code.append(header)
            self.init_mass_code.append(init)
            self.comp_proxy_mass_code.append(pMat)
            self.comp_proxy_link_code.append(pInt)
            name = proxy
            return name
        else:
            return name


    ########################################################
    ####       phyMdl file parsing
    ####        read through the model file, ignoring comments, etc.
    ########################################################

    def parseModel(self, modelDescr, includeMotionData):
        # dest = open(genCodePath,'w')

        error = 0
        err_msg = ""

        self.motion_code.clear()

        print("About to enter model generation...")

        compList = modelDescr.split("\n")

        # First, iterate to fill out any mass-type modules

        for line in compList:
            if  line.startswith('#') == True :
                pass
            else :
                rCom = line.rsplit('#')
                l = rCom[0].rsplit()

                nb_args = len(l)

                #####################################################
                ###      Generate gendsp code from the model information
                #####################################################

                if(nb_args > 2):

                    if l[1] == "ground":
                        if (nb_args == 3) or (nb_args == 6):
                            header, init, body = phyMdlCodeGenerator.genGroundCode(l[0][1:], l[2])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericMotionData(l[0])
                            if nb_args == 6:
                                self.writeSpecificMotionData(l[0], str(l[3]), l[4], l[5])
                                self.addMotionBufferToList(str(l[3]))
                            self.mat_list.append(l[0])
                        else:
                            error = -1
                            err_msg = "Error: Wrong number of parameters for ground module: " + str(l)
                            break

                    elif l[1] == "mass":
                        if (nb_args == 5) or (nb_args == 8):
                            header, init, body = phyMdlCodeGenerator.genMassCode(l[0][1:], l[2], l[3], l[4])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericMotionData(l[0])
                            if nb_args == 8:
                                self.writeSpecificMotionData(l[0], str(l[5]), l[6], l[7])
                                self.addMotionBufferToList(str(l[5]))
                            self.mat_list.append(l[0])
                        else:
                            error = -2
                            err_msg = "Error: Wrong number of parameters for mass module: " + str(l)
                            break

                    elif l[1] == "massG":
                        if (nb_args == 6) or (nb_args == 9):
                            header, init, body = phyMdlCodeGenerator.genMassGravityCode(l[0][1:], l[2], l[3], l[4], l[5])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericMotionData(l[0])
                            if nb_args == 9:
                                self.writeSpecificMotionData(l[0], str(l[6]), l[7], l[8])
                                self.addMotionBufferToList(str(l[6]))
                            self.mat_list.append(l[0])
                        else:
                            error = -3
                            err_msg = "Error: Wrong number of parameters for massG module: " + str(l)
                            break

                    elif l[1] == "osc":
                        if (nb_args == 7) or (nb_args == 10):
                            header, init, body = phyMdlCodeGenerator.genOscCode(l[0][1:], l[2], l[3], l[4], l[5], l[6])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericMotionData(l[0])
                            if nb_args == 10:
                                self.writeSpecificMotionData(l[0], str(l[7]), l[8], l[9])
                                self.addMotionBufferToList(str(l[7]))
                            self.mat_list.append(l[0])
                        else:
                            error = -4
                            err_msg = "Error: Wrong number of parameters for osc module: " + str(l)
                            break

                    elif l[1] == "posInput":
                        if nb_args == 3 or nb_args == 6:
                            mod_name = self.moduleName(l[0])
                            header, init, body = phyMdlCodeGenerator.genPosInputCode(mod_name, l[0][1:], l[2])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)
                            self.inputs += 1

                            self.writeGenericMotionData('@' + mod_name)
                            if nb_args == 6:
                                self.writeSpecificMotionData(mod_name, str(l[3]), l[4], l[5])
                                self.addMotionBufferToList(str(l[3]))
                            self.mat_list.append('@' + mod_name)
                        else:
                            error = -20
                            err_msg = "Error: Wrong number of parameters for posInput module: " + str(l)
                            break

                    # Create integrated string
                    elif l[1] == "string":
                        if nb_args == 7:
                            header, init, body = phyMdlCodeGenerator.genStringCode(l[0][1:], l[2], l[3], l[4], l[5], l[6])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericIntegratedMotionData(l[0])
                            for i in range(0, int(l[2])):
                                self.mat_list.append(l[0]+"_"+str(i))
                            self.integ_list.append(l[0][1:])
                        else:
                            error = -5
                            err_msg = "Error: Wrong number of parameters for String module: " + str(l)
                            break

                    # Create integrated string
                    elif l[1] == "stiffString":
                        if nb_args == 8:
                            header, init, body = phyMdlCodeGenerator.genStiffStringCode(l[0][1:], l[2], l[3], l[4], l[5], l[6], l[7])
                            self.struct_code.append(header)
                            self.init_mass_code.append(init)
                            self.comp_mass_code.append(body)

                            self.writeGenericIntegratedMotionData(l[0])
                            for i in range(0, l[2]):
                                self.mat_list.append(l[0]+"_"+str(i))
                            self.integ_list.append(l[0][1:])
                        else:
                            error = -5
                            err_msg = "Error: Wrong number of parameters for Stiff String module: " + str(l)
                            break

                    # else:
                    #     error = -30
                    #     err_msg = "Unknown module name" + str(l)
                    #     break

        # Then iterate again to find all the interactions, inputs/outputs, etc.

        for line in compList:
            if line.startswith('#') == True:
                pass
            else:
                rCom = line.rsplit('#')
                l = rCom[0].rsplit()

                nb_args = len(l)

                #####################################################
                ###      Generate gendsp code from the model information
                #####################################################

                if (nb_args > 2):

                    if l[1] == "param":
                        self.param_code.append(phyMdlCodeGenerator.genParamCode(l[0][1:], l[2]))

                    elif l[1] == "audioParam":
                        self.audio_param_code.append(phyMdlCodeGenerator.genParamAudioCode(l[0][1:], l[2][1:]))
                        self.inputs += 1


                    elif l[1] in phyDict.link_modules:

                        name = l[1]

                        p1 = self.checkForProxies(self.moduleName(l[2]))
                        p2 = self.checkForProxies(self.moduleName(l[3]))

                        # if there is a proxy we don't expect the same number of arguments
                        proxies_detected = p1 + p2

                        m1 = self.moduleName(l[2])
                        m2 = self.moduleName(l[3])

                        if p1 and p2:
                            m1 = self.addProxies(self.moduleName(l[2]), l[-2])
                            m2 = self.addProxies(self.moduleName(l[3]), l[-1])
                        elif p1:
                            m1 = self.addProxies(self.moduleName(l[2]), l[-1])
                        elif p2:
                            m2 = self.addProxies(self.moduleName(l[3]), l[-1])

                        body = ""

                        if name == "spring":
                            if nb_args == 5 + proxies_detected:
                                body = phyMdlCodeGenerator.genSpringCode(self.moduleName(l[0][1:]), m1, m2, l[4])
                            elif nb_args == 6 + proxies_detected:
                                body = phyMdlCodeGenerator.genSpringDamperCode(l[0][1:], m1, m2, l[4], l[5])
                            else:
                                error = -10
                                err_msg = "Error: Wrong number of parameters for spring module: " + str(l)
                                break

                        elif name == "damper":
                            if nb_args == 5 + proxies_detected:
                                body = phyMdlCodeGenerator.genDamperCode(l[0][1:], m1, m2, l[4])
                            else:
                                error = -11
                                err_msg = "Error: Wrong number of parameters for damper module: " + str(l)
                                break

                        elif name == "springDamper":
                            if nb_args == 6 + proxies_detected:
                                body = phyMdlCodeGenerator.genSpringDamperCode(l[0][1:], m1, m2, l[4], l[5])
                            else:
                                error = -12
                                err_msg = "Error: Wrong number of parameters for springDamper module: " + str(l)
                                break

                        elif name == "contact":
                            if nb_args == 7 + proxies_detected:
                                body = phyMdlCodeGenerator.genContactCode(l[0][1:], m1, m2, l[4], l[5], l[6])
                            else:
                                error = -13
                                err_msg = "Error: Wrong number of parameters for contact module: " + str(l)
                                break

                        elif name == "nlBow":
                            if nb_args == 6 + proxies_detected:
                                body = phyMdlCodeGenerator.genNLBowCode(l[0][1:], m1, m2, l[4], l[5])
                            else:
                                error = -14
                                err_msg = "Error: Wrong number of parameters for nlBow module: " + str(l)
                                break

                        elif name == "nlPluck":
                            if nb_args == 6 + proxies_detected:
                                body = phyMdlCodeGenerator.genNLPluckCode(l[0][1:], m1, m2, l[4], l[5])
                            else:
                                error = -15
                                err_msg = "Error: Wrong number of parameters for nlPick module: " + str(l)
                                break

                        elif name == "nlSpring" or l[1] == "nlSpring2":
                            if nb_args == 7 + proxies_detected:
                                body = phyMdlCodeGenerator.genSpringDamperCode_NL2(l[0][1:], m1, m2,
                                                                                   l[4], l[5], l[6])
                            else:
                                error = -16
                                err_msg = "Error: Wrong number of parameters for nlSpring2 module: " + str(l)
                                break

                        elif name == "nlSpring3":
                            if nb_args == 7 + proxies_detected:
                                body = phyMdlCodeGenerator.genSpringDamperCode_NL3(l[0][1:], m1, m2,
                                                                                   l[4], l[5], l[6])
                                self.comp_link_code.append(body)
                            else:
                                error = -17
                                err_msg = "Error: Wrong number of parameters for nlSpring3 module: " + str(l)
                                break

                        self.comp_link_code.append(body)


                    elif l[1] in phyDict.in_out_modules:

                        name = l[1]
                        p1 = self.checkForProxies(self.moduleName(l[2]))

                        if p1:
                            m1 = self.addProxies(self.moduleName(l[2]), l[-1])
                        else:
                            m1 = l[2][1:]

                        if name == "frcInput":
                            if nb_args == 3 + p1:
                                mod_name = self.moduleName(l[0])
                                body = phyMdlCodeGenerator.genForceInputCode(m1, l[0][1:])
                                self.comp_link_code.append(body)
                                self.inputs += 1
                            else:
                                error = -21
                                err_msg = "Error: Wrong number of parameters for frcInput module: " + str(l)
                                break

                        elif l[1] == "posOutput":
                            if nb_args == 3 + p1:
                                mod_name = self.moduleName(l[0])
                                body = phyMdlCodeGenerator.genPosOutputCode(m1, mod_name)
                                self.outputs_code.append(body)
                                self.outputs += 1
                            else:
                                error = -22
                                err_msg = "Error: Wrong number of parameters for posOutput module: " + str(l)
                                break

                        elif l[1] == "frcOutput":
                            if nb_args == 3 + p1:
                                mod_name = self.moduleName(l[0])
                                src = m1
                                if src[0:2] == "in":
                                    src = self.moduleName(l[2])
                                body = phyMdlCodeGenerator.genForceOutputCode(src, mod_name)
                                self.outputs_code.append(body)
                                self.outputs += 1
                            else:
                                error = -23
                                err_msg = "Error: Wrong number of parameters for frcOutput module: " + str(l)
                                break



                    # elif l[1] == "spring":
                    #     if nb_args == 5:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #
                    #         m1 = self.checkForProxies(self.moduleName(l[2]))
                    #         m2 = self.checkForProxies(self.moduleName(l[3]))
                    #
                    #         body = phyMdlCodeGenerator.genSpringCode(self.moduleName(l[0][1:]), m1, m2, l[4])
                    #         self.comp_link_code.append(body)
                    #     elif nb_args == 6:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #
                    #         m1 = self.checkForProxies(self.moduleName(l[2]))
                    #         m2 = self.checkForProxies(self.moduleName(l[3]))
                    #
                    #         body = phyMdlCodeGenerator.genSpringDamperCode(l[0][1:], m1, m2, l[4], l[5])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -10
                    #         err_msg = "Error: Wrong number of parameters for spring module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "damper":
                    #     if nb_args == 5:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genDamperCode(l[0][1:], m1, m2, l[4])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -11
                    #         err_msg = "Error: Wrong number of parameters for damper module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "springDamper":
                    #     if nb_args == 6:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genSpringDamperCode(l[0][1:], m1, m2, l[4], l[5])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -12
                    #         err_msg = "Error: Wrong number of parameters for springDamper module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "contact":
                    #     if nb_args == 7:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genContactCode(l[0][1:], m1, m2, l[4], l[5], l[6])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -13
                    #         err_msg = "Error: Wrong number of parameters for contact module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "nlBow":
                    #     if nb_args == 6:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genNLBowCode(l[0][1:], m1, m2, l[4], l[5])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -14
                    #         err_msg = "Error: Wrong number of parameters for nlBow module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "nlPluck":
                    #     if nb_args == 6:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genNLPluckCode(l[0][1:], m1, m2, l[4], l[5])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -15
                    #         err_msg = "Error: Wrong number of parameters for nlPick module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "nlSpring" or l[1] == "nlSpring2":
                    #     if nb_args == 7:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genSpringDamperCode_NL2(l[0][1:], m1, m2,
                    #                                                            l[4], l[5], l[6])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -16
                    #         err_msg = "Error: Wrong number of parameters for nlSpring2 module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "nlSpring3":
                    #     if nb_args == 7:
                    #         m1 = self.moduleName(l[2])
                    #         m2 = self.moduleName(l[3])
                    #         body = phyMdlCodeGenerator.genSpringDamperCode_NL3(l[0][1:], m1, m2,
                    #                                                            l[4], l[5], l[6])
                    #         self.comp_link_code.append(body)
                    #     else:
                    #         error = -17
                    #         err_msg = "Error: Wrong number of parameters for nlSpring3 module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "frcInput":
                    #     if nb_args == 3:
                    #         mod_name = self.moduleName(l[0])
                    #         body = phyMdlCodeGenerator.genForceInputCode(l[2][1:], l[0][1:])
                    #         self.comp_link_code.append(body)
                    #         self.inputs += 1
                    #     else:
                    #         error = -21
                    #         err_msg = "Error: Wrong number of parameters for frcInput module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "posOutput":
                    #     if nb_args == 3:
                    #         mod_name = self.moduleName(l[0])
                    #         body = phyMdlCodeGenerator.genPosOutputCode(l[2][1:], mod_name)
                    #         self.outputs_code.append(body)
                    #         self.outputs += 1
                    #     else:
                    #         error = -22
                    #         err_msg = "Error: Wrong number of parameters for posOutput module: " + str(l)
                    #         break
                    #
                    # elif l[1] == "frcOutput":
                    #     if nb_args == 3:
                    #         mod_name = self.moduleName(l[0])
                    #         src = l[2][1:]
                    #         if src[0:2] == "in":
                    #             src = self.moduleName(l[2])
                    #         body = phyMdlCodeGenerator.genForceOutputCode(src, mod_name)
                    #         self.outputs_code.append(body)
                    #         self.outputs += 1
                    #     else:
                    #         error = -23
                    #         err_msg = "Error: Wrong number of parameters for frcOutput module: " + str(l)
                    #         break

                    # else:
                    #     error = -30
                    #     err_msg = "Unknown module name" + str(l)
                    #     break

        if error:
            return error, err_msg

        ########################################################
        ####       Write the generated code to the output destination,
        ####        respecting order (structures, declarations, simcode)
        ########################################################

        if(LIB_VERSION):
            self.generated_code += 'require(\\"migen-lib\\");\n'
            if self.integ_list:
                self.generated_code += 'require(\\"migen-extras2\\");\n'


        if (includeMotionData == 1):
            self.generated_code += "Buffer " + self.motionBufferName + ";\n"

        self.declareBufferList()


        if (error == 0):

            self.generated_code += "\n// Model data structures\n"
            while len(self.struct_code) > 0:
                tmp = self.struct_code.pop()
                self.generated_code += tmp + "\n"

            self.generated_code += "\n// Control Rate Parameters\n"
            while len(self.param_code) > 0:
                tmp = self.param_code.pop()
                self.generated_code += tmp + "\n"

            self.generated_code += "\nParam display_motion(0);\n"

            self.generated_code += "\n// Model initialisation flag\n"
            self.generated_code += "History model_init(0);\n"
            self.generated_code += "History render_cpt(0);\n\n"

            self.generated_code += "// Audio Rate Parameters\n"
            while len(self.audio_param_code) > 0:
                tmp = self.audio_param_code.pop()
                self.generated_code += tmp + "\n"



            self.generated_code += "\n// Model init phase\n"
            self.generated_code += "\nif(model_init == 0){\n"

            while len(self.init_mass_code) > 0:
                tmp = self.init_mass_code.pop()
                self.generated_code += tmp + "\n"

            self.generated_code += "\n// Raise init flag\n"
            self.generated_code += "model_init = 1;\n}\n\n"

            self.generated_code += "// Model computation\n"
            while len(self.comp_mass_code) > 0:
                tmp = self.comp_mass_code.pop()
                self.generated_code += tmp + "\n"

            while len(self.comp_proxy_mass_code) > 0:
                tmp = self.comp_proxy_mass_code.pop()
                self.generated_code += tmp + "\n"

            while len(self.comp_link_code) > 0:
                tmp = self.comp_link_code.pop()
                self.generated_code += tmp + "\n"

            while len(self.comp_proxy_link_code) > 0:
                tmp = self.comp_proxy_link_code.pop()
                self.generated_code += tmp + "\n"

            self.generated_code += "\n// Output routing\n"
            while len(self.outputs_code) > 0:
                tmp = self.outputs_code.pop()
                self.generated_code += tmp + "\n"

            self.generated_code += "\n// Motion data routing to Max/MSP buffer objects\n"
            self.generated_code += "if (display_motion){\n"
            self.generated_code += "if (render_cpt == 0){\n"
            if (includeMotionData):
                while len(self.motion_code) > 0:
                    self.generated_code += self.motion_code.pop()
            self.generated_code += "}\n"
            self.generated_code += "render_cpt = (render_cpt + 1) % 200;}\n"

            print(self.generated_code)

        return 0, "all OK"

    def createDspObj(self, targetPath):
        self.generated_code = self.generated_code.replace('\n', '\\r\\n')
        phyMdlDspObjGenerator.generateDspObj(targetPath, self.generated_code, self.inputs, self.outputs)

