######################################################
#           File: phyMdlDspObjGenerator.py                                           #
#           Author:     James Leonard                                                            #
#           Date:           09/10/2017                                                                  #
#         Read an input phyMdl file and generate the gendsp        #
#         patch, for direct import in Max/MSP                                        #
######################################################


def generateHeader():
    return """{
	"patcher" : 	{
		"fileversion" : 1,
		"appversion" : 		{
			"major" : 7,
			"minor" : 3,
			"revision" : 1,
			"architecture" : "x64",
			"modernui" : 1
		}
,
		"rect" : [ 67.0, 109.0, 600.0, 450.0 ],
		"editing_bgcolor" : [ 0.9, 0.9, 0.9, 1.0 ],
		"bglocked" : 0,
		"openinpresentation" : 0,
		"default_fontsize" : 12.0,
		"default_fontface" : 0,
		"default_fontname" : "Arial",
		"gridonopen" : 1,
		"gridsize" : [ 15.0, 15.0 ],
		"gridsnaponopen" : 1,
		"objectsnaponopen" : 1,
		"statusbarvisible" : 2,
		"toolbarvisible" : 1,
		"lefttoolbarpinned" : 0,
		"toptoolbarpinned" : 0,
		"righttoolbarpinned" : 0,
		"bottomtoolbarpinned" : 0,
		"toolbars_unpinned_last_save" : 0,
		"tallnewobj" : 0,
		"boxanimatetime" : 200,
		"enablehscroll" : 1,
		"enablevscroll" : 1,
		"devicewidth" : 0.0,
		"description" : "",
		"digest" : "",
		"tags" : "",
		"style" : "",
		"subpatcher_template" : "",
                """


def generateNewObjBox(box_Id, nb_In, nb_Out, objName, xPos, yPos):
    boxText = """{ "box" : 				{
					"id" : " """ + box_Id + """ ",
					"maxclass" : "newobj",
					"numinlets" :  """ + str(nb_In) + """,
					"numoutlets" : """ + str(nb_Out) + """,
					"outlettype" : [ "" ],
					"patching_rect" : [ """ + str(yPos) + """, """ + str(xPos) + """, 30.0, 22.0 ],
					"style" : "",
					"text" : " """ + objName + """ "
				} }"""
    return boxText


def generateCodeBox(codeStr, box_Id, nb_In, nb_Out, xPos, yPos):
    boxText = """{ "box" : 				{
					"code" : " """ + codeStr + """ ",
					"fontface" : 0,
					"fontname" : "Arial",
					"fontsize" : 12.0,
					"id" : " """ + box_Id + """ ",
					"maxclass" : "codebox",
					"numinlets" : """ + str(nb_In) + """,
					"numoutlets" : """ + str(nb_Out) + """,
					"outlettype" : [ "" ],
					"patching_rect" : [ """ + str(yPos) + """, """ + str(xPos) + """, 250.0, 200.0 ],
					"style" : ""
				} }"""
    return boxText


def generatePatchLines(source, srcNb, dest, dstNb):
    text = """ {
				"patchline" : 				{
					"destination" : [ " """ + dest + """ ", """ + str(dstNb) + """ ],
					"disabled" : 0,
					"hidden" : 0,
					"source" : [ " """ + source + """ ", """ + str(srcNb) + """ ]
				}
			}"""
    return text


def generateDspObj(name, codeboxCode, nbIn, nbOut):
    outFile = open(name, 'w')

    ## GenDSP File Header: always the same
    ##  might have to change the 'x64' for 32 bit OS
    outFile.write(generateHeader())

    ## Boxes: codebox + inputs & outputs
    outFile.write('\n "boxes" : [ ')

    ## PhyMdl Codebox
    outFile.write(generateCodeBox(codeboxCode, "phyMdlBox", nbIn, nbOut, 50., 20.))
    outFile.write(', ')

    ## Input objects
    for x in range(1, nbIn + 1):
        outFile.write(generateNewObjBox("inbox_" + str(x), 0, 1, "in " + str(x), 20., 20. + x * 50.))
        outFile.write(', ')

    ## Output objects
    for x in range(1, nbOut):
        outFile.write(generateNewObjBox("outbox_" + str(x), 1, 0, "out " + str(x), 320., 20. + x * 50.))
        outFile.write(', ')
    outFile.write(generateNewObjBox("outbox_" + str(nbOut), 1, 0, "out " + str(nbOut), 320., 20. + nbOut * 50.))
    outFile.write('],\n "lines" : [  ')

    ##  Connections
    for x in range(0, nbIn):
        outFile.write(generatePatchLines("inbox_" + str(x + 1), 0, "phyMdlBox", x))
        outFile.write(', ')
    for x in range(0, nbOut - 1):
        outFile.write(generatePatchLines("phyMdlBox", x, "outbox_" + str(x + 1), 0))
        outFile.write(', ')
    outFile.write(generatePatchLines("phyMdlBox", nbOut - 1, "outbox_" + str(nbOut), 0))

    ## End of GenDSP File
    outFile.write('] } } ')

##########################################################
##########################################################

