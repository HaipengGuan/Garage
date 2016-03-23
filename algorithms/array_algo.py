#!/usr/bin/env python

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class ArrayAlgo(object):
    def mergeKLists(self, lists):
        """https://leetcode.com/problems/merge-k-sorted-lists/
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        if lists == []: return None
        elif len(lists) == 1: return lists[0]
        elif len(lists) == 2: return self.mergeTwoLists(lists[0], lists[1])
        else: return self.mergeTwoLists(self.mergeKLists(lists[:len(lists)/2]), self.mergeKLists(lists[len(lists)/2:]))

    def mergeTwoLists(self, l1, l2):
        """https://leetcode.com/problems/merge-two-sorted-lists/
        Another recursive method is also possible.
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        pointer = ListNode(0)
        root = pointer
        while l1 and l2:
            if l1.val <= l2.val:
                pointer.next = l1
                l1 = l1.next
            else:
                pointer.next = l2
                l2 = l2.next
            pointer = pointer.next
        pointer.next = l1 if l1 else l2
        return root.next

    def merge(self, nums1, m, nums2, n):
        """https://leetcode.com/problems/merge-sorted-array/
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: void Do not return anything, modify nums1 in-place instead.
        """
        if n == 0: return # nothing to merge
        x, y = m-1, n-1
        k = m+n-1
        while x >=0 and y >= 0:
            print x, y
            if nums1[x] >= nums2[y]:
                nums1[k] = nums1[x]
                x, k = x-1, k-1
            else:
                nums1[k] = nums2[y]
                y, k = y-1, k-1
        while y >= 0:
            nums1[k] = nums2[y]
            y, k = y-1, k-1

    def binarySearch(self, nums, k, lo, hi):
        while lo <= hi:
            mid = (lo+hi)/2
            if k == nums[mid]:
                return mid
            elif k < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # (-(insertion point) - 1)
        # the index of the first element greater than the key
        return -lo-1


