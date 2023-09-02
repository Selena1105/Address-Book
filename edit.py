import pandas as pd
import numpy as np
from sort import name_sort
import add

# 用于编辑信息模块的查找，根据电话返回某个联系人的类型
# 输入:电话，六个类别的分dataframe
# 输出：电话所对应联系人类别
def find_detail(phone, student_df, professor_df, friend_df, colleague_df, family_df, others_df):

    if (len(student_df[student_df.phone == phone].index.tolist()) != 0):
        type = "student"
    
    if (len( professor_df[ professor_df.phone == phone].index.tolist()) != 0):
        type = "professor"
    
    if (len(friend_df[student_df.phone == phone].index.tolist()) != 0):
        type = "friend"
    
    if (len(colleague_df[student_df.phone == phone].index.tolist()) != 0):
        type = "colleague"
    
    if (len(family_df[student_df.phone == phone].index.tolist()) != 0):
        type = "family"
    
    if (len(others_df[student_df.phone == phone].index.tolist()) != 0):
        type = "others"
    
    return type




# 修改联系人:先删除再新增
# 函数名字都是：edit_类名

# 输入：被修改联系人的修改前电话, 所有人的DataFrame，所对应类型的DataFrame, 修改后的所有内容（包括有修改、无修改，一个存储所有星标联系人电话的list
# ！！！注意输入的有旧phone 新phone 两个
# 输出：更新后的所有人的DataFrame，所对应类型的DataFrame

def edit_student(phone_old, all_df, type_df, name, phone, gender, birthday, email, school_s, college_s, grade, major, phone_list):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_student(name, gender, birthday, phone, email, school_s, college_s, grade, major)

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"school":person.school_s, "college": person.college_s, "grade":person.grade, "major":person.major},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df

def edit_professor(phone_old, all_df, type_df, name, gender, birthday, phone, email, school_t, college_t, post, phone_list):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_professor(name, gender, birthday, phone, email, school_t, college_t, post, phone_list)

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"school":person.school_t, "college" :person.college_t, "post": person.post},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df


def edit_friend(phone_old, all_df, type_df, name, gender, birthday, phone, email, phone_list, place="", time="", ):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_friend(name, gender, birthday, phone, email, place="", time="")

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"place": person.place, "time":person.time},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df


def edit_colleague(phone_old, all_df, type_df, name, gender, birthday, phone, email, company, department, job, phone_list):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_colleague(name, gender, birthday, phone, email, company, department, job)

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"company": person.company, "department" :person.department, "job": person.job},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df


def edit_family(phone_old, all_df, type_df, name, gender, birthday, phone, email, relation, home_address, phone_list):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_family (name, gender, birthday, phone, email, relation, home_address)

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"relation": person.relation, "home_address":person.home_address},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df


def edit_others(phone_old, all_df, type_df, name, gender, birthday, phone, email, phone_list, note=""):
    
    # 更新总数据库

    all_row = all_df[all_df.phone == phone_old].index.tolist()
    all_df = all_df.drop(index = all_row ) 
    all_df = name_sort(all_df, phone_list)

    # 更新分数据库

    type_row = all_df[all_df.phone == phone_old].index.tolist()
    type_df = all_df.drop(index = type_row ) 
    type_df = name_sort(type_df, phone_list)

    print("删除联系人成功")

    # 新增联系人

    person = add.add_others(name, gender, birthday, phone, email, note="")

    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)

    add_type = pd.DataFrame({"note": person.note},index=[0])
    add_type = pd.concat([add_all, add_type], axis=1)
    type_df = pd.concat([type_df, add_type], ignore_index=True)
    type_df = name_sort(type_df, phone_list)

    print("修改联系人成功")

    return all_df, type_df