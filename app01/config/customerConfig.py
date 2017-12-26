from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.http import QueryDict
from django.conf.urls import url

from stark.service import v1



class CustomerConfig(v1.StarkConfig):
    def gender_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '性别'
        return obj.get_gender_display()

    def education_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '学历'
        return obj.get_education_display()

    def experience_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '工作经验'
        return obj.get_experience_display()

    def work_status_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '职业状态'
        return obj.get_work_status_display()


    def source_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '客户来源'
        return obj.get_source_display()



    def referral_from_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '转介绍自学员'
        return obj.referral_from.name


    def consultant_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '课程顾问'
        return obj.consultant.name


    def course_dispaly(self,obj=None,is_head=False):
        if is_head:
            return '咨询课程'
        courses= obj.course.all()
        l=[]
        for course in courses:
            html='<div style="display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;">%s<a href="/stark/app01/customer/%s/%s/delete_cource/" >X</a></div>'%(course.name,obj.pk,course.pk)
            l.append(html)
        return mark_safe(''.join(l))


    def record_display(self,obj=None,is_head=False):
        if is_head:
            return '跟进记录'
        return  mark_safe('<a href="/stark/app01/consultrecord/?customer=%s">查看跟进记录</a>'%(obj.pk))





    list_display = ['qq','name',gender_dispaly,education_dispaly,'graduation_school','major',experience_dispaly,work_status_dispaly,'company','salary',source_dispaly
                    ,course_dispaly,'status',consultant_dispaly,record_display
                    ]

    show_search_form = True
    search_fileds = ['qq__contains','name__contains','graduation_school__contains','major__contains','company__contains','salary__contains']

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
    combine_seach = [
        v1.FilterOption('gender',is_choice=True),
        v1.FilterOption('education',is_choice=True),
        v1.FilterOption('experience',is_choice=True),
        v1.FilterOption('work_status',is_choice=True),
        v1.FilterOption('course',is_multi=True),
        v1.FilterOption('source',is_choice=True),
        v1.FilterOption('status',is_choice=True),
        v1.FilterOption('consultant'),
    ]


    def delete_cource(self,request,customer_id,course_id):
        customer=self.model_class.objects.filter(pk=customer_id).first()
        customer.course.remove(course_id)
        menu=self.request.GET.urlencode()
        print(menu)
        params=QueryDict(mutable=True)
        params[self.search_key]=menu
        print(params,'----------------------++++++++++++')
        url='%s?%s'%(self.get_list_url(),params.urlencode())
        return redirect(url)




    def extra_url(self):
        app_model_class=self.model_class._meta.app_label,self.model_class._meta.model_name
        patterns=[
            url(r'^(\d+)/(\d+)/delete_cource/$',self.wrap(self.delete_cource),name='%s_%s_dc'%app_model_class)
        ]
        return patterns