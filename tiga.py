import os
import sys
import django

sys.path.append(r'D:\test\DjangoTest\crm')
os.chdir(r'D:\test\DjangoTest\crm')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

import redis

POOL = redis.ConnectionPool(host='192.168.20.150', port=6379, password='')
CONN = redis.Redis(connection_pool=POOL)


class Tiga(object):
    users = None  # [1,2,1,2,3,1,...]
    iter_users = None  # iter([1,2,1,2,3,1,...])
    reset_status = False
    rollback_list = []

    @classmethod
    def fetch_users(cls):
        from app01 import models
        sales = models.SaleRank.objects.all().order_by('-weight')
        item = []
        # 方法一
        # d={}
        # for sale in sales:
        #     #print(sale.user.name, sale.user_id,sale.num,sale.weight)
        #     d[sale.user.id]=sale.num
        # print(d)
        # sum=0
        # for k,v in d.items():
        #     sum+=int(v)
        # print(sum)
        # for i in range(sum):
        #     for k,v in d.items():
        #         if item.count(k)>=v:
        #             continue
        #         else:
        #             item.append(k)
        #         if len(item)>sum:
        #             break

        # 方法二:
        count = 0
        while True:
            flag = False
            for sale in sales:
                if count < sale.num:
                    item.append(sale.user_id)
                    flag = True
            count += 1
            if not flag:
                break

        if item:
            CONN.rpush('ctz_sale_id_list', *item)
            CONN.rpush('ctz_sale_id_list_origin', *item)
            return True
        else:
            return False

    @classmethod
    def get_sale_id(cls):
        origin_count = CONN.llen('ctz_sale_id_list_origin')
        if not origin_count:
            status = cls.fetch_users()
            if not status:
                return None

        sale_id = CONN.lpop('ctz_sale_id_list')
        if sale_id:
            return sale_id

        reset = CONN.rpop('ctz_reset_id')
        if reset:
            CONN.delete('ctz_sale_id_list_origin')
            status = cls.fetch_users()
            if not status:
                return None
            CONN.delete('ctz_reset_id')
            return CONN.lpop('ctz_sale_id_list')
        else:
            count = CONN.llen('ctz_sale_id_list_origin')
            for i in range(count):
                v = CONN.lindex('ctz_sale_id_list_origin', i)
                CONN.rpush('ctz_sale_id_list', v)
            return CONN.lpop('ctz_sale_id_list')


            # if cls.rollback_list:
            #     return cls.rollback_list.pop()
            # if not cls.users:
            #     cls.fetch_users()
            # if not cls.iter_users:
            #     cls.iter_users = iter(cls.users)
            # try:
            #     user_id = next(cls.iter_users)
            # except StopIteration as e:
            #     if cls.reset_status:
            #         cls.fetch_users()
            #         cls.reset_status = False
            #     cls.iter_users = iter(cls.users)
            #     user_id = cls.get_sale_id()
            # return user_id

    @classmethod
    def reset(cls):
        CONN.rpush('ctz_reset_id', 1)

    @classmethod
    def rollback(cls, nid):
        CONN.lpush('ctz_sale_id_list', nid)


Tiga.fetch_users()
