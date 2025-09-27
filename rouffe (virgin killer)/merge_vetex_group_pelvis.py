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


merge_vertex_groups(obj, ["butt right","butt left","unused bip001 pelvis"], "下半身")
#merge_vertex_groups(obj, ["butt right","butt left","下半身"], "下半身")
merge_vertex_groups(obj, ["unused muscle strand023","unused bip001 thightwist_rb","unused bip001 thightwist_rt","右足"], "右足")
merge_vertex_groups(obj, ["unused muscle strand005","unused bip001 thightwist_lb","unused bip001 thightwist_lt", "左足"], "左足")

#替换之后要把butt right ，butt left， unused bip001 pelvis ，unused muscle strand023 ，unused muscle strand005 这些都删掉
