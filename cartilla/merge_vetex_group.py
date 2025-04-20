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
    "head neck upper",
    "head cheek left 1", 
    "head cheek right 1",
    "head jaw",
    "head lip lower middle",
    "head lip lower left",
    "head lip lower right",
    "head tongue 1",
    "head tongue 2",
    "head tongue 2",
    "unused teeth_dw",
    "head eyebrow left root",
    "head eyebrow left 2",
    "head eyebrow left 3",
    "head eyebrow left 1",
    "head eyebrow right root",
    "head eyebrow right 2",
    "head eyebrow right 1",
    "head eyebrow right 3",
    "head eyelid lower left",
    "unused ac eyelid_bl",
    "head eyelid upper left",
    "unused ac eyelid_ul",
    "head eyelid lower right",
    "unused ac eyelid_br",
    "head eyelid upper right",
    "unused ac eyelid_ur",
    "head mouth corner left",
    "head mouth corner right",
    "head lip upper middle",
    "head lip upper left",
    "head lip upper right",
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
    "head cheek left 2",
    "head cheek left 3",
    "head cheek left 4",
    "head cheek left 5",
    "head cheek right 2",
    "head cheek right 3",
    "head cheek right 4",
    "head cheek right 5"
    
]

# 新顶点组的名称
new_group_name = "頭"

# 调用函数合并顶点组
merge_vertex_groups(obj, group_names, new_group_name)