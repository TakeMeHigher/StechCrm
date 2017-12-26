from django.shortcuts import redirect

from stark.service import v1


class CourseConfig(v1.StarkConfig):
    list_display = ['name']
    show_search_form = True
    search_fileds=['name']
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