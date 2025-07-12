import bpy

# 获取当前选中的物体
obj = bpy.context.object

# 确认所选物体存在且为网格类型
if obj and obj.type == 'MESH':
    # 筛选以'head'开头的顶点组名字
    head_vgroups = [vg for vg in obj.vertex_groups if vg.name.startswith('Ab')]

    # 打印所有符合条件的顶点组名字
    print("顶点组名以 'head' 开头的组为:")
    for vg in head_vgroups:
        print(vg.name)
else:
    print("请选中一个网格物体。")
