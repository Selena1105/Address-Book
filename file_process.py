import pandas as pd

# 读入xlsx数据，在程序一开始调用
# 输入：无，输出：7个DataFrame，包括所有人及六个分类

def getData(filepath = 'data.xls'):
    all_df =  pd.read_excel(filepath, sheet_name='all')
    schoolmate_df = pd.read_excel(filepath, sheet_name='schoolmate')
    teacher_df = pd.read_excel(filepath, sheet_name='teacher')
    friend_df = pd.read_excel(filepath, sheet_name='friend')
    colleague_df = pd.read_excel(filepath, sheet_name='colleague')
    family_df = pd.read_excel(filepath, sheet_name='family')
    others_df = pd.read_excel(filepath, sheet_name='others')
    print("读取数据库成功！")
    return all_df, schoolmate_df, teacher_df, friend_df, colleague_df, family_df, others_df

    
# 存入xlsx数据，在程序最终结束时调用
# 输入：7个DataFrame，输出：无

def saveData(all_df, schoolmate_df, teacher_df, friend_df, colleague_df, family_df, others_df, filepath = 'data.xls' ):
    with pd.ExcelWriter(filepath) as writer:
        all_df.to_excel(writer, sheet_name = 'all', index = False)
        schoolmate_df.to_excel(writer, sheet_name = 'schoolmate', index = False)
        teacher_df.to_excel(writer, sheet_name = 'teacher', index = False)
        friend_df.to_excel(writer, sheet_name = 'friend', index = False)
        colleague_df.to_excel(writer, sheet_name = 'colleague', index = False)
        family_df.to_excel(writer, sheet_name = 'family', index = False)
        others_df.to_excel(writer, sheet_name = 'others', index = False)
        print("更新数据库成功 !")