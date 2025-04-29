bl_info = {
    "name": "Circular Arrange",
    "blender": (2, 80, 0),
    "category": "Object",
    "version": (1, 2, 1),
    "author": "Ruprous",
    "location": "View3D > Sidebar > Tool Tab",
    "doc_url": "https://github.com/Ruprous/blenderAddons"
    #made by Ruprous
    #X/Twitter:@Ruprous
    #Copyright (c) 2024 Ruprous
}

import bpy
import math

class OBJECT_OT_circular_arrange(bpy.types.Operator):
    bl_idname = "object.circular_arrange"
    bl_label = "Circular Arrange"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        count = scene.circular_arrange_count
        radius = scene.circular_arrange_radius
        merge = scene.circular_arrange_merge
        
        obj = context.active_object
        if obj is None:
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        original_location = obj.location.copy()
        original_rotation = obj.rotation_euler.copy()  # 中心オブジェクトの回転を保持
        
        duplicated_objects = []
        
        for i in range(count):
            angle = 2 * math.pi * i / count
            x = radius * math.cos(angle) + original_location.x
            y = radius * math.sin(angle) + original_location.y
            bpy.ops.object.duplicate()
            obj = context.active_object
            obj.location = (x, y, original_location.z)
            duplicated_objects.append(obj)
            
            # 中心オブジェクトからの相対的な角度を計算し、複製オブジェクトの回転を調整する
            relative_angle = angle - math.pi
            obj.rotation_euler = (original_rotation.x, original_rotation.y, original_rotation.z + relative_angle)

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
        layout.prop(scene, "circular_arrange_count")
        layout.prop(scene, "circular_arrange_radius")
        layout.prop(scene, "circular_arrange_merge")
        layout.operator("object.circular_arrange")

def register():
    bpy.utils.register_class(OBJECT_OT_circular_arrange)
    bpy.utils.register_class(VIEW3D_PT_circular_arrange_panel)
    bpy.types.Scene.circular_arrange_count = bpy.props.IntProperty(
        name="Count",
        description="Number of duplicates",
        default=8,
        min=2,
    )
    bpy.types.Scene.circular_arrange_radius = bpy.props.FloatProperty(
        name="Radius",
        description="Radius of the circle",
        default=2.0,
        min=0.1,
    )
    bpy.types.Scene.circular_arrange_merge = bpy.props.BoolProperty(
        name="Merge Objects",
        description="Merge duplicated objects into one",
        default=False,
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_circular_arrange)
    bpy.utils.unregister_class(VIEW3D_PT_circular_arrange_panel)
    del bpy.types.Scene.circular_arrange_count
    del bpy.types.Scene.circular_arrange_radius
    del bpy.types.Scene.circular_arrange_merge

if __name__ == "__main__":
    register()
