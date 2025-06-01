import bpy
import mathutils
from mathutils import Matrix, Vector
from typing import List, Union

def batch_bone_alignment(
    bone_pairs: List[Union[tuple, dict]],
    align_mode: str = 'FULL',
    length_mode: str = 'AUTO',
    report_progress: bool = True
):
    """
    批量骨骼对齐核心函数
    
    参数格式示例：
    1. 元组列表: [("ArmatureA:bone1", "ArmatureB:boneX"), ...]
    2. 字典列表: [{"src": "ArmatureA:bone1", "tgt": "ArmatureB:boneX", "align": "HEAD"}, ...]
    """
    
    # 模式预处理
    original_mode = bpy.context.mode
    if original_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # 数据缓存优化
    matrix_cache = {}
    processed_armatures = set()

    try:
        # 预计算所有源骨骼矩阵
        for pair in bone_pairs:
            src_info = pair['src'] if isinstance(pair, dict) else pair[0]
            src_arm_name, src_bone_name = src_info.split(":")
            
            if src_arm_name not in matrix_cache:
                src_arm = bpy.data.objects.get(src_arm_name)
                if not src_arm or src_arm.type != 'ARMATURE':
                    continue
                
                # 进入编辑模式获取骨骼数据
                bpy.context.view_layer.objects.active = src_arm
                bpy.ops.object.mode_set(mode='EDIT')
                matrix_cache[src_arm_name] = {
                    bone.name: (src_arm.matrix_world @ bone.matrix, bone.length)
                    for bone in src_arm.data.edit_bones
                }
                bpy.ops.object.mode_set(mode='OBJECT')

        # 批量处理目标骨骼
        for idx, pair in enumerate(bone_pairs):
            # 解析参数
            if isinstance(pair, dict):
                src = pair['src']
                tgt = pair['tgt']
                local_align = pair.get('align', align_mode)
                local_length = pair.get('length', length_mode)
            else:
                src, tgt = pair
                local_align = align_mode
                local_length = length_mode

            src_arm_name, src_bone_name = src.split(":")
            tgt_arm_name, tgt_bone_name = tgt.split(":")
            
            if report_progress:
                print(f"Processing {idx+1}/{len(bone_pairs)}: {src} => {tgt}")

            # 获取目标骨架
            tgt_arm = bpy.data.objects.get(tgt_arm_name)
            if not tgt_arm or tgt_arm.type != 'ARMATURE':
                print(f"跳过无效目标骨架: {tgt_arm_name}")
                continue

            # 切换到目标骨架编辑模式（优化模式切换）
            if tgt_arm_name not in processed_armatures:
                bpy.context.view_layer.objects.active = tgt_arm
                bpy.ops.object.mode_set(mode='EDIT')
                processed_armatures.add(tgt_arm_name)

            # 获取骨骼数据
            try:
                src_matrix, src_length = matrix_cache[src_arm_name][src_bone_name]
                tgt_ebone = tgt_arm.data.edit_bones[tgt_bone_name]
            except KeyError as e:
                print(f"骨骼不存在: {e}")
                continue

            # 坐标转换
            local_matrix = tgt_arm.matrix_world.inverted() @ src_matrix

            # 应用对齐
            if local_align in ['HEAD', 'HEAD_TAIL', 'FULL']:
                tgt_ebone.head = local_matrix.translation
            
            if local_align in ['TAIL', 'HEAD_TAIL', 'FULL']:
                if local_align == 'FULL':
                    tgt_ebone.matrix = local_matrix
                else:
                    src_dir = (src_matrix.translation - src_matrix.to_3x3() @ Vector((0,0,0))).normalized()
                    tgt_ebone.tail = local_matrix.translation + src_dir * tgt_ebone.length

            # 处理长度
            if local_length == 'PRESERVE_SRC':
                tgt_ebone.length = src_length
            elif local_length == 'AUTO':
                if local_align == 'HEAD':
                    tgt_ebone.tail = tgt_ebone.head + (src_matrix.to_3x3() @ Vector((0, src_length, 0)))
                elif local_align == 'TAIL':
                    tgt_ebone.head = tgt_ebone.tail - (src_matrix.to_3x3() @ Vector((0, src_length, 0)))

            # 方向修正
            if local_align in ['HEAD_TAIL', 'FULL']:
                tgt_ebone.align_roll((src_matrix.to_3x3() @ Vector((0,1,0))).normalized())

    finally:
        # 恢复原始状态
        bpy.ops.object.mode_set(mode='OBJECT')
        if original_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=original_mode)

# 使用示例 1：简单元组列表
bone_list = [
    ("Character:Hand_L", "Weapon:Hold_L"),
    ("Character:Hand_R", "Weapon:Hold_R"),
    ("Character:Head", "Helmet:Base")
]
target_armature_name="Rouffe_arm"
source_armature_name="标准骨骼与刚体_arm"



# 使用示例 2：带参数的字典列表
advanced_list = [
    {
        "src": target_armature_name+":arm left shoulder 2",
        "tgt": source_armature_name+":腕.L",
        "align": "FULL",
        "length": "PRESERVE_SRC"
    },
    {
        "src": target_armature_name+":arm left shoulder 1",
        "tgt": source_armature_name+":肩.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left elbow",
        "tgt": source_armature_name+":ひじ.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left wrist",
        "tgt": source_armature_name+":手首.L",
        "align": "HEAD",
        "length": "AUTO"
    },
     {
        "src": target_armature_name+":arm left finger 1a",
        "tgt": source_armature_name+":親指０.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 1b",
        "tgt": source_armature_name+":親指１.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 1c",
        "tgt": source_armature_name+":親指２.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 2a",
        "tgt": source_armature_name+":人指１.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 2b",
        "tgt": source_armature_name+":人指２.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 2c",
        "tgt": source_armature_name+":人指３.L",
        "align": "HEAD",
        "length": "AUTO"
    },
     {
        "src": target_armature_name+":arm left finger 3a",
        "tgt": source_armature_name+":中指１.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 3b",
        "tgt": source_armature_name+":中指２.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 3c",
        "tgt": source_armature_name+":中指３.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 4a",
        "tgt": source_armature_name+":薬指１.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 4b",
        "tgt": source_armature_name+":薬指２.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 4c",
        "tgt": source_armature_name+":薬指３.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 5a",
        "tgt": source_armature_name+":小指１.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 5b",
        "tgt": source_armature_name+":小指２.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm left finger 5c",
        "tgt": source_armature_name+":小指３.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right shoulder 2",
        "tgt": source_armature_name+":腕.R",
        "align": "FULL",
        "length": "PRESERVE_SRC"
    },
    {
        "src": target_armature_name+":arm right shoulder 2",
        "tgt": source_armature_name+":腕捩.R",
        "align": "FULL",
        "length": "PRESERVE_SRC"
    },
    {
        "src": target_armature_name+":arm right shoulder 1",
        "tgt": source_armature_name+":肩.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right elbow",
        "tgt": source_armature_name+":ひじ.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right wrist",
        "tgt": source_armature_name+":手首.R",
        "align": "HEAD",
        "length": "AUTO"
    },
     {
        "src": target_armature_name+":arm right finger 1a",
        "tgt": source_armature_name+":親指０.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 1b",
        "tgt": source_armature_name+":親指１.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 1c",
        "tgt": source_armature_name+":親指２.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 2a",
        "tgt": source_armature_name+":人指１.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 2b",
        "tgt": source_armature_name+":人指２.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 2c",
        "tgt": source_armature_name+":人指３.R",
        "align": "HEAD",
        "length": "AUTO"
    },
     {
        "src": target_armature_name+":arm right finger 3a",
        "tgt": source_armature_name+":中指１.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 3b",
        "tgt": source_armature_name+":中指２.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 3c",
        "tgt": source_armature_name+":中指３.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 4a",
        "tgt": source_armature_name+":薬指１.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 4b",
        "tgt": source_armature_name+":薬指２.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 4c",
        "tgt": source_armature_name+":薬指３.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 5a",
        "tgt": source_armature_name+":小指１.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 5b",
        "tgt": source_armature_name+":小指２.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":arm right finger 5c",
        "tgt": source_armature_name+":小指３.R",
        "align": "HEAD",
        "length": "AUTO"
    },

    {
        "src": target_armature_name+":leg left thigh",
        "tgt": source_armature_name+":足.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":leg right thigh",
        "tgt": source_armature_name+":足.R",
        "align": "HEAD",
        "length": "AUTO"
    },

    {
        "src": target_armature_name+":leg left knee",
        "tgt": source_armature_name+":ひざ.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":leg right knee",
        "tgt": source_armature_name+":ひざ.R",
        "align": "HEAD",
        "length": "AUTO"
    },

    {
        "src": target_armature_name+":leg left ankle",
        "tgt": source_armature_name+":足首.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":leg right ankle",
        "tgt": source_armature_name+":足首.R",
        "align": "HEAD",
        "length": "AUTO"
    },

    {
        "src": target_armature_name+":spine lower",
        "tgt": source_armature_name+":上半身",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":spine middle",
        "tgt": source_armature_name+":上半身1",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":spine upper",
        "tgt": source_armature_name+":上半身2",
        "align": "HEAD",
        "length": "AUTO"
    },
    
    {
        "src": target_armature_name+":head neck lower",
        "tgt": source_armature_name+":首",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":head neck upper",
        "tgt": source_armature_name+":頭",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":head eyeball left",
        "tgt": source_armature_name+":目.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":head eyeball right",
        "tgt": source_armature_name+":目.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":boob right 1",
        "tgt": source_armature_name+":乳奶1.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":boob right 2",
        "tgt": source_armature_name+":乳奶2.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":boob left 1",
        "tgt": source_armature_name+":乳奶1.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": target_armature_name+":boob left 2",
        "tgt": source_armature_name+":乳奶2.L",
        "align": "HEAD",
        "length": "AUTO"
    },

]

# 执行批量对齐
batch_bone_alignment(
    bone_pairs=advanced_list,
    align_mode='HEAD_TAIL',
    report_progress=True
)

#################### align_shoulder_mmd2mmd.py ##############



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


# 调用函数进行骨骼对齐
#align_bone_heads(source_armature_name, source_bone_name, target_armature_name, target_bone_name)
align_bone_heads(source_armature_name, "肩P.L", target_armature_name, "arm left shoulder 1")
align_bone_heads(source_armature_name, "肩C.L", target_armature_name, "arm left shoulder 2")
align_bone_heads(source_armature_name, "肩P.R", target_armature_name, "arm right shoulder 1")
align_bone_heads(source_armature_name, "肩C.R", target_armature_name, "arm right shoulder 2")

align_bone_heads(source_armature_name, "下半身", source_armature_name, "上半身")
align_bone_tail2heads(source_armature_name, "腰", source_armature_name, "上半身")


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




