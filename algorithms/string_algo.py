#!/usr/bin/env python

class StringAlgo(object):

    def isInterleave(self, s1, s2, s3):
        """https://leetcode.com/problems/interleaving-string/
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        if not len(s3) == len(s1) + len(s2): return False
        path = [[False for _ in xrange(len(s1)+1)] for _ in xrange(len(s2)+1)]
        for i in xrange(len(s2)+1):
            for j in xrange(len(s1)+1):
                if i+j == 0: path[i][j] = True
                elif i == 0: path[i][j] = path[i][j-1] if s3[i+j-1] == s1[j-1] else False
                elif j == 0: path[i][j] = path[i-1][j] if s3[i+j-1] == s2[i-1] else False
                else: path[i][j] = (s3[i+j-1] == s2[i-1] and path[i-1][j]) or (s3[i+j-1] == s1[j-1] and path[i][j-1])
        return path[len(s2)][len(s1)]

    def reverseWords(self, s):
        """https://leetcode.com/problems/reverse-words-in-a-string/
        Try to use O(1) space: r
            - remove all leading, tailing and duplicate spaces
            - everse each words and reverse whole string
        :type s: str
        :rtype: str
        """
        # ----- one line solution: -----
        # return ''.join(reversed(s.split()))
        # ------ O(1) space approach ----------
        s = list(s) # sorry, string is immutable in Python, let's not count it as extra space.
        print s
        # TODO: remove all leading, tailing and duplicate spaces
        start = end = 0
        while start < len(s) and end < len(s):
            while start < len(s) and s[start] == ' ':
                start += 1
            end = start+1
            while end+1 < len(s) and s[end+1] != ' ':
                end += 1
            print start, end
            self.reverseString(s, start, end)
            print s
            start = end+2
        self.reverseString(s, 0, len(s)-1)
        return ''.join(s)

    def reverseString(self, s, lo, hi): # hi in inclusive
        while lo < hi:
            s[lo], s[hi] = s[hi], s[lo]
            lo, hi = lo+1, hi-1


