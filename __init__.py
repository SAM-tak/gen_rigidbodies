import bpy
from bpy.props import *

bl_info = {
    "name": "Generate rigidbodies from bone",
    "author": "SAM-tak, 12funkeys",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "pose > selected bones",
    "description": "Set rigid bodies and constraints easily",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "https://github.com/SAM-tak/gen_rigidbodies/wiki",
    "tracker_url": "https://github.com/SAM-tak/gen_rigidbodies",
    "category": "Rigging"
}

translation_dict = {
    "en_US" : {
        ("*", "Make Rigid Body Tools") : "Make Rigid Body Tools", 
        ("*", "Rigid Body Gen") : "Rigid Body Gen", 
        ("*", "Make Rigid Bodies") : "Make Rigid Bodies", 
        ("*", "Add Passive(on bones)") : "Add Passive(on bones)", 
        ("*", "make rigibodies move on bones") : "make rigibodies move on bones", 
        ("*", "Add Active") : "Add Active",
        ("*", "Add Joints") : "Add Joints",
        ("*", "Add Active & Joints") : "Add Active & Joints"
    },
    "ja_JP" : {
        ("*", "Make Rigid Body Tools") : "選択ボーン", 
        ("*", "Rigid Body Gen") : "剛体ツール", 
        ("*", "Make Rigid Bodies") : "選択ボーン", 
        ("*", "Add Passive(on bones)") : "基礎剛体の作成‐ボーン追従", 
        ("*", "make rigibodies move on bones") : "ボーンに追従する剛体を作成します", 
        ("*", "Add Active") : "基礎剛体の作成‐物理演算",
        ("*", "Add Joints") : "基礎Jointの作成",
        ("*", "Add Active & Joints") : "基礎剛体／連結Jointの作成"
    }
}

shapes = [
    ('MESH', 'Mesh', 'Mesh'),
    ('CONVEX_HULL', 'Convex Hull', 'Convex Hull'),
    ('CONE', 'Cone', 'Cone'),
    ('CYLINDER', 'Cylinder', 'Cylinder'),
    ('CAPSULE', 'Capsule', 'Capsule'),
    ('SPHERE', 'Sphere', 'Sphere'),
    ('BOX', 'Box', 'Box')
]

types = [
    ('MOTOR', 'Motor', 'Motor'),
    ('GENERIC_SPRING', 'Generic Spring', 'Generic Spring'),
    ('GENERIC', 'Generic', 'Generic')
]

### add Tool Panel
class GenRigidBodyToolsPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rigid Body Tools"
    bl_context = "posemode"
    bl_label = "Make Rigid Body Tools"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(CreateRigidBodiesOnBones.bl_idname, text=bpy.app.translations.pgettext("Add Passive(on bones)"), icon='BONE_DATA')
        col.operator(CreateRigidBodiesPhysics.bl_idname, text=bpy.app.translations.pgettext("Add Active"), icon='PHYSICS')
        col.operator(CreateRigidBodiesJoints.bl_idname, text=bpy.app.translations.pgettext("Add Joints"), icon='CONSTRAINT_DATA')
        col.operator(CreateRigidBodiesPhysicsJoints.bl_idname, text=bpy.app.translations.pgettext("Add Active & Joints"), icon='MOD_PHYSICS')


### add Object Physics Menu
class MakeJointsPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Physics"
    bl_context = "object"
    bl_label = "Make Joint Tool"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(CreateRigidBodiesJoints.bl_idname, text=bpy.app.translations.pgettext("Add Joints"), icon='CONSTRAINT_DATA')


### add MainMenu
class MenuRigidBodies(bpy.types.Menu):
    bl_idname = "menu.genrigidbodies"
    bl_label = "Make Rigid Bodies"
    bl_description = "make rigibodies & constraint"

    def draw(self, context):
        layout = self.layout
        layout.operator(CreateRigidBodiesOnBones.bl_idname, icon='BONE_DATA')
        layout.operator(CreateRigidBodiesPhysics.bl_idname, icon='PHYSICS')
        layout.operator(CreateRigidBodiesJoints.bl_idname, icon='CONSTRAINT_DATA')
        layout.operator(CreateRigidBodiesPhysicsJoints.bl_idname, icon='MOD_PHYSICS')


### user prop
class UProp:
    
    rb_shape = EnumProperty(
        name='Shape',
        description='Choose Rigid Body Shape',
        items=shapes,
        #items=bpy.types.RigidBodyObject.collision_shape,
        default='CAPSULE')
        #update=update_shape)

    rc_dim = FloatVectorProperty(
        name = "Dimensions",
        description = "rigid body Dimensions XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5)

    rc_mass = FloatProperty(
        name = "Mass",
        description = "rigid body mass",
        default = 1.0,
        subtype = 'NONE',
        min = 0.001,)

    rc_friction = FloatProperty(
        name = "Friction",
        description = "rigid body friction",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    rc_bounciness = FloatProperty(
        name = "Bounciness",
        description = "rigid body bounciness",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    rc_translation = FloatProperty(
        name = "Translation",
        description = "rigid body translation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    rc_rotation = FloatProperty(
        name = "Rotation",
        description = "rigid body rotation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    jo_type = EnumProperty(
        name='Type',
        description='Choose Contstraint Type',
        items=types,
        default='GENERIC_SPRING')

    jo_size = FloatProperty(
        name = "joint Size",
        description = "joint Size",
        default = 1,
        subtype = 'NONE',
        min = 0,
        max = 5)

    jo_limit_lin_x = BoolProperty(
        name='X Axis',
        description='limit x',
        default=True,
        options={'ANIMATABLE'})

    jo_limit_lin_y = BoolProperty(
        name='Y Axis',
        description='limit y',
        default=True)

    jo_limit_lin_z = BoolProperty(
        name='Z Axis',
        description='limit z',
        default=True)

    jo_limit_lin_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_x_lower",
        default = 0,
        subtype = 'NONE')

    jo_limit_lin_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_y_lower",
        default = 0,
        subtype = 'NONE')

    jo_limit_lin_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_z_lower",
        default = 0,
        subtype = 'NONE')

    jo_limit_lin_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_x_upper",
        default = 0,
        subtype = 'NONE')

    jo_limit_lin_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_y_upper",
        default = 0,
        subtype = 'NONE')

    jo_limit_lin_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_z_upper",
        default = 0,
        subtype = 'NONE')

    jo_limit_ang_x = BoolProperty(
        name='X Angle',
        description='Angle limit x',
        default=True,
        options={'ANIMATABLE'})

    jo_limit_ang_y = BoolProperty(
        name='Y Angle',
        description='Angle limit y',
        default=True)

    jo_limit_ang_z = BoolProperty(
        name='Z Angle',
        description='Angle limit z',
        default=True)

    jo_limit_ang_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_x_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    jo_limit_ang_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_y_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    jo_limit_ang_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_z_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    jo_limit_ang_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_x_upper",
        default = 0.785398,
        subtype = 'ANGLE')

    jo_limit_ang_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_y_upper",
        default = 0.785398,
        subtype = 'ANGLE')

    jo_limit_ang_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_z_upper",
        default = 0.785398,
        subtype = 'ANGLE')


    jo_use_spring_x = BoolProperty(
        name='X',
        description='use spring x',
        default=False)

    jo_use_spring_y = BoolProperty(
        name='Y',
        description='use spring y',
        default=False)

    jo_use_spring_z = BoolProperty(
        name='Z',
        description='use spring z',
        default=False)

    jo_spring_stiffness_x = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the X Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)

    jo_spring_stiffness_y = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Y Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)
        
    jo_spring_stiffness_z = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Z Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)

    jo_spring_damping_x = FloatProperty(
        name = "Damping X",
        description = "Damping on the X Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    jo_spring_damping_y = FloatProperty(
        name = "Damping Y",
        description = "Damping on the Y Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    jo_spring_damping_z = FloatProperty(
        name = "Damping Z",
        description = "Damping on the Z Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)
        
    
    jo_constraint_object = BoolProperty(
        name='Auto Constraint Object',
        description='Constraint Object',
        default=True)

    rc_rootbody_passive = BoolProperty(
        name='Passive',
        description='Rigid Body Type Passive',
        default=True)

    rc_add_pole_rootbody = BoolProperty(
        name='Add Pole Object',
        description='Add Pole Object',
        default=True)

    rc_pole_rootbody_dim = FloatVectorProperty(
        name = "Pole Object Dimension",
        description = "Pole Object Dimension XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5)

    rc_rootbody_animated = BoolProperty(
        name='animated',
        description='Root Rigid Body sets animated',
        default=True)


### Create Rigid Bodies On Bones
class CreateRigidBodiesOnBones(bpy.types.Operator):

    bl_idname = "genrigidbodies.onbones"
    bl_label = "Add Passive(on bones)"
    bl_description = "make rigibodies move on bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    p_rb_rootbody_passive = UProp.rc_rootbody_passive
    p_rb_rootbody_animated = UProp.rc_rootbody_animated


    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)


    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}
                        

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.label(text="Damping:")
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')
        box.prop(self, 'p_rb_rootbody_passive')
        box.prop(self, 'p_rb_rootbody_animated')

    ### 
    def execute(self, context):
                
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)

        if len(bpy.context.selected_pose_bones) == 0:
            return {'FINISHED'}

        for selected_bone in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bone.vector[0]))            
            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bone.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            rc.name = "rb." + ob.name + '.' + selected_bone.name
            rc.show_x_ray = True
            rc.draw_type = 'BOUNDS'
            rc.hide_render = True

            ### Set up Track Constraints
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            dt = bpy.context.object.constraints["Damped Track"]
            dt.target = ob
            dt.subtarget = selected_bone.name
            dt.head_tail = 1
            dt.track_axis = 'TRACK_Z'
            
            ### Apply Tranceform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(dt)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bone.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bone.length * self.init_rc_dimZ * self.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            if self.p_rb_rootbody_passive == True:
                bpy.context.object.rigid_body.type = "PASSIVE"
            else:
                bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.kinematic = self.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation

            ### Child OF
            CoC = rc.constraints.new("CHILD_OF")
            CoC.name = 'Child_Of_' + selected_bone.name
            CoC.target = ob
            CoC.subtarget = selected_bone.name
            
            #without ops way to childof_set_inverse
            sub_target = bpy.data.objects[ob.name].pose.bones[selected_bone.name]
            #self.report({'INFO'}, str(sub_target))
            CoC.inverse_matrix = sub_target.matrix.inverted()   
            rc.update_tag({'OBJECT'})
            bpy.context.scene.update()

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')  
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}

#
class CreateRigidBodiesPhysics(bpy.types.Operator):

    bl_idname = "genrigidbodies.physics"
    bl_label = "Add Active"
    bl_description = "make physics engine on rigibodies"
    bl_options = {'REGISTER', 'UNDO'}

    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30    

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    #p_rb_rootbody_passive = UProp.rc_rootbody_passive
    p_rb_rootbody_animated = UProp.rc_rootbody_animated

    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)
        self.tr_size = 0.33

    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')
        #box.prop(self, 'p_rb_rootbody_passive')
        box.prop(self, 'p_rb_rootbody_animated')

    ### 
    def execute(self, context):
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)

        for selected_bone in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bone.vector[0]))

            ###Create Rigidbody Cube
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bone.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = "rb." + ob.name + '.' + selected_bone.name
            rc.show_x_ray = True
            rc.draw_type = 'BOUNDS'
            rc.hide_render = True

            ### Set Damped Track Constraint
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            con = bpy.context.object.constraints["Damped Track"]
            con.target = ob
            con.subtarget = selected_bone.name
            con.head_tail = 1
            con.track_axis = 'TRACK_Z'
            
            ### Apply Transform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(con)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bone.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bone.length * self.init_rc_dimZ * self.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.kinematic = self.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation

            ## Make Track offset point
            bpy.ops.object.empty_add(type='ARROWS', view_align=False, location=selected_bone.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.parent = rc
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            tr = bpy.context.active_object
            bpy.context.object.name = "tr." + selected_bone.name
            bpy.context.object.empty_draw_size = selected_bone.length * self.tr_size

            ### Set Copy Transform Constraint
            bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
            con = bpy.context.object.constraints["Copy Transforms"]
            con.target = ob
            con.subtarget = selected_bone.name
            
            ### Apply Transform
            bpy.ops.object.visual_transform_apply()
            bpy.context.object.constraints.remove(con)

            ### Set Copy Transform Constraint To Bone
            bpy.context.scene.objects.active = ob
            bpy.ops.object.mode_set(mode='POSE')
            #bpy.ops.pose.armature_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bone.name]
            ab = bpy.context.active_pose_bone

            #self.report({'INFO'}, str(rc.name))
            con = ab.constraints.new("COPY_TRANSFORMS")
            #self.report({'INFO'}, "info:" + str(CoC))
            con.name = 'Copy Transforms Of ' + tr.name
            con.target = tr

            ###bone's use_connect turn to false
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.context.active_bone.use_connect = False
            
        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}
    
#
class CreateRigidBodiesJoints(bpy.types.Operator):

    bl_idname = "genrigidbodies.joints"
    bl_label = "Add Joints"
    bl_description = "add Add Joints on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_joint_size = 0.16

    ###instance UProp.joint
    joint_type = UProp.jo_type
    joint_size = UProp.jo_size
    joint_Axis_limit_x = UProp.jo_limit_lin_x
    joint_Axis_limit_y = UProp.jo_limit_lin_y
    joint_Axis_limit_z = UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower = UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower = UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower = UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper = UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper = UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper = UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x = UProp.jo_limit_ang_x
    joint_Angle_limit_y = UProp.jo_limit_ang_y
    joint_Angle_limit_z = UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower = UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower = UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower = UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper = UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper = UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper = UProp.jo_limit_ang_z_upper
    joint_use_spring_x = UProp.jo_use_spring_x
    joint_use_spring_y = UProp.jo_use_spring_y
    joint_use_spring_z = UProp.jo_use_spring_z
    joint_spring_stiffness_x = UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y = UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z = UProp.jo_spring_stiffness_z
    joint_spring_damping_x = UProp.jo_spring_damping_x
    joint_spring_damping_y = UProp.jo_spring_damping_y
    joint_spring_damping_z = UProp.jo_spring_damping_z

    def __init__(self):

        self.joint_size = 1


    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_size')


        col = box.column(align=True)
        col.label("Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_x', toggle=True)
        sub.prop(self, 'joint_Axis_limit_x_lower')
        sub.prop(self, 'joint_Axis_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_y', toggle=True)
        sub.prop(self, 'joint_Axis_limit_y_lower')
        sub.prop(self, 'joint_Axis_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_z', toggle=True)
        sub.prop(self, 'joint_Axis_limit_z_lower')  
        sub.prop(self, 'joint_Axis_limit_z_upper')

        #col = layout.column(align=True)

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_x', toggle=True)
        sub.prop(self, 'joint_Angle_limit_x_lower')
        sub.prop(self, 'joint_Angle_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_y', toggle=True)
        sub.prop(self, 'joint_Angle_limit_y_lower')
        sub.prop(self, 'joint_Angle_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_z', toggle=True)
        sub.prop(self, 'joint_Angle_limit_z_lower')  
        sub.prop(self, 'joint_Angle_limit_z_upper')


        #col = layout.column(align=True)
        col.label("Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_x', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_x')
        sub.prop(self, 'joint_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_y', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_y')
        sub.prop(self, 'joint_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_z', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_z')  
        sub.prop(self, 'joint_spring_damping_z')


    ### 
    def execute(self, context):
 
        add_RigidBody_World()
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)
        spb = bpy.context.selected_pose_bones

        ### Apply Object transform
        bpy.ops.object.mode_set(mode='OBJECT')

        for selected_bone in spb:
            #self.report({'INFO'}, str(selected_bone.vector[0]))            
            
            ###Create Empty Sphere
            bpy.ops.object.empty_add(type='SPHERE', view_align=False, location=selected_bone.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = "joint." + selected_bone.name
            
            ### Rigid Body Dimensions
            bpy.context.object.empty_draw_size = selected_bone.length * self.init_joint_size * self.joint_size

            ### Set Rigid Body Constraint
            bpy.ops.rigidbody.constraint_add()
            bpy.context.object.rigid_body_constraint.type = self.joint_type
            bpy.context.object.rigid_body_constraint.use_breaking = False
            bpy.context.object.rigid_body_constraint.use_override_solver_iterations = True
            bpy.context.object.rigid_body_constraint.breaking_threshold = 10
            bpy.context.object.rigid_body_constraint.solver_iterations = 10

            bpy.context.object.rigid_body_constraint.use_limit_lin_x = self.joint_Axis_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_lin_y = self.joint_Axis_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_lin_z = self.joint_Axis_limit_z
            bpy.context.object.rigid_body_constraint.limit_lin_x_lower = self.joint_Axis_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_lin_y_lower = self.joint_Axis_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_lin_z_lower = self.joint_Axis_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_lin_x_upper = self.joint_Axis_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_lin_y_upper = self.joint_Axis_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_lin_z_upper = self.joint_Axis_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_limit_ang_x = self.joint_Angle_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_ang_y = self.joint_Angle_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_ang_z = self.joint_Angle_limit_z
            bpy.context.object.rigid_body_constraint.limit_ang_x_lower = self.joint_Angle_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_ang_y_lower = self.joint_Angle_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_ang_z_lower = self.joint_Angle_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_ang_x_upper = self.joint_Angle_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_ang_y_upper = self.joint_Angle_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_ang_z_upper = self.joint_Angle_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_spring_x = self.joint_use_spring_x
            bpy.context.object.rigid_body_constraint.use_spring_y = self.joint_use_spring_y
            bpy.context.object.rigid_body_constraint.use_spring_z = self.joint_use_spring_z
            bpy.context.object.rigid_body_constraint.spring_stiffness_x = self.joint_spring_stiffness_x
            bpy.context.object.rigid_body_constraint.spring_stiffness_y = self.joint_spring_stiffness_y
            bpy.context.object.rigid_body_constraint.spring_stiffness_z = self.joint_spring_stiffness_z
            bpy.context.object.rigid_body_constraint.spring_damping_x = self.joint_spring_damping_x
            bpy.context.object.rigid_body_constraint.spring_damping_y = self.joint_spring_damping_y
            bpy.context.object.rigid_body_constraint.spring_damping_z = self.joint_spring_damping_z

            ###constraint.object
            #bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects["rigidbody.Bone"]
            #bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects["rigidbody.Bone.001"]

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}


class CreateRigidBodiesPhysicsJoints(bpy.types.Operator):

    bl_idname = "genrigidbodies.physicsjoints"
    bl_label = "Add Active & Joints"
    bl_description = "Add Active & Joints"
    bl_options = {'REGISTER', 'UNDO'}

    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30    

    #pole_dict = {}

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    p_rb_add_pole_rootbody = UProp.rc_add_pole_rootbody
    p_rb_pole_rootbody_dim = UProp.rc_pole_rootbody_dim

    init_joint_size = 0.16
    init_polerb_size = 0.33

    ###instance UProp.joint
    joint_type = UProp.jo_type
    joint_size = UProp.jo_size
    joint_Axis_limit_x = UProp.jo_limit_lin_x
    joint_Axis_limit_y = UProp.jo_limit_lin_y
    joint_Axis_limit_z = UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower = UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower = UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower = UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper = UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper = UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper = UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x = UProp.jo_limit_ang_x
    joint_Angle_limit_y = UProp.jo_limit_ang_y
    joint_Angle_limit_z = UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower = UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower = UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower = UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper = UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper = UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper = UProp.jo_limit_ang_z_upper
    joint_use_spring_x = UProp.jo_use_spring_x
    joint_use_spring_y = UProp.jo_use_spring_y
    joint_use_spring_z = UProp.jo_use_spring_z
    joint_spring_stiffness_x = UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y = UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z = UProp.jo_spring_stiffness_z
    joint_spring_damping_x = UProp.jo_spring_damping_x
    joint_spring_damping_y = UProp.jo_spring_damping_y
    joint_spring_damping_z = UProp.jo_spring_damping_z
    joint_constraint_object = UProp.jo_constraint_object


    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)
        self.joint_size = 1
        self.tr_size = 0.33


    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        ###Rigid Body Object
        layout = self.layout

        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')

        #Joint Object
        layout = self.layout

        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_size')
        box.prop(self, 'joint_constraint_object')
        box.prop(self, 'p_rb_add_pole_rootbody')

        col = box.column(align=True)
        col.label("Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_x', toggle=True)
        sub.prop(self, 'joint_Axis_limit_x_lower')
        sub.prop(self, 'joint_Axis_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_y', toggle=True)
        sub.prop(self, 'joint_Axis_limit_y_lower')
        sub.prop(self, 'joint_Axis_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_z', toggle=True)
        sub.prop(self, 'joint_Axis_limit_z_lower')  
        sub.prop(self, 'joint_Axis_limit_z_upper')

        #col = layout.column(align=True)

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_x', toggle=True)
        sub.prop(self, 'joint_Angle_limit_x_lower')
        sub.prop(self, 'joint_Angle_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_y', toggle=True)
        sub.prop(self, 'joint_Angle_limit_y_lower')
        sub.prop(self, 'joint_Angle_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_z', toggle=True)
        sub.prop(self, 'joint_Angle_limit_z_lower')  
        sub.prop(self, 'joint_Angle_limit_z_upper')


        #col = layout.column(align=True)
        col.label("Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_x', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_x')
        sub.prop(self, 'joint_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_y', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_y')
        sub.prop(self, 'joint_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_z', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_z')  
        sub.prop(self, 'joint_spring_damping_z')

    # 
    def execute(self, context):

        add_RigidBody_World()        
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        self.report({'INFO'}, "ob:" + str(ob))

        spb = bpy.context.selected_pose_bones

        bpy.ops.object.mode_set(mode='OBJECT')
        
        parent_bones_ob = ""
        
        pole_dict = {}
        
        wm = bpy.context.window_manager 

        tot = len(spb)
        wm.progress_begin(0, tot)
        i = 0

        for selected_bone in spb:
            #self.report({'INFO'}, str(selected_bone.vector[0]))

            i += 1
            wm.progress_update(i)

            ###Joint Session
            ###Create Joint Empty
            bpy.ops.object.empty_add(type='SPHERE', view_align=False, location=selected_bone.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            jc = bpy.context.active_object
            jc.name = "joint." + ob.name + "." + selected_bone.name
            
            ### Set Joint radius
            bpy.context.object.empty_draw_size = selected_bone.length * self.init_joint_size * self.joint_size
            
            ### Set Rigid Body
            bpy.ops.rigidbody.constraint_add()
            jc.rigid_body_constraint.type = self.joint_type
            jc.rigid_body_constraint.use_breaking = False
            jc.rigid_body_constraint.use_override_solver_iterations = True
            jc.rigid_body_constraint.breaking_threshold = 10
            jc.rigid_body_constraint.solver_iterations = 10

            jc.rigid_body_constraint.use_limit_lin_x = self.joint_Axis_limit_x
            jc.rigid_body_constraint.use_limit_lin_y = self.joint_Axis_limit_y
            jc.rigid_body_constraint.use_limit_lin_z = self.joint_Axis_limit_z
            jc.rigid_body_constraint.limit_lin_x_lower = self.joint_Axis_limit_x_lower
            jc.rigid_body_constraint.limit_lin_y_lower = self.joint_Axis_limit_y_lower
            jc.rigid_body_constraint.limit_lin_z_lower = self.joint_Axis_limit_z_lower
            jc.rigid_body_constraint.limit_lin_x_upper = self.joint_Axis_limit_x_upper
            jc.rigid_body_constraint.limit_lin_y_upper = self.joint_Axis_limit_y_upper
            jc.rigid_body_constraint.limit_lin_z_upper = self.joint_Axis_limit_z_upper

            jc.rigid_body_constraint.use_limit_ang_x = self.joint_Angle_limit_x
            jc.rigid_body_constraint.use_limit_ang_y = self.joint_Angle_limit_y
            jc.rigid_body_constraint.use_limit_ang_z = self.joint_Angle_limit_z
            jc.rigid_body_constraint.limit_ang_x_lower = self.joint_Angle_limit_x_lower
            jc.rigid_body_constraint.limit_ang_y_lower = self.joint_Angle_limit_y_lower
            jc.rigid_body_constraint.limit_ang_z_lower = self.joint_Angle_limit_z_lower
            jc.rigid_body_constraint.limit_ang_x_upper = self.joint_Angle_limit_x_upper
            jc.rigid_body_constraint.limit_ang_y_upper = self.joint_Angle_limit_y_upper
            jc.rigid_body_constraint.limit_ang_z_upper = self.joint_Angle_limit_z_upper

            jc.rigid_body_constraint.use_spring_x = self.joint_use_spring_x
            jc.rigid_body_constraint.use_spring_y = self.joint_use_spring_y
            jc.rigid_body_constraint.use_spring_z = self.joint_use_spring_z
            jc.rigid_body_constraint.spring_stiffness_x = self.joint_spring_stiffness_x
            jc.rigid_body_constraint.spring_stiffness_y = self.joint_spring_stiffness_y
            jc.rigid_body_constraint.spring_stiffness_z = self.joint_spring_stiffness_z
            jc.rigid_body_constraint.spring_damping_x = self.joint_spring_damping_x
            jc.rigid_body_constraint.spring_damping_y = self.joint_spring_damping_y
            jc.rigid_body_constraint.spring_damping_z = self.joint_spring_damping_z

            #self.report({'INFO'}, "selected_bone.parent:" + str(selected_bone.parent))
            if selected_bone.parent is not None and selected_bone.parent not in spb and selected_bone.parent not in pole_dict and self.p_rb_add_pole_rootbody == True:

                ###Create Rigidbody Cube
                bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bone.parent.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
                bpy.context.object.layers[acrive_layer] = True
                bpy.context.object.layers[19] = False
                rc2 = bpy.context.active_object
                rc2.name = "rb.pole." + ob.name + "." + selected_bone.parent.name
                rc2.show_x_ray = True
                rc2.hide_render = True
                rc2.draw_type = 'BOUNDS'
                
                ### Rigid Body Dimensions
                bpy.context.object.dimensions = [
                    selected_bone.parent.length * self.init_polerb_size * self.p_rb_pole_rootbody_dim[0],
                    selected_bone.parent.length * self.init_polerb_size * self.p_rb_pole_rootbody_dim[1],
                    selected_bone.parent.length * self.init_polerb_size * self.p_rb_pole_rootbody_dim[2]
                ]
                
                ### Scale Apply
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

                ### Set Rigid Body
                bpy.ops.rigidbody.object_add()

                rc2.rigid_body.type = "PASSIVE"
                rc2.rigid_body.collision_shape = "BOX"
                #rc2.rigid_body.collision_shape = self.p_rb_shape
                #rc2.rigid_body.mass = self.p_rb_mass
                #rc2.rigid_body.friction = self.p_rb_friction
                #rc2.rigid_body.restitution = self.p_rb_bounciness
                #rc2.rigid_body.linear_damping = self.p_rb_translation
                #rc2.rigid_body.angular_damping = self.p_rb_rotation
                rc2.rigid_body.kinematic = True

                ### Child OF
                CoC2 = rc2.constraints.new("CHILD_OF")
                CoC2.name = 'Child_Of_' + selected_bone.parent.name
                CoC2.target = ob
                CoC2.subtarget = selected_bone.parent.name
                
                #without ops way to childof_set_inverse
                sub_target = bpy.data.objects[ob.name].pose.bones[selected_bone.parent.name]
                #self.report({'INFO'}, str(sub_target))
                CoC2.inverse_matrix = sub_target.matrix.inverted()   
                rc2.update_tag({'OBJECT'})
                bpy.context.scene.update()

            ###constraint.object1
            
            if selected_bone.parent is not None and selected_bone.parent not in spb and self.p_rb_add_pole_rootbody == True:
                    
                if selected_bone.parent not in pole_dict:
                    pole_dict[selected_bone.parent] = rc2 
                    self.report({'INFO'}, "pole_dict:" + str(pole_dict)) 
                    jc.rigid_body_constraint.object1 = rc2
                    parent_bones_ob = "rb." + ob.name + "." + selected_bone.name
                else:
                    jc.rigid_body_constraint.object1 = pole_dict[selected_bone.parent]
                    parent_bones_ob = "rb." + ob.name + "." + selected_bone.name

            else:
                if parent_bones_ob != "":
                    jc.rigid_body_constraint.object1 = bpy.data.objects[parent_bones_ob]

                parent_bones_ob = "rb." + ob.name + "." + selected_bone.name

            #self.report({'INFO'}, "recursive:" + str(selected_bone.children_recursive)) 
            #self.report({'INFO'}, "parent_bones_ob:" + str(parent_bones_ob)) 

            ###Rigid Body Session
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bone.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = parent_bones_ob
            rc.show_x_ray = True
            rc.draw_type = 'BOUNDS'
            rc.hide_render = True

            ###constraint.object2
            #self.report({'INFO'}, "parent_bones_ob:" + str(parent_bones_ob))
            if parent_bones_ob != "":            
                jc.rigid_body_constraint.object2 = bpy.data.objects[parent_bones_ob]

            if len(selected_bone.children_recursive) == 0:
                parent_bones_ob = ""

            ###Material set
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            con = bpy.context.object.constraints["Damped Track"]
            con.target = ob
            con.subtarget = selected_bone.name
            con.head_tail = 1
            con.track_axis = 'TRACK_Z'
            
            ### Apply Tranceform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(con)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bone.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bone.length * self.init_rc_dimZ * self.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"
            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation

            ## Make Track offset point
            bpy.ops.object.empty_add(type='ARROWS', view_align=False, location=selected_bone.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.parent = rc
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            tr = bpy.context.active_object
            bpy.context.object.name = "tr." + selected_bone.name
            bpy.context.object.empty_draw_size = selected_bone.length * self.tr_size

            ### Set Copy Transform Constraint
            bpy.ops.object.constraint_add(type='COPY_TRANSFORMS')
            con = bpy.context.object.constraints["Copy Transforms"]
            con.target = ob
            con.subtarget = selected_bone.name
            
            ### Apply Transform
            bpy.ops.object.visual_transform_apply()
            bpy.context.object.constraints.remove(con)

            ### Set Copy Transform Constraint To Bone
            bpy.context.scene.objects.active = ob
            bpy.ops.object.mode_set(mode='POSE')
            #bpy.ops.pose.armature_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bone.name]
            ab = bpy.context.active_pose_bone

            #self.report({'INFO'}, str(rc.name))
            con = ab.constraints.new("COPY_TRANSFORMS")
            #self.report({'INFO'}, "info:" + str(CoC))
            con.name = 'Copy Transforms Of ' + tr.name
            con.target = tr

            ###bone's use_connect turn to false
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.context.active_bone.use_connect = False

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.update()

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')

        wm.progress_end()

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

# add menu
def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(MenuRigidBodies.bl_idname, icon='MESH_ICOSPHERE')

def add_RigidBody_World():
        scene = bpy.context.scene
        if scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()

# addon enable
def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_pose.append(menu_fn)
    bpy.app.translations.register(__name__, translation_dict)


# addon disable
def unregister():
    bpy.app.translations.unregister(__name__)
    bpy.types.VIEW3D_MT_pose.remove(menu_fn)
    bpy.utils.unregister_module(__name__)


# main
if __name__ == "__main__":
    register()
