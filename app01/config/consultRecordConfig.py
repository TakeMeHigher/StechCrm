from django.shortcuts import  redirect


from stark.service import v1

class ConsultRecordConfig(v1.StarkConfig):
    def customer_display(self,obj=None,is_head=False):
        if is_head:
            return '所咨询客户'
        return obj.customer.name

    def consultant_display(self,obj=None,is_head=False):
        if is_head:
            return '跟踪人'
        return obj.consultant.name


    list_display = ['date','note',customer_display,consultant_display]


    combine_seach = [
        v1.FilterOption('customer')
    ]

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

    show_search_form = True
    search_fileds =['date__contains']