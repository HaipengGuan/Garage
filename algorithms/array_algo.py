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

    def increasingTriplet(self, nums):
        """https://leetcode.com/problems/increasing-triplet-subsequence/
        :type nums: List[int]
        :rtype: bool
        """
        cache = [0, 0]
        list_len = 0
        for x in nums:
            index = self.binary_search(cache, x, 0, list_len-1)
            if index == -3: return True
            if index < 0: index = -(index+1)
            cache[index] = x
            if index == list_len: list_len += 1
        return False


    def binary_search(self, nums, k, lo, hi): # hi is inclusive
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


    def build_max_heap(self, nums, size=None):
        start = len(nums)/2-1
        for i in xrange(start+1):
            self.max_heapify(nums, start-i)
        return nums

    def heap_sort(self, nums):
        end = len(nums)-1
        while end > 0:
            nums[:end+1] = self.build_max_heap(nums[:end+1])
            nums[0], nums[end] = nums[end], nums[0]
            end -= 1
        return nums


    def max_heapify(self, nums, i=0):
        left, right = 2*i+1, 2*i+2
        max_index = i
        if left < len(nums) and nums[left] > nums[max_index]:
            max_index = left
        if right < len(nums) and nums[right] > nums[max_index]:
            max_index = right
        if not max_index == i:
            nums[i], nums[max_index] = nums[max_index], nums[i]
            self.max_heapify(nums, max_index)

    def min_heapify(self, nums, i=0):
        left, right = 2*i+1, 2*i+2
        max_index = i
        if left < len(nums) and nums[left] < nums[max_index]:
            max_index = left
        if right < len(nums) and nums[right] < nums[max_index]:
            max_index = right
        if not max_index == i:
            nums[i], nums[max_index] = nums[max_index], nums[i]
            self.max_heapify(nums, max_index)

    def partition(self, nums, lo, hi): # hi is inclusive
        pivot = nums[hi]
        for i in range(lo, hi):
            if nums[i] <= pivot:
                nums[i], nums[lo] = nums[lo], nums[i]
                lo += 1
        nums[hi], nums[lo] = nums[lo], nums[hi]
        return lo

    def quick_sort(self, nums, lo, hi):
        if lo < hi:
            index = self.partition(nums, lo, hi)
            self.quick_sort(nums, lo, index-1)
            self.quick_sort(nums, index+1, hi)

    def findKthLargest(self, nums, k):
        """https://leetcode.com/problems/kth-largest-element-in-an-array/
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # ---------- max heap solution: ----------
        # for i in range(k):
        #     nums[i:] = self.build_max_heap(nums[i:])
        # return nums[k-1]

        # ---------- divide-and-conquer: ----------
        lo, hi = 0, len(nums)-1
        index = self.partition(nums, lo, hi)
        while not index == len(nums)-k:
            # print lo, index, hi
            if index < len(nums)-k:
                lo = index+1
            else:
                hi = index-1
            index = self.partition(nums, lo, hi)
        return nums[index]

    def search_rotated_sorted(self, nums, target):
        """https://leetcode.com/problems/search-in-rotated-sorted-array/
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        lo, hi = 0, len(nums)-1
        while lo <= hi:
            mid = (lo+hi)/2
            if nums[mid] == target: return mid
            elif nums[lo] <= nums[mid]: # nums[lo: mid+1] is sorted
                if nums[lo] <= target < nums[mid]: # target in nums[lo: mid+1]
                    hi = mid-1
                else:
                    lo = mid+1
            else: # nums[mid: hi+1] is sorted
                if nums[mid] < target <= nums[hi]:  # target in nums[mid: hi+1]
                    lo = mid+1
                else:
                    hi = mid-1
        return -1


    def findMin_rotated_sorted(self, nums):
        """https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/
        :type nums: List[int]
        :rtype: int
        """
        lo, hi = 0, len(nums)-1
        while lo < hi:
            mid = (lo+hi)/2
            # print nums[lo:hi+1]
            print nums[lo], nums[mid], nums[hi]
            if nums[hi] < nums[mid]: # nums[lo: mid+1] is sorted, min in [mid:hi+1]
                lo = mid+1
            elif nums[mid] < nums[hi]: # nums[mid: hi+1] is sorted, min in [lo:mid+1]
                hi = mid
            else: hi-=1
        return nums[lo]

    class MaxProfit(object):
        """https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"""
        def maxProfit_I(self, prices):
            """https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
            :type prices: List[int]
            :rtype: int
            """
            # ---------- more concise solution: -----------
            # if len(prices) <= 1: return 0
            # min_price = prices[0]
            # max_profit = 0
            # for i in xrange(1, len(nums)):
            #     min_price = min(min_price, prices[i])
            #     max_profit = max(max_profit, prices[i]-min_price)
            # return max_profit
            # ---------- my initial solution: -------------
            if len(prices) <= 1: return 0
            buy = 0
            while buy+1 < len(prices) and prices[buy+1] <= prices[buy]:
                buy += 1
            hold = buy
            max_profit = 0
            while hold+1 < len(prices) and prices[hold+1] > prices[buy]:
                hold += 1
                max_profit = max(max_profit, prices[hold] - prices[buy])
            return max(max_profit, self.maxProfit(prices[hold+1:]))
        def maxProfit_II(self, prices):
            """https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
            :type prices: List[int]
            :rtype: int
            """
            profit = 0
            for i in range(1, len(prices)):
                if prices[i] > prices[i-1]:
                    profit += prices[i] - prices[i-1]
            return profit

