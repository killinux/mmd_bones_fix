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
    "足.R",
    "unused bip001 xtra02"
]

# 新顶点组的名称
new_group_name = "足.R"

# 调用函数合并顶点组
#merge_vertex_groups(obj, group_names, new_group_name)

#merge_vertex_groups(obj, ["unused bip001 xtra02","leg right thigh","足.R"], "足.R")
#merge_vertex_groups(obj, ["unused bip001 xtra04","leg left thigh","足.L"], "足.L")
#merge_vertex_groups(obj, ["unused bip001 xtra07","腕.R"], "腕.R")
#merge_vertex_groups(obj, ["unused bip001 xtra07pp","腕.L"], "腕.L")

merge_vertex_groups(obj, ["arm left sleeve 1","arm left sleeve 2","arm left sleeve 3","ひじ.L"], "ひじ.L")
