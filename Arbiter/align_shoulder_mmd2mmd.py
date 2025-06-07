import bpy


def align_bone_heads(source_armature_name, source_bone_name, target_armature_name, target_bone_name):
    # 获取源骨架对象和目标骨架对象
    source_armature_obj = bpy.data.objects.get(source_armature_name)
    target_armature_obj = bpy.data.objects.get(target_armature_name)

    # 检查源骨架对象和目标骨架对象是否存在
    if source_armature_obj is None or target_armature_obj is None:
        print("指定的骨架对象不存在，请检查骨架名称。")
        return

    # 检查源骨架对象和目标骨架对象是否为骨骼对象
    if source_armature_obj.type != 'ARMATURE' or target_armature_obj.type != 'ARMATURE':
        print("指定的对象不是骨骼对象，请选择骨骼对象。")
        return

    # 获取源骨架数据和目标骨架数据
    source_armature = source_armature_obj.data
    target_armature = target_armature_obj.data

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = source_armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    try:
        # 获取源骨骼和目标骨骼
        source_bone = source_armature.edit_bones[source_bone_name]
        target_bone = target_armature.bones[target_bone_name]

        # 计算目标骨骼头部的世界坐标
        target_bone_world_head = target_armature_obj.matrix_world @ target_bone.head_local

        # 计算源骨骼当前的向量（从头部到尾部）
        source_bone_vector = source_bone.tail - source_bone.head

        # 将源骨骼头部移动到目标骨骼头部的世界坐标
        source_bone.head = source_armature_obj.matrix_world.inverted() @ target_bone_world_head

        # 根据之前的向量重新定位源骨骼尾部，以保持骨骼形状
        source_bone.tail = source_bone.head + source_bone_vector

    except KeyError:
        print("指定的骨骼名称不存在，请检查骨骼名称。")

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')

def align_bone_tail(source_armature_name, source_bone_name, target_armature_name, target_bone_name):
    # 获取源骨架对象和目标骨架对象
    source_armature_obj = bpy.data.objects.get(source_armature_name)
    target_armature_obj = bpy.data.objects.get(target_armature_name)

    # 检查源骨架对象和目标骨架对象是否存在
    if source_armature_obj is None or target_armature_obj is None:
        print("指定的骨架对象不存在，请检查骨架名称。")
        return

    # 检查源骨架对象和目标骨架对象是否为骨骼对象
    if source_armature_obj.type != 'ARMATURE' or target_armature_obj.type != 'ARMATURE':
        print("指定的对象不是骨骼对象，请选择骨骼对象。")
        return

    # 获取源骨架数据和目标骨架数据
    source_armature = source_armature_obj.data
    target_armature = target_armature_obj.data

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = source_armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    try:
        # 获取源骨骼和目标骨骼
        source_bone = source_armature.edit_bones[source_bone_name]
        target_bone = target_armature.bones[target_bone_name]

        # 计算目标骨骼头部的世界坐标
        target_bone_world_tail = target_armature_obj.matrix_world @ target_bone.tail_local

        # 计算源骨骼当前的向量（从头部到尾部）
        source_bone_vector = source_bone.tail - source_bone.head

        # 将源骨骼头部移动到目标骨骼头部的世界坐标
        source_bone.head = source_armature_obj.matrix_world.inverted() @ target_bone_world_tail

        # 根据之前的向量重新定位源骨骼尾部，以保持骨骼形状
        source_bone.tail = source_bone.head + source_bone_vector

    except KeyError:
        print("指定的骨骼名称不存在，请检查骨骼名称。")

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')

def align_bone_tail2heads(source_armature_name, source_bone_name, target_armature_name, target_bone_name):
    # 获取源骨架对象和目标骨架对象
    source_armature_obj = bpy.data.objects.get(source_armature_name)
    target_armature_obj = bpy.data.objects.get(target_armature_name)

    # 检查源骨架对象和目标骨架对象是否存在
    if source_armature_obj is None or target_armature_obj is None:
        print("指定的骨架对象不存在，请检查骨架名称。")
        return

    # 检查源骨架对象和目标骨架对象是否为骨骼对象
    if source_armature_obj.type != 'ARMATURE' or target_armature_obj.type != 'ARMATURE':
        print("指定的对象不是骨骼对象，请选择骨骼对象。")
        return

    # 获取源骨架数据和目标骨架数据
    source_armature = source_armature_obj.data
    target_armature = target_armature_obj.data

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = source_armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    try:
        # 获取源骨骼和目标骨骼
        source_bone = source_armature.edit_bones[source_bone_name]
        target_bone = target_armature.bones[target_bone_name]

        # 计算目标骨骼头部的世界坐标
        target_bone_world_head = target_armature_obj.matrix_world @ target_bone.head_local

        # 计算源骨骼当前的向量（从头部到尾部）
        source_bone_vector = source_bone.tail - source_bone.head

        # 将源骨骼头部移动到目标骨骼头部的世界坐标
        #source_bone.head = source_armature_obj.matrix_world.inverted() @ target_bone_world_head

        source_bone.tail = source_armature_obj.matrix_world.inverted() @ target_bone_world_head

        # 根据之前的向量重新定位源骨骼尾部，以保持骨骼形状
        #source_bone.tail = source_bone.head + source_bone_vector
        source_bone.head = source_bone.tail - source_bone_vector

    except KeyError:
        print("指定的骨骼名称不存在，请检查骨骼名称。")

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')
def align_bone_heads2tail(source_armature_name, source_bone_name, target_armature_name, target_bone_name):
    # 获取源骨架对象和目标骨架对象
    source_armature_obj = bpy.data.objects.get(source_armature_name)
    target_armature_obj = bpy.data.objects.get(target_armature_name)

    # 检查源骨架对象和目标骨架对象是否存在
    if source_armature_obj is None or target_armature_obj is None:
        print("指定的骨架对象不存在，请检查骨架名称。")
        return

    # 检查源骨架对象和目标骨架对象是否为骨骼对象
    if source_armature_obj.type != 'ARMATURE' or target_armature_obj.type != 'ARMATURE':
        print("指定的对象不是骨骼对象，请选择骨骼对象。")
        return

    # 获取源骨架数据和目标骨架数据
    source_armature = source_armature_obj.data
    target_armature = target_armature_obj.data

    # 进入编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = source_armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    try:
        # 获取源骨骼和目标骨骼
        source_bone = source_armature.edit_bones[source_bone_name]
        target_bone = target_armature.bones[target_bone_name]

        # 计算目标骨骼头部的世界坐标
        target_bone_world_head = target_armature_obj.matrix_world @ target_bone.head_local
        target_bone_world_tail = target_armature_obj.matrix_world @ target_bone.tail_local

        # 计算源骨骼当前的向量（从头部到尾部）
        source_bone_vector = source_bone.tail - source_bone.head
        #target_bone_vector = target_bone.tail - target_bone.head
        target_bone_vector = target_bone_world_tail - target_bone_world_head

        # 将源骨骼头部移动到目标骨骼头部的世界坐标
        #source_bone.head = source_armature_obj.matrix_world.inverted() @ target_bone_world_head
        source_bone.head = source_armature_obj.matrix_world.inverted() @ target_bone_world_tail
        #source_bone.tail = source_armature_obj.matrix_world.inverted() @ target_bone_world_tail

        # 根据之前的向量重新定位源骨骼尾部，以保持骨骼形状
        source_bone.tail = source_bone.head + target_bone_vector
        #source_bone.head = source_bone.tail - source_bone_vector

    except KeyError:
        print("指定的骨骼名称不存在，请检查骨骼名称。")

    # 退出编辑模式
    bpy.ops.object.mode_set(mode='OBJECT')


# 在这里设置源骨架名称、源骨骼名称、目标骨架名称和目标骨骼名称
target_armature_name = "Arbiter_arm"
target_bone_name = "arm left shoulder 1"
source_armature_name = "标准骨架_arm"
source_bone_name = "肩P.L"

# 调用函数进行骨骼对齐
#align_bone_heads(source_armature_name, source_bone_name, target_armature_name, target_bone_name)
align_bone_heads(source_armature_name, "肩P.L", target_armature_name, "arm left shoulder 1")
align_bone_heads(source_armature_name, "肩C.L", target_armature_name, "arm left shoulder 2")
align_bone_heads(source_armature_name, "肩P.R", target_armature_name, "arm right shoulder 1")
align_bone_heads(source_armature_name, "肩C.R", target_armature_name, "arm right shoulder 2")

align_bone_heads(source_armature_name, "下半身", source_armature_name, "上半身")
align_bone_tail2heads(source_armature_name, "腰", source_armature_name, "上半身")


align_bone_tail(source_armature_name, "腕捩.R", source_armature_name, "腕.R")
align_bone_tail(source_armature_name, "腕捩.L", source_armature_name, "腕.L")
align_bone_tail(source_armature_name, "手捩.R", source_armature_name, "ひじ.R")
align_bone_tail(source_armature_name, "手捩.L", source_armature_name, "ひじ.L")

align_bone_tail(source_armature_name, "ダミー.R", source_armature_name, "手首.R")
align_bone_tail(source_armature_name, "ダミー.L", source_armature_name, "手首.L")

align_bone_heads2tail(source_armature_name, "手先.L", source_armature_name, "手首.L")
align_bone_heads2tail(source_armature_name, "手先.R", source_armature_name, "手首.R")

align_bone_tail(source_armature_name, "小指先.R", source_armature_name, "小指３.R")
align_bone_tail(source_armature_name, "薬指先.R", source_armature_name, "薬指３.R")
align_bone_tail(source_armature_name, "中指先.R", source_armature_name, "中指３.R")
align_bone_tail(source_armature_name, "人指先.R", source_armature_name, "人指３.R")
align_bone_tail(source_armature_name, "親指先.R", source_armature_name, "親指２.R")

align_bone_tail(source_armature_name, "小指先.L", source_armature_name, "小指３.L")
align_bone_tail(source_armature_name, "薬指先.L", source_armature_name, "薬指３.L")
align_bone_tail(source_armature_name, "中指先.L", source_armature_name, "中指３.L")
align_bone_tail(source_armature_name, "人指先.L", source_armature_name, "人指３.L")
align_bone_tail(source_armature_name, "親指先.L", source_armature_name, "親指２.L")

#グルーブ

align_bone_heads(source_armature_name, "腰キャンセル.R", source_armature_name, "足.L")
align_bone_heads(source_armature_name, "足D.L", source_armature_name, "足.L")
align_bone_heads(source_armature_name, "ひざD.L", source_armature_name, "ひざ.L")
align_bone_heads(source_armature_name, "足首D.L", source_armature_name, "足首.L")
align_bone_heads(source_armature_name, "足ＩＫ.L", source_armature_name, "足首.L")
align_bone_tail2heads(source_armature_name, "足IK親.L", source_armature_name, "足首.L")
align_bone_tail(source_armature_name, "足先EX.L", source_armature_name, "足首.L")
align_bone_tail(source_armature_name, "つま先ＩＫ.L", source_armature_name, "足首.L")

align_bone_heads(source_armature_name, "腰キャンセル.L", source_armature_name, "足.R")
align_bone_heads(source_armature_name, "足D.R", source_armature_name, "足.R")
align_bone_heads(source_armature_name, "ひざD.R", source_armature_name, "ひざ.R")
align_bone_heads(source_armature_name, "足首D.R", source_armature_name, "足首.R")
align_bone_heads(source_armature_name, "足ＩＫ.R", source_armature_name, "足首.R")
align_bone_tail2heads(source_armature_name, "足IK親.R", source_armature_name, "足首.R")
align_bone_tail(source_armature_name, "足先EX.R", source_armature_name, "足首.R")
align_bone_tail(source_armature_name, "つま先ＩＫ.R", source_armature_name, "足首.R")




