# model code Generator: various topologies, etc.
import numpy as np


def createString(size, name, M, K, Z, hasZosc, Zosc,
                 mParamName=None, kParamName=None, zParamName=None, zoscParamName=None):
    s = ""

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





##### Ajout JV ######

def createTriangleMembrane(size, name, M, K, Z, hasZosc, Zosc,
                           mParamName=None, kParamName=None, zParamName=None, zoscParamName=None,
                           mem_name = "triangle_membrane", spacing = 0.1):
    s = ""
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
    for j in range(0,size):
        for i in range(0,size-j):
            index = "@" + name + "_m" + str(j) + "_" + str(i)
            if not hasZosc:
                s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(spacing * j) + " " + str(
                    spacing*(i + j / 2.0)) + "\n"
            else:
                s += index + " osc " + massVal + " 0 " + zoscVal +" 0. 0. " + mem_name + " " + str(spacing * j) + " " + str(
                    spacing * i) + "\n"
            mList.append(index)
    s += "\n"

    sprIndex = 0

    # horizontal connections
    masCount = 0
    for j in range(0,size-1):
        for i in range(0,size-1-j):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[masCount] + " " + mList[masCount + 1]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
            masCount += 1
        masCount += 1
    s += "\n"

    # first diagonal connections
    masCount = 0
    for j in range(0, size - 1):
        for i in range(0, size - 1 - j):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[masCount + i] + " " + mList[masCount + i + size - j]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
        masCount += size-j
    s += "\n"

    # second diagonal connections
    masCount = 1
    for j in range(0, size - 1):
        for i in range(0, size - 1 - j):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[masCount + i] + " " + mList[masCount + i + size - j - 1]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
        masCount += size - j
    s += "\n"
    print(s)

    return s


def createHexagonaleMembrane(size, name, M, K, Z, hasZosc, Zosc,
                           mParamName=None, kParamName=None, zParamName=None, zoscParamName=None,
                           mem_name = "hexagonale_membrane", spacing = 0.1):
    s = ""
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
    # The model is built by stacking concentric hexagonal arrays of masses (Russian dolls style)
    # size = 1   size = 2  etc.
    #              ____
    #    __       / __ \
    #   /  \     / /  \ \
    #   \__/     \ \__/ /
    #             \____/
    #
    # and connecting each mass with a triangular pattern
    ############################

    # Create the central masse
    index = "@" + name + "_m" + str(0) + "_" + str(0)
    if not hasZosc:
        s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(spacing * 0) + " " + str(
            spacing * 0) + "\n"
    else:
        s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(spacing * 0) + " " + str(
            spacing * 0) + "\n"
    mList.append(index)

    dX = spacing/2
    dY = np.sqrt(dX*dX+spacing*spacing)
    # Create all the other masses one hexagon after another
    for j in range(0,size+1):
        X = (j)*dX
        Y = (j)*dY

        ## First mass of each hexagonal array
        # if not hasZosc:
        #     s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
        # else:
        #     s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
        # mList.append(index)

        for i in range(0,j*6):
            index = "@" + name + "_m" + str(j) + "_" + str(i)

            ## Masses for each face of the hexagon
            if i < j :

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X + dX
                Y = Y - dY

            elif i < 2 * j:

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X - dX
                Y = Y - dY

            elif i < 3 * j:

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X - 2 * dX
                Y = Y

            elif i < 4 * j:

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X - dX
                Y = Y + dY

            elif i < 5 * j:

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X + dX
                Y = Y + dY

            else :

                if not hasZosc:
                    s += index + " mass " + massVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(Y) + "\n"
                else:
                    s += index + " osc " + massVal + " 0 " + zoscVal + " 0. 0. " + mem_name + " " + str(X) + " " + str(
                        Y) + "\n"
                mList.append(index)
                X = X + 2 * dX
                Y = Y


    s += "\n"

    sprIndex = 0

    # "external" connections
    masCount = 1
    for j in range(1, size+1):
        for i in range(0, j*6-1):
            s += "@" + name + "_r" + str(sprIndex) + " spring "
            s += mList[masCount] + " " + mList[masCount + 1]
            s += " " + stiffVal + " " + dampVal + "\n"
            sprIndex += 1
            masCount += 1
        s += "@" + name + "_r" + str(sprIndex) + " spring "
        s += mList[masCount] + " " + mList[masCount - j*6+1]
        s += " " + stiffVal + " " + dampVal + "\n"
        sprIndex += 1
        masCount += 1
    s += "\n"

    # "internal" connections
    ### connections around central mass
    for j in range(1, 7):
        s += "@" + name + "_r" + str(sprIndex) + " spring "
        s += mList[0] + " " + mList[j]
        s += " " + stiffVal + " " + dampVal + "\n"
        sprIndex += 1
    s += "\n"
    s += "\n"

    ### other connections
    altLowFlag = 0
    massCountLow = 1
    massCountHigh = 0
    for j in range(1, size):
        sprCountSection = 0

        angleFlag = 2 * (j+1) - 1
        massCountLow = massCountLow
        print("debut")
        print(massCountLow)
        massCountHigh = 6 * ( j ) + massCountLow
        print(massCountHigh)
        sprLocalCount = 0

        while sprLocalCount < (2*(j+1)-1)*6-1:
            if not altLowFlag:
                s += "@" + name + "_r" + str(sprIndex) + " spring "
                s += mList[massCountLow] + " " + mList[massCountHigh]
                s += " " + stiffVal + " " + dampVal + "\n"
                sprIndex += 1
                sprCountSection += 1
                sprLocalCount += 1
                massCountHigh += 1
                altLowFlag = 1

                if sprCountSection == angleFlag :
                    s += "@" + name + "_r" + str(sprIndex) + " spring "
                    s += mList[massCountLow] + " " + mList[massCountHigh]
                    s += " " + stiffVal + " " + dampVal + "\n"
                    sprIndex += 1
                    sprCountSection = 1
                    sprLocalCount += 1
                    massCountHigh += 1

            else :
                s += "@" + name + "_r" + str(sprIndex) + " spring "
                s += mList[massCountLow] + " " + mList[massCountHigh]
                s += " " + stiffVal + " " + dampVal + "\n"
                sprIndex += 1
                sprCountSection += 1
                sprLocalCount += 1
                massCountLow += 1
                altLowFlag = 0

        s += "@" + name + "_r" + str(sprIndex) + " spring "
        s += mList[massCountLow-j*6] + " " + mList[massCountHigh]
        s += " " + stiffVal + " " + dampVal + "\n"
        sprIndex += 1

        print("fin")
        print(massCountLow)
        print(massCountHigh)

        s += "\n"

    print(s)


    return s
