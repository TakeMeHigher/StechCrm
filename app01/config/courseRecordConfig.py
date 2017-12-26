from django.shortcuts import redirect,render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import  url
from django.forms import Form
from django.forms import fields
from django.forms import widgets



from  stark.service import v1
from app01 import models


class CourseRecordConfig(v1.StarkConfig):
    def teacher_display(self,obj=None,is_head=False):
        if is_head:
            return '老师'
        return obj.teacher.name

    #考勤
    def CheckWa(self,obj=None,is_head=False):
        if is_head:
            return '考勤'
        url='/stark/app01/studyrecord/?course_record=%s'%obj.id
        return mark_safe("<a href='%s'>考勤管理</a>"%url)


    def extra_url(self):
        app_model_name=self.model_class._meta.app_label,self.model_class._meta.model_name
        url_list=[
           url(r'^(\d+)/inputScore/$',self.wrap(self.inputScore),name='%s_%s_inputScore'%app_model_name)
        ]

        return url_list
    def inputScore(self,request,cr_id):
        if request.method=='GET':
            studyRecord_list=models.StudyRecord.objects.filter(course_record_id=cr_id)
            data=[]
            for studyRecord in studyRecord_list:
                SRForm=type('SRForm',(Form,),{
                    'score_%s'%studyRecord.id : fields.ChoiceField(models.StudyRecord.score_choices),
                    'homework_note_%s'%studyRecord.id :fields.ChoiceField(widget=widgets.Textarea(attrs={"style":'width:395px;height:45px'}))
                })
                data.append({"studyRecord":studyRecord,"form":SRForm(initial={'score_%s'%studyRecord.id:studyRecord.score,'homework_note_%s'%studyRecord.id:studyRecord.homework_note})})
            return render(request,'inputScore.html',{'data':data})
        else:
            data=request.POST
            print(data)
            for k,v in data.items():
                if k=='csrfmiddlewaretoken':
                    continue

                name,studyRecord_id=k.rsplit('_',1)

                data_dic={}
                if studyRecord_id in data_dic:
                    data_dic[studyRecord_id][name]=v
                else:
                    data_dic[studyRecord_id]={name:v}


                for id,dic in data_dic.items():
                    models.StudyRecord.objects.filter(id=id).update(**dic)


            return redirect(request.path_info)





    def scoreInput(self,obj=None,is_head=False):
        if is_head:
            return '成绩录入'
        url=reverse("stark:app01_courserecord_inputScore",args=(obj.id,))
        return mark_safe("<a href='%s'>成绩录入</a>"%url)

    list_display = ['class_obj','day_num',teacher_display,CheckWa,scoreInput]

    show_search_form = True
    search_fileds = ['course_title__contains','day_num__contains','course_memo__contains']

    combine_seach = [
        v1.FilterOption('class_obj'),
        v1.FilterOption('teacher')
    ]



    show_action = True

    def multi_del(self, request):
        id_list = request.POST.getlist('pk')
        # print(id_list,'****------')
        self.model_class.objects.filter(id__in=id_list).delete()
        return redirect(self.get_list_url())

    multi_del.short_desc = '批量删除'


    def multu_init(self,request):
        id_list=request.POST.getlist('pk')
        CourseRecord_list=models.CourseRecord.objects.filter(id__in=id_list).all()
        for courseRecord in CourseRecord_list:

            exists=models.StudyRecord.objects.filter(course_record=courseRecord).exists()
            if exists:
                continue

            class_obj=courseRecord.class_obj
            student_list=models.Student.objects.filter(class_list=class_obj)
            studyrecord_list=[]
            for student in student_list:
                studyrecord= models.StudyRecord(course_record=courseRecord,student=student)
                studyrecord_list.append(studyrecord)
            models.StudyRecord.objects.bulk_create(studyrecord_list)


    multu_init.short_desc='学生初始化'

    action_func_list = [multu_init,multi_del]