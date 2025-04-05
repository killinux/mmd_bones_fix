import bpy

# 定义XPS到MMD的骨骼名称映射
xps_to_mmd_mapping = {

    "arm left finger 1a": "親指０.L",
    "arm left finger 1b": "親指１.L",
    "arm left finger 1c": "親指２.L",
    "arm left finger 2a": "人指１.L",
    "arm left finger 2b": "人指２.L",
    "arm left finger 2c": "人指３.L",
    "arm left finger 3a": "中指１.L",
    "arm left finger 3b": "中指２L",
    "arm left finger 3c": "中指３.L",
    "arm left finger 4a": "薬指１.L",
    "arm left finger 4b": "薬指２.L",
    "arm left finger 4c": "薬指３.L",
    "arm left finger 5a": "小指１.L",
    "arm left finger 5b": "小指２.L",
    "arm left finger 5c": "小指３.L",

    "arm right finger 1a": "親指０.R",
    "arm right finger 1b": "親指１.R",
    "arm right finger 1c": "親指２.R",
    "arm right finger 2a": "人指１.R",
    "arm right finger 2b": "人指２.R",
    "arm right finger 2c": "人指３.R",
    "arm right finger 3a": "中指１.R",
    "arm right finger 3b": "中指２R",
    "arm right finger 3c": "中指３.R",
    "arm right finger 4a": "薬指１.R",
    "arm right finger 4b": "薬指２.R",
    "arm right finger 4c": "薬指３.R",
    "arm right finger 5a": "小指１.R",
    "arm right finger 5b": "小指２.R",
    "arm right finger 5c": "小指３.R",


    "leg left thigh": "足.L",
    "leg right thigh": "足.R",
    "leg left knee": "ひざ.L",
    "leg right knee": "ひざ.R",
    "leg left toes": "足先EX.L",
    "leg right toes": "足先EX.R",
    "leg left ankle": "足首.L",
    "leg right ankle": "足首.R",

    "DEF-spine.001": "下半身",
    "spine lower": "上半身",
    "spine middle": "上半身2",
    "spine upper": "上半身3",
    
    "Dhead neck lower": "首",
    "head neck upper": "頭",
    "arm left shoulder 1": "肩.L",
    "arm right shoulder 1": "肩.R",
    "arm left shoulder 2": "腕.L",
    "arm right shoulder 2": "腕.R",
    "arm left elbow": "ひじ.L",
    "arm right elbow": "ひじ.R",
    "arm left wrist": "手首.L",
    "arm right wrist": "手首.R",
    
    "unused bip001 l foretwist1":"手捩.L",
    "unused bip001 r foretwist1":"手捩.R",
    "unused bip001 luparmtwist1":"腕捩.L",
    "unused bip001 ruparmtwist1":"腕捩.R"
    
}


bl_info = {
    "name": "rigify to MMD Bone Name Converter",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Tools",
    "description": "Convert XPS bone names to MMD bone names",
    "category": "Rigging",
}


class XPStoMMDBoneNameConverter(bpy.types.Operator):
    """Convert XPS bone names to MMD bone names"""
    bl_idname = "rig.xps_to_mmd_bone_names"
    bl_label = "Convert rigify to MMD Bone Names"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 获取当前活动的骨架对象
        obj = context.active_object
        if obj and obj.type == 'ARMATURE':
            armature = obj.data
            for bone in armature.bones:
                if bone.name in xps_to_mmd_mapping:
                    bone.name = xps_to_mmd_mapping[bone.name]
            self.report({'INFO'}, "Bone names converted successfully.")
        else:
            self.report({'ERROR'}, "Please select an armature object.")
        return {'FINISHED'}


class XPStoMMDBoneNamePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "rigify to MMD Bone Name Converter"
    bl_idname = "OBJECT_PT_xps_to_mmd_bone_name"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("rig.xps_to_mmd_bone_names")


def register():
    bpy.utils.register_class(XPStoMMDBoneNameConverter)
    bpy.utils.register_class(XPStoMMDBoneNamePanel)


def unregister():
    bpy.utils.unregister_class(XPStoMMDBoneNamePanel)
    bpy.utils.unregister_class(XPStoMMDBoneNameConverter)


if __name__ == "__main__":
    register()