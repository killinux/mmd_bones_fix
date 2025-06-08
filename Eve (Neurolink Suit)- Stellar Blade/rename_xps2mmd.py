import bpy

# 定义mmd到MMD的骨骼名称映射
xps_to_mmd_mapping = {
    
    "boob left 1": "乳奶1.L",
    "boob left 2": "乳奶2.L",
    "boob right 1": "乳奶1.R",
    "boob right 2": "乳奶2.R",

    "lEye": "目.L",
    "rEye": "目.R",

    "lThumb1": "親指０.L",
    "lThumb2": "親指１.L",
    "lThumb3": "親指２.L",
    "lIndex1": "人指１.L",
    "lIndex2": "人指２.L",
    "lIndex3": "人指３.L",
    "lMid1": "中指１.L",
    "lMid2": "中指２.L",
    "lMid3": "中指３.L",
    "lRing1": "薬指１.L",
    "lRing2": "薬指２.L",
    "lRing3": "薬指３.L",
    "lPinky1": "小指１.L",
    "lPinky2": "小指２.L",
    "lPinky3": "小指３.L",

    "rThumb1": "親指０.R",
    "rThumb2": "親指１.R",
    "rThumb3": "親指２.R",
    "rIndex1": "人指１.R",
    "rIndex2": "人指２.R",
    "rIndex3": "人指３.R",
    "rMid1": "中指１.R",
    "rMid2": "中指２R",
    "rMid3": "中指３.R",
    "rRing1": "薬指１.R",
    "rRing2": "薬指２.R",
    "rRing3": "薬指３.R",
    "rPinky1": "小指１.R",
    "rPinky2": "小指２.R",
    "rPinky3": "小指３.R",


#    "unused trash 15": "足D.L",
#    "unused trash 16": "足D.R",
#    "unused bip001 xtra04": "足D.L",
#    "unused bip001 xtra02": "足D.R",
    "lThighBend": "足D.L",
    "rThighBend": "足D.R",      
#    "unused bip001 l thigh_twist": "足D.L",
#    "unused bip001 r thigh_twist": "足D.R",
    
#    "unused bip001 lthightwist1": "足.L",
#    "unused bip001 rthightwist1": "足.R",   
    "lThighTwist": "足.L",
    "rThighTwist": "足.R",
    
    "lShin": "ひざD.L",
    "rShin": "ひざD.R",
    
#    "lMetatarsals": "足首.L",
#    "rMetatarsals": "足首.R", 
    
#    "lToe": "足先EX.L",
#    "rToe": "足先EX.R",


    "pelvis": "下半身",
    "abdomenLower": "上半身",
    "abdomenUpper": "上半身1",
    "chestLower": "上半身2",
    "chestUpper": "上半身3",
    
#    "neckLower": "首",

    "lCollar": "肩.L",
    "rCollar": "肩.R",
    
#    "arm left shoulder 2": "腕.L",
#    "arm right shoulder 2": "腕.R",
#    "unused bip001 luparmtwist": "腕.L",
#    "unused bip001 ruparmtwist": "腕.R",
#    "unused bip001 xtra07pp": "腕.L",
#    "unused bip001 xtra07": "腕.R", 
#    "unused bip001 upperarm_sub_l": "腕.L",
#    "unused bip001 upperarm_sub_r": "腕.R",
    "lShldrBend": "腕.L",
    "rShldrBend": "腕.R",    
#    "unused bip001 luparmtwist1":"腕捩.L",
#    "unused bip001 ruparmtwist1":"腕捩.R"
    "lShldrTwist":"腕捩.L",
    "rShldrTwist":"腕捩.R",
    
#    "arm left elbow": "ひじ.L",
#    "arm right elbow": "ひじ.R",    
#    "unused trash 18": "ひじ.L",
#    "unused trash 19": "ひじ.R",  
    "lForearmBend": "ひじ.L",
    "rForearmBend": "ひじ.R",  
#    "unused bip001 l foretwist1":"手捩.L",
#    "unused bip001 r foretwist1":"手捩.R",
    "lForearmTwist":"手捩.L",
    "rForearmTwist":"手捩.R",   
#    "lHand": "手首.L",
#    "rHand": "手首.R",
   
}
#    "head neck upper": "頭",

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
    bl_label = "Convert mmd to MMD Bone Names"
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