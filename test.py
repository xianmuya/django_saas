# _ author : Administrator
# date : 2020/4/13
# def foo():
#     for i in range(5):
#         yield i
# a = foo()
# print(next(a),next(a))
# next(a)
# a = [[1] + [2]] + [2]
# print(a)
# import time
# c = time.time()
# a = [1,2,3]
# for i in a[:]:
#     print(i)
# time.sleep(1)
# d = time.time()
# print(d - c)
# class Solution:
#     def permutation(self, S: str):
#         if S == '':
#             return []
#         res = []
#         path = ''
#
#         def backtrack(S, path, res):
#             if S == '':
#                 res.append(path)
#                 return
#
#             for i in range(len(S)):
#                 cur = S[i]
#                 backtrack(S[:i] + S[i + 1:], path + cur, res)
#
#         backtrack(S, path, res)
#
#         return res
#
#
# print(Solution().permutation('qwe'))
# from itertools import permutations
# a = list(permutations('qwe'))
# for i in a:
#     c = ''.join(i)
#     print(c)
# def foo():
#     for i in range(4):
#         yield i
# print(list(foo()))
# class Solution:
#
#     def permutation(self, S):
#         from itertools import permutations
#         res = list(permutations(S))
#         for i in res[:]:
#             yield ''.join(i)
#
# print(list(Solution().permutation('qwe')))
# c = 'safsa'
# d = []
# f = ''.join(c)
# print(f)
# d.extend(f)
# print(d)

#
# pairs = [[0,3],[1,2],[0,8]]
# print(sorted(pairs))
# print(sorted(pairs,key=lambda x:x[1]))

# try:
#     a = input()
#     raise ValueError('cuoqu')
#
# except Exception as e:
#     print(e)

# def not_zero(num):
#     try:
#         if num == 0:
#             raise ValueError('参数错误')
#         print(2)
#     except Exception as e:
#         print(e)
# not_zero(0)