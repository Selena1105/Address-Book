# 功能实现：新增联系人信息

from Person import Student, Friend, Professor, Colleague, Family, Others
from sort import name_sort
import pandas as pd

#-----------------------------第一步---------------------------------------
# 下列所增加属性信息都应为文本形式
# 增加联系人，同学
# 输入：页面输入框内所有属性信息，输出：Student类对象
def add_student(name, gender, birthday, phone, email, school_s, college_s, grade, major):
    stu = Student(name, gender, birthday, phone, email, school_s, college_s, grade, major)
    return stu


# 增加联系人,老师
# 输入：页面输入框内所有属性信息，输出：Professor类对象
def add_professor(name, gender, birthday, phone, email, school_t, college_t, post):
    pro = Professor(name, gender, birthday, phone, email, school_t, college_t, post)
    return pro


# 增加联系人，朋友
# 输入：页面输入框内所有属性信息，输出：Friend类对象
def add_friend(name, gender, birthday, phone, email, place="", time=""):
    fri = Friend(name, gender, birthday, phone, email, place, time)
    return fri


# 增加联系人，同事
# 输入：页面输入框内所有属性信息，输出：Colleague类对象
def add_colleague(name, gender, birthday, phone, email, company, department, job):
    coll = Colleague(name, gender, birthday, phone, email, company, department, job)
    return coll
    

# 增加联系人，亲戚
# 输入：页面输入框内所有属性信息，输出：Family类对象
def add_family (name, gender, birthday, phone, email, relation, home_address):
    fam = Family(name, gender, birthday, phone, email,  relation, home_address)
    return fam


# 增加联系人，其他
# 输入：页面输入框内所有属性信息，输出：Others类对象
def add_others(name, gender, birthday, phone, email, note=""):
    oth = Others(name, gender, birthday, phone, email, note)
    return oth

# ------------------------------第二步-------------------------------------
# 增加联系人后更新数据库
# 输入：某一类型对象(包含对应属性），全部人DataFrame, 某一类型对应的DataFrame，一个存储所有星标联系人电话的list
# 输出：增加联系人后的全部人的新DataFrame按名字排序）， 某一类型的新DataFrame（按名字排序)

def update_df(person, all_df, type_df, phone_list):
    add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])
    all_df = pd.concat([all_df, add_all], ignore_index=True)
    all_df = name_sort(all_df, phone_list)
    
    if isinstance(person, Student):
        add_type = pd.DataFrame({"school":person.school_s, "college": person.college_s, "grade":person.grade, "major":person.major},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)

    elif isinstance(person, Friend):
        add_type = pd.DataFrame({"place": person.place, "time":person.time},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)

    elif isinstance(person, Professor):
        add_type = pd.DataFrame({"school":person.school_t, "college" :person.college_t, "post": person.post},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)

    elif isinstance(person, Colleague):
        add_type = pd.DataFrame({"company": person.company, "department" :person.department, "job": person.job},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)

    elif isinstance(person, Family):
        add_type = pd.DataFrame({"relation": person.relation, "home_address":person.home_address},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)
    
    elif isinstance(person, Others):
        add_type = pd.DataFrame({"note": person.note},index=[0])
        add_type = pd.concat([add_all, add_type], axis=1)
        type_df = pd.concat([type_df, add_type], ignore_index=True)
        type_df = name_sort(type_df, phone_list)
    
    return all_df, type_df

# all_df = pd.read_excel('data.xls', sheet_name='schoolmate')
# person = add_student("11", "11", "11", "11", "11", "aaa", "aaa", "aaa", "aaa")

# add_all = pd.DataFrame({"name":person.name,"gender":person.gender, "birthday":person.birthday, "phone":person.phone, "email":person.email},index=[0])

# add_type = pd.DataFrame({"school":"aaa", "college": "aaa", "grade": "aaa", "major":"aaa"},index=[0])
# # print(add_type)
# add_all = pd.concat([add_all, add_type], axis=1)
# all_df = pd.concat([all_df, add_all], ignore_index=True)
# print(all_df)
# # all_df = name_sort(all_df)
