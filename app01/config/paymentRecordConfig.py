from django.shortcuts import redirect

from stark.service import v1
from  app01.permission.basePermission import BasePermission


class PaymentRecordConfig(BasePermission,v1.StarkConfig):
    def customer_display(self,obj=None,is_head=False):
        if is_head:
            return '客户'
        return obj.customer.name

    def class_list_display(self,obj=None,is_head=False):
        if is_head:
            return '班级'
        return obj.class_list.semester


    def pay_type_display(self,obj=None,is_head=False):
        if is_head:
            return '费用类型'
        return obj.get_pay_type_display()

    def consultant_display(self,obj=None,is_head=False):
        if is_head:
            return '负责老师'
        return obj.consultant.name

    list_display = [customer_display,class_list_display,pay_type_display,'paid_fee','turnover','quote','note','date']



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

    combine_seach = [
        v1.FilterOption('class_list'),
        v1.FilterOption('pay_type',is_choice=True),
        v1.FilterOption('consultant'),
    ]