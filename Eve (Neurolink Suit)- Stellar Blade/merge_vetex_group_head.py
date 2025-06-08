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
    "head",
    "lowerJaw",
    "lNasolabialLower",
    "rNasolabialLower",
    "lNasolabialMouthCorner",
    "rNasolabialMouthCorner",
    "lLipCorner",
    "lLipLowerOuter",
    "lLipLowerInner",
    "LipLowerMiddle",
    "rLipLowerInner",
    "rLipLowerOuter",
    "rLipCorner",
    "LipBelow",
    "Chin",
    "lCheekLower",
    "rCheekLower",
    "BelowJaw",
    "lJawClench",
    "rJawClench",
    "rBrowInner",
    "rBrowMid",
    "rBrowOuter",
    "lBrowInner",
    "lBrowMid",
    "lBrowOuter",
    "CenterBrow",
    "MidNoseBridge",
    "lEyelidInner",
    "lEyelidUpper",
    "lEyelidUpperInner",
    "lEyelidUpperOuter",
    "lEyelidOuter",
    "lEyelidLower",
    "lEyelidLowerOuter",
    "lEyelidLowerInner",
    "rEyelidInner",
    "rEyelidUpper",
    "rEyelidUpperInner",
    "rEyelidUpperOuter",
    "rEyelidOuter",
    "rEyelidLower",
    "rEyelidLowerOuter",
    "rEyelidLowerInner",
    "lSquintInner",
    "lSquintOuter",
    "rSquintInner",
    "rSquintOuter",
    "lCheekUpper",
    "rCheekUpper",
    "Nose",
    "lNostril",
    "rNostril",
    "lLipBelowNose",
    "rLipBelowNose",
    "lLipNasolabialCrease",
    "rLipNasolabialCrease",
    "lNasolabialUpper",
    "rNasolabialUpper",
    "lNasolabialMiddle",
    "rNasolabialMiddle",
    "LipUpperMiddle",
    "lLipUpperOuter",
    "lLipUpperInner",
    "rLipUpperInner",
    "rLipUpperOuter",
    "lEar",
    "rEar",
    
    "HairRoot",
    "Ab-HairVFLL01",
    "Ab-HairVFLL02",
    "Ab-HairVFL01",
    "Ab-HairVFL02",
    "Ab-HairVFR01",
    "Ab-HairVFR02",
    "Ab-HairVFRR01",
    "Ab-HairVFRR02",
    
    "Bip001-Head",
    "Ab-TL-HairB01",
    "Ab-TL-HairB02",
    "Ab-TL-HairB03",
    "Ab-TL-HairB04",
    "Ab-TL-HairB05",
    "Ab-TL-HairB06",
    "Ab-TL-HairB07",
    "Ab-TL-HairB08",
    "Ab-TL-HairB09",
    
    "Point003",
    "AB_WP02_Gear02",
    "AB_WP02_Gear03",
    "AB_WP02_Gear04",
    "AB_WP02_Gear05",
    "AB_WP02_Gear06",
    "AB_WP02_Gear07",
    "AB_WP02_Gear08",
    "AB_WP02_Gear09",
    "AB_WP02_Body2",
    "AB_WP02_Body",
    "AB_WP02_Top",
    "AB_WP02_TopL",
    "AB_WP02_TopR",
    "AB_WP02_TopT",
    "AB_WP02_TopC",
    "AB_WP02_TopL2",
    "AB_WP02_TopR2",
    "AB_WP02_BodyWLK",
    "AB_WP02_BodyWLF",
    "AB_WP02_BodyWRK",
    "AB_WP02_BodyWRF",
    "AB_WP02_Panel01",
    "AB_WP02_Panel02",
    "AB_WP02_Panel03",
    "AB_WP02_Panel04",
    "AB_WP02_Panel05",
    "AB_WP02_Panel06",
    "AB_WP02_Panel07",
    "AB_WP02_Gear01",
    "AB_WP02_Main_UP",
    "AB_WP02_Main_Dn",
    "AB_WP02_Tap4",
    "AB_WP02_Grip",
    "AB_WP02_Grip_sub",
    "AB_WP02_Tap1",
    "AB_WP02_Tap2",
    "AB_WP02_Tap3",
    "AB_WP02_Tap3_sub",

#    "下面是另一种",

]

# 新顶点组的名称
new_group_name = "頭"

# 调用函数合并顶点组
merge_vertex_groups(obj, group_names, new_group_name)