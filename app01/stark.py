from stark.service import v1
from app01 import models
from app01.config.deparentConfig import DepartmentConfig
from app01.config.userinfoConfig import UserInfoConfig
from app01.config.courseConfig import CourseConfig
from app01.config.schoolConfig import SchoolConfig
from app01.config.classListConfig import ClassListConfig
from app01.config.customerConfig import  CustomerConfig
from app01.config.consultRecordConfig import ConsultRecordConfig
from app01.config.paymentRecordConfig import PaymentRecordConfig
from app01.config.studentConfig import StudentConfig
from app01.config.courseRecordConfig import CourseRecordConfig
from app01.config.studyRecordConfig import StudyRecordConfig


v1.site.register(models.Department,DepartmentConfig)
v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Course,CourseConfig)
v1.site.register(models.School,SchoolConfig)
v1.site.register(models.ClassList,ClassListConfig)
v1.site.register(models.Customer,CustomerConfig)
v1.site.register(models.ConsultRecord,ConsultRecordConfig)
v1.site.register(models.PaymentRecord,PaymentRecordConfig)
v1.site.register(models.Student,StudentConfig)
v1.site.register(models.CourseRecord,CourseRecordConfig)
v1.site.register(models.StudyRecord,StudyRecordConfig)