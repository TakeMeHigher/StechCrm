from  django.shortcuts import redirect

from stark.service import v1
from  app01.permission.basePermission import BasePermission



class ClassListConfig(BasePermission,v1.StarkConfig):
    def school_display(self,obj=None,is_head=False):
        if is_head:
            return '校区'
        return obj.school.title

    def semester_course_display(self,obj=None,is_head=False):
        if is_head:
            return '课程名称'
        return '%s(%s期)'%(obj.course.name,obj.semester)

    def teachers_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '授课教师'

        teachers=obj.teachers.all()
        l=[]
        for teacher in teachers:
            l.append(teacher.username)
        return ','.join(l)

    def tutor_display(self,obj=None,is_head=False):
        if is_head:
            return '班主任'
        return obj.tutor.name


    def num_display(self,obj=None,is_head=False):
        if is_head:
            return '人数'
        return obj.student_set.all().count()


    list_display = [semester_course_display,'price',num_display,'start_date','graduate_date','memo',school_display,teachers_dispaly,tutor_display]
    show_search_form = True
    search_fileds = ['semester']

    show_action = True

    def multi_del(self, request):
        id_list = request.POST.getlist('pk')
        # print(id_list,'****------')
        self.model_class.objects.filter(id__in=id_list).delete()
        return redirect(self.get_list_url())

    multi_del.short_desc = '批量删除'

    def multi_info(self, request):
        pass

    multi_info.short_desc = '批量初始化'

    action_func_list = [multi_del, multi_info]
    show_combine_seach = True
    combine_seach=[
        v1.FilterOption('school',),
        v1.FilterOption('course',),
        v1.FilterOption('teachers',is_multi=True),
        v1.FilterOption('tutor',),
    ]