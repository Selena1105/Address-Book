# 功能实现： 删除联系人信息

import pandas as pd
import numpy as np
from sort import name_sort


# 删除联系人(为避免误删，只删除返回结果的第一项)

# 输入：被删除联系人的电话(为了确保不会有重复），所有人、6个分类共7个DataFrame，一个存储所有星标联系人电话的list
# 输出：更新后的所有人、6个分类共7个DataFrame

def delete(phone, all_df, student_df, professor_df, friend_df, colleague_df, family_df, others_df, phone_list):

    # 更新总数据库
    all_row = all_df[all_df.phone == phone].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)
    print("删除总联系人成功")

    # 更新分数据库

    if (len(student_df[student_df.phone == phone].index.tolist()) != 0):
        print("已进入")

        flag = student_df[student_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        student_df=student_df.drop(index = type_row )
        print("删除联系人成功")
        student_df=name_sort(student_df, phone_list)
    
    elif  ( len(professor_df[ professor_df.phone == phone].index.tolist())!= 0):
        print("已进入")
        flag =  professor_df[professor_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        professor_df=professor_df.drop(index = type_row )
        print("删除联系人成功")
        professor_df=name_sort(professor_df, phone_list)
    
    elif  (len(friend_df[friend_df.phone == phone].index.tolist())!= 0):
        print("已进入")
        flag = friend_df[friend_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        friend_df=friend_df.drop(index = type_row )
        print("删除联系人成功")
        friend_df=name_sort(friend_df, phone_list)
    
    elif  (len(colleague_df[colleague_df.phone == phone].index.tolist())!= 0):
        print("已进入")
        flag = colleague_df[colleague_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        colleague_df=colleague_df.drop(index = type_row )
        print("删除联系人成功")
        colleague_df=name_sort(colleague_df, phone_list)
    
    elif  (len(family_df[family_df.phone == phone].index.tolist())!= 0):
        print("已进入")
        flag = family_df[family_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        family_df=family_df.drop(index = type_row )
        print("删除联系人成功")
        family_df=name_sort(family_df, phone_list)
    
    elif  ( len(others_df[ others_df.phone == phone].index.tolist())!= 0):
        print("已进入")
        flag =  others_df[ others_df.phone == phone].index.tolist()
        # flag非空，已找到
        type_row = flag
        others_df=others_df.drop(index = type_row )
        print("删除联系人成功")
        others_df=name_sort( others_df, phone_list)


    return all_df, student_df, professor_df, friend_df, colleague_df, family_df, others_df




