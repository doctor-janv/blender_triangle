## Class naming conventions in Blender

```python
UPPER_CASE_{SEPARATOR}_mixed_case
```

Where the {SEPARATOR} is two letters denoting the class belonging to a certain type (from which type the class is inherited):

HT – Header
MT – Menu
OT – Operator
PT – Panel
UL – UI list
The class identifier “bl_idname” mast match the class name.


Examples of valid class names and identifiers:

```python
class MYADDON_OT_my_operator(bpy.types.Operator):
    bl_idname = 'myaddon.my_operator'
    ...

class MYADDON_MT_my_menu(bpy.types.Menu):
    bl_idname = 'MYADDON_MT_my_menu'
    ...

class MYADDON_HT_my_header(bpy.types.Header):
    bl_idname = 'MYADDON_HT_my_header'
    ...

class MYADDON_PT_my_panel(bpy.types.Panel):
    bl_idname = 'MYADDON_PT_my_panel'
    ...
```