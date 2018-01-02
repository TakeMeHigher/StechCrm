import datetime

from django.db import transaction
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, HttpResponse, render
from django.http import QueryDict
from django.conf.urls import url
from django.forms import ModelForm
from django.http import StreamingHttpResponse

from stark.service import v1
from app01 import models
from stark.utils import message


# from tiga import  Tiga as t
# from tiga1 import  Tiga




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

    order_list = ['-status']

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
        # 条件：未报名 status=2 并且 （15天未成单(当前时间-15 > 接客时间) or  3天未跟进(当前时间-3天>最后跟进日期) ） Q对象

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
        current_user_id = 5
        now_date = datetime.datetime.now().date()
        order_deadtime = now_date - datetime.timedelta(days=15)
        talk_deadtime = now_date - datetime.timedelta(days=3)
        customers = models.Customer.objects.filter(
            Q(recv_date__lt=order_deadtime) | Q(last_consult_date__lt=talk_deadtime), status=2).all()

        return render(request, 'public_customer_view.html',
                      {"customers": customers, 'current_user_id': current_user_id})

    def myuser_view(self, request):
        '''
        我的客户
        :param request:
        :return:
        '''
        current_user_id = request.session['user'].get("id")

        customers_list = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')

        return render(request, 'myuser.html', {'customers': customers_list})

    def competition_view(self, request, cid):
        '''
        抢单
        条件:必须原顾问不是自己 状态必须是未报名 并且 （15天未成单(当前时间-15 > 接客时间) or  3天未跟进(当前时间-3天>最后跟进日期) ）
        :param request:
        :param cid: 客户id
        :return:
        '''

        current_usr_id = request.session['user'].get('id')
        now_date = datetime.datetime.now().date()
        order_deadtime = now_date - datetime.timedelta(days=15)
        talk_deadtime = now_date - datetime.timedelta(days=3)
        update_count = models.Customer.objects.filter(
            Q(recv_date__lt=order_deadtime) | Q(last_consult_date__lt=talk_deadtime), status=2, id=cid).exclude(
            consultant_id=current_usr_id).update(consultant_id=current_usr_id, last_consult_date=now_date,
                                                 recv_date=now_date)
        if not update_count:
            return HttpResponse("抢单失败")

        models.CustomerDistribution.objects.create(user_id=current_usr_id, customer_id=cid, ctime=now_date)
        return HttpResponse('抢单成功')

    def singleInput_view(self, request):
        if request.method == 'GET':
            form = SingleModelForm()
            return render(request, 'singleInput.html', {'form': form})
        else:
            """客户表新增数据：
                             - 获取该分配的课程顾问id
                             - 当前时间
                          客户分配表中新增数据
                             - 获取新创建的客户ID
                             - 顾问ID
                          """
            form = SingleModelForm(data=request.POST)
            if form.is_valid():

                from tiga1 import Tiga
                user_id = Tiga.get_sale_id()
                if not user_id:
                    return HttpResponse('无销售顾问,无法进行分配')
                try:
                    with transaction.atomic():
                        now_date = datetime.datetime.now().date()
                        # form.cleaned_data['consultant_id'] = user_id
                        # form.cleaned_data['status'] = 2
                        # form.cleaned_data['last_consult_date'] = now_date
                        # form.cleaned_data['recv_date'] = now_date
                        # course = form.cleaned_data.pop('course')
                        # customer = models.Customer.objects.create(**form.cleaned_data)
                        # print(form)
                        # customer.course.add(*course)
                        form.instance.consultant_id = user_id
                        form.instance.last_consult_date = now_date
                        form.instance.recv_date = now_date
                        customer = form.save()
                        print(customer)
                        print('.....')
                        models.CustomerDistribution.objects.create(customer=customer, user_id=user_id, ctime=now_date)
                        body = '给你分配新用户了'
                        print(564123)
                        message.send_message('分配新用户', body, '1789920207@qq.com', 'zjm')

                except Exception as e:
                    # Tiga.rollback(user_id)
                    return HttpResponse('录入异常')

                return redirect('/stark/app01/customer/')

            return render(request, 'singleInput.html', {'form': form})

    def multiInput_view(self, request):
        if request.method == 'GET':
            return render(request, 'multiInput.html')
        else:
            from tiga1 import Tiga
            user_id = Tiga.get_sale_id()
            now_date = datetime.datetime.now().date()
            fileObj = request.FILES.get('file')
            # with open('multiInput.xlsx', 'wb')as f:
            #     for chuck in fileObj:
            #         f.write(chuck)

            import xlrd
            #workbook = xlrd.open_workbook('multiInput.xlsx')
            workbook = xlrd.open_workbook(file_contents=fileObj.read())
            sheet = workbook.sheet_by_index(0)
            maps = {
                0: 'qq',
                1: 'name',
                2: 'gender',
                3: 'course',
            }

            for index in range(1, sheet.nrows):
                row = sheet.row(index)
                dic = {}
                for i in maps:
                    key = maps[i]
                    cell = row[i]
                    if i in (0, 2):
                        dic[key] = int(cell.value)
                    elif i == 1:
                        dic[key] = cell.value
                    else:
                        course_id = cell.value
                        course_list_str = course_id.split('_')
                        course_list_int = []
                        for i in course_list_str:
                            course_list_int.append(int(i))
                        dic[key] = course_list_int

                print(dic)
                try:
                    with transaction.atomic():

                        dic['consultant_id'] = user_id
                        dic['recv_date'] = now_date
                        print(dic)
                        print(type(dic['qq']))
                        course_list = dic.pop('course')
                        print(dic)
                        print(course_list)
                        customer = models.Customer.objects.create(**dic)
                        customer.course.add(*course_list)
                        print(customer)
                        models.CustomerDistribution.objects.create(customer=customer, user_id=user_id, ctime=now_date)

                except Exception as e:
                    Tiga.rollback(user_id)
                    return HttpResponse('批量导入出现异常')

            return HttpResponse('ok')

    def downtemplate_view(self, request):
        # do something...

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = "模板.xlsx"
        response = StreamingHttpResponse(file_iterator(the_file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        return response

    def extra_url(self):
        app_model_class = self.model_class._meta.app_label, self.model_class._meta.model_name
        patterns = [
            url(r'^(\d+)/(\d+)/delete_cource/$', self.wrap(self.delete_cource), name='%s_%s_dc' % app_model_class),
            url(r'^public/$', self.wrap(self.public_view), name='%s_%s_public' % app_model_class),
            url(r'^myuser/$', self.wrap(self.myuser_view), name='%s_%s_myuser' % app_model_class),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition" % app_model_class),
            url(r'^singleInput/$', self.wrap(self.singleInput_view), name='%s_%s_singleInput' % app_model_class),
            url(r'^multiInput/$', self.wrap(self.multiInput_view), name='%s_%s_multiInput' % app_model_class),
            url(r'^downtemplate/$', self.wrap(self.downtemplate_view), name='%s_%s_downtemplate' % app_model_class),
        ]
        return patterns
