import os
import sys
import django

sys.path.append(r'D:\test\DjangoTest\crm')
os.chdir(r'D:\test\DjangoTest\crm')
os.environ.setdefault("DJANGO_SETTINGS_MODULE","crm.settings")
django.setup()


class Tiga(object):
    users = None  # [1,2,1,2,3,1,...]
    iter_users = None  # iter([1,2,1,2,3,1,...])
    reset_status = False

    @classmethod
    def fetch_users(cls):
        from app01 import models
        sales = models.SaleRank.objects.all().order_by('-weight')
        item = []
        d={}
        for sale in sales:
            #print(sale.user.name, sale.user_id,sale.num,sale.weight)
            d[sale.user.id]=sale.num
        print(d)
        sum=0
        for k,v in d.items():
            sum+=int(v)
        print(sum)
        for i in range(sum):
            for k,v in d.items():
                if item.count(k)>=v:
                    continue
                else:
                    item.append(k)
                if len(item)>sum:
                    break
        print(item)

        cls.users = item

    @classmethod
    def get_sale_id(cls):
        if not cls.users:
            cls.fetch_users()
        if not cls.iter_users:
            cls.iter_users = iter(cls.users)
        try:
            user_id = next(cls.iter_users)
        except StopIteration as e:
            if cls.reset_status:
                cls.fetch_users()
                cls.reset_status = False
            cls.iter_users = iter(cls.users)
            user_id = cls.get_sale_id()
        return user_id

    @classmethod
    def reset(cls):
        cls.reset_status = True

Tiga.fetch_users()