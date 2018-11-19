# model code Generator: various topologies, etc.

def createString(size, name, M, K, Z, hasZosc, Zosc,
                 mParamName=None, kParamName=None, zParamName=None, zoscParamName=None):
    s = ""

    massVal = ""
    stiffVal = ""
    dampVal = ""
    zoscVal = ""

    if mParamName:
        s += "@" + mParamName + " param " + str(M) + "\n"
        massVal = mParamName
    else:
        massVal = str(M)
    if kParamName:
        s += "@" + kParamName + " param " + str(K) + "\n"
        stiffVal = kParamName
    else:
        stiffVal = str(K)
    if zParamName:
        s += "@" + zParamName + " param " + str(Z) + "\n"
        dampVal = zParamName
    else:
        dampVal = str(Z)
    if hasZosc:
        if zoscParamName:
            s += "@" + zoscParamName + " param " + str(Zosc) + "\n"
            zoscVal = zoscParamName
        else:
            zoscVal = str(Zosc)
    s += "\n"

    s += "@" + name + "_s0 ground 0.\n"
    i = 0
    while i < size:
        if not hasZosc:
            s += "@" + name + "_m" + str(i) + " mass " + massVal + " 0. 0.\n"
        else:
            s += "@" + name + "_m" + str(i) + " osc " + massVal + " 0 " + zoscVal + " 0. 0.\n"
        i = i + 1
    s += "@" + name + "_s1 ground 0.\n"
    s += "\n"

    i = 0
    s += "@" + name + "_r" + str(i) + " spring "
    s += "@" + name + "_s0 @" + name + "_m" + str(i) + " "
    s += stiffVal + " " + dampVal + "\n"
    while i < size - 1:
        s += "@" + name + "_r" + str(i + 1) + " spring "
        s += "@" + name + "_m" + str(i) + " @" + name + "_m" + str(i + 1) + " "
        s += stiffVal + " " + dampVal + "\n"
        i = i + 1
    s += "@" + name + "_r" + str(i + 1) + " spring "
    s += "@" + name + "_m" + str(i) + " @" + name + "_s1 "
    s += stiffVal + " " + dampVal + "\n"
    s += "\n"
    return s


def createMembrane(sizeL, sizeH, name, M, K, Z, hasZosc, Zosc,
                 mParamName=None, kParamName=None, zParamName=None, zoscParamName=None,
                   mem_name = "membrane", spacing = 0.1):
    s = ""

    massVal = ""
    stiffVal = ""
    dampVal = ""
    zoscVal = ""

    # Define parameter modules, if they are to be named explicitly
    if mParamName:
        s += "@" + mParamName + " param " + str(M) + "\n"
        massVal = mParamName
    else:
        massVal = str(M)
    if kParamName:
        s += "@" + kParamName + " param " + str(K) + "\n"
        stiffVal = kParamName
    else:
        stiffVal = str(K)
    if zParamName:
        s += "@" + zParamName + " param " + str(Z) + "\n"
        dampVal = zParamName
    else:
        dampVal = str(Z)
    if hasZosc:
        if zoscParamName:
            s += "@" + zoscParamName + " param " + str(Zosc) + "\n"
            zoscVal = zoscParamName
        else:
            zoscVal = str(Zosc)
    s += "\n"

    # now we can generate the membrane
    mList = []
    # Create the rows of masses
    for j in range(0,sizeL):
        for i in range(0,sizeH):
            index = "@" + name + "_m" + str(j) + "_" + str(i)
            if not hasZosc:
                s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(spacing * j) + " " + str(
                    spacing * i) + "\n"
            else:
                s += index + " osc " + massVal + " 0 " + zoscVal +" 0. 0. " + mem_name + " " + str(spacing * j) + " " + str(
                    spacing * i) + "\n"
            mList.append(index)
    s += "\n"

    sprIndex = 0

    # horizontal connections
    for j in range(0,sizeL):
        for i in range(0,sizeH-1):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[j * (sizeH - 1) + i + j] + " " + mList[j * (sizeH - 1) + i + 1 + j]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
    s += "\n"


    # vertical connections
    for j in range(0,sizeL-1):
        for i in range(0,sizeH):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[j * (sizeH) + i] + " " + mList[(j + 1) * (sizeH) + i]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
    s += "\n"
    return s


    # s += "@" + name + "_s0 ground 0.\n"
    # i = 0
    # while i < size:
    #     if not hasZosc:
    #         s += "@" + name + "_m" + str(i) + " mass " + massVal + " 0. 0.\n"
    #     else:
    #         s += "@" + name + "_m" + str(i) + " osc " + massVal + " 0 " + zoscVal + " 0. 0.\n"
    #     i = i + 1
    # s += "@" + name + "_s1 ground 0.\n"
    # s += "\n"
    #
    # i = 0
    # s += "@" + name + "_r" + str(i) + " spring "
    # s += "@" + name + "_s0 @" + name + "_m" + str(i) + " "
    # s += stiffVal + " " + dampVal + "\n"
    # while i < size - 1:
    #     s += "@" + name + "_r" + str(i + 1) + " spring "
    #     s += "@" + name + "_m" + str(i) + " @" + name + "_m" + str(i + 1) + " "
    #     s += stiffVal + " " + dampVal + "\n"
    #     i = i + 1
    # s += "@" + name + "_r" + str(i + 1) + " spring "
    # s += "@" + name + "_m" + str(i) + " @" + name + "_s1 "
    # s += stiffVal + " " + dampVal + "\n"
    # s += "\n"
    # return s


def createMembrane_OLD(sizeH, sizeL, name, M, K, Z):
    s = "@param " + name + "_M " + str(M) + "\n"
    s += "@param " + name + "_K " + str(K) + "\n"
    s += "@param " + name + "_Z " + str(Z) + "\n"
    s += "\n"

    mList = []
    # Create the rows of masses
    j = 0
    while j < (sizeL):
        i = 0
        while i < sizeH:
            index = "@" + name + "_m" + str(j) + "_" + str(i)
            s += index + " mass " + name + "_M 0. 0.\n"
            mList.append(index)
            i = i + 1
        j = j + 1
    s += "\n"

    # horizontal connections
    j = 0
    while j < (sizeL):
        i = 0
        while i < (sizeH - 1):
            s += "@" + name + "_r" + " spring "
            s += mList[j * (sizeH - 1) + i + j] + " " + mList[j * (sizeH - 1) + i + 1 + j]
            s += " " + name + "_K " + name + "_Z\n"
            i = i + 1
        j = j + 1
    s += "\n"

    # vertical connections
    j = 0
    while j < (sizeL - 1):
        i = 0
        while i < (sizeH):
            s += "@" + name + "_r" + " spring "
            s += mList[j * (sizeH) + i] + " " + mList[(j + 1) * (sizeH) + i]
            s += " " + name + "_K " + name + "_Z\n"
            i = i + 1
        j = j + 1
    s += "\n"
    return s


def createNLMembrane(sizeH, sizeL, name, M, K, Q, Z, Zc):
    s = "@param " + name + "_M " + str(M) + "\n"
    s += "@param " + name + "_K " + str(K) + "\n"
    s += "@param " + name + "_Q " + str(Q) + "\n"
    s += "@param " + name + "_Z " + str(Z) + "\n"
    s += "@param " + name + "_Zc " + str(Zc) + "\n"

    s += "\n"

    mList = []
    # Create the rows of masses
    j = 0
    while j < (sizeL):
        i = 0
        while i < sizeH:
            index = "@" + name + "_c" + str(j) + "_" + str(i)
            s += index + " cel " + name + "_M 0 " + name + "_Zc 0. 0.\n"
            mList.append(index)
            i = i + 1
        j = j + 1
    s += "\n"

    # horizontal connections
    j = 0
    while j < (sizeL):
        i = 0
        while i < (sizeH - 1):
            s += "@" + name + "_r" + " nlSpring "
            s += mList[j * (sizeH - 1) + i + j] + " " + mList[j * (sizeH - 1) + i + 1 + j]
            s += " " + name + "_K " + name + "_Q " + name + "_Z\n"
            i = i + 1
        j = j + 1
    s += "\n"

    # vertical connections
    j = 0
    while j < (sizeL - 1):
        i = 0
        while i < (sizeH):
            s += "@" + name + "_r" + " nlSpring "
            s += mList[j * (sizeH) + i] + " " + mList[(j + 1) * (sizeH) + i]
            s += " " + name + "_K " + name + "_Q " + name + "_Z\n"
            i = i + 1
        j = j + 1
    s += "\n"
    return s


def createForceInput(number, destname, index):
    s = "@in" + str(number) + " forceInput @" + destname + str(index) + "\n"
    return s


def createPosOutput(number, destname, index):
    s = "@out" + str(number) + " posOutput @" + destname + str(index) + "\n"
    return s
