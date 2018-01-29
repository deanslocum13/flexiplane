'''
Dean Slocum
deanslocum@gmail.com
flexi_plane.py

Description:
	
	v1.2

	Creats the Flexi-plane rigging component for a limb.

How to Run:

import flexi_plane
reload(flexi_plane)
flexi_plane.gui()

'''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

win = 'Flexi Plane'
print 'Flexi Plane Activated'

w = 90
h = 180
h2 = 8
b1 = [0,.5,0]
b2 = [0,.5,.5]

def gui():	

	global prefix_input,mat_check

	if(cmds.window(win,ex=1)):
		cmds.deleteUI(win)
	if (cmds.windowPref(win,ex=1)):
		cmds.windowPref(win,r=1)

	cmds.window(win,s=1,vis=1,w=w,h=h)
	
	cmds.rowColumnLayout()

	cmds.frameLayout(l=' Add a Prefix & press BUILD',bgc=b1)

	cmds.rowColumnLayout(co=[1,'both',16])
	cmds.rowColumnLayout(nc=2)
	cmds.text(' ')
	cmds.text(' ')

	cmds.text(l='Prefix: ')
	prefix_input=pm.textField(w=100,pht='lt_arm, etc.')

	cmds.text(' ')
	cmds.text(' ')
	cmds.text(' ')

	cmds.button(l='BUILD',c=flexi_plane,bgc=b2)

	cmds.rowColumnLayout(nc=1)
	cmds.setParent('..')
	cmds.setParent('..')

	cmds.text(' ')

	mat_check=pm.checkBox(l='Build Materials', v=1)

	cmds.text(' ')

	cmds.showWindow()

def flexi_plane(*args):

	# create nurbs plane w/ x attrs
	# nurbsPlane -p 0 0 0 -ax 0 1 0 -w 5 -lr 0.2 -d 3 -u 5 -v 1 -ch 1;
	nurbs_plane=cmds.nurbsPlane(ax=(0,1,0),w=10,lr=0.2,d=3,u=5,v=1,ch=0,n='flexi_surface_01')
	cmds.setAttr('flexi_surface_01Shape.castsShadows',0)
	cmds.setAttr('flexi_surface_01Shape.receiveShadows',0)
	cmds.setAttr('flexi_surface_01Shape.motionBlur',0)
	cmds.setAttr('flexi_surface_01Shape.primaryVisibility',0)
	cmds.setAttr('flexi_surface_01Shape.smoothShading',0)
	cmds.setAttr('flexi_surface_01Shape.visibleInReflections',0)
	cmds.setAttr('flexi_surface_01Shape.visibleInRefractions',0)

	# create new material
	# cmds.shadingNode('lambert',asShader=1,n='flexi_surface_mat_01')
	# make material light blue and lower transparency
	# asign material to nurbs plane
	if mat_check.getValue() == True:
		flexi_mat=cmds.shadingNode('lambert',asShader=1,n='flexi_surface_mat_01')
		cmds.setAttr(flexi_mat+'.color',0.0,1.0,1.0,type='double3')
		cmds.setAttr(flexi_mat+'.transparency',0.75,0.75,0.75,type='double3')
		cmds.select(nurbs_plane)
		cmds.hyperShade(assign=flexi_mat)
	elif mat_check.getValue() == False:
		print 'no surface material created'

	# create nHair on plane w/ default settings w/ u-5, v-1
	# createHair 5 1 10 0 0 0 0 5 0 1 1 1;
	cmds.select(nurbs_plane)
	mel.eval('createHair 5 1 10 0 0 0 0 5 0 1 1 1;')

	# select and delete hair objects, hairSystem, nucleus
	cmds.delete('pfxHair*')
	cmds.delete('nucleus*')

	cmds.select('hairSystem*')
	cmds.select('hairSystem*Follicles',d=1)
	cmds.delete()

	# rename follicle grp to flexi_flcs_grp
	cmds.rename('hairSystem*Follicles','flexi_flcs_grp_01')

	# rename follicles to flexi_flcs_a01-e01
	cmds.rename('flexi_surface_*Follicle1050','flexi_flcs_a01')
	cmds.rename('flexi_surface_*Follicle3050','flexi_flcs_b01')
	cmds.rename('flexi_surface_*Follicle5050','flexi_flcs_c01')
	cmds.rename('flexi_surface_*Follicle6950','flexi_flcs_d01')
	cmds.rename('flexi_surface_*Follicle8950','flexi_flcs_e01')

	# create square CV , CP , end of plane, name flexi_icon_a01, change color to yellow, repeat for other end
	# curve -d 1 -p -6 0 -1 -p -6 0 1 -p -4 0 1 -p -4 0 -1 -p -6 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 ;
	cmds.curve(d=1, p=[(-5.6,0,-0.6),(-4.4,0,-0.6),(-4.4,0,0.6),(-5.6,0,0.6),(-5.6,0,-0.6)], k=[0,1,2,3,4], n='flexi_icon_a01')
	cmds.xform(cp=1)

	sel=cmds.ls(sl=1)
	for obj in sel:
		shapeNodes=cmds.listRelatives(obj,shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.overrideEnabled".format(shape), 1)
			cmds.setAttr("{0}.overrideColor".format(shape), 17)

	cmds.select(cl=1)

	cmds.curve(d=1, p=[(4.4,0,-0.6),(5.6,0,-0.6),(5.6,0,0.6),(4.4,0,0.6),(4.4,0,-0.6)], k=[0,1,2,3,4], n='flexi_icon_b01')
	cmds.xform(cp=1)

	sel=cmds.ls(sl=1)
	for obj in sel:
		shapeNodes=cmds.listRelatives(obj,shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.overrideEnabled".format(shape), 1)
			cmds.setAttr("{0}.overrideColor".format(shape), 17)

	cmds.select(cl=1)

	# duplicate plane, translate Z axis -5, reanme to flexi_bShp_surface_01
	bShp_surface=cmds.duplicate(nurbs_plane,n='flexi_bShp_surface_01')
	cmds.select(bShp_surface)
	cmds.xform(t=[0,0,-5])

	# create blendshape w/ default settings, name flexi_bShpNode_surface_01
	cmds.blendShape(bShp_surface,nurbs_plane,n='flexi_bShpNode_surface_01')

	# output settings to always on = 1
	cmds.setAttr('flexi_bShpNode_surface_01.flexi_bShp_surface_01',1)

	# rename tweak node to flexi_bShp_surface_tweak_01
	# cmds.rename('tweak1','flexi_bShp_surface_tweak_01')

	# CV w/ 3 pts on dup plane, degree-2, rename to flexi_wire_surface_01
	wire_surface=cmds.curve(d=2,p=[(-5,0,-5),(0,0,-5),(5,0,-5)],k=[0,0,1,1],n='flexi_wire_surface_01')

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
	cmds.wire('flexi_bShp_surface_01',gw=0,dds=(0,20),en=1.0,ce=0.0,li=0.0,w=wire_surface,n='flexi_wireAttrs_surface_01')
	cmds.select(cl=1)

	# rename cleanup
	# cmds.rename('wire1','flexi_wireAttrs_surface_01')
	# cmds.rename('tweak1','flexi_cl_Cluster_tweak_01')
	# cmds.rename('tweak2','flexi_wire_surface_tweak_01')

	# select start control, start cluster, open conection editor, connect translate to translate
	# connectAttr -f flexi_icon_a01.translate flexi_cl_a01.translate;
	cmds.connectAttr('flexi_icon_a01.translate','flexi_cl_a01.translate',f=1)

	# repeat for other end
	cmds.connectAttr('flexi_icon_b01.translate','flexi_cl_b01.translate',f=1)

	# group the 3 clusters together, name it flexi_cls_01
	cmds.group(clus_1,clus_2,clus_3,n='flexi_cls_01')

	# lock and hide transform channels of group
	cmds.setAttr('flexi_cls_01.tx',l=1, k=0)
	cmds.setAttr('flexi_cls_01.ty',l=1, k=0)
	cmds.setAttr('flexi_cls_01.tz',l=1, k=0)

	cmds.setAttr('flexi_cls_01.rx',l=1, k=0)
	cmds.setAttr('flexi_cls_01.ry',l=1, k=0)
	cmds.setAttr('flexi_cls_01.rz',l=1, k=0)

	cmds.setAttr('flexi_cls_01.sx',l=1, k=0)
	cmds.setAttr('flexi_cls_01.sy',l=1, k=0)
	cmds.setAttr('flexi_cls_01.sz',l=1, k=0)

	# create group for 2 current controls, name it flexi_icons_01
	cmds.group('flexi_icon_a01','flexi_icon_b01',n='flexi_icons_01')

	# lock and hide transform channels of group
	cmds.setAttr('flexi_icons_01.tx',l=1, k=0)
	cmds.setAttr('flexi_icons_01.ty',l=1, k=0)
	cmds.setAttr('flexi_icons_01.tz',l=1, k=0)

	cmds.setAttr('flexi_icons_01.rx',l=1, k=0)
	cmds.setAttr('flexi_icons_01.ry',l=1, k=0)
	cmds.setAttr('flexi_icons_01.rz',l=1, k=0)

	cmds.setAttr('flexi_icons_01.sx',l=1, k=0)
	cmds.setAttr('flexi_icons_01.sy',l=1, k=0)
	cmds.setAttr('flexi_icons_01.sz',l=1, k=0)

	# create center control, name it flexi_midBend_01
	# sphere -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -nsp 4 -ch 1;
	mid_ctrl=cmds.sphere(p=[0,0,0],ax=[0,1,0],ssw=0,esw=360,ch=0,r=0.3,d=3,ut=0,tol=0.8,nsp=4,n='flexi_midBend_01')
	cmds.setAttr('flexi_midBend_01Shape.castsShadows',0)
	cmds.setAttr('flexi_midBend_01Shape.receiveShadows',0)
	cmds.setAttr('flexi_midBend_01Shape.motionBlur',0)
	cmds.setAttr('flexi_midBend_01Shape.primaryVisibility',0)
	cmds.setAttr('flexi_midBend_01Shape.smoothShading',0)
	cmds.setAttr('flexi_midBend_01Shape.visibleInReflections',0)
	cmds.setAttr('flexi_midBend_01Shape.visibleInRefractions',0)

	# new material, surface shader, yellow color, name flexi_ss_midBend_01
	if mat_check.getValue() == True:
		flexi_mat_2=cmds.shadingNode('surfaceShader',asShader=1,n='flexi_mid_mat_01')
		cmds.setAttr(flexi_mat_2+'.outColor',1.0,1.0,0.0,type='double3')
		cmds.select(mid_ctrl)
		cmds.hyperShade(assign=flexi_mat_2)
	elif mat_check.getValue() == False:
		print 'no mid ctrl material created'

	# uncheck render stats of all expect doublesided for control, 2 nurbs planes

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
	cmds.setAttr('flexiPlane_rig_01.tx',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.ty',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.tz',l=1, k=0)

	cmds.setAttr('flexiPlane_rig_01.rx',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.ry',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.rz',l=1, k=0)

	cmds.setAttr('flexiPlane_rig_01.sx',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.sy',l=1, k=0)
	cmds.setAttr('flexiPlane_rig_01.sz',l=1, k=0)

	# group flexi surface and icons grp, name flexi_globalMove_01
	cmds.group('flexi_surface_01','flexi_icons_01',n='flexi_globalMove_01')

	# group all but global, name flexi_extraNodes_01
	cmds.group('flexi_flcs_grp_01','flexi_bShp_surface_01','flexi_wire_surface_01','flexi_wire_surface_01BaseWire',
				'flexi_cls_01',n='flexi_extraNodes_01')
	cmds.select(cl=1)

	# scale constrain each follicle to the global move grp
	cmds.scaleConstraint('flexi_globalMove_01','flexi_flcs_a01',mo=0)
	cmds.scaleConstraint('flexi_globalMove_01','flexi_flcs_b01',mo=0)
	cmds.scaleConstraint('flexi_globalMove_01','flexi_flcs_c01',mo=0)
	cmds.scaleConstraint('flexi_globalMove_01','flexi_flcs_d01',mo=0)
	cmds.scaleConstraint('flexi_globalMove_01','flexi_flcs_e01',mo=0)

	# build global control
	cmds.curve(d=1, p=[(0,0,-1.667542),(-0.332458,0,-2),(0.332458,0,-2),(0,0,-1.667542),(0,0,1.667542),(0.332458,0,2),
						(-0.332458,0,2),(0,0,1.667542)], k=[0,1,2,3,4,5,6,7], n='flexi_icon_global_01')
	cmds.xform(cp=1)

	sel=cmds.ls(sl=1)
	for obj in sel:
		shapeNodes=cmds.listRelatives(obj,shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.overrideEnabled".format(shape), 1)
			cmds.setAttr("{0}.overrideColor".format(shape), 17)

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
	cmds.select('flexi_bind_a01','flexi_bind_b01','flexi_bind_c01','flexi_bind_d01','flexi_bind_e01')

	sel=cmds.ls(sl=1)
	for obj in sel:
		mel.eval('ToggleLocalRotationAxes')

	cmds.select(cl=1)

	# parent each joint under its respective follicle
	cmds.parent('flexi_bind_a01','flexi_flcs_a01')
	cmds.parent('flexi_bind_b01','flexi_flcs_b01')
	cmds.parent('flexi_bind_c01','flexi_flcs_c01')
	cmds.parent('flexi_bind_d01','flexi_flcs_d01')
	cmds.parent('flexi_bind_e01','flexi_flcs_e01')

	cmds.select(cl=1)

	# select bShp surface and create twist deformer
	# nonLinear -type twist -lowBound -1 -highBound 1 -startAngle 0 -endAngle 0;
	cmds.nonLinear('flexi_bShp_surface_01',typ='twist')

	# rotate twist node 90 degrees in z axis
	cmds.xform('twist*Handle',ro=(0,0,90))

	# rename twist to flexi_twist_surface_01
	cmds.rename('twist*Handle','flexi_twist_surface_01')
	# cmds.rename('twist1','flexi_twistAttrs_surface_01')
	twist_list=cmds.ls(et='nonLinear')
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
	# reorderDeformers "flexi_wireAttrs_surface_01" "flexi_twistAttrs_surface_01" "flexiPlane_rig_01|flexi_extraNodes_01|flexi_bShp_surface_01";
	cmds.reorderDeformers('flexi_wireAttrs_surface_01','flexi_twistAttrs_surface_01','flexiPlane_rig_01|flexi_extraNodes_01|flexi_bShp_surface_01')

	# remove tranforms on flexi plane surface
	cmds.setAttr('flexi_surface_01.tx',l=1, k=0)
	cmds.setAttr('flexi_surface_01.ty',l=1, k=0)
	cmds.setAttr('flexi_surface_01.tz',l=1, k=0)

	cmds.setAttr('flexi_surface_01.rx',l=1, k=0)
	cmds.setAttr('flexi_surface_01.ry',l=1, k=0)
	cmds.setAttr('flexi_surface_01.rz',l=1, k=0)

	cmds.setAttr('flexi_surface_01.sx',l=1, k=0)
	cmds.setAttr('flexi_surface_01.sy',l=1, k=0)
	cmds.setAttr('flexi_surface_01.sz',l=1, k=0)

	# hide bshp surface, cls grp, twist surface
	cmds.setAttr('flexi_bShp_surface_01.visibility',0)
	cmds.setAttr('flexi_cls_01.visibility',0)
	cmds.setAttr('flexi_twist_surface_01.visibility',0)

	# turn off objecy display - visibility for follicles
	cmds.select('flexi_flcs_a01','flexi_flcs_b01','flexi_flcs_c01','flexi_flcs_d01','flexi_flcs_e01')

	sel=cmds.ls(sl=1)
	for obj in sel:
		shapeNodes=cmds.listRelatives(obj,shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.visibility".format(shape), 0)

	cmds.select(cl=1)

	# create volume attr on global ctrl
	cmds.select('flexi_icon_global_01')

	cmds.addAttr('flexi_icon_global_01',ln='VOLUME', at='enum', en='--------:', k=1)
	cmds.addAttr('flexi_icon_global_01',ln='Enable', k=1, at='enum', en='OFF:ON:')

	cmds.select(cl=1)

	# set up node editor

	# select -r flexi_wire_surface_01 ;
	# arclen -ch 1;
	cmds.select('flexi_wire_surface_01')
	mel.eval('arclen -ch 1;')
	cmds.rename('curveInfo1','flexi_curveInfo_01')

	# shadingNode -asUtility multiplyDivide;
	# // multiplyDivide1 // 
	cmds.shadingNode('multiplyDivide',au=1,n='flexi_div_squashStretch_length_01')

	# setAttr "multiplyDivide1.operation" 2;
	cmds.setAttr('flexi_div_squashStretch_length_01.operation',2)

	# connectAttr -f flexi_curveInfo_01.arcLength flexi_div_squashStretch_length_01.input1X;
	cmds.connectAttr('flexi_curveInfo_01.arcLength','flexi_div_squashStretch_length_01.input1X',f=1)

	# setAttr "flexi_div_squashStretch_length_01.input2X" 10;
	cmds.setAttr('flexi_div_squashStretch_length_01.input2X',10)

	# duplicate -rr;setAttr "flexi_div_volume_01.input1X" 1;
	cmds.shadingNode('multiplyDivide',au=1,n='flexi_div_volume_01')
	cmds.setAttr('flexi_div_volume_01.operation',2)
	cmds.setAttr('flexi_div_volume_01.input1X',1)

	# connectAttr -f flexi_div_squashStretch_length_01.outputX flexi_div_volume_01.input2X;
	cmds.connectAttr('flexi_div_squashStretch_length_01.outputX','flexi_div_volume_01.input2X',f=1)

	# shadingNode -asUtility condition;
	# // condition1 // 
	cmds.shadingNode('condition',au=1,n='flexi_con_volume_01')

	# setAttr "flexi_con_volume_01.secondTerm" 1;
	cmds.setAttr('flexi_con_volume_01.secondTerm',1)

	# connectAttr -f flexi_icon_global_01.Enable flexi_con_volume_01.firstTerm;
	cmds.connectAttr('flexi_icon_global_01.Enable','flexi_con_volume_01.firstTerm',f=1)

	# connectAttr -f flexi_div_volume_01.outputX flexi_con_volume_01.colorIfTrueR;
	cmds.connectAttr('flexi_div_volume_01.outputX','flexi_con_volume_01.colorIfTrueR',f=1)

	# connect volume condition out color r to joints a-e scale y & z 
	# connectAttr -f flexi_con_volume_01.outColorR flexi_bind_a01.scaleY;
	# connectAttr -f flexi_con_volume_01.outColorR flexi_bind_a01.scaleZ;
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_a01.scaleY',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_a01.scaleZ',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_b01.scaleY',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_b01.scaleZ',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_c01.scaleY',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_c01.scaleZ',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_d01.scaleY',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_d01.scaleZ',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_e01.scaleY',f=1)
	cmds.connectAttr('flexi_con_volume_01.outColorR','flexi_bind_e01.scaleZ',f=1)

	# hide wire
	cmds.setAttr('flexi_wire_surface_01.visibility',0)

	cmds.select(cl=1)

	# create indy controls for joints
	cmds.circle(nr=[1,0,0],r=0.8,d=3,s=8,ch=0,n='flexi_indy_icon_a01')
	cmds.xform(t=[-4,0,0])
	cmds.parent('flexi_indy_icon_a01','flexi_flcs_a01')
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	cmds.parent('flexi_bind_a01','flexi_indy_icon_a01')

	cmds.circle(nr=[1,0,0],r=0.8,d=3,s=8,ch=0,n='flexi_indy_icon_b01')
	cmds.xform(t=[-2,0,0])
	cmds.parent('flexi_indy_icon_b01','flexi_flcs_b01')
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	cmds.parent('flexi_bind_b01','flexi_indy_icon_b01')

	cmds.circle(nr=[1,0,0],r=0.8,d=3,s=8,ch=0,n='flexi_indy_icon_c01')
	cmds.xform(t=[0,0,0])
	cmds.parent('flexi_indy_icon_c01','flexi_flcs_c01')
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	cmds.parent('flexi_bind_c01','flexi_indy_icon_c01')

	cmds.circle(nr=[1,0,0],r=0.8,d=3,s=8,ch=0,n='flexi_indy_icon_d01')
	cmds.xform(t=[2,0,0])
	cmds.parent('flexi_indy_icon_d01','flexi_flcs_d01')
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	cmds.parent('flexi_bind_d01','flexi_indy_icon_d01')

	cmds.circle(nr=[1,0,0],r=0.8,d=3,s=8,ch=0,n='flexi_indy_icon_e01')
	cmds.xform(t=[4,0,0])
	cmds.parent('flexi_indy_icon_e01','flexi_flcs_e01')
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	cmds.parent('flexi_bind_e01','flexi_indy_icon_e01')

	cmds.select(cl=1)

	# recolor indy controls to magenta
	cmds.select('flexi_indy_icon_a01','flexi_indy_icon_b01','flexi_indy_icon_c01','flexi_indy_icon_d01','flexi_indy_icon_e01')

	sel=cmds.ls(sl=1)
	for obj in sel:
		shapeNodes=cmds.listRelatives(obj, shapes=1)
		for shape in shapeNodes:
			cmds.setAttr("{0}.overrideEnabled".format(shape), 1)
			cmds.setAttr("{0}.overrideColor".format(shape), 31)

	cmds.select(cl=1)

	# visibility control for indy controls
	cmds.select('flexi_midBend_01')

	cmds.addAttr('flexi_midBend_01',ln='VIS', at='enum', en='--------:', k=1)
	cmds.addAttr('flexi_midBend_01',ln='Indy_Ctrls', k=1, at='enum', en='OFF:ON:')
	cmds.setAttr('flexi_midBend_01.Indy_Ctrls',1)

	# connect indy ctrl vis to on/off switch
	# flexi_indy_icon_c01Shape.visibility
	cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','flexi_indy_icon_a01Shape.visibility',f=1)
	cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','flexi_indy_icon_b01Shape.visibility',f=1)
	cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','flexi_indy_icon_c01Shape.visibility',f=1)
	cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','flexi_indy_icon_d01Shape.visibility',f=1)
	cmds.connectAttr('flexi_midBend_01.Indy_Ctrls','flexi_indy_icon_e01Shape.visibility',f=1)

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

	if mat_check.getValue() == True:
		cmds.select('flexi_surface_mat_01','flexi_mid_mat_01',add=1)
	elif mat_check.getValue() == False:
		print 'no materials added to rig'

	sel=cmds.ls(sl=1,o=1)
	prefix=prefix_input.getText()
	for each in sel:
		cmds.select(each)
		cmds.rename(each,prefix+'_'+each)

	cmds.select(cl=1)







