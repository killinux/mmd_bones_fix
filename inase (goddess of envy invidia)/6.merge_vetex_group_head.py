import bpy

def merge_vertex_groups(obj, group_names, new_group_name):
    # 创建一个新的顶点组
    new_group = obj.vertex_groups.new(name=new_group_name)

    # 遍历所有指定的顶点组
    for group_name in group_names:
        if group_name in obj.vertex_groups:
            group = obj.vertex_groups[group_name]
            # 遍历所有顶点
            for v in obj.data.vertices:
                for g in v.groups:
                    if g.group == group.index:
                        # 获取当前顶点在该组中的权重
                        weight = group.weight(v.index)
                        try:
                            # 将权重添加到新的顶点组中
                            new_group.add([v.index], weight, 'ADD')
                        except RuntimeError:
                            pass

# 获取当前选中的对象
obj = bpy.context.active_object

# 要合并的顶点组名称列表
group_names = [
    "unused bip001 teeth_up",
    "unused bip001 teeth_dw",
    "head neck upper",
    "head eyelid upper right",
    "head eyelid upper left",
    "head eyelid lower right",
    "head eyelid lower left",
    "head mouth corner left",
    "head mouth corner right",
    "head hair left 1",
    "head hair left 2",
    "head hair left 3",
    "head hair front right",
    "head hair front right 1",
    "head hair front right 2",
    "head hair front right 3",
    "head hair right 1",
    "head hair right 2",
    "head hair right 3",


    "head jaw",
    "head lip lower middle",
    "head lip lower left",
    "head lip lower right",
    "head tongue !",
    "head tongue 1",
    "head tongue 2",
    "head tongue 3",
    
    "head lip upper left",
    "head lip upper right",
    "head cheek right",
    "head cheek left",
    "head nose nostril left",
    "head nose nostril right",
    "head lip upper middle",
    "head pince-nez chain 1",
    "head pince-nez chain 2",
    "head pince-nez chain 3",
    "head eyebrow right root",
    "head eyebrow right 1",
    "head eyebrow right 2",
    "head eyebrow right 3",
    "head eyebrow left root",
    "head eyebrow left 1",
    "head eyebrow left 2",
    "head eyebrow left 3",
    
    "head hair braid right 1",
    "head hair braid right 2",
    "head hair braid right 3",
    "head hair braid right 4",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    
    "unused teeth_dw",
    "unused ac eyelid_bl",
    "unused ac eyelid_ul",
    "unused ac eyelid_br",
    "unused ac eyelid_ur",

    "unused bip001 nose_l",
    "unused bip001 nose_r",
    "head front right 1",
    "head front right 2",
    "head front right 3",
    "head back middle 1",
    "head back middle 2",
    "head back middle 3",
    
    "head back left 1",
    "head back left 2",
    "head back left 3",
    "head front middle",
    "unused teeth_up",
    "unused ac head",
    "head cheek left 1",
    "head cheek left 2",
    "head cheek left 3",
    "head cheek left 4",
    "head cheek left 5",
    "head cheek right 1",
    "head cheek right 2",
    "head cheek right 3",
    "head cheek right 4",
    "head cheek right 5",
    "unused bip001 xtra42",
    "unused bip001 xtra42opp",
    "head hair back middle",
    "head hair back left",
    "head hair back right",
    
    "unused ac cheekbone_l",
    "unused ac cheekbone_r",
    "unused ac lip_bcl",
    "unused ac lip_bcr",
    "unused ac eyelid_bone_bl",
    "unused ac eyelid_bone_br",
    "unused ac eyelid_bone_ul",
    "unused ac eyelid_bone_ur",
    "unused ac lip_ucl",
    "unused ac lip_ucr",
    "unused ac nose_l",
    "unused ac nose_r",
    "head hair front middle",
    "head hair front middle 1",
    "head hair front middle 2",
    "head hair back middle 1",
    "head hair back middle 2",
    "head hair back middle 3",
    "head hair back middle 4",
    "head hair back middle 5",
    "head hair back left 1",
    "head hair back left 2",
    "head hair back left 3",
    "head hair back left 4",
    "head hair back left 5",
    "head hair back right 1",
    "head hair back right 2",
    "head hair back right 3",
    "head hair back right 4",
    "head hair back right 5",
    "head hair front left 1",
    "head hair front left 2",
    "head hair front left 3",
    "head earring left",
]

# 新顶点组的名称
new_group_name = "頭"

# 调用函数合并顶点组
merge_vertex_groups(obj, group_names, new_group_name)