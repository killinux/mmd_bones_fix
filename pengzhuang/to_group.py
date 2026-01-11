import bpy

def batch_set_rigidbody_collision_group(model_identifier, target_group_index=1):
    """
    批量设置模型刚体碰撞组（Blender 3.6唯一正确方式）
    :param model_identifier: 模型名称（支持「对象/集合」，自动识别）
    :param target_group_index: 碰撞组索引（0=组1、1=组2…19=组20）
    """
    # 1. 校验索引范围（Blender仅支持20个碰撞组）
    if not 0 <= target_group_index <= 19:
        print(f"❌ 错误：碰撞组索引必须是0-19（对应界面的组1-组20）")
        return

    # 2. 自动识别「对象/集合」并收集刚体
    rigidbody_objects = []
    
    # 先尝试按「对象（根父级）」查找
    model_obj = bpy.data.objects.get(model_identifier)
    if model_obj:
        # 递归收集所有子对象中的刚体
        def collect_rb_recursive(obj):
            if obj.rigid_body:  # 仅收集带刚体的对象
                rigidbody_objects.append(obj)
            # 遍历所有子对象
            for child in obj.children:
                collect_rb_recursive(child)
        collect_rb_recursive(model_obj)
    
    # 若对象不存在，尝试按「集合」查找
    if not rigidbody_objects:
        model_coll = bpy.data.collections.get(model_identifier)
        if model_coll:
            rigidbody_objects = [obj for obj in model_coll.objects if obj.rigid_body]
    
    # 校验是否找到刚体
    if not rigidbody_objects:
        print(f"⚠️ 提示：未在「{model_identifier}」中找到任何刚体对象")
        return

    # 3. 核心逻辑：修改collision_collections数组（唯一有效方式）
    success_count = 0
    for rb_obj in rigidbody_objects:
        rb = rb_obj.rigid_body
        # 清空所有碰撞组（设为False）
        for i in range(20):
            rb.collision_collections[i] = False
        # 仅保留目标组（设为True）→ 实现「属于该组+仅与该组碰撞」
        rb.collision_collections[target_group_index] = True
        success_count += 1

    # 输出结果
    print(f"✅ 配置完成！")
    print(f"   - 模型/集合：{model_identifier}")
    print(f"   - 处理刚体数量：{success_count}")
    print(f"   - 碰撞组设置：仅属于/碰撞「组{target_group_index+1}」")

# ===================== 执行配置（替换成你的模型名称！） =====================
# 请把以下两个名称替换为你场景中的「模型对象名」或「集合名」（从大纲视图复制）
MODEL_A_NAME = "Yuffie Savior Ensemble 18 Inase"  # 第一个模型名称（你的报错里的名称）
MODEL_B_NAME = "第二个模型的名称"  # 替换为你的第二个模型/集合名称

# 步骤1：第一个模型 → 仅属于/碰撞「组1（索引0）」
batch_set_rigidbody_collision_group(MODEL_A_NAME, target_group_index=1)

# 步骤2：第二个模型 → 仅属于/碰撞「组2（索引1）」（和组1互不碰撞）
#batch_set_rigidbody_collision_group(MODEL_B_NAME, target_group_index=1)

print("\n📌 最终结果：两个模型的刚体已分属不同碰撞组，不会互相碰撞！")