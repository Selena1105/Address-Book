# 实现功能：对数据进行多种方式的排序

import pandas as pd

# 打乱表格，用于测试排序代码

# 输入：未打乱的DataFrame，输出：打乱的DataFrame
def random_file(df):
    df_random = df.sample(frac = 1)
    print("打乱顺序成功")

    return df_random


# --------------------------------------------------------------------

# 按姓名字母排序

# 初次打开页面时使用，恢复按名字排序时使用，可用于所有类型
# 输入：未排序的DataFrame，输出：按名字排序的DataFrame
def name_sort(df, phone_list):
    # df = pd.DataFrame(df)
    
    # 查找出所有星标联系人,
    
    if not phone_list:
        star_df = pd.DataFrame()
        for phone in phone_list:
            star = df.query(f' phone == "{phone}" ')
            star_df = pd.concat([star_df, star], ignore_index=True)

            # 从原表中删掉
            star_row = df[df.phone == phone].index.tolist()
            df = df.drop(index = star_row )
    
    df_name = df.sort_values(by="name" , ascending=False) # 升序


    print("按姓名排序成功")

    return df_name
    

# 以下所有排序方式，若相同则再按照姓名字母排序



# 按生日顺序排序

# 按生日排序键时使用,可用于所有类型
# 输入：未排序的DataFrame，输出：按生日排序的DataFrame
def birthday_sort(df, phone_list):
    # df = pd.DataFrame(df)
    
    # 查找出所有星标联系人,
    
    if not phone_list:
        star_df = pd.DataFrame()
        for phone in phone_list:
            star = df.query(f' phone == "{phone}" ')
            star_df = pd.concat([star_df, star], ignore_index=True)

            # 从原表中删掉
            star_row = df[df.phone == phone].index.tolist()
            df = df.drop(index = star_row )
    

    df_bir = df.sort_values(by=["birthday","name"] ,ascending=[True,True])
    df_bir = pd.concat([star_df, df_bir], ignore_index=True)
    
    print("按生日排序成功")

    return df_bir



# 同学，按专业名字、年级排序

# 按专业排序键时使用,仅限同学类型
# 输入：未排序的DataFrame，输出：按专业排序的DataFrame
def student_major_sort(df):
    # df = pd.DataFrame(df)
    df_major = df.sort_values(by=["major", "grade", "name"] , ascending=[True,True,True]) # 升序
    print("同学按专业排序成功")

    return df_major



# 老师，按学院名字、职务名字排序

# 按学院排序键时使用,仅限老师类型
# 输入：未排序的DataFrame，输出：按学院名字、职务名字排序的DataFrame
def professor_college_sort(df):
    # df = pd.DataFrame(df)
    df_coll = df.sort_values(by=["college", "post", "name"], ascending=[True,True,True]) # 升序
    print("老师按学院、职务排序成功")

    return df_coll



# 同事，按公司名字、部门名字排序

# 按公司排序键时使用,仅限同事类型
# 输入：未排序的DataFrame，输出：按公司、部门排序的DataFrame
def colleague_company_sort(df):
    # df = pd.DataFrame(df)
    df_com = df.sort_values(by=["company", "department","name"], ascending=[True,True,True]) # 升序
    print("同事按公司、部门排序成功")

    return df_com



# 亲戚，按亲属关系排序

# 按亲属关系排序键时使用,仅限亲戚类型
# 输入：未排序的DataFrame，输出：按亲属关系排序的DataFrame
def family_relation_sort(df):
    # df = pd.DataFrame(df)
    df_rela = df.sort_values(by=["relation", "name"], ascending=[True,True]) # 升序
    print("亲戚按亲属关系按公司排序成功")
    
    return df_rela

