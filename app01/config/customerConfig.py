import datetime

from django.db.models import Q
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, HttpResponse, render
from django.http import QueryDict
from django.conf.urls import url
from django.forms import ModelForm


from stark.service import v1
from app01 import models


class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', 'status', 'recv_date', 'last_consult_date']


class CustomerConfig(v1.StarkConfig):
    def gender_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '性别'
        return obj.get_gender_display()

    def education_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '学历'
        return obj.get_education_display()

    def experience_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '工作经验'
        return obj.get_experience_display()

    def work_status_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '职业状态'
        return obj.get_work_status_display()

    def source_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '客户来源'
        return obj.get_source_display()

    def referral_from_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '转介绍自学员'
        return obj.referral_from.name

    def consultant_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '课程顾问'
        return obj.consultant.name

    def course_dispaly(self, obj=None, is_head=False):
        if is_head:
            return '咨询课程'
        courses = obj.course.all()
        l = []
        for course in courses:
            html = '<div style="display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;">%s<a href="/stark/app01/customer/%s/%s/delete_cource/" >X</a></div>' % (
                course.name, obj.pk, course.pk)
            l.append(html)
        return mark_safe(''.join(l))

    def record_display(self, obj=None, is_head=False):
        if is_head:
            return '跟进记录'
        return mark_safe('<a href="/stark/app01/consultrecord/?customer=%s">查看跟进记录</a>' % (obj.pk))

    def status_display(self, obj=None, is_head=False):
        if is_head:
            return '状态'
        return obj.get_status_display()

    list_display = ['qq', 'name', gender_dispaly, education_dispaly, 'graduation_school', 'major', experience_dispaly,
                    work_status_dispaly, 'company', 'salary', source_dispaly
        , course_dispaly, status_display, consultant_dispaly, record_display
                    ]

    show_search_form = True
    search_fileds = ['qq__contains', 'name__contains', 'graduation_school__contains', 'major__contains',
                     'company__contains', 'salary__contains']

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
        v1.FilterOption('gender', is_choice=True),
        v1.FilterOption('education', is_choice=True),
        v1.FilterOption('experience', is_choice=True),
        v1.FilterOption('work_status', is_choice=True),
        v1.FilterOption('course', is_multi=True),
        v1.FilterOption('source', is_choice=True),
        v1.FilterOption('status', is_choice=True),
        v1.FilterOption('consultant'),
    ]

    def delete_cource(self, request, customer_id, course_id):
        """
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        """
        customer = self.model_class.objects.filter(pk=customer_id).first()
        customer.course.remove(course_id)
        menu = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self.search_key] = menu
        url = '%s?%s' % (self.get_list_url(), params.urlencode())
        return redirect(url)

    def public_view(self, request):
        """
        公共客户资源
        :param request:
        :return:
        """
        # 条件：未报名 并且 （ 15天未成单(当前时间-15 > 接客时间) or  3天未跟进(当前时间-3天>最后跟进日期) ） Q对象
        # status=2
        # 方法一
        # con = Q()
        # con1 = Q()
        # con1.children.append(('status', 2))
        #
        # con2 = Q()
        # con2.connector = 'OR'
        # import datetime
        # now_date = datetime.datetime.now().date()
        # order_deadtime = now_date - datetime.timedelta(days=15)
        # talk_deadtime = now_date - datetime.timedelta(days=3)
        #
        # con2.children.append(('recv_date__lt', order_deadtime))
        # con2.children.append(('last_consult_date__lt', talk_deadtime))
        #
        # con.add(con1, 'AND')
        # con.add(con2, 'AND')
        # print(con, '------')
        # if con:
        #     customers = models.Customer.objects.filter(con).all()
        #     print(customers, '*****')
        # 方法二:

        now_date = datetime.datetime.now().date()
        order_deadtime = now_date - datetime.timedelta(days=15)
        talk_deadtime = now_date - datetime.timedelta(days=3)
        customers = models.Customer.objects.filter(
            Q(recv_date__lt=order_deadtime) | Q(last_consult_date__lt=talk_deadtime), status=2).all()

        return render(request, 'public_customer_view.html', {"customers": customers})

    def myuser_view(self, request):
        '''
        我的客户
        :param request:
        :return:
        '''

        current_user_id = 5

        customers_list = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')
        print(customers_list, '---')
        return render(request, 'myuser.html', {'customers': customers_list})

    def competition_view(self, request, cid):
        '''
        抢单
        条件:必须原顾问不是自己 状态必须是未报名 并且 （15天未成单(当前时间-15 > 接客时间) or  3天未跟进(当前时间-3天>最后跟进日期) ）
        :param request:
        :param cid: 客户id
        :return:
        '''

        current_usr_id = 5
        now_date = datetime.datetime.now().date()
        order_deadtime = now_date - datetime.timedelta(days=15)
        talk_deadtime = now_date - datetime.timedelta(days=3)
        update_count = models.Customer.objects.filter(
            Q(recv_date__lt=order_deadtime) | Q(last_consult_date__lt=talk_deadtime), status=2,id=cid).exclude(
            consultant_id=current_usr_id).update(consultant_id=current_usr_id, last_consult_date=now_date,
                                                 recv_date=now_date)
        if not update_count:
            return HttpResponse("抢单失败")

        models.CustomerDistribution.objects.create(user_id=current_usr_id,customer_id=cid,ctime=now_date)
        return HttpResponse('抢单成功')




    def singleInput_view(self,request):
        if request.method=='GET':
            form=SingleModelForm()
            return render(request,'')




    def extra_url(self):
        app_model_class = self.model_class._meta.app_label, self.model_class._meta.model_name
        patterns = [
            url(r'^(\d+)/(\d+)/delete_cource/$', self.wrap(self.delete_cource), name='%s_%s_dc' % app_model_class),
            url(r'^public/$', self.wrap(self.public_view), name='%s_%s_public' % app_model_class),
            url(r'^myuser/$', self.wrap(self.myuser_view), name='%s_%s_myuser' % app_model_class),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition" % app_model_class),
            url(r'^singleInput/$', self.wrap(self.singleInput_view), name='%s_%s_singleInput' % app_model_class),
        ]
        return patterns
