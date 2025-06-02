import bpy
from mathutils import Vector

def merge_adjacent_bones(parent_bone_name, child_bone_name, keep_name='PARENT'):
    """
    合并相邻骨骼的修正版
    
    参数：
    parent_bone_name : str - 父骨骼名称
    child_bone_name : str - 子骨骼名称
    keep_name : str - 命名策略（PARENT/CHILD/AUTO）
    """
    # 保存当前模式
    original_mode = bpy.context.mode
    if original_mode != 'EDIT':
        # 正确切换至编辑模式
        bpy.ops.object.mode_set(mode='EDIT')  # 关键修正点

    try:
        # 获取骨骼对象
        armature = bpy.context.object.data
        parent = armature.edit_bones.get(parent_bone_name)
        child = armature.edit_bones.get(child_bone_name)

        # 验证有效性
        if not parent or not child:
            raise ValueError("骨骼不存在")
        if child.parent != parent:
            raise ValueError("骨骼需为直接父子关系")
        if (parent.tail - child.head).length > 1e-6:
            raise ValueError("骨骼需首尾相接")

        # 记录原始数据
        original_children = child.children[:]
        original_tail = child.tail.copy()

        # 合并操作
        parent.tail = original_tail

        # 处理子骨骼继承
        for grandchild in original_children:
            grandchild.parent = parent
            grandchild.use_connect = True

        # 命名策略
        if keep_name == 'CHILD':
            parent.name, child.name = child.name, parent.name  # 交换名称后再删除
        elif keep_name == 'AUTO':
            if any(marker in child.name for marker in ('_L', '_R')):
                parent.name = child.name

        # 删除子骨骼
        armature.edit_bones.remove(child)

        # 自动修正连接状态
        if parent.parent:
            parent.use_connect = (parent.head - parent.parent.tail).length < 1e-6

        # 自动调整Roll角度
        if original_children:
            parent.align_roll(original_children[0].vector.normalized())

    finally:
        # 恢复原始模式
        if original_mode != 'EDIT':
            print(original_mode)
            #bpy.ops.object.mode_set(mode=original_mode)

def merge_selected_bones():
    """自动合并选中的两个相邻骨骼"""
    selected_bones = bpy.context.selected_editable_bones
    if len(selected_bones) != 2:
        raise ValueError("需选中两个相邻骨骼")

    # 自动识别父子关系
    parent = next((b for b in selected_bones if not b.parent or b.parent not in selected_bones), None)
    child = next((b for b in selected_bones if b != parent), None)

    if parent and child and child.parent == parent:
        merge_adjacent_bones(parent.name, child.name, keep_name='AUTO')
    else:
        raise ValueError("无法识别有效父子关系")

# 执行合并操作
merge_selected_bones()