from django.shortcuts import redirect

from stark.service import v1
from  app01.permission.basePermission import BasePermission

class UserInfoConfig(BasePermission,v1.StarkConfig):
    def depart_display(self,obj=None,is_head=False):
        if is_head:
            return '部门'
        return obj.depart.title

    list_display = ['name','username','email',depart_display]

    show_search_form = True
    search_fileds=['name__contains','username__contains','email__contains']

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

    show_combine_seach=True

    combine_seach=[
        v1.FilterOption('depart',text_func_name=lambda x: str(x),val_func_name=lambda x: x.code,),
    ]