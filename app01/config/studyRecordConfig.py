
from stark.service import v1
from app01 import models



class StudyRecordConfig(v1.StarkConfig):


    def student_display(self,obj=None,is_head=False):
        if is_head:
            return '学员'
        return obj.student.username

    def record_displaty(self,obj=None,is_head=False):
        if is_head:
            return '出勤'
        return obj.get_record_display()

    def score_display(self,obj=None,is_head=False):
        if is_head:
            return  '本节成绩'

        return obj.get_score_display()

    list_display = ['course_record',student_display,record_displaty,
                    score_display
                    ]

    show_search_form = True
    search_fileds =['date__contains','stu_memo__contains','homework_note__contains','note__contains']

    combine_seach = [
        v1.FilterOption('course_record'),
        v1.FilterOption('student'),
    ]


    def checked(self,request):
        id_list=request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=id_list).update(record='checked')

    checked.short_desc='已签到'

    def vacate(self, request):
        id_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=id_list).update(record='vacate')

    vacate.short_desc = '请假'


    def late(self,request):
        id_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=id_list).update(record='late')

    late.short_desc='迟到'

    def noshow(self, request):
        id_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=id_list).update(record='noshow')


    noshow.short_desc = '缺勤'

    def leave_early(self,request):
        id_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=id_list).update(record='leave_early')

    leave_early.short_desc='早退'


    show_action = True
    action_func_list = [checked,vacate,late,noshow,leave_early]

    add_btn = False