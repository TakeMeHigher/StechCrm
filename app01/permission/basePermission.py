from stark.service import v1

class BasePermission(object):

    def get_add_btn(self):

        if 'add' in self.request.permission_code_list:
            return True


    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            if 'edit' in self.request.permission_code_list:
                data.append(v1.StarkConfig.edit)
            if 'del' in self.request.permission_code_list:
                data.append(v1.StarkConfig.delete)
            data.insert(0, v1.StarkConfig.checkbox)
        return data