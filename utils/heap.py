#
# from common.option import Option
#
# #=========================
# #   在数组中实现二叉树时，父节点与子节点的关系为： 左节点=2*index+1 右节点=2*index+2
# #       实现大根堆
# #=========================
# class MaxHeap():
#
#     def __init__(self):
#         self.l = []
#         self.heap_size=0
#
#     def add(self,x :Option):
#         self.heap_size +=1
#         if self.heap_size> len(self.l):
#             self.l.append(x)
#         else:
#             self.l[self.heap_size-1]= x
#         self.heap_insert(self.heap_size-1)
#
#     def swap(self, i, j):
#         t=self.l[i]
#         self.l[i]=self.l[j]
#         self.l[j]=t
#
#     def heap_insert(self,index):
#         '''
#             向最大根堆中添加一个数
#                 添加子节点时与其父节点比较，大于其父节点则交换位置，并继续向上比较
#                 从下向上查询
#         :param l:
#         :param index:
#         :return:
#         '''
#         while(int((index-1)/2)>=0 and self.l[index].grid> self.l[int((index-1)/2)].grid):
#             self.swap(index,int((index-1)/2))
#             index=int((index-1)/2)
#
#
#     def heapify(self,index,heap_size):
#         '''
#             移除最大根堆中的最大值
#                 移除时将数组末尾的数交换到开头，然后将他与两个子节点比较，如果他最大则无需移动，如果子节点较大将他与较大的子节点交换，然后再向下比较
#                 从上向下查询
#         :param index:
#         :param heap_size:
#         :return:
#         '''
#
#         left = 2*index+1
#         while (left<heap_size):
#
#             if (left+1<heap_size and self.l[left+1]>self.l[left]):
#                 larger=left+1
#             else:
#                 larger=left
#
#             if self.l[larger]>self.l[index]:
#                 largest=larger
#             else:
#                 break
#
#             self.swap(index,largest)
#             index = largest
#             left = 2*index+1
