from django.conf.urls import url
from django.http import QueryDict
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.utils.safestring import mark_safe


from stark.service import v1


class DepartmentConfig(v1.StarkConfig):
    list_display=['title','code']
    show_search_form=True
    search_fileds=['title__contains','code__contains']

    show_action=True

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