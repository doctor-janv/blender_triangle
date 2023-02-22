import os
import bpy

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class BLENDERTRIANGLE_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Triangle1.6 Interface"
    bl_idname = "BLENDERTRIANGLE_PT_main_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    props=[]

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        app_data = context.scene.blendertriangle_properties

        # Path to triangle
        layout.label(text=" Path to Triangle executable:\n")
        layout.label(text="(Absolute path to the triangle executable)")
        layout.prop(app_data, 'path_to_triangle_exe', text="")

        split = layout.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(text="Maximum triangle area")
        col2.prop(app_data, 'max_tri_area',text="")

        split = layout.split()
        col1 = split.column()
        col2 = split.column()
        col1.label(text="Minmum triangle angle (degrees)")
        col2.prop(app_data, 'min_tri_angle',text="")

        split = layout.split(factor=0.9)
        col1 = split.column()
        col2 = split.column()
        col1.label(text="Inhibit boundary Steiner-points")
        col2.use_property_split = True
        col2.use_property_decorate = False
        col2.prop(app_data, 'inhibit_bndry_steiner',
                  text="Whether to inhibit boundary Steiner-points")

        split = layout.split(factor=0.9)
        col1 = split.column()
        col2 = split.column()
        col1.label(text="Inhibit internal Steiner-points")
        col2.use_property_split = True
        col2.use_property_decorate = False
        col2.prop(app_data, 'inhibit_internal_steiner',
                  text="Whether to inhibit internal Steiner-points")

        split = layout.split()
        col1 = split.column()
        col2 = split.column()
        col3 = split.column()
        col2.operator("blendertriangle.gen_mesh",text="Generate Mesh")

def register():
    bpy.utils.register_class(BLENDERTRIANGLE_PT_main_panel)

def unregister():
    bpy.utils.unregister_class(BLENDERTRIANGLE_PT_main_panel)    

if __name__ == "__main__":
    register()