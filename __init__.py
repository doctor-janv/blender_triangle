bl_info = {
    "name": "Triangle Mesher for Blender",
    "author": "Doctor Jan",
    "description" : "",
    "blender" : (3, 4, 1),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category": "Object"
}
modulesNames = ['src_00_data_structs',
                'src_01_UI',
                'src_01a_gen_mesh']

import sys
import importlib

modulesFullNames = {}
for name in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[name] = ('{}'.format(name))
    else:
        modulesFullNames[name] = ('{}.{}'.format(__name__, name))
 
for fullname in modulesFullNames.values():
    if fullname in sys.modules:
        importlib.reload(sys.modules[fullname])
    else:
        globals()[fullname] = importlib.import_module(fullname)
        setattr(globals()[fullname], 'modulesNames', modulesFullNames)
 
def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()
 
def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()