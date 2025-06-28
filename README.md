# blender 对齐骨骼

rename_xps2mmd.py 把xps文件重新命名

align_bones_xps2mmd.py 把xps骨骼和pmx骨骼对齐

align_shoulder_xps2mmd.py肩膀等部分骨骼需要单独平移动对齐

merge_adjacent_bones.py，如果胳膊是两段骨骼，需要合并骨骼

##########
1.first 原始版本
2.cartilla  这里修改的一点
3.inase_arbiter
4.misaki
5.rouffe   简化版本
6.cartilla/white rose 使用“标准骨架.pmx” 2025.06.02
7.Arbiter  使用“标准骨架.pmx” 2025.06.07
8.Eve (Neurolink Suit)- Stellar Blade  使用"标准骨架.pmx" 2025.06.08
	rename_xps2mmd:去掉rhand和rToe，lhand和lToe，neckLower,首，足首.L,足首.R, 放到merge_vetex_group_hand.py 里合并定点组
9.rouffe (glistening grace)  	记得骨骼细分，使用"标准骨架.pmx"  小腿要合并,对齐手捩骨，似乎还是弯曲的
10.alana (archdemon baal)    
	使用“标准骨骼与刚体.pmx”，
	合并骨骼：小腿合并，ひじ.L要合并 关节骨，手臂，手捩骨 ，三个，否则 会有弯曲问题，
	rename中去掉 ひざD.R和ひじ.R，merge_vetex_group_leg.py里面建立
11.rouffe glistening grace 2 重新做一次 
	使用“标准骨架_g.pmx”,不用处理上半身1了,但是这个不行，还是使用“标准骨骼与刚体.pmx”重新建，细分上半身1，
	检查小腿的权重，是两个需要合并，使用 merge_vetex_group_leg 
	手捩骨不应单独权重？，手臂的骨骼，和手腕的骨骼叶合并一下，，也是在merge_vetex_group_leg
	问题：关节不自然，还是手臂错位，是不是vmd的问题呀，捩骨到底用户用控制顶点权重呀？
	


