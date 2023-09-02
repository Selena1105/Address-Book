# 功能实现：设计了一个父类，六个子类

# 父类Person，属性：姓名，性别，生日（mm-dd)，电话号码，邮件地址，类别
class Person(object):
    def __init__(self, name, gender, birthday, phone, email):
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.email = email



# 子类Student，增加属性：学校，学院，年级，专业
class Student(Person):
    def __init__(self, name, gender, birthday, phone, email, school_s, college_s, grade, major):
        super().__init__(name, gender, birthday, phone, email)

        self.school_s = school_s
        self.college_s = college_s
        self.grade = grade
        self.major = major



# 子类Friend，增加属性：认识地点，认识时间（非必填）
class Friend(Person):
    def __init__(self, name, gender, birthday, phone, email, place="", time=""):
        super().__init__(name, gender, birthday, phone, email)

        self.place = place
        self.time = time



# 子类Professor，增加属性：学校，学院，职务
class Professor(Person):
    def __init__(self, name, gender, birthday, phone, email, school_t, college_t, post):
        super().__init__(name, gender, birthday, phone, email)

        self.school_t = school_t
        self.college_t = college_t
        self.post = post



# 子类Colleague，增加属性：公司名称，部门，工作
class Colleague(Person):
    def __init__(self, name, gender, birthday, phone, email, company, department, job):
        super().__init__(name, gender, birthday, phone, email)

        self.company = company
        self.department = department
        self.job = job



# 子类Family，增加属性：亲属关系，家庭地址
class Family(Person):
    def __init__(self, name, gender, birthday, phone, email, relation, home_address):
        super().__init__(name, gender, birthday, phone, email)

        self.relation = relation
        self.home_address = home_address
        


# 子类Others，增加属性：备注（非必填）
class Others(Person):
    def __init__(self, name, gender, birthday, phone, email, note=""):
        super().__init__(name, gender, birthday, phone, email)
        
        self.note = note