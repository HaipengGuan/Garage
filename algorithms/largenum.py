class LargeNum(object):

    def multiply_str(self, num1, num2):
        """https://leetcode.com/problems/multiply-strings/
        :type num1: str
        :type num2: str
        :rtype: str
        """
        p = [0 for _ in xrange(len(num1)+len(num2))]
        for i in reversed(xrange(len(num1))):
            for j in reversed(xrange(len(num2))):
                num = int(num1[i])*int(num2[j])+p[i+j+1]
                p[i+j+1] = num % 10
                p[i+j] += num/10
        index = 0
        while index+1 < len(p) and p[index] == 0: index += 1
        return ''.join([str(n) for n in p[index:]])

    def plusOne(self, digits):
        """https://leetcode.com/submissions/detail/57347105/
        :type digits: List[int]
        :rtype: List[int]
        """
        carry = 1
        ans = [0 for _ in xrange(len(digits))]
        for i in reversed(xrange(len(digits))):
            carry += digits[i]
            ans[i] = carry%10
            carry = carry/10
        if carry: ans.insert(0, 1)
        return ans

    def to_bit_str(self, num):
        if num == 0: return '0'
        res = ''
        while num != 0:
            res.insert(0, num&0x01)
            num = num >> 1
        return res

    def addBinary(self, a, b):
        """https://leetcode.com/problems/add-binary/
        a = "11", b = "1" -> Return "100"
        :type a: str
        :type b: str
        :rtype: str
        """
        s = ''
        carry = 0
        i, j = len(a)-1, len(b)-1
        while i >= 0 or j >= 0 or carry == 1:
            if i >= 0:
                carry += int(a[i])
                i -= 1
            if j >= 0:
                carry += int(b[j])
                j -= 1
            s = str(carry%2) + s
            carry = carry/2
        return s

    def addTwoNumbers(self, l1, l2):
        """https://leetcode.com/problems/add-two-numbers/
            Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
            Output: 7 -> 0 -> 8
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        dummy = ListNode(0)
        pointer = dummy
        carry = 0
        while l1 or l2:
            pointer.next = ListNode(carry)
            pointer = pointer.next
            if l1:
                pointer.val += l1.val
                l1 = l1.next
            if l2:
                pointer.val += l2.val
                l2 = l2.next
            carry = pointer.val / 10
            pointer.val = pointer.val % 10
        if carry: pointer.next = ListNode(carry)
        return dummy.next

    def add(self, a, b):
        """ a = [1,2,3], b = [1,1] -> return [1,3,4]
        :type a: List[int]
        :type b: List[int]
        :rtype: List[int]
        """
        res = []
        i ,j = len(a)-1, len(b)-1
        carry = 0
        while i >= 0 or j >= 0 or carry == 1:
            if i >= 0:
                carry += a[i]
                i -= 1
            if j >= 0:
                carry += b[j]
                j -= 1
            res.insert(0, carry%10)
            carry = carry / 10
        return res

    def multiply(self, a, b):
        """ a = [1,2,3], b = [1,2] -> return [1,4,7,6]
        :type a: List[int]
        :type b: List[int]
        :rtype: List[int]
        """
        p = [0 for _ in xrange(len(a)+len(b))]
        for i in reversed(xrange(len(a))):
            for j in reversed(xrange(len(b))):
                num = a[i]*b[j] + p[i+j+1]
                p[i+j+1] = num % 10
                p[i+j] += num / 10
        for i in xrange(len(p)-1):
            if not p[i] == 0: return p[i:]
        return p[-1:]
