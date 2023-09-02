# 实现功能：对数据的文本内容进行查找

import pandas as pd

# 查找功能：1 单条件精确查找，2 双条件精确查找， 3 单条件模糊查找， 4 双条件模糊查找 
# 每种类型的查找都支持多种不同属性、多表查找，可用于总的DataFrame,每个类型单独的DataFrame

# 输入：所查的DataFrame，所查的类型（all, student, professor, friend, colleague, family, others), 目标内容
# 输出：包含flag(int)表示是否有返回，找到返回1，没找到返回0；还返回包含所有查找结果的DataFrame(如果没找到为空)

# -----------------------------------------------------------------------------------

# 第一类

# 单条件，全属性，模糊查找，包含就返回
def find_single_vague(df, type, content):
    if content == '':
        return df
    attri = []
    new_df = pd.DataFrame()

    # 添加不同类型的可查找属性值

    if type == "all":
        attri = ["name", "gender"]

    elif type == "student":
        attri = ["name", "gender",  "school", "college",  "major"]

    elif type == "professor":
        attri = ["name", "gender",  "school", "college", "post"]

    elif type == "friend":
        attri = ["name", "gender", "place"]

    elif type == "colleague":
        attri = ["name", "gender",  "company", "department", "job"]

    elif type == "family":
        attri = ["name", "gender",  "relation", "home_address"]

    elif type == "others":
        attri = ["name", "gender",  "note"]
    

    for a in attri:
        try:
            temp = df[df[a].str.contains(content)]
            if temp.index.tolist() != []:
                new_df = pd.concat([new_df, temp], ignore_index=True)
        except:
            pass
    # 根据是否找到返回不同类型
    return new_df



# 单条件，全属性，精确查找，完全一致才返回
def find_single(df, type, content):

    attri = []
    flag = 0
    new_df = pd.DataFrame()

    # 添加不同类型的可查找属性值

    if type == "all":
        # attri = ["name", "gender", "birthday", "phone", "email" ]
        attri = ["name", "gender", "birthday"]

    elif type == "student":
        attri = ["name", "gender", "birthday" , "school", "college",  "major"]

    elif type == "professor":
        attri = ["name", "gender", "birthday", "school", "college", "post"]

    elif type == "friend":
        attri = ["name", "gender", "birthday", "place", "time"]

    elif type == "colleague":
        attri = ["name", "gender", "birthday", "company", "department", "job"]

    elif type == "family":
        attri = ["name", "gender", "birthday", "relation", "home_address"]

    elif type == "others":
        attri = ["name", "gender", "birthday", "note"]
    
    for a in attri:
        if not (df.query(f'{a} == "{content}" ')).empty:
            flag = 1
            add = df.query(f'{a}.str.contains("{content}")')
            new_df = pd.concat([new_df, add], ignore_index=True)
    
    # 根据是否找到返回不同类型
    return flag, new_df

# -------------------------------------------------------------------------
# 第二类

# 单条件，指定属性，精确查找
def sfind_single(df, content_1, attri_1 = "phone"):
    # df = pd.DataFrame(df) 
    new_df = df.query(f' {attri_1} == "{content_1}" ')

    return new_df



# 单条件，指定属性，模糊查找
def sfind_single_vague(df, attri_1, content_1):
    # df = pd.DataFrame(df)
    new_df = df.query(f' {attri_1}str.contains("{content_1}") ')

    return new_df

# --------------------------------------------------------------------
# 第三类

# 双条件，指定属性，精确查找
def sfind_double(df, attri_1, attri_2, content_1, content_2):
    # df = pd.DataFrame(df) 
    new_df = df.query(f' {attri_1} == "{content_1}" & {attri_2} == "{content_2}"')

    return new_df



# 双条件，指定属性，模糊查找
def sfind_double_vague(df, attri_1, attri_2, content_1, content_2):
    # df = pd.DataFrame(df)
    new_df = df.query(f' {attri_1}str.contains("{content_1}") & {attri_2}str.contains("{content_2}")')

    return new_df

# ---------------------------------------------------------------------

# 用于编辑信息模块的查找，根据电话返回某个联系人的类型
# 输入:电话，六个类别的分dataframe
# 输出：电话所对应联系人类别
def find_detail(phone, student_df, professor_df, friend_df, colleague_df, family_df, others_df):
    info_df = pd.DataFrame()
    print("*" * 60)
    print(student_df)
    print("*"*60)
    print("*" * 60)
    print(professor_df)
    print("*" * 60)
    print("*" * 60)
    print(friend_df)
    print("*" * 60)
    print("*" * 60)
    print(colleague_df)
    print("*" * 60)
    print("*" * 60)
    print(family_df)
    print("*" * 60)
    print("*" * 60)
    print(others_df)
    print("*" * 60)

    if (len(student_df[student_df.phone == phone].index.tolist()) != 0):
        print("sss")
        info_df=sfind_single(student_df, phone)
    print(professor_df[professor_df.phone == phone].index.tolist())
    if (len(professor_df[professor_df.phone == phone].index.tolist()) != 0):
        print(professor_df)
        print("sss")
        info_df=sfind_single(professor_df, phone)
    
    if (len(friend_df[friend_df.phone == phone].index.tolist()) != 0):
        print(friend_df)
        print("sss")
        info_df=sfind_single(friend_df, phone)
    
    if (len(colleague_df[colleague_df.phone == phone].index.tolist()) != 0):
        print(colleague_df)
        print("sss")
        info_df=sfind_single(colleague_df, phone)
    
    if (len(family_df[family_df.phone == phone].index.tolist()) != 0):
        print(family_df)
        print("sss")
        info_df=sfind_single(family_df, phone)
    
    if (len(others_df[others_df.phone == phone].index.tolist()) != 0):
        print(others_df)
        print("sss")
        info_df=sfind_single(others_df, phone)
    
    return info_df



# 测试代码
# df = pd.read_excel('data.xls', sheet_name='all')
# if df.query(' name.str.contains("Se")').empty: 
#     print(1)