import bpy

def bind_vertex_groups_to_bones(vertex_group_name, bone_name):
    # 获取当前激活的对象
    obj = bpy.context.active_object

    # 检查是否为网格对象
    if obj.type != 'MESH':
        print("所选对象不是网格对象。")
        return

    # 获取绑定的骨架
    armature = None
    for modifier in obj.modifiers:
        if modifier.type == 'ARMATURE':
            armature = modifier.object
            break

    if armature is None:
        print("未找到骨架修改器。")
        return

    # 获取指定的顶点组
    vertex_group = obj.vertex_groups.get(vertex_group_name)
    if vertex_group is None:
        print(f"未找到名为 {vertex_group_name} 的顶点组。")
        return

    # 获取指定的骨骼
    pose_bone = armature.pose.bones.get(bone_name)
    if pose_bone is None:
        print(f"未找到名为 {bone_name} 的骨骼。")
        return

    vg_bone = armature.data.bones.get(bone_name)
    if vg_bone:
        # 确保对象处于编辑模式
        bpy.ops.object.mode_set(mode='OBJECT')
        # 绑定顶点组到骨骼
        obj.vertex_groups.active = vertex_group
        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
        print(f"成功将顶点组 {vertex_group_name} 绑定到骨骼 {bone_name}。")

# 调用函数执行绑定操作，这里需要你根据实际情况修改顶点组和骨骼的名称
vertex_group_name = "unused bip001 lthightwist1"
bone_name = "足.L"
bind_vertex_groups_to_bones(vertex_group_name, bone_name)
    