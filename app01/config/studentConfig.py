import json

from django.shortcuts import redirect,render,HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import url



from stark.service import v1
from app01 import  models


class StudentConfig(v1.StarkConfig):

    def extra_url(self):
        app_model_name=self.model_class._meta.app_label,self.model_class._meta.model_name
        url_list=[
          url(r'^(\d+)/view_score/$',self.wrap(self.view_score),name='%s_%s_view_score'%app_model_name),
          url(r'^score_list/$',self.wrap(self.score_list),name='%s_%s_score_list'%app_model_name)
        ]

        return url_list
    #查看成绩先列出班级
    def view_score(self,request,id):
        if request.method=='GET':
            student=models.Student.objects.filter(id=id).first()
            print(student.username)
            if  not student:
                return HttpResponse("查无此人")
            cls_list=student.class_list.all()
            print(cls_list,'****')
            return render(request,'viewScore.html',{"cls_list":cls_list,'sid':id})
    #查看成绩 返回data 给柱状图
    def score_list(self,request):
        ret = {'status': False, 'data': None, 'msg': None}
        try:
            #class_id
            cid=request.GET.get('cid')
            #student_id
            sid=request.GET.get('sid')
            studyRecord_list=models.StudyRecord.objects.filter(course_record__class_obj_id=cid,student_id=sid)
            print(studyRecord_list)
            data=[]
            for studyRecord in studyRecord_list:
                day_num=studyRecord.course_record.day_num
                data.append([day_num,studyRecord.score])
            ret['status']=True
            ret['data']=data


        except Exception as e:
            ret['msg'] = '无法获取'
        return HttpResponse(json.dumps(ret))



    def seeScore(self,obj=None,is_head=False):
        if is_head:
            return '查看成绩'
        url=reverse('stark:app01_student_view_score',args=(obj.id,))
        return mark_safe("<a href='%s'>查看成绩</a>"%url)



    list_display = ['username',seeScore]

    show_action = True

    def multi_del(self, request):
        id_list = request.POST.getlist('pk')
        # print(id_list,'****------')
        self.model_class.objects.filter(id__in=id_list).delete()
        return redirect(self.get_list_url())

    multi_del.short_desc = '批量删除'



    action_func_list = [multi_del]

    show_search_form = True
    search_fileds = ['username__contains']

    combine_seach=[
        v1.FilterOption('customer'),
        v1.FilterOption('class_list',is_multi=True),
    ]