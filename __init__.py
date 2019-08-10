import bpy
from bpy.props import *

bl_info = {
    "name": "Generate rigidbodies from bone",
    "author": "SAM-tak, 12funkeys",
    "version": (1, 0),
    "blender": (2, 80, 0),
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
class AddPassivePanel(bpy.types.Panel):
    bl_idname = "GENRIGIDBODIES_PT_AddPassive"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gen Rigidbody'
    bl_context = "posemode"
    bl_label = "Add Passive(on bones)"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        context.window_manager.genrigidbodies.addpassive.draw(col)
        op = col.operator(AddPassiveOperator.bl_idname, text=bpy.app.translations.pgettext("Execute"), icon='BONE_DATA')


class AddActivePanel(bpy.types.Panel):
    bl_idname = "GENRIGIDBODIES_PT_AddActive"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gen Rigidbody'
    bl_context = "posemode"
    bl_label = "Add Active"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        context.window_manager.genrigidbodies.addactive.draw(col)
        col.operator(AddActiveOperator.bl_idname, text=bpy.app.translations.pgettext("Execute"), icon='PHYSICS')


class AddJointPanel(bpy.types.Panel):
    bl_idname = "GENRIGIDBODIES_PT_AddJoint"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gen Rigidbody'
    bl_context = "posemode"
    bl_label = "Add Joint"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        context.window_manager.genrigidbodies.addjoint.draw(col)
        col.operator(AddJointOperator.bl_idname, text=bpy.app.translations.pgettext("Execute"), icon='CONSTRAINT')


class AddActiveNJointPanel(bpy.types.Panel):
    bl_idname = "GENRIGIDBODIES_PT_AddActiveNJoint"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Gen Rigidbody'
    bl_context = "posemode"
    bl_label = "Add Active & Joint"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        context.window_manager.genrigidbodies.addactivenjoint.draw(col)
        col.operator(AddActiveNJointOperator.bl_idname, text=bpy.app.translations.pgettext("Execute"), icon='MOD_PHYSICS')


### add MainMenu
class Menu(bpy.types.Menu):
    bl_idname = "GENRIGIDBODIES_MT_SubMenuRoot"
    bl_label = "Gen Rigid Bodies"
    bl_description = "make rigibodies & constraint"

    def draw(self, context):
        layout = self.layout
        layout.operator(AddPassiveOperator.bl_idname, icon='BONE_DATA')
        layout.operator(AddActiveOperator.bl_idname, icon='PHYSICS')
        layout.operator(AddJointOperator.bl_idname, icon='CONSTRAINT')
        layout.operator(AddActiveNJointOperator.bl_idname, icon='MOD_PHYSICS')
        
    @classmethod
    def register(cls):
        bpy.types.VIEW3D_MT_pose.append(drawmenu)
    
    @classmethod
    def unregister(cls):
        bpy.types.VIEW3D_MT_pose.remove(drawmenu)


def drawmenu(self, context):
    self.layout.separator()
    self.layout.menu(Menu.bl_idname, icon='MESH_ICOSPHERE')


### user prop
class UProp:
    rb_shape = EnumProperty(
        name='Shape',
        description='Choose Rigid Body Shape',
        items=shapes,
        #items=bpy.types.RigidBodyObject.collision_shape,
        #update=update_shape,
        default='CAPSULE'
    )
    rb_dim = FloatVectorProperty(
        name = "Dimensions",
        description = "rigid body Dimensions XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5
    )
    rb_mass = FloatProperty(
        name = "Mass",
        description = "rigid body mass",
        default = 1.0,
        subtype = 'NONE',
        min = 0.001
    )
    rb_friction = FloatProperty(
        name = "Friction",
        description = "rigid body friction",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    rb_bounciness = FloatProperty(
        name = "Bounciness",
        description = "rigid body bounciness",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    rb_translation = FloatProperty(
        name = "Translation",
        description = "rigid body translation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    rb_rotation = FloatProperty(
        name = "Rotation",
        description = "rigid body rotation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    rb_rootbody_passive = BoolProperty(
        name='Passive',
        description='Rigid Body Type Passive',
        default=True
    )
    rb_add_pole_rootbody = BoolProperty(
        name='Add Pole Object',
        description='Add Pole Object',
        default=True
    )
    rb_pole_rootbody_dim = FloatVectorProperty(
        name = "Pole Object Dimension",
        description = "Pole Object Dimension XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5
    )
    rb_rootbody_animated = BoolProperty(
        name='animated',
        description='Root Rigid Body sets animated',
        default=True
    )
    
    jo_type = EnumProperty(
        name='Type',
        description='Choose Contstraint Type',
        items=types,
        default='GENERIC_SPRING'
    )
    jo_size = FloatProperty(
        name = "joint Size",
        description = "joint Size",
        default = 1,
        subtype = 'NONE',
        min = 0,
        max = 5
    )
    jo_limit_lin_x = BoolProperty(
        name='X Axis',
        description='limit x',
        default=True,
        options={'ANIMATABLE'}
    )
    jo_limit_lin_y = BoolProperty(
        name='Y Axis',
        description='limit y',
        default=True
    )
    jo_limit_lin_z = BoolProperty(
        name='Z Axis',
        description='limit z',
        default=True
    )
    jo_limit_lin_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_x_lower",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_lin_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_y_lower",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_lin_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_z_lower",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_lin_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_x_upper",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_lin_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_y_upper",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_lin_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_z_upper",
        default = 0,
        subtype = 'NONE'
    )
    jo_limit_ang_x = BoolProperty(
        name='X Angle',
        description='Angle limit x',
        default=True,
        options={'ANIMATABLE'}
    )
    jo_limit_ang_y = BoolProperty(
        name='Y Angle',
        description='Angle limit y',
        default=True
    )
    jo_limit_ang_z = BoolProperty(
        name='Z Angle',
        description='Angle limit z',
        default=True
    )
    jo_limit_ang_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_x_lower",
        default = -0.785398,
        subtype = 'ANGLE'
    )
    jo_limit_ang_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_y_lower",
        default = -0.785398,
        subtype = 'ANGLE'
    )
    jo_limit_ang_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_z_lower",
        default = -0.785398,
        subtype = 'ANGLE'
    )
    jo_limit_ang_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_x_upper",
        default = 0.785398,
        subtype = 'ANGLE'
    )
    jo_limit_ang_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_y_upper",
        default = 0.785398,
        subtype = 'ANGLE'
    )
    jo_limit_ang_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_z_upper",
        default = 0.785398,
        subtype = 'ANGLE'
    )
    jo_use_spring_x = BoolProperty(
        name='X',
        description='use spring x',
        default=False
    )
    jo_use_spring_y = BoolProperty(
        name='Y',
        description='use spring y',
        default=False
    )
    jo_use_spring_z = BoolProperty(
        name='Z',
        description='use spring z',
        default=False
    )
    jo_spring_stiffness_x = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the X Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0
    )
    jo_spring_stiffness_y = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Y Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0
    )   
    jo_spring_stiffness_z = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Z Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0
    )
    jo_spring_damping_x = FloatProperty(
        name = "Damping X",
        description = "Damping on the X Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    jo_spring_damping_y = FloatProperty(
        name = "Damping Y",
        description = "Damping on the Y Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    jo_spring_damping_z = FloatProperty(
        name = "Damping Z",
        description = "Damping on the Z Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1
    )
    jo_align_bone = BoolProperty(
        name='Align Joint To Bone',
        description='Set same rotation of bone to joint object',
        default=True
    )


class AddPassiveProperties(bpy.types.PropertyGroup):
    ###instance UProp.rigidbody
    p_rb_shape : UProp.rb_shape
    p_rb_dim : UProp.rb_dim
    p_rb_mass : UProp.rb_mass
    p_rb_friction : UProp.rb_friction
    p_rb_bounciness : UProp.rb_bounciness
    p_rb_translation : UProp.rb_translation
    p_rb_rotation : UProp.rb_rotation
    p_rb_rootbody_passive : UProp.rb_rootbody_passive
    p_rb_rootbody_animated : UProp.rb_rootbody_animated

    def draw(self, layout):
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


class AddActiveProperties(bpy.types.PropertyGroup):
    ###instance UProp.rigidbody
    p_rb_shape : UProp.rb_shape
    p_rb_dim : UProp.rb_dim
    p_rb_mass : UProp.rb_mass
    p_rb_friction : UProp.rb_friction
    p_rb_bounciness : UProp.rb_bounciness
    p_rb_translation : UProp.rb_translation
    p_rb_rotation : UProp.rb_rotation
    p_rb_rootbody_animated : UProp.rb_rootbody_animated

    def draw(self, layout):
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


class AddJointProperties(bpy.types.PropertyGroup):
    ###instance UProp.joint
    joint_type : UProp.jo_type
    joint_size : UProp.jo_size
    joint_align_bone : UProp.jo_align_bone
    joint_Axis_limit_x : UProp.jo_limit_lin_x
    joint_Axis_limit_y : UProp.jo_limit_lin_y
    joint_Axis_limit_z : UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower : UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower : UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower : UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper : UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper : UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper : UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x : UProp.jo_limit_ang_x
    joint_Angle_limit_y : UProp.jo_limit_ang_y
    joint_Angle_limit_z : UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower : UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower : UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower : UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper : UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper : UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper : UProp.jo_limit_ang_z_upper
    joint_use_spring_x : UProp.jo_use_spring_x
    joint_use_spring_y : UProp.jo_use_spring_y
    joint_use_spring_z : UProp.jo_use_spring_z
    joint_spring_stiffness_x : UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y : UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z : UProp.jo_spring_stiffness_z
    joint_spring_damping_x : UProp.jo_spring_damping_x
    joint_spring_damping_y : UProp.jo_spring_damping_y
    joint_spring_damping_z : UProp.jo_spring_damping_z

    def draw(self, layout):
        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_size')
        box.prop(self, 'joint_align_bone')

        col = box.column(align=True)
        col.label(text="Limits:")

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
        col.label(text="Springs:")

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


class AddActiveNJointProperties(bpy.types.PropertyGroup):
    ###instance UProp.rigidbody
    p_rb_shape : UProp.rb_shape
    p_rb_dim : UProp.rb_dim
    p_rb_mass : UProp.rb_mass
    p_rb_friction : UProp.rb_friction
    p_rb_bounciness : UProp.rb_bounciness
    p_rb_translation : UProp.rb_translation
    p_rb_rotation : UProp.rb_rotation
    p_rb_add_pole_rootbody : UProp.rb_add_pole_rootbody
    p_rb_pole_rootbody_dim : UProp.rb_pole_rootbody_dim

    ###instance UProp.joint
    joint_type : UProp.jo_type
    joint_size : UProp.jo_size
    joint_align_bone : UProp.jo_align_bone
    joint_Axis_limit_x : UProp.jo_limit_lin_x
    joint_Axis_limit_y : UProp.jo_limit_lin_y
    joint_Axis_limit_z : UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower : UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower : UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower : UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper : UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper : UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper : UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x : UProp.jo_limit_ang_x
    joint_Angle_limit_y : UProp.jo_limit_ang_y
    joint_Angle_limit_z : UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower : UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower : UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower : UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper : UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper : UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper : UProp.jo_limit_ang_z_upper
    joint_use_spring_x : UProp.jo_use_spring_x
    joint_use_spring_y : UProp.jo_use_spring_y
    joint_use_spring_z : UProp.jo_use_spring_z
    joint_spring_stiffness_x : UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y : UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z : UProp.jo_spring_stiffness_z
    joint_spring_damping_x : UProp.jo_spring_damping_x
    joint_spring_damping_y : UProp.jo_spring_damping_y
    joint_spring_damping_z : UProp.jo_spring_damping_z

    def draw(self, layout):
        ###Rigid Body Object
        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')

        #Joint Object
        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_size')
        box.prop(self, 'joint_align_bone')
        box.prop(self, 'p_rb_add_pole_rootbody')

        col = box.column(align=True)
        col.label(text="Limits:")

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
        col.label(text="Springs:")

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


class Properties(bpy.types.PropertyGroup):
    addpassive : PointerProperty(type=AddPassiveProperties)
    addactive : PointerProperty(type=AddActiveProperties)
    addjoint : PointerProperty(type=AddJointProperties)
    addactivenjoint : PointerProperty(type=AddActiveNJointProperties)

    @classmethod
    def register(cls):
        bpy.types.WindowManager.genrigidbodies = PointerProperty(type=cls)
        bpy.app.translations.register(__name__, translation_dict)

    @classmethod
    def unregister(cls):
        bpy.app.translations.unregister(__name__)
        del bpy.types.WindowManager.genrigidbodies


### Create Rigid Bodies On Bones
class AddPassiveOperator(bpy.types.Operator):
    bl_idname = "genrigidbodies.addpassivejoint"
    bl_label = "Add Passive(on bones)"
    bl_description = "make rigibodies move on bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    init_rb_dimX = 0.28
    init_rb_dimY = 1.30
    init_rb_dimZ = 0.28

    def draw(self, context):
        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label(text="You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        # Branch specs
        #layout.label(text='Tree Definition')

        #layout.prop(self,'chooseSet')
        
        context.window_manager.genrigidbodies.addpassive.draw(self.layout)

    ### 
    def execute(self, context):
        ###selected Armature
        ob = bpy.context.active_object
        #self.report({'INFO'}, ob.data)

        if len(bpy.context.selected_pose_bones) == 0:
            return {'FINISHED'}

        params = context.window_manager.genrigidbodies.addpassive

        for selected_bone in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bone.vector[0]))            
            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1, location=selected_bone.center)
            rc = bpy.context.active_object
            if rc is None:
                self.report({'INFO'}, 'Rigidboy creation Failded. Verify Rigidbody World exists and set current collection to Rigidbody World')
                return {'CANCELLED'}
            rc.name = "rb." + ob.name + '.' + selected_bone.name
            rc.rotation_mode = 'QUATERNION'
            rc.show_in_front = True
            rc.display.show_shadows = False
            rc.display_type = 'BOUNDS'
            rc.hide_render = True
            rc.cycles_visibility.transmission = False
            rc.cycles_visibility.camera = False
            rc.cycles_visibility.diffuse = False
            rc.cycles_visibility.scatter = False
            rc.cycles_visibility.shadow = False
            rc.cycles_visibility.glossy = False
            rc.show_bounds = True
            rc.display_bounds_type = params.p_rb_shape

            align_obj_to_bone(rc, ob, selected_bone.name, True)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rb_dimX * params.p_rb_dim[0], 
                selected_bone.length * self.init_rb_dimY * params.p_rb_dim[1], 
                selected_bone.length * self.init_rb_dimZ * params.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            if params.p_rb_rootbody_passive == True:
                bpy.context.object.rigid_body.type = "PASSIVE"
            else:
                bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = params.p_rb_shape
            bpy.context.object.rigid_body.kinematic = params.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = params.p_rb_mass
            bpy.context.object.rigid_body.friction = params.p_rb_friction
            bpy.context.object.rigid_body.restitution = params.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = params.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = params.p_rb_rotation

            ### Child OF
            CoC = rc.constraints.new('CHILD_OF')
            CoC.name = 'Child_Of_' + selected_bone.name
            CoC.target = ob
            CoC.subtarget = selected_bone.name
            
            #without ops way to childof_set_inverse
            sub_target = bpy.data.objects[ob.name].pose.bones[selected_bone.name]
            #self.report({'INFO'}, str(sub_target))
            CoC.inverse_matrix = sub_target.matrix.inverted()   
            rc.update_tag(refresh={'OBJECT'})

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')  
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}


#
class AddActiveOperator(bpy.types.Operator):
    bl_idname = "genrigidbodies.addactive"
    bl_label = "Add Active"
    bl_description = "make active rigibodies on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_rb_dimX = 0.28
    init_rb_dimY = 1.30
    init_rb_dimZ = 0.28

    tr_size = 0.33

    def draw(self, context):
        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label(text="You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        # Branch specs
        #layout.label(text='Tree Definition')

        #layout.prop(self,'chooseSet')
        context.window_manager.genrigidbodies.addactive.draw(self.layout)

    ### 
    def execute(self, context):
        ###selected Armature
        ob = bpy.context.active_object
        #self.report({'INFO'}, ob.data)

        params = context.window_manager.genrigidbodies.addactive

        for selected_bone in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bone.vector[0]))

            ###Create Rigidbody Cube
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.primitive_cube_add(size=1, location=selected_bone.center)
            rc = bpy.context.active_object
            if rc is None:
                self.report({'INFO'}, 'Rigidboy creation Failded. Verify Rigidbody World exists and set current collection to Rigidbody World')
                return {'CANCELLED'}
            rc.name = "rb." + ob.name + '.' + selected_bone.name
            rc.rotation_mode = 'QUATERNION'
            rc.show_in_front = True
            rc.display.show_shadows = False
            rc.display_type = 'BOUNDS'
            rc.hide_render = True
            rc.cycles_visibility.transmission = False
            rc.cycles_visibility.camera = False
            rc.cycles_visibility.diffuse = False
            rc.cycles_visibility.scatter = False
            rc.cycles_visibility.shadow = False
            rc.cycles_visibility.glossy = False
            rc.show_bounds = True
            rc.display_bounds_type = params.p_rb_shape

            align_obj_to_bone(rc, ob, selected_bone.name, True)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rb_dimX * params.p_rb_dim[0], 
                selected_bone.length * self.init_rb_dimY * params.p_rb_dim[1], 
                selected_bone.length * self.init_rb_dimZ * params.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = params.p_rb_shape
            bpy.context.object.rigid_body.kinematic = params.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = params.p_rb_mass
            bpy.context.object.rigid_body.friction = params.p_rb_friction
            bpy.context.object.rigid_body.restitution = params.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = params.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = params.p_rb_rotation

            ## Make Track offset point
            bpy.ops.object.empty_add(type='ARROWS', location=selected_bone.head)
            tr = bpy.context.active_object
            tr.name = "tr." + ob.name + "." + selected_bone.name
            tr.empty_display_size = selected_bone.length * self.tr_size
            tr.rotation_mode = 'QUATERNION'

            ### Align track object to bone
            align_obj_to_bone(tr, ob, selected_bone.name)
            tr.parent = rc
            tr.matrix_parent_inverse = rc.matrix_world.inverted()

            ### Set Copy Transform Constraint To Bone
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode='POSE')
            #bpy.ops.pose.armature_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bone.name]
            ab = bpy.context.active_pose_bone

            #self.report({'INFO'}, str(rc.name))
            con = ab.constraints.new('COPY_TRANSFORMS')
            #self.report({'INFO'}, "info:" + str(CoC))
            con.name = 'Copy Transforms Of ' + tr.name
            con.target = tr

            ###bone's use_connect turn to false
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.context.active_bone.use_connect = False
        
        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}


#
class AddJointOperator(bpy.types.Operator):
    bl_idname = "genrigidbodies.addjoint"
    bl_label = "Add Joints"
    bl_description = "add Add Joints on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_joint_size = 0.33

    def draw(self, context):
        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label(text="You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        # Branch specs
        #layout.label(text='Tree Definition')

        #layout.prop(self,'chooseSet')
        context.window_manager.genrigidbodies.addjoint.draw(self.layout)

    ### 
    def execute(self, context):
        add_rigidbody_world()
        
        ###selected Armature
        ob = bpy.context.active_object
        #self.report({'INFO'}, ob.data)
        spb = bpy.context.selected_pose_bones

        ### Apply Object transform
        bpy.ops.object.mode_set(mode='OBJECT')

        params = context.window_manager.genrigidbodies.addjoint

        for selected_bone in spb:
            #self.report({'INFO'}, str(selected_bone.vector[0]))            
            
            ###Create Empty Sphere
            bpy.ops.object.empty_add(type='ARROWS', location=selected_bone.head)
            jc = bpy.context.active_object
            if jc is None:
                self.report({'INFO'}, 'Rigidboy creation Failded. Verify Rigidbody World exists and set current collection to Rigidbody World')
                return {'CANCELLED'}
            jc.name = "joint." + ob.name + "." + selected_bone.name
            jc.show_in_front = True
            jc.rotation_mode = 'QUATERNION'
            
            if params.joint_align_bone:
                align_obj_to_bone(jc, ob, selected_bone.name)
            
            ### Rigid Body Dimensions
            bpy.context.object.empty_display_size = selected_bone.length * self.init_joint_size * params.joint_size

            ### Set Rigid Body Constraint
            bpy.ops.rigidbody.constraint_add()
            bpy.context.object.rigid_body_constraint.type = params.joint_type
            bpy.context.object.rigid_body_constraint.use_breaking = False
            bpy.context.object.rigid_body_constraint.use_override_solver_iterations = True
            bpy.context.object.rigid_body_constraint.breaking_threshold = 10
            bpy.context.object.rigid_body_constraint.solver_iterations = 10

            bpy.context.object.rigid_body_constraint.use_limit_lin_x = params.joint_Axis_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_lin_y = params.joint_Axis_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_lin_z = params.joint_Axis_limit_z
            bpy.context.object.rigid_body_constraint.limit_lin_x_lower = params.joint_Axis_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_lin_y_lower = params.joint_Axis_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_lin_z_lower = params.joint_Axis_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_lin_x_upper = params.joint_Axis_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_lin_y_upper = params.joint_Axis_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_lin_z_upper = params.joint_Axis_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_limit_ang_x = params.joint_Angle_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_ang_y = params.joint_Angle_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_ang_z = params.joint_Angle_limit_z
            bpy.context.object.rigid_body_constraint.limit_ang_x_lower = params.joint_Angle_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_ang_y_lower = params.joint_Angle_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_ang_z_lower = params.joint_Angle_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_ang_x_upper = params.joint_Angle_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_ang_y_upper = params.joint_Angle_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_ang_z_upper = params.joint_Angle_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_spring_x = params.joint_use_spring_x
            bpy.context.object.rigid_body_constraint.use_spring_y = params.joint_use_spring_y
            bpy.context.object.rigid_body_constraint.use_spring_z = params.joint_use_spring_z
            bpy.context.object.rigid_body_constraint.spring_stiffness_x = params.joint_spring_stiffness_x
            bpy.context.object.rigid_body_constraint.spring_stiffness_y = params.joint_spring_stiffness_y
            bpy.context.object.rigid_body_constraint.spring_stiffness_z = params.joint_spring_stiffness_z
            bpy.context.object.rigid_body_constraint.spring_damping_x = params.joint_spring_damping_x
            bpy.context.object.rigid_body_constraint.spring_damping_y = params.joint_spring_damping_y
            bpy.context.object.rigid_body_constraint.spring_damping_z = params.joint_spring_damping_z

            ###constraint.object
            #bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects["rigidbody.Bone"]
            #bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects["rigidbody.Bone.001"]

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}


class AddActiveNJointOperator(bpy.types.Operator):
    bl_idname = "genrigidbodies.addactivenjoint"
    bl_label = "Add Active & Joints"
    bl_description = "Add Active & Joints"
    bl_options = {'REGISTER', 'UNDO'}

    init_rb_dimX = 0.28
    init_rb_dimY = 1.30
    init_rb_dimZ = 0.28

    #pole_dict = {}

    init_joint_size = 0.33
    init_polerb_size = 0.33

    tr_size = 0.33

    def draw(self, context):
        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label(text="You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        ###Rigid Body Object
        context.window_manager.genrigidbodies.addactivenjoint.draw(self.layout)

    # 
    def execute(self, context):
        add_rigidbody_world()
        
        ###selected Armature
        ob = bpy.context.active_object
        #self.report({'INFO'}, "ob:" + str(ob))

        spb = bpy.context.selected_pose_bones

        bpy.ops.object.mode_set(mode='OBJECT')

        params = context.window_manager.genrigidbodies.addactivenjoint
        
        rb_dict = {}
        
        wm = bpy.context.window_manager 
        
        tot = len(spb) * 2
        wm.progress_begin(0, tot)
        i = 0

        ###Rigid Body Session
        for selected_bone in spb:
            print(selected_bone)
            #self.report({'INFO'}, str(selected_bone.vector[0]))

            i += 1
            wm.progress_update(i)

            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1, location=selected_bone.center)
            rc = bpy.context.active_object
            if rc is None:
                self.report({'INFO'}, 'Rigidboy creation Failded. Verify Rigidbody World exists and set current collection to Rigidbody World')
                return {'CANCELLED'}
            rc.name = "rb." + ob.name + "." + selected_bone.name
            rc.rotation_mode = 'QUATERNION'
            rc.show_in_front = True
            rc.display.show_shadows = False
            rc.display_type = 'BOUNDS'
            rc.hide_render = True
            rc.show_bounds = True
            rc.display_bounds_type = params.p_rb_shape

            rb_dict[selected_bone] = rc
            
            ### Aligh to Bone
            align_obj_to_bone(rc, ob, selected_bone.name, True)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bone.length * self.init_rb_dimX * params.p_rb_dim[0], 
                selected_bone.length * self.init_rb_dimY * params.p_rb_dim[1], 
                selected_bone.length * self.init_rb_dimZ * params.p_rb_dim[2]
            ]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"
            bpy.context.object.rigid_body.collision_shape = params.p_rb_shape
            bpy.context.object.rigid_body.mass = params.p_rb_mass
            bpy.context.object.rigid_body.friction = params.p_rb_friction
            bpy.context.object.rigid_body.restitution = params.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = params.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = params.p_rb_rotation

            ## Make Track offset point
            bpy.ops.object.empty_add(type='ARROWS', location=selected_bone.head)
            tr = bpy.context.active_object
            tr.name = "tr." + ob.name + "." + selected_bone.name
            tr.empty_display_size = selected_bone.length * self.tr_size
            tr.rotation_mode = 'QUATERNION'

            ### Align track object to bone
            align_obj_to_bone(tr, ob, selected_bone.name)
            tr.parent = rc
            tr.matrix_parent_inverse = rc.matrix_world.inverted()

            ### Set Copy Transform Constraint To Bone
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode='POSE')
            #bpy.ops.pose.armature_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bone.name]
            ab = bpy.context.active_pose_bone

            #self.report({'INFO'}, str(rc.name))
            con = ab.constraints.new('COPY_TRANSFORMS')
            #self.report({'INFO'}, "info:" + str(CoC))
            con.name = 'Copy Transforms Of ' + tr.name
            con.target = tr

            ###bone's use_connect turn to false
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.context.active_bone.use_connect = False

            bpy.ops.object.mode_set(mode='OBJECT')

            if params.p_rb_add_pole_rootbody == True and selected_bone.parent is not None\
                and selected_bone.parent not in spb and selected_bone.parent not in rb_dict:
                ###Create Rigidbody Cube
                bpy.ops.mesh.primitive_cube_add(size=1, location=selected_bone.parent.center)
                rc = bpy.context.active_object
                rc.name = "rb.pole." + ob.name + "." + selected_bone.parent.name
                rc.rotation_mode = 'QUATERNION'
                rc.show_in_front = True
                rc.display.show_shadows = False
                rc.hide_render = True
                rc.display_type = 'BOUNDS'
                rc.show_bounds = True
                rc.display_bounds_type = 'BOX'
                
                rb_dict[selected_bone.parent] = rc

                ### Rigid Body Dimensions
                bpy.context.object.dimensions = [
                    selected_bone.parent.length * self.init_polerb_size * params.p_rb_pole_rootbody_dim[0],
                    selected_bone.parent.length * self.init_polerb_size * params.p_rb_pole_rootbody_dim[1],
                    selected_bone.parent.length * self.init_polerb_size * params.p_rb_pole_rootbody_dim[2]
                ]
                
                ### Scale Apply
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

                ### Set Rigid Body
                bpy.ops.rigidbody.object_add()

                rc.rigid_body.type = "PASSIVE"
                rc.rigid_body.collision_shape = "BOX"
                #rc.rigid_body.collision_shape = params.p_rb_shape
                #rc.rigid_body.mass = params.p_rb_mass
                #rc.rigid_body.friction = params.p_rb_friction
                #rc.rigid_body.restitution = params.p_rb_bounciness
                #rc.rigid_body.linear_damping = params.p_rb_translation
                #rc.rigid_body.angular_damping = params.p_rb_rotation
                rc.rigid_body.kinematic = True

                ### Child OF
                CoC = rc.constraints.new('CHILD_OF')
                CoC.name = 'Child_Of_' + selected_bone.parent.name
                CoC.target = ob
                CoC.subtarget = selected_bone.parent.name
                
                #without ops way to childof_set_inverse
                sub_target = bpy.data.objects[ob.name].pose.bones[selected_bone.parent.name]
                #self.report({'INFO'}, str(sub_target))
                CoC.inverse_matrix = sub_target.matrix.inverted()
        
        #bpy.context.view_layer.update()
        print('Joint Session')
        
        ###Joint Session
        for selected_bone in spb:
            print(selected_bone)

            #self.report({'INFO'}, str(selected_bone.vector[0]))

            i += 1
            wm.progress_update(i)

            if selected_bone in rb_dict and selected_bone.parent in rb_dict:
                ###Create Joint Empty
                bpy.ops.object.empty_add(type='ARROWS', location=selected_bone.head)
                jc = bpy.context.active_object
                jc.name = "joint." + ob.name + "." + selected_bone.name
                jc.show_in_front = True
                jc.rotation_mode = 'QUATERNION'
                
                if params.joint_align_bone:
                    align_obj_to_bone(jc, ob, selected_bone.name)

                ### Set Joint radius
                bpy.context.object.empty_display_size = selected_bone.length * self.init_joint_size * params.joint_size
                
                ### Set Rigid Body Constraint
                bpy.ops.rigidbody.constraint_add()
                
                jc.rigid_body_constraint.object1 = rb_dict[selected_bone.parent]
                jc.rigid_body_constraint.object2 = rb_dict[selected_bone]

                jc.rigid_body_constraint.type = params.joint_type
                jc.rigid_body_constraint.use_breaking = False
                jc.rigid_body_constraint.use_override_solver_iterations = True
                jc.rigid_body_constraint.breaking_threshold = 10
                jc.rigid_body_constraint.solver_iterations = 10

                jc.rigid_body_constraint.use_limit_lin_x = params.joint_Axis_limit_x
                jc.rigid_body_constraint.use_limit_lin_y = params.joint_Axis_limit_y
                jc.rigid_body_constraint.use_limit_lin_z = params.joint_Axis_limit_z
                jc.rigid_body_constraint.limit_lin_x_lower = params.joint_Axis_limit_x_lower
                jc.rigid_body_constraint.limit_lin_y_lower = params.joint_Axis_limit_y_lower
                jc.rigid_body_constraint.limit_lin_z_lower = params.joint_Axis_limit_z_lower
                jc.rigid_body_constraint.limit_lin_x_upper = params.joint_Axis_limit_x_upper
                jc.rigid_body_constraint.limit_lin_y_upper = params.joint_Axis_limit_y_upper
                jc.rigid_body_constraint.limit_lin_z_upper = params.joint_Axis_limit_z_upper

                jc.rigid_body_constraint.use_limit_ang_x = params.joint_Angle_limit_x
                jc.rigid_body_constraint.use_limit_ang_y = params.joint_Angle_limit_y
                jc.rigid_body_constraint.use_limit_ang_z = params.joint_Angle_limit_z
                jc.rigid_body_constraint.limit_ang_x_lower = params.joint_Angle_limit_x_lower
                jc.rigid_body_constraint.limit_ang_y_lower = params.joint_Angle_limit_y_lower
                jc.rigid_body_constraint.limit_ang_z_lower = params.joint_Angle_limit_z_lower
                jc.rigid_body_constraint.limit_ang_x_upper = params.joint_Angle_limit_x_upper
                jc.rigid_body_constraint.limit_ang_y_upper = params.joint_Angle_limit_y_upper
                jc.rigid_body_constraint.limit_ang_z_upper = params.joint_Angle_limit_z_upper

                jc.rigid_body_constraint.use_spring_x = params.joint_use_spring_x
                jc.rigid_body_constraint.use_spring_y = params.joint_use_spring_y
                jc.rigid_body_constraint.use_spring_z = params.joint_use_spring_z
                jc.rigid_body_constraint.spring_stiffness_x = params.joint_spring_stiffness_x
                jc.rigid_body_constraint.spring_stiffness_y = params.joint_spring_stiffness_y
                jc.rigid_body_constraint.spring_stiffness_z = params.joint_spring_stiffness_z
                jc.rigid_body_constraint.spring_damping_x = params.joint_spring_damping_x
                jc.rigid_body_constraint.spring_damping_y = params.joint_spring_damping_y
                jc.rigid_body_constraint.spring_damping_z = params.joint_spring_damping_z

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='DESELECT')

        wm.progress_end()

        self.report({'INFO'}, "OK")
        return {'FINISHED'}


# utils
def add_rigidbody_world():
    scene = bpy.context.scene
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()


def align_obj_to_bone(obj, rig, bone_name, lock_loc=False):
    bone = rig.data.bones[bone_name]

    mat = rig.matrix_world @ bone.matrix_local

    if not lock_loc:
        obj.location = mat.to_translation()

    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = mat.to_quaternion()


# add menu
register, unregister = bpy.utils.register_classes_factory((
    AddPassivePanel,
    AddPassiveOperator,
    AddPassiveProperties,
    AddActivePanel,
    AddActiveOperator,
    AddActiveProperties,
    AddJointPanel,
    AddJointOperator,
    AddJointProperties,
    AddActiveNJointPanel,
    AddActiveNJointOperator,
    AddActiveNJointProperties,
    Properties,
    Menu,
))
