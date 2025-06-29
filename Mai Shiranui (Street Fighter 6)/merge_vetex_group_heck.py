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
    "neckUpper",
    "neckLower",
    "neck trapezius a 2.L",
    "neck trapezius a 2.R",
    "neck_collar root",
    "neck_collar 2.L",
    "neck_collar 2.R",
#    "首",
]

body_names = [
    "chestLower",
    "zipper 1",
    "zipper 2",
    "上半身2",

#    "首",
]

# 新顶点组的名称
new_group_name = "首"

# 调用函数合并顶点组
merge_vertex_groups(obj, group_names, new_group_name)

merge_vertex_groups(obj, body_names, "上半身2")

