bl_info = {
    "name": "Circular Arrange",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 3, 0),
    "author": "Ruprous",
    "location": "View3D > Sidebar > Tool Tab",
    "doc_url": "https://github.com/Ruprous/Circular-Arrange"
    #made by Ruprous
    #X/Twitter:@Ruprous
    #Copyright (c) 2024 Ruprous
}

import bpy
import math

class OBJECT_OT_circular_arrange(bpy.types.Operator):
    bl_idname = "object.circular_arrange"
    bl_label = "Circular Arrange"
    bl_description = "Duplicate and arrange the active object in a circle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        count = scene.circular_arrange_count
        radius = scene.circular_arrange_radius
        merge = scene.circular_arrange_merge
        angle_mode = scene.circular_arrange_angle_mode
        fixed_angle = scene.circular_arrange_fixed_angle
        relative_angle_offset = scene.circular_arrange_relative_angle_offset

        obj = context.active_object
        if obj is None:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        original_location = obj.location.copy()
        original_rotation = obj.rotation_euler.copy()  # Store the center object's rotation
        
        duplicated_objects = []
        
        for i in range(count):
            angle = 2 * math.pi * i / count
            x = radius * math.cos(angle) + original_location.x
            y = radius * math.sin(angle) + original_location.y
            bpy.ops.object.duplicate()
            obj = context.active_object
            obj.location = (x, y, original_location.z)
            duplicated_objects.append(obj)
            
            # Rotation by mode
            if angle_mode == 'RELATIVE':
                # Relative angle + offset
                relative_angle = angle - math.pi + math.radians(relative_angle_offset)
                obj.rotation_euler = (original_rotation.x, original_rotation.y, original_rotation.z + relative_angle)
            elif angle_mode == 'FIXED':
                # Fixed angle (degrees to radians)
                obj.rotation_euler = (original_rotation.x, original_rotation.y, math.radians(fixed_angle))

        if merge:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in duplicated_objects:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = duplicated_objects[0]
            bpy.ops.object.join()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')

        return {'FINISHED'}

class VIEW3D_PT_circular_arrange_panel(bpy.types.Panel):
    bl_label = "Circular Arrange"
    bl_idname = "VIEW3D_PT_circular_arrange_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "circular_arrange_count", text="Count", icon='MOD_ARRAY')
        layout.prop(scene, "circular_arrange_radius", text="Radius", icon='EMPTY_ARROWS')
        layout.prop(scene, "circular_arrange_merge", text="Merge Objects", icon='AUTOMERGE_ON')
        layout.prop(scene, "circular_arrange_angle_mode", text="Angle Mode", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        if scene.circular_arrange_angle_mode == 'RELATIVE':
            layout.prop(scene, "circular_arrange_relative_angle_offset", text="Relative Angle Offset (deg)", icon='CON_ROTLIKE')
        if scene.circular_arrange_angle_mode == 'FIXED':
            layout.prop(scene, "circular_arrange_fixed_angle", text="Fixed Angle (deg)", icon='CON_ROTLIKE')
        layout.operator("object.circular_arrange", text="Circular Arrange", icon='GROUP')

def register():
    bpy.utils.register_class(OBJECT_OT_circular_arrange)
    bpy.utils.register_class(VIEW3D_PT_circular_arrange_panel)
    bpy.types.Scene.circular_arrange_count = bpy.props.IntProperty(
        name="Count",
        description="Number of duplicates to arrange in a circle",
        default=8,
        min=2,
    )
    bpy.types.Scene.circular_arrange_radius = bpy.props.FloatProperty(
        name="Radius",
        description="Radius of the circle for arrangement",
        default=2.0,
        min=0.1,
    )
    bpy.types.Scene.circular_arrange_merge = bpy.props.BoolProperty(
        name="Merge Objects",
        description="Merge all duplicated objects into one object after arrangement",
        default=False,
    )
    bpy.types.Scene.circular_arrange_angle_mode = bpy.props.EnumProperty(
        name="Angle Mode",
        description="How to set the rotation of duplicated objects: Relative (each object faces outward) or Fixed (all objects have the same rotation)",
        items=[
            ('RELATIVE', "Relative", "Arrange with relative angle (each object faces outward from the center)"),
            ('FIXED', "Fixed", "Set all objects to the same rotation angle"),
        ],
        default='RELATIVE',
    )
    bpy.types.Scene.circular_arrange_fixed_angle = bpy.props.FloatProperty(
        name="Fixed Angle",
        description="Rotation angle (in degrees) for all objects when using Fixed mode",
        default=0.0,
    )
    bpy.types.Scene.circular_arrange_relative_angle_offset = bpy.props.FloatProperty(
        name="Relative Angle Offset",
        description="Additional rotation angle (in degrees) added to each object in Relative mode",
        default=0.0,
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_circular_arrange)
    bpy.utils.unregister_class(VIEW3D_PT_circular_arrange_panel)
    del bpy.types.Scene.circular_arrange_count
    del bpy.types.Scene.circular_arrange_radius
    del bpy.types.Scene.circular_arrange_merge
    del bpy.types.Scene.circular_arrange_angle_mode
    del bpy.types.Scene.circular_arrange_fixed_angle
    del bpy.types.Scene.circular_arrange_relative_angle_offset

if __name__ == "__main__":
    register()
