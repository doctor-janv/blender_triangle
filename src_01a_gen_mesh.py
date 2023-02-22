import os
import bpy
import sys

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class BLENDERTRIANGLE_OT_gen_mesh(bpy.types.Operator):
    bl_label = "Generate Triangulation"
    bl_idname = "blendertriangle.gen_mesh"  
    bl_description = "Generate a triangulation from the selected items"

    def invoke(self, context, event):
        print("Executing gen_mesh operation")

        app_data = context.scene.blendertriangle_properties

        if not os.path.exists(app_data.path_to_triangle_exe):
            self.report({'ERROR'},"Invalid path to triangle executable: \"" + \
                                   app_data.path_to_triangle_exe + "\"")
            return {"FINISHED"}
        
        TRI_PATH = app_data.path_to_triangle_exe

        if bpy.context.mode != "OBJECT":
            self.report({'ERROR'},"Must be in 'OBJECT' mode")
            return {"FINISHED"}

        if not bpy.data.is_saved:
            self.report({'ERROR'},"Save file first to somewhere for path resolution.")
            return {"FINISHED"}

        svar_area = app_data.max_tri_area
        svar_angle = app_data.min_tri_angle
        svar_steiner_bndries = app_data.inhibit_bndry_steiner
        svar_steiner_internl = app_data.inhibit_internal_steiner

        blend_dir = os.path.dirname(bpy.data.filepath)
        if blend_dir not in sys.path:
            sys.path.append(blend_dir)

        print("blend_dir:",blend_dir)


        from collections import OrderedDict

        if bpy.context.active_object == None:
            self.report({'ERROR'},"No edges selected.")
            return {"FINISHED"}

        edges    = bpy.context.active_object.data.edges
        vertices = bpy.context.active_object.data.vertices

        #================================= Determine selected edges
        selected_edges = []

        for edge in edges:
            if edge.select:
                selected_edges.append(list(edge.vertices))
                
        #print("selected_edges:",selected_edges)

        #================================= Extract linear list of relevant vertices
        raw_vertex_list = []
        for e in selected_edges:
            for vid in e:
                raw_vertex_list.append(vid)

        #print("raw_vertex_list:",raw_vertex_list)

        #================================= Load auxiliary vertices
        for vid in range(0,len(vertices)):
            if not vid in raw_vertex_list:
                raw_vertex_list.append(vid)

        #================================= Create a vertex map
        vertex_map = OrderedDict.fromkeys(raw_vertex_list)
        id=0
        for k in vertex_map:
            vertex_map[k] = id 
            id += 1
            
        #print("vertex_map:",vertex_map)
        
        #================================= Write the poly file
        poly_file_name = blend_dir+"/V.poly"
        poly_file = open(blend_dir+"/V.poly", "w")

        poly_file.write(str(len(vertex_map))+" 2 0 0\n")

        for vid in vertex_map:
            vertex = vertices[vid].co
            poly_file.write(str(vertex_map[vid]+1)+" ")
            poly_file.write(str(vertex[0])+" ")
            poly_file.write(str(vertex[1])+" ")
            poly_file.write("\n")

        poly_file.write(str(len(selected_edges))+" 0\n")

        id=0
        for edge in selected_edges:
            poly_file.write(str(id+1)+" ")
            poly_file.write(str(vertex_map[edge[0]]+1)+" ")
            poly_file.write(str(vertex_map[edge[1]]+1)+" ")
            poly_file.write("\n")

        poly_file.write("0\n")

        poly_file.close()

        #================================= Run triangle
        steiner_flag = ""
        if svar_steiner_bndries: steiner_flag = "Y"
        if svar_steiner_bndries and svar_steiner_internl: steiner_flag = "YY"
        print("Running "+(TRI_PATH+" -pj"+str(steiner_flag)+"q"+str(svar_angle)+"a"+str(svar_area)+" " + poly_file_name))
        stream = os.popen(TRI_PATH+" -pj"+str(steiner_flag)+"q"+str(svar_angle)+"a"+str(svar_area)+" " + poly_file_name)
        output = stream.read()
        print("Output ",output)

        #================================= Read generated vertices
        new_vertex_cos = []
        node_file_name = blend_dir+"/V.1.node"
        node_file = open(node_file_name, "r")

        lines = node_file.readlines()

        words = lines[0].split()
        num_nodes = int(words[0])
        for k in range(1,num_nodes+1):
            words = lines[k].split()
            x = float(words[1])
            y = float(words[2])
            z = 0.0
            new_vertex_cos.append((x,y,z))

        node_file.close()
        #print("new_vertex_cos:", new_vertex_cos)

        #================================= Read generated triangles
        new_tris = []
        elem_file_name = blend_dir+"/V.1.ele"
        elem_file = open(elem_file_name,"r")

        lines = elem_file.readlines()

        words = lines[0].split()
        num_elems = int(words[0])
        for k in range(1,num_elems+1):
            words = lines[k].split()
            id0 = int(words[1])-1
            id1 = int(words[2])-1
            id2 = int(words[3])-1

            new_tris.append([id0,id1,id2])

        elem_file.close()
        #print("new_tris",new_tris)

        #================================= Write an obj file
        obj_file_name = blend_dir+"/V.1.obj"

        obj_file = open(obj_file_name,"w")

        obj_file.write("o Triangulated PLSG\n")

        for vertex in new_vertex_cos:
            obj_file.write("v "+str(vertex[0])+" "+str(vertex[1])+" "+str(vertex[2])+"\n")

        obj_file.write("vn 0.0 0.0 1.0\n")

        for poly in new_tris:
            obj_file.write("f ")
            for vid in poly:
                obj_file.write(str(vid+1)+"//1 ")
            obj_file.write("\n")

        obj_file.close()

        #================================= Import the obj file
        old_objs = set(context.scene.objects)
        bpy.ops.import_scene.obj(filepath=blend_dir+"/V.1.obj",axis_forward='Y',axis_up='Z')
        imported_objs = set(context.scene.objects) - old_objs

        for imported_obj in imported_objs:
            imported_obj.show_wire = True

        
        return {"FINISHED"}

def register():
    bpy.utils.register_class(BLENDERTRIANGLE_OT_gen_mesh)
   

def unregister():
    bpy.utils.unregister_class(BLENDERTRIANGLE_OT_gen_mesh)

if __name__ == "__main__":
    register()