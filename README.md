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
9.rouffe (glistening grace)  	记得骨骼细分，使用"标准骨架.pmx"  小腿要合并



