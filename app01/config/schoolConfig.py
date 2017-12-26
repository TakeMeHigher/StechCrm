from django.shortcuts import redirect

from  stark.service import v1


class SchoolConfig(v1.StarkConfig):
    list_display = ['title']
    show_search_form = True
    search_fileds = ['title']

    show_action = True

    def multi_del(self, request):
        id_list = request.POST.getlist('pk')
        # print(id_list,'****------')
        self.model_class.objects.filter(id__in=id_list).delete()
        return redirect(self.get_list_url())

    multi_del.short_desc = '批量删除'


    show_combine_seach = True
    action_func_list = [multi_del]