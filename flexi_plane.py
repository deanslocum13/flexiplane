'''
Dean Slocum
deanslocum@gmail.com
flexi_plane.py

Description:
	
	v2.3

	Creates the Flexi-plane rigging component for a limb.

How to Run:

import flexi_plane
reload(flexi_plane)

'''

import maya.cmds as cmds

class FlexiPlaneUI(object):
	def __init__(self):
		self.win='Flexi Plane'
		self.w=90
		self.h=180
		self.b1=[0,.5,0]
		self.b2=[0,.5,.5]
		self.co=[1,'both',16]

	def gui(self):	
		
		if(cmds.window(self.win,ex=1)):
			cmds.deleteUI(self.win)
		if (cmds.windowPref(self.win,ex=1)):
			cmds.windowPref(self.win,r=1)

		self.win=cmds.window(self.win,s=1,vis=1,w=self.w,h=self.h)

		flexiPlaneUi=cmds.rowColumnLayout('flexiPlaneUi',p=self.win)

		frameLayout=cmds.frameLayout(l=' Add a Prefix & press BUILD',bgc=self.b1)

		textLayout=cmds.rowColumnLayout('textLayout',co=self.co,p=frameLayout)

		cmds.text(' ')

		self.prefixText=cmds.textFieldGrp('prefix_input',l='Prefix: ',pht='lt_arm, etc.',cal=[1,'left'],cw2=[40,100],p=textLayout)
		# cmds.textFieldGrp(self.prefixText,q=1,text=1)

		checkBoxLayout=cmds.rowColumnLayout('checkBoxLayout',nc=1,co=self.co,p=frameLayout)

		self.matCheckBox=cmds.checkBox('mat_check',l='Build Materials',v=1,p=checkBoxLayout)
		# cmds.checkBox(self.matCheckBox,q=1,v=1)

		buttonLayout=cmds.rowColumnLayout('buttonLayout',nc=2,co=self.co,p=frameLayout)

		cmds.text('     ')

		cmds.button(l='BUILD',c=self.flexi_plane,bgc=self.b2,w=80,p=buttonLayout)

		cmds.text(' ')

		cmds.showWindow()

	def flexi_plane(self,*args):

		# create nurbs plane w/ x attrs
		# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 5 -lr 0.2 -d 3 -u 5 -v 1 -ch 1;
		nurbs_plane=cmds.nurbsPlane(ax=(0,1,0),w=10,lengthRatio=0.2,d=3,u=5,v=1,ch=0,n='flexi_surface_01')

		attrs=['castsShadows','receiveShadows','motionBlur','primaryVisibility','smoothShading',
				'visibleInReflections','visibleInRefractions']		
		for attr in attrs:
			cmds.setAttr('flexi_surface_01Shape.{0}'.format(attr),0)

		# create new material
		# cmds.shadingNode('lambert',asShader=1,n='flexi_surface_mat_01')
		# make material light blue and lower transparency
		# asign material to nurbs plane
		if cmds.checkBox(self.matCheckBox,q=1,v=1) == True:
			flexi_mat=cmds.shadingNode('lambert',asShader=1,n='flexi_surface_mat_01')
			cmds.setAttr(flexi_mat+'.color',0.0,1.0,1.0,type='double3')
			cmds.setAttr(flexi_mat+'.transparency',0.75,0.75,0.75,type='double3')
			cmds.select(nurbs_plane)
			cmds.hyperShade(assign=flexi_mat)
		elif cmds.checkBox(self.matCheckBox,q=1,v=1) == False:
			print 'no surface material created'

		# create follicle system
		# create 5 flcs
		flc_a01=cmds.createNode('follicle',skipSelect=1)
		cmds.rename('follicle1','flexi_flcs_a01')

		flc_b01=cmds.createNode('follicle',skipSelect=1)
		cmds.rename('follicle1','flexi_flcs_b01')

		flc_c01=cmds.createNode('follicle',skipSelect=1)
		cmds.rename('follicle1','flexi_flcs_c01')

		flc_d01=cmds.createNode('follicle',skipSelect=1)
		cmds.rename('follicle1','flexi_flcs_d01')

		flc_e01=cmds.createNode('follicle',skipSelect=1)
		cmds.rename('follicle1','flexi_flcs_e01')

		# hide flcs shape vis and set up node network
		shapeNodes=cmds.listRelatives('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01',shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.visibility".format(shape),0)
			cmds.connectAttr('flexi_surface_01Shape.local','{0}.inputSurface'.format(shape),f=1)
			cmds.connectAttr('flexi_surface_01Shape.worldMatrix[0]','{0}.inputWorldMatrix'.format(shape),f=1)

		# node network cont.
		sel_shape=cmds.listRelatives('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01',shapes=1)
		sel=cmds.ls('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')
		count=-1
		for shape in sel_shape:
			count=count+1
			cmds.connectAttr('{0}.outRotate'.format(sel_shape[count]),'{0}.rotate'.format(sel[count]),f=1)
			cmds.connectAttr('{0}.outTranslate'.format(sel_shape[count]),'{0}.translate'.format(sel[count]),f=1)

		# move the U & V parameters for each flc
		sel=cmds.ls('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')
		count=-0.1
		for each in sel:
			count=count+0.2
			cmds.setAttr('{0}.parameterU'.format(each),count)
			cmds.setAttr('{0}.parameterV'.format(each),0.5)

		# lock trans and rot on flcs
		sel=cmds.ls('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')
		attrs=['tx','ty','tz','rx','ry','rz']
		for each in sel:
			for attr in attrs:
				cmds.setAttr('{0}.{1}'.format(each,attr),l=1)

		# group flcs w/ name flexi_flcs_grp_01
		cmds.group('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01',n='flexi_flcs_grp_01')

		# create square CV , CP , end of plane, name flexi_icon_a01, change color to yellow, repeat for other end
		# curve -d 1 -p -6 0 -1 -p -6 0 1 -p -4 0 1 -p -4 0 -1 -p -6 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 ;
		ctrl_a01=cmds.curve(d=1,p=[(-5.6,0,-0.6),
						  		   (-4.4,0,-0.6),
						  		   (-4.4,0,0.6),
						  		   (-5.6,0,0.6),
						  		   (-5.6,0,-0.6)], 
								k=[0,1,2,3,4], n='flexi_icon_a01')
		
		cmds.xform(ctrl_a01,cp=1)

		cmds.select(cl=1)

		ctrl_b01=cmds.curve(d=1,p=[(4.4,0,-0.6),
						  			(5.6,0,-0.6),
						  			(5.6,0,0.6),
						 		    (4.4,0,0.6),
						  			(4.4,0,-0.6)],
								k=[0,1,2,3,4],n='flexi_icon_b01')

		cmds.xform(ctrl_b01,cp=1)

		shapeNodes=cmds.listRelatives(ctrl_a01,ctrl_b01,shapes=1)
		for shape in shapeNodes:
				cmds.setAttr("{0}.overrideEnabled".format(shape),1)
				cmds.setAttr("{0}.overrideColor".format(shape),17)

		cmds.select(cl=1)

		# duplicate plane, translate Z axis -5, reanme to flexi_bShp_surface_01
		bShp_surface=cmds.duplicate(nurbs_plane,n='flexi_bShp_surface_01')
		cmds.select(bShp_surface)
		cmds.xform(t=[0,0,-5])

		# create blendshape w/ default settings, name flexi_bShpNode_surface_01
		cmds.blendShape(bShp_surface,nurbs_plane,n='flexi_bShpNode_surface_01')

		# output settings to always on = 1
		cmds.setAttr('flexi_bShpNode_surface_01.flexi_bShp_surface_01',1)

		# CV w/ 3 pts on dup plane, degree-2, rename to flexi_wire_surface_01
		wire_surface=cmds.curve(d=2,p=[(-5,0,-5),
								   	   (0,0,-5),
								       (5,0,-5)],
									k=[0,0,1,1],n='flexi_wire_surface_01')

		# create cluster w/ relative=ON, on left and mid cv points, rename to flexi_cl_a01
		cmds.select(cl=1)
		clus=cmds.cluster(['flexi_wire_surface_01.cv[0:1]'],rel=1,n='flexi_clus_')

		clus_sel=cmds.select('flexi_clus_Handle')
		clus_1=cmds.rename(clus_sel,'flexi_cl_a01')

		# set cluster origin=-6
		cmds.setAttr('|flexi_cl_a01|flexi_cl_a01Shape.originX',-6)

		# move pivot to end of dup plane
		cmds.xform(piv=[-5,0,-5])

		# repeat previous steps for other side 
		cmds.select(cl=1)
		clus=cmds.cluster(['flexi_wire_surface_01.cv[1:2]'],rel=1,n='flexi_clus_')

		clus_sel=cmds.select('flexi_clus_Handle')
		clus_2=cmds.rename(clus_sel,'flexi_cl_b01')

		cmds.setAttr('|flexi_cl_b01|flexi_cl_b01Shape.originX',6)

		cmds.xform(piv=[5,0,-5])

		# repeat for middle
		cmds.select(cl=1)
		clus=cmds.cluster(['flexi_wire_surface_01.cv[1]'],rel=1,n='flexi_clus_')

		clus_sel=cmds.select('flexi_clus_Handle')
		clus_3=cmds.rename(clus_sel,'flexi_cl_mid01')

		# select mid CV point, component editor, weighted deformer tab, a & b node set to 0.5
		# select -r flexi_wire_surface_01.cv[1] ;
		# percent -v 0.5 flexi_cl_a01Cluster flexi_wire_surface_01.cv[1] ;
		# percent -v 0.5 flexi_cl_b01Cluster flexi_wire_surface_01.cv[1] ;
		cmds.select(cl=1)
		cmds.select('flexi_wire_surface_01.cv[1]')
		cmds.percent('flexi_cl_a01Cluster',v=0.5)
		cmds.percent('flexi_cl_b01Cluster',v=0.5)
		cmds.select(cl=1)

		# wire deformer, select CV then the dup plane and press enter, dropoff distance to 20
		# mel.eval('wire -gw false -dds 0 20 -en 1.000000 -ce 0.000000 -li 0.000000 -w flexi_wire_surface_01 flexi_bShp_surface_01;')
		cmds.wire('flexi_bShp_surface_01',groupWithBase=0,dropoffDistance=(0,20),envelope=1.0,crossingEffect=0.0,
										  localInfluence=0.0,wire=wire_surface,n='flexi_wireAttrs_surface_01')
		cmds.select(cl=1)

		# select start control, start cluster, open conection editor, connect translate to translate
		# connectAttr -f flexi_icon_a01.translate flexi_cl_a01.translate;
		cmds.connectAttr('flexi_icon_a01.translate','flexi_cl_a01.translate',f=1)

		# repeat for other end
		cmds.connectAttr('flexi_icon_b01.translate','flexi_cl_b01.translate',f=1)

		# group the 3 clusters together, name it flexi_cls_01
		cmds.group(clus_1,clus_2,clus_3,n='flexi_cls_01')

		# create group for 2 current controls, name it flexi_icons_01
		cmds.group('flexi_icon_a01','flexi_icon_b01',n='flexi_icons_01')

		# lock and hide transform channels of groups
		attrs=['tx','ty','tz','rx','ry','rz','sx','sy','sz']
		for attr in attrs:
			cmds.setAttr('flexi_cls_01.{0}'.format(attr),l=1,k=0)
			cmds.setAttr('flexi_icons_01.{0}'.format(attr),l=1,k=0)

		# create center control, name it flexi_midBend_01
		# sphere -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -nsp 4 -ch 1;
		mid_ctrl=cmds.sphere(pivot=[0,0,0],ax=[0,1,0],startSweep=0,endSweep=360,ch=0,r=0.3,d=3,
							 useTolerance=0,tol=0.8,spans=4,n='flexi_midBend_01')

		attrs=['castsShadows','receiveShadows','motionBlur','primaryVisibility','smoothShading',
				'visibleInReflections','visibleInRefractions']
		for attr in attrs:
			cmds.setAttr('flexi_midBend_01Shape.{0}'.format(attr),0)

		# new material, surface shader, yellow color, name flexi_ss_midBend_01
		if cmds.checkBox(self.matCheckBox,q=1,v=1) == True:
			flexi_mat_2=cmds.shadingNode('surfaceShader',asShader=1,n='flexi_mid_mat_01')
			cmds.setAttr(flexi_mat_2+'.outColor',1.0,1.0,0.0,type='double3')
			cmds.select(mid_ctrl)
			cmds.hyperShade(assign=flexi_mat_2)
		elif cmds.checkBox(self.matCheckBox,q=1,v=1) == False:
			print 'no mid ctrl material created'

		# connect translates for new mid control to mid cluster
		cmds.connectAttr('flexi_midBend_01.translate','flexi_cl_mid01.translate',f=1)

		# create group for mid control, name flexi_grp_midBend_01
		cmds.group('flexi_midBend_01',n='flexi_grp_midBend_01')

		# point constraint, select 2 outside controls, then ctrl click mid control, point constraint
		cmds.pointConstraint('flexi_icon_a01','flexi_icon_b01','flexi_grp_midBend_01',mo=1)

		# parent midBend grp under icons grp
		cmds.parent('flexi_grp_midBend_01','flexi_icons_01')

		# group all nodes under single group, name flexiPlane_rig_01
		cmds.group('flexi_surface_01','flexi_flcs_grp_01','flexi_bShp_surface_01','flexi_wire_surface_01','flexi_wire_surface_01BaseWire',
					'flexi_cls_01','flexi_icons_01',n='flexiPlane_rig_01')

		# lock and hide group transforms
		attrs=['tx','ty','tz','rx','ry','rz','sx','sy','sz']
		for attr in attrs:
			cmds.setAttr('flexiPlane_rig_01.{0}'.format(attr),l=1,k=0)

		# group flexi surface and icons grp, name flexi_globalMove_01
		cmds.group('flexi_surface_01','flexi_icons_01',n='flexi_globalMove_01')

		# group all but global, name flexi_extraNodes_01
		cmds.group('flexi_flcs_grp_01','flexi_bShp_surface_01','flexi_wire_surface_01','flexi_wire_surface_01BaseWire',
					'flexi_cls_01',n='flexi_extraNodes_01')
		cmds.select(cl=1)

		# scale constrain each follicle to the global move grp
		sel=cmds.ls('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')
		for each in sel:
			cmds.scaleConstraint('flexi_globalMove_01','{0}'.format(each),mo=0)

		# build global control
		ctrl_global=cmds.curve(d=1,p=[(0,0,-1.667542),
						  			  (-0.332458,0,-2),
						  			  (0.332458,0,-2),
						  			  (0,0,-1.667542),
					   	  			  (0,0,1.667542),
					   	  			  (0.332458,0,2),
					   	  			  (-0.332458,0,2),
					   	 			  (0,0,1.667542)], 
									k=[0,1,2,3,4,5,6,7], n='flexi_icon_global_01')
		
		cmds.xform(ctrl_global,cp=1)

		shapeNodes=cmds.listRelatives(ctrl_global,shapes=1)
		for shape in shapeNodes:
				cmds.setAttr("{0}.overrideEnabled".format(shape),1)
				cmds.setAttr("{0}.overrideColor".format(shape),17)

		cmds.select(cl=1)

		# parent global ctrl under main flexi grp
		cmds.parent('flexi_icon_global_01','flexiPlane_rig_01')

		# parent global grp under ctrl
		cmds.parent('flexi_globalMove_01','flexi_icon_global_01')

		cmds.select(cl=1)

		# create 5 joints, positioned at each follicle, w/ name of flexi_bind_a01 ... e01
		cmds.joint(p=[-4,0,0],n='flexi_bind_a01')
		cmds.select(cl=1)
		cmds.joint(p=[-2,0,0],n='flexi_bind_b01')
		cmds.select(cl=1)
		cmds.joint(p=[0,0,0],n='flexi_bind_c01')
		cmds.select(cl=1)
		cmds.joint(p=[2,0,0],n='flexi_bind_d01')
		cmds.select(cl=1)
		cmds.joint(p=[4,0,0],n='flexi_bind_e01')
		cmds.select(cl=1)

		# turn on local rotation axis for 5 joints
		sel=cmds.ls('flexi_bind_a01','flexi_bind_b01','flexi_bind_c01','flexi_bind_d01','flexi_bind_e01')
		for obj in sel:
			# mel.eval('ToggleLocalRotationAxes')
			cmds.toggle(sel,localAxis=1)

		cmds.select(cl=1)

		# parent each joint under its respective follicle
		sel_parent=cmds.ls('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')
		sel_child=cmds.ls('flexi_bind_a01','flexi_bind_b01','flexi_bind_c01','flexi_bind_d01','flexi_bind_e01')
		count=-1
		for each in sel_parent:
			count=count+1
			cmds.parent('{0}'.format(sel_child[count]),'{0}'.format(sel_parent[count]))

		cmds.select(cl=1)

		# select bShp surface and create twist deformer
		# nonLinear -type twist -lowBound -1 -highBound 1 -startAngle 0 -endAngle 0;
		cmds.nonLinear('flexi_bShp_surface_01',typ='twist')

		# rotate twist node 90 degrees in z axis
		cmds.xform('twist*Handle',ro=(0,0,90))

		# rename twist to flexi_twist_surface_01
		cmds.rename('twist*Handle','flexi_twist_surface_01')
		# cmds.rename('twist1','flexi_twistAttrs_surface_01')
		twist_list=cmds.ls(exactType='nonLinear')
		refined_list=cmds.select(twist_list[-1])
		cmds.rename(refined_list,'flexi_twistAttrs_surface_01')

		# parent twist under the extra grp
		cmds.parent('flexi_twist_surface_01','flexi_extraNodes_01')

		# connect rotate x of start/end ctrls to start/end angles of twist deformer via direct connections
		# select deformer input node, then the controls
		# connect b01 control to the start angle and vice versa
		cmds.connectAttr('flexi_icon_b01.rotateX','flexi_twistAttrs_surface_01.startAngle')
		cmds.connectAttr('flexi_icon_a01.rotateX','flexi_twistAttrs_surface_01.endAngle')

		# change rotate order for ctrls to XZY
		cmds.xform('flexi_icon_a01','flexi_icon_b01',roo='xzy')

		# select bShp surface and change input order, twist between wire & tweak
		# reorderDeformers "flexi_wireAttrs_surface_01" "flexi_twistAttrs_surface_01" 
						 # "flexiPlane_rig_01|flexi_extraNodes_01|flexi_bShp_surface_01";
		cmds.reorderDeformers('flexi_wireAttrs_surface_01','flexi_twistAttrs_surface_01',
							  'flexiPlane_rig_01|flexi_extraNodes_01|flexi_bShp_surface_01')

		# remove tranforms on flexi plane surface
		attrs=['tx','ty','tz','rx','ry','rz','sx','sy','sz']
		for attr in attrs:
			cmds.setAttr('flexi_surface_01.{0}'.format(attr),l=1,k=0)

		# hide bshp surface, cls grp, twist surface
		obj=cmds.ls('flexi_bShp_surface_01','flexi_cls_01','flexi_twist_surface_01')
		for each in obj:
			cmds.setAttr("{0}.visibility".format(each),0)

		# turn off objecy display - visibility for follicles
		shapeNodes=cmds.listRelatives('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01',shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.visibility".format(shape),0)

		cmds.select(cl=1)

		# create volume attr on global ctrl
		cmds.addAttr('flexi_icon_global_01',longName='VOLUME',attributeType='enum',enumName='--------:',k=1)
		cmds.addAttr('flexi_icon_global_01',longName='Enable',k=1,attributeType='enum',enumName='OFF:ON:')

		cmds.select(cl=1)

		# set up node editor

		# select -r flexi_wire_surface_01 ;
		# mel.eval('arclen -ch 1;')
		cmds.arclen('flexi_wire_surface_01',ch=1)
		cmds.rename('curveInfo1','flexi_curveInfo_01')

		# shadingNode -asUtility multiplyDivide;
		# // multiplyDivide1 // 
		cmds.shadingNode('multiplyDivide',asUtility=1,n='flexi_div_squashStretch_length_01')

		# setAttr "multiplyDivide1.operation" 2;
		cmds.setAttr('flexi_div_squashStretch_length_01.operation',2)

		# connectAttr -f flexi_curveInfo_01.arcLength flexi_div_squashStretch_length_01.input1X;
		cmds.connectAttr('flexi_curveInfo_01.arcLength','flexi_div_squashStretch_length_01.input1X',f=1)

		# setAttr "flexi_div_squashStretch_length_01.input2X" 10;
		cmds.setAttr('flexi_div_squashStretch_length_01.input2X',10)

		# duplicate -rr;setAttr "flexi_div_volume_01.input1X" 1;
		cmds.shadingNode('multiplyDivide',asUtility=1,n='flexi_div_volume_01')
		cmds.setAttr('flexi_div_volume_01.operation',2)
		cmds.setAttr('flexi_div_volume_01.input1X',1)

		# connectAttr -f flexi_div_squashStretch_length_01.outputX flexi_div_volume_01.input2X;
		cmds.connectAttr('flexi_div_squashStretch_length_01.outputX','flexi_div_volume_01.input2X',f=1)

		# shadingNode -asUtility condition;
		# // condition1 // 
		cmds.shadingNode('condition',asUtility=1,n='flexi_con_volume_01')

		# setAttr "flexi_con_volume_01.secondTerm" 1;
		cmds.setAttr('flexi_con_volume_01.secondTerm',1)

		# connectAttr -f flexi_icon_global_01.Enable flexi_con_volume_01.firstTerm;
		cmds.connectAttr('flexi_icon_global_01.Enable','flexi_con_volume_01.firstTerm',f=1)

		# connectAttr -f flexi_div_volume_01.outputX flexi_con_volume_01.colorIfTrueR;
		cmds.connectAttr('flexi_div_volume_01.outputX','flexi_con_volume_01.colorIfTrueR',f=1)

		# connect volume condition out color r to joints a-e scale y & z 
		# connectAttr -f flexi_con_volume_01.outColorR flexi_bind_a01.scaleY;
		# connectAttr -f flexi_con_volume_01.outColorR flexi_bind_a01.scaleZ;
		sel=cmds.ls('flexi_bind_a01','flexi_bind_b01','flexi_bind_c01','flexi_bind_d01','flexi_bind_e01')
		for each in sel:
			cmds.connectAttr('flexi_con_volume_01.outColorR','{0}.scaleY'.format(each),f=1)
			cmds.connectAttr('flexi_con_volume_01.outColorR','{0}.scaleZ'.format(each),f=1)

		# hide wire
		cmds.setAttr('flexi_wire_surface_01.visibility',0)

		cmds.select(cl=1)

		# create indy controls for joints
		indy_1=cmds.circle(normal=[1,0,0],r=0.8,d=3,sections=8,ch=0,n='flexi_indy_icon_a01')
		cmds.xform(t=[-4,0,0])
		cmds.parent('flexi_indy_icon_a01','flexi_flcs_a01')
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
		cmds.parent('flexi_bind_a01','flexi_indy_icon_a01')

		indy_2=cmds.circle(normal=[1,0,0],r=0.8,d=3,sections=8,ch=0,n='flexi_indy_icon_b01')
		cmds.xform(t=[-2,0,0])
		cmds.parent('flexi_indy_icon_b01','flexi_flcs_b01')
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
		cmds.parent('flexi_bind_b01','flexi_indy_icon_b01')

		indy_3=cmds.circle(normal=[1,0,0],r=0.8,d=3,sections=8,ch=0,n='flexi_indy_icon_c01')
		cmds.xform(t=[0,0,0])
		cmds.parent('flexi_indy_icon_c01','flexi_flcs_c01')
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
		cmds.parent('flexi_bind_c01','flexi_indy_icon_c01')

		indy_4=cmds.circle(normal=[1,0,0],r=0.8,d=3,sections=8,ch=0,n='flexi_indy_icon_d01')
		cmds.xform(t=[2,0,0])
		cmds.parent('flexi_indy_icon_d01','flexi_flcs_d01')
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
		cmds.parent('flexi_bind_d01','flexi_indy_icon_d01')

		indy_5=cmds.circle(normal=[1,0,0],r=0.8,d=3,sections=8,ch=0,n='flexi_indy_icon_e01')
		cmds.xform(t=[4,0,0])
		cmds.parent('flexi_indy_icon_e01','flexi_flcs_e01')
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
		cmds.parent('flexi_bind_e01','flexi_indy_icon_e01')

		cmds.select(cl=1)

		# recolor indy controls to magenta
		shapeNodes=cmds.listRelatives(indy_1,indy_2,indy_3,indy_4,indy_5,shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.overrideEnabled".format(shape),1)
			cmds.setAttr("{0}.overrideColor".format(shape),31)

		cmds.select(cl=1)

		# visibility control for indy controls
		cmds.addAttr('flexi_midBend_01',longName='VIS',attributeType='enum',enumName='--------:',k=1)
		cmds.addAttr('flexi_midBend_01',longName='Indy_Ctrls',k=1,attributeType='enum',enumName='OFF:ON:')
		cmds.setAttr('flexi_midBend_01.Indy_Ctrls',1)

		# connect indy ctrl vis to on/off switch
		# flexi_indy_icon_c01Shape.visibility
		sel=cmds.ls('flexi_indy_icon_a01Shape','flexi_indy_icon_b01Shape','flexi_indy_icon_c01Shape',
					'flexi_indy_icon_d01Shape','flexi_indy_icon_e01Shape')
		for each in sel:
			cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','{0}.visibility'.format(each),f=1)

		cmds.select(cl=1)
			
		# select all created objects
		orig_names=cmds.select('flexi_surface_01','flexi_flcs_grp_01','flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01',
					'flexi_flcs_e01','flexi_icon_a01','flexi_icon_b01','flexi_bShp_surface_01','flexi_bShpNode_surface_01',
					'flexi_wire_surface_01','flexi_cl_a01','flexi_cl_b01','flexi_cl_mid01','flexi_wireAttrs_surface_01','flexi_cls_01',
					'flexi_wire_surface_01BaseWire','flexi_icons_01','flexi_midBend_01','flexi_grp_midBend_01','flexiPlane_rig_01',
					'flexi_globalMove_01','flexi_extraNodes_01','flexi_icon_global_01','flexi_bind_a01','flexi_bind_b01','flexi_bind_c01',
					'flexi_bind_d01','flexi_bind_e01','flexi_twist_surface_01','flexi_twistAttrs_surface_01','flexi_curveInfo_01',
					'flexi_div_squashStretch_length_01','flexi_div_volume_01','flexi_con_volume_01','flexi_indy_icon_a01',
					'flexi_indy_icon_b01','flexi_indy_icon_c01','flexi_indy_icon_d01','flexi_indy_icon_e01')

		if cmds.checkBox(self.matCheckBox,q=1,v=1) == True:
			cmds.select('flexi_surface_mat_01','flexi_mid_mat_01',add=1)
		elif cmds.checkBox(self.matCheckBox,q=1,v=1) == False:
			print 'no materials added to rig'

		sel=cmds.ls(sl=1,o=1)
		prefix=cmds.textFieldGrp(self.prefixText,q=1,text=1)
		for each in sel:
			cmds.select(each)
			cmds.rename(each,prefix+'_'+each)

		cmds.select(cl=1)

flexiPlaneInstance=FlexiPlaneUI()
flexiPlaneInstance.gui()




