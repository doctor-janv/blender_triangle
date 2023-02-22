import os
import bpy

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# This is the main data structure that gets loaded onto the 
# blender context. It will always be available via
# context.scene.blendertriangle_properties
class BlenderTriangleProperties(bpy.types.PropertyGroup):
    bl_idname = "BlenderTriangleProperties"
    
    path_to_triangle_exe : bpy.props.StringProperty(default="Path-To-triangle-exe",subtype='FILE_PATH')
    
    max_tri_area : bpy.props.FloatProperty(min=1.0e-6, default=1.0,precision=5)
    min_tri_angle : bpy.props.FloatProperty(min=5.0,max=85.0,default=30.0,precision=1)
    inhibit_bndry_steiner : bpy.props.BoolProperty(default=True)
    inhibit_internal_steiner : bpy.props.BoolProperty(default=True)

def register():
    bpy.utils.register_class(BlenderTriangleProperties)
    bpy.types.Scene.blendertriangle_properties = \
        bpy.props.PointerProperty(type=BlenderTriangleProperties)

def unregister():

    bpy.utils.unregister_class(BlenderTriangleProperties)
    

if __name__ == "__main__":
    register()