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



#merge_vertex_groups(obj, ["unused muscle_elbow_l","unused bip001 l foretwist","unused bip001 l foretwist1"], "ひじ.L")
#merge_vertex_groups(obj, ["unused muscle_elbow_l","手捩.L","unused bip001 l foretwist"], "ひじ.L")
#merge_vertex_groups(obj, ["unused muscle_elbow_r","手捩.R","unused bip001 r foretwist"], "ひじ.R")

#merge_vertex_groups(obj, ["unused muscle_elbow_l","手捩.L","unused trash 18"], "ひじ.L")
#merge_vertex_groups(obj, ["unused muscle_elbow_r","手捩.R","unused trash 19"], "ひじ.R")

#merge_vertex_groups(obj, ["unused bip001 luparmtwist","unused bip001 luparmtwist1","unused muscle_elbow_l"], "腕.L")
#merge_vertex_groups(obj, ["unused bip001 ruparmtwist","unused bip001 ruparmtwist1","unused muscle_elbow_r"], "腕.R")

#merge_vertex_groups(obj, ["unused bip001 luparmtwist","unused bip001 luparmtwist1"], "腕.L")
#merge_vertex_groups(obj, ["unused bip001 ruparmtwist","unused bip001 ruparmtwist1"], "腕.R")


merge_vertex_groups(obj, ["unused collar","head neck lower","首"], "首")

merge_vertex_groups(obj, ["unused geosphere001","arm left shoulder 1"], "肩.L")
merge_vertex_groups(obj, ["unused geosphere002","arm right shoulder 1"], "肩.R")

#merge_vertex_groups(obj, ["arm left shoulder 2","unused bip001 armtwist_l","unused muscle_elbow_l","arm left shoulder pad","unused chain_arm01"], "腕.L")
#merge_vertex_groups(obj, ["arm right shoulder 2","unused bip001 armtwist_r","unused muscle_elbow_r"], "腕.R")

#merge_vertex_groups(obj, ["unused trash 18","unused bip001 l foretwist1","arm left elbow"], "ひじ.L")
#merge_vertex_groups(obj, ["unused trash 19","unused bip001 r foretwist1"], "ひじ.R")

merge_vertex_groups(obj, ["unused bip001 lcalftwist","unused bip001 lcalftwist1"], "ひざD.L")
merge_vertex_groups(obj, ["unused bip001 rcalftwist","unused bip001 rcalftwist1"], "ひざD.R")


#merge_vertex_groups(obj, ["手捩.L","ひじ.L"], "手捩.L")
#merge_vertex_groups(obj, ["手捩.R","ひじ.R"], "手捩.R")