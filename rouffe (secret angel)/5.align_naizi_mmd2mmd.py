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

# 使用示例 2：带参数的字典列表
advanced_list = [
     {
        "src": "Rouffe_arm:乳奶1.R",
        "tgt": "Rouffe Bone Lg_arm:乳奶1.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": "Rouffe_arm:乳奶2.R",
        "tgt": "Rouffe Bone Lg_arm:乳奶2.R",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": "Rouffe_arm:乳奶1.L",
        "tgt": "Rouffe Bone Lg_arm:乳奶1.L",
        "align": "HEAD",
        "length": "AUTO"
    },
    {
        "src": "Rouffe_arm:乳奶2.L",
        "tgt": "Rouffe Bone Lg_arm:乳奶2.L",
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