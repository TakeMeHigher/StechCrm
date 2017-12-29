# import  redis
#
# conn=redis.Redis(host='192.168.20.150',port=6379,password='')
# #
# #conn.lpush('ctz',*[1,2,3])
# # a=conn.lpop('ctz')
# # print(a)
#
# # conn.set('aa',1)
# # print(conn.get('aa'))
#
# # conn.lpush('ctz',*[1,2,3])
# # conn.rpush('ctz',*[4,5,6])
# # conn.lpush('ctz',*[7,8,9])
#
# # count=conn.llen('ctz')
# # for i in range(count):
# #     #a=conn.lindex('ctz',i)
# #     v=conn.lpop('ctz')
# #     print(v)
#
# #
# # conn.rpush('ztc',*[1,2,3,4,5,6,7,8,9])
# # count=conn.llen('ztc')
# # for i in range(count):
# #     v=conn.lindex('ztc',i)
# #     conn.rpush('ctz',v)
# #
# # l=conn.llen('ctz')
# # for i in range(l):
# #     v1=conn.lpop('ctz')
# #     print(v1)