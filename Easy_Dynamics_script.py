import maya.cmds as cmds

#some lists to populate layers with
global assetsLayer
global duplicateMeshArray
assetsLayer =[]
duplicateMeshArray = []

#some lists to store some selections
global origMeshArray
global dupeMeshArray


#some nameplace vars I stored
dupMeshGroup = 'dupGroup'

base = "base_j"
scaleFactor = float(.95)

dlayNameA = 'actual assets'
dlayNameB = 'dynamic dups'




#quick function to store the original mesh list
def storeOrigArray():
    #declare the list
    global origMeshArray
    #Store the listed selection in the list var
    origMeshArray = cmds.ls(sl =True)
    print(origMeshArray)

#quick function to select every object in the original mesh list
def selectOrigArray():
    #declare the list
    global origMeshArray
    print(origMeshArray)
    #clear any current selection
    cmds.select(cl=1)
    #quick loop to select all objects in the list
    for x in origMeshArray:
        cmds.select( x, add=True)

#quick function to select the duplicate meshes if they exist based off..
#..names of the original mesh list        
def selectDupeArray():
    #declare the list
    global origMeshArray
    print(origMeshArray)
    #clear any current selection
    cmds.select(cl=1)
    #quick loop to select any dupilcate meshes
    for x in origMeshArray:
        cmds.select( "D_" + x, add=True)
    

#the function to run a pop up window to take a scale value for the duplicate meshes..
#.. and then run the rigging and duplicating process the same as in the riggDynamicMesh()..
#.. function although now with the scale value factored into the duplicate mesh size
def getScale():
    #defining a pop up window
    popUp = cmds.window(title = "Scale Value", sizeable=False, resizeToFitChildren=True)
    #defining the layout
    cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [(5, 150), (5, 1500), (5, 150)])
    #placing some empty text objects
    cmds.text(label='')
    #placing the pop up instructions
    cmds.text(label="Set Duplicate Mesh Scale")
    #more empty text objects
    cmds.text(label='')
    cmds.text(label='')
    #float field for the scale value
    scaleField = cmds.floatField( minValue=0, maxValue=1.0, value=.95 )
    #more empty text objects
    cmds.text(label='')
    cmds.text(label='')
    
    # a modified version of the original rig dynamic mesh function but with scale..
    #.. factoring in
    def riggDynamicMeshScale(self):
	    scaleFactor = cmds.floatField(scaleField, q=1, v=1)
	    meshArray = cmds.ls( sl = True )
	    cmds.deleteUI(popUp, window = True)
	    cmds.select(cl=1)

	    cmds.joint( n = base, a=1, p = (0, 0, 0))
	    cmds.select(cl=1)
	
	    for mesh in meshArray:
		    jointName = (mesh + "_j")
		    dupeMeshName = ("D_" + mesh)
		    meshLoc = cmds.xform( mesh, q = 1, ws = 1, rp = 1)
		    cmds.joint(n = jointName, p = meshLoc)
		
		    cmds.parent(jointName, base)
		    cmds.select(cl=1)
		
		    cmds.duplicate(mesh, n = dupeMeshName)
		    cmds.setAttr((dupeMeshName + ".scaleX"), scaleFactor) 
		    cmds.setAttr((dupeMeshName + ".scaleY"), scaleFactor) 
		    cmds.setAttr((dupeMeshName + ".scaleZ"), scaleFactor) 
		    cmds.select(cl=1)
		    
		    global assetsLayer
		    assetsLayer.append(jointName)
		    assetsLayer.append(mesh)
		    global duplicateMeshArray
		    duplicateMeshArray.append(dupeMeshName)
		    cmds.select(cl=1)
	
		    cmds.skinCluster( jointName, mesh, tsb=True, mi=1)
	    cmds.select(cl=1)
	    cmds.select(duplicateMeshArray)
	    cmds.group(n=dupMeshGroup)
	    
	    assetsLayer.append('base_j')
	    cmds.select(assetsLayer)
	    cmds.createDisplayLayer(nr=True, n=dlayNameA)
	    cmds.select(cl=True)
	    
	    cmds.select(duplicateMeshArray)
	    cmds.createDisplayLayer(nr=True, n=dlayNameB)
	    cmds.select(cl=True)
	    meshArray = []
	    assetsLayer = []
	     
    cmds.button(label = "Rigg Dynamic Mesh and Dupe", command = riggDynamicMeshScale)
    cmds.showWindow(popUp)	

#the main function for making and placing the duplicate meshes and the joints..
# .. for the rig	
def riggDynamicMesh():
    #take the current selection as a list to run through
	meshArray = cmds.ls( sl = True )
    #clear selection
	cmds.select(cl=1)
    #create a quick base joint
	cmds.joint( n = base, a=1, p = (0, 0, 0))
    #safety clear selection
	cmds.select(cl=1)
	
    #the loop that will cycle through the list and make the joints and dupelicate..
    #.. meshes
	for mesh in meshArray:
        #store a new joint name based on the mesh list item
		jointName = (mesh + "_j")
        #store a new dupelicate mesh name based on the mesh list item
		dupeMeshName = ("D_" + mesh)
        #store the mesh location
		meshLoc = cmds.xform( mesh, q = 1, ws = 1, rp = 1)
        #create a joint at the mesh location
		cmds.joint(n = jointName, p = meshLoc)
		
        #parent the joint to the base joint
		cmds.parent(jointName, base)
        #safety clear the selection 
		cmds.select(cl=1)
		
        #duplicate each mesh and give the duplicate an name
		cmds.duplicate(mesh, n = dupeMeshName)
        #safety clear the selection
		cmds.select(cl=1)
		
        #declare the asset layer list
		global assetsLayer
        #add the joint and mesh from the list to the asset layer list
		assetsLayer.append(jointName)
		assetsLayer.append(mesh)
        #declare the duplicate asset layer list
		global duplicateMeshArray
        #now add the duplicate mesh to the duplicate layer list
		duplicateMeshArray.append(dupeMeshName)
        #clear selection
		cmds.select(cl=1)
        #now skin the mesh item to the joint
		cmds.skinCluster( jointName, mesh, tsb=True, mi=1)
	#clear the selections
    cmds.select(cl=1)
	print(duplicateMeshArray)
    #group the duplicate meshes
	cmds.select(duplicateMeshArray)
	cmds.group(n=dupMeshGroup)
	
    #add the base joint to the asset list
	assetsLayer.append('base_j')
    #select all of the asset layer list contents
	cmds.select(assetsLayer)
    #create a display layer containing the list contents
	cmds.createDisplayLayer(nr=True, n=dlayNameA)
    #clear the selection
	cmds.select(cl=True)
	
    #select all of the duplicate mesh list contents
	cmds.select(duplicateMeshArray)
    #create a display layer containing the list contents
	cmds.createDisplayLayer(nr=True, n=dlayNameB)
    #clear the selection
	cmds.select(cl=True)
    #redeclare the mesh list, duplicate mesh list, and asset list, all as empty lists
	meshArray = []
	duplicateMeshArray = []
	assetsLayer = []

# function that goes through and contrains the joints to the duplicate meshes..
# and adds the active rigid bodies to the duplicate meshes.	
def constrainAndRigibody():
    #store the current selection as the select list
    selectArray = cmds.ls( sl = True )

    #a loop that adds contrains and rigid bodies to the selected assets
    for mesh in selectArray:
        #store a temp mesh name
        origMeshName = str(mesh)
        #correct it to the original mesh name
        origMeshName = origMeshName.replace('D_', '')
        print (origMeshName)
        #store a reconstructed corresponding joint name
        jointName = (origMeshName + "_j")
        #add a constraint from the duplicate mesh (constrainor) to..
        # .. the joint (constrainee)
        cmds.parentConstraint( mesh, jointName, mo = 1 )
        #clear the selection
        cmds.select(cl=1)
        #select the duplicate mesh
        cmds.select(mesh)
        #add an active rigidbody
        cmds.rigidBody( active = 1)
        #clear the selection
        cmds.select(cl=1)

#quick function that adds a ground plane and gives it a passive rigid body
def basicGround():
    cmds.polyPlane(name='Basic_Ground')
    cmds.select('Basic_Ground')
    cmds.rigidBody(active = False, passive = True)
    cmds.select(cl=1)

#quick function that adds gravity solver and connects its influence to..
#.. to the duplicate meshes    
def addGravity():
    selectDupeArray()
    gravInf= cmds.ls(sl=True)
    cmds.select(cl=True)
    cmds.gravity()
    cmds.connectDynamic( gravInf, f= 'gravityField1')

#quick function that adds air solver and connects its influence to..
#.. to the duplicate meshes
def addAir():
    selectDupeArray()
    airInf= cmds.ls(sl=True)
    cmds.select(cl=True)
    cmds.air()
    cmds.connectDynamic( airInf, f= 'airField1')
    
#a function to bake down the dynamic animation, and also export the rig and mesh
def bakeDownAndFinishNewPackage():
	#get its file name
	fileName = cmds.file( q=True, sn=True )
	print(fileName)
	#save current file
	cmds.file( save = True, type = 'mayaAscii')
  
	#bake the simulation
	animStart = int(cmds.playbackOptions(q = True, minTime = True))
	print(animStart)
	animEnd = int(cmds.playbackOptions(q = True, maxTime = True))
	print(animEnd)
	#select all the joints before baking anim or sim
	cmds.select(cmds.ls(type='joint'))
	cmds.bakeResults(t=(animStart, animEnd), simulation=True)
	#bakeFinish
	#delete constraints
	cmds.select('base_j')
	#delete constraints 
	cmds.select(hi = True)
	cmds.delete(cn = True)
	#select everything for clearing
	cmds.select(cmds.ls(tr = True))
	#deselect what you want to save by selecting the assets layers objects
	dontDelete= cmds.editDisplayLayerMembers( 'actual_assets', q=True )
	cmds.select(dontDelete, d = True, ne = True)
	cmds.delete()
	cmds.select(cl=1)
	#delete display layers
	cmds.delete(cmds.ls(type = 'displayLayer'))
	cmds.select(cl=1)
 
	#select the mesh and rig for fbx save
	cmds.select(cmds.ls(type='mesh'))
	cmds.select(cmds.ls(type='joint'), add=True)
	#save out the file as an fbx
	cmds.file( force = True, options = "v=0;",type = "FBX export")
  
	#reopen the file to a point before the bake happened
	cmds.file(fileName, f=True, o=True)

    
#a function to bake down the dynamic animation
def bakeDownAndFinishNewAnimation():
	#get its file name
	fileName = cmds.file( q=True, sn=True )
	print(fileName)
	#save current file
	cmds.file( save = True, type = 'mayaAscii')
  
	#bake the simulation
	animStart = int(cmds.playbackOptions(q = True, minTime = True))
	print(animStart)
	animEnd = int(cmds.playbackOptions(q = True, maxTime = True))
	print(animEnd)
	#select all the joints before baking anim or sim
	cmds.select(cmds.ls(type='joint'))
	cmds.bakeResults(t=(animStart, animEnd), simulation=True)
	#bakeFinish
	#delete constraints
	cmds.select('base_j')
	#delete constraints
	cmds.select(hi = True)
	cmds.delete(cn = True)
	#select everything for clearing
	cmds.select(cmds.ls(tr = True))
	#deselect what you want to save by selecting the assets layers objects
	dontDelete= cmds.ls(type='joint')
	cmds.select(dontDelete, d = True, ne = True)
	cmds.delete()
	cmds.select(cl=1)
	#delete display layers
	cmds.delete(cmds.ls(type = 'displayLayer'))
	cmds.select(cl=1)
 
	#select the mesh and rig for fbx save
	cmds.select(cmds.ls(type='joint'), add=True)
	#save out the file as an fbx
	cmds.file( force = True, options = "v=0;",type = "FBX export")
  
	#reopen the file to a point before the bake happened
	cmds.file(fileName, f=True, o=True)


    
#-------------------------------- UI components ---------------------------------

window = cmds.window(title = "Easy Dynamics Panel", widthHeight = (370,250))
cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(5, 300), (5, 300), (5, 300)])
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.button(label = "store Orig. Array", command = 'storeOrigArray()')
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.button(label = "sel Orig. Array", command = 'selectOrigArray()')
cmds.button(label = "sel Dupe Array", command = 'selectDupeArray()')
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.button(label = "Rigg Dynamic Mesh and Dupe / Scale", command = 'getScale()')
cmds.button(label = "Rigg Dynamic Mesh and Dupe", command= 'riggDynamicMesh()')
cmds.button(label = "constrain and rigibody", command= 'constrainAndRigibody()')
cmds.button(label = "insert basic ground", command= 'basicGround()')
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.button(label = "Add Gravity", command = 'addGravity()')
cmds.button(label = "Add Wind/Air", command = 'addAir()')
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.text(label = '', width = 150)
cmds.button(label = "bake out new package", command= 'bakeDownAndFinishNewPackage())')
cmds.button(label = "bake out new animation", command= 'bakeDownAndFinishNewAnimation()')
cmds.showWindow(window)