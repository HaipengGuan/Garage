class Palindrome(object):
    def shortestPalindrome(self, s):
        """https://leetcode.com/problems/shortest-palindrome/
        - Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it.
        - Find and return the shortest palindrome you can find by performing this transformation.
        - Given "aacecaaa", return "aaacecaaa". Given "abcd", return "dcbabcd".
        :type s: str
        :rtype: str
        """
        j = 0
        for i in reversed(xrange(len(s))):
            if s[i] == s[j]: j += 1
        if j == len(s): return s
        return ''.join(s[:j-1:-1]) + self.shortestPalindrome(s[:j]) + s[j:]


    # def shortestPalindrome(self, s):
    #     """https://leetcode.com/problems/shortest-palindrome/
    #     - Given a string S, you are allowed to convert it to a palindrome by adding characters in front of it.
    #     - Find and return the shortest palindrome you can find by performing this transformation.
    #     - Given "aacecaaa", return "aaacecaaa". Given "abcd", return "dcbabcd".
    #     :type s: str
    #     :rtype: str
    #     """
    #     current_center = end = begin = 0
    #     s_1 = '#' + '#'.join(list(s)) + '#'
    #     dp = [0] * len(s_1)
    #     while current_center < len(s_1):
    #         while begin > 0 and end < len(s_1)-1 and s_1[begin-1] == s_1[end+1]:
    #             begin -= 1
    #             end += 1
    #         dp[current_center] = (end - begin + 1)/2
    #         if end == len(s_1)-1: break
    #         new_center = current_center+1
    #         while new_center <= end:
    #             sym_index = 2 * current_center - new_center
    #             if new_center + dp[sym_index] < end:
    #                 dp[new_center] = dp[sym_index]
    #                 new_center += 1
    #             elif new_center + dp[sym_index] == end:
    #                 dp[new_center] = dp[sym_index]
    #                 break
    #             else:
    #                 dp[new_center] = end - new_center
    #                 new_center += 1
    #         current_center = new_center
    #         begin = new_center - dp[new_center]
    #         end   = new_center + dp[new_center]
    #     max_index = 0
    #     max_length = 1
    #     for i in range(len(dp)):
    #         if i/2 - dp[i]/2 <= 0 and dp[i] > max_length:
    #             max_length = dp[i]
    #     return ''.join(s[:max_length-1:-1]) + s


    def longestPalindrome(self, s):
        """https://leetcode.com/problems/longest-palindromic-substring/
        - Given a string S, find the longest palindromic substring in S.
        - You may assume that the maximum length of S is 1000, and there exists one unique longest palindromic substring.
        - NOTE: the difference between SUBSTRING and SUBSEQUENCE
        - idea: Manacher algorithm
        :type s: str
        :rtype: str
        """
        current_center = end = begin = 0
        s_1 = '#' + '#'.join(list(s)) + '#'
        dp = [0] * len(s_1)
        while current_center < len(s_1):
            # expend
            while begin > 0 and end < len(s_1)-1 and s_1[begin-1] == s_1[end+1]:
                begin -= 1
                end += 1
            dp[current_center] = (end - begin + 1)/2
            # reach the end of string
            if end == len(s_1)-1: break
            new_center = current_center+1
            while new_center <= end:
                sym_index = 2 * current_center - new_center
                if new_center + dp[sym_index] < end:
                    dp[new_center] = dp[sym_index]
                    new_center += 1
                elif new_center + dp[sym_index] == end:
                    # it's time to expend a new center
                    dp[new_center] = dp[sym_index]
                    break
                else:
                    dp[new_center] = end - new_center
                    new_center += 1
            current_center = new_center
            begin = new_center - dp[new_center]
            end   = new_center + dp[new_center]
        max_index = 0
        for i in range(len(dp)):
            if dp[i] > dp[max_index]:
                max_index = i
        start = max_index/2 - dp[max_index]/2
        return s[start : start + dp[max_index]]



    def longestPalindrome_dynamic(self, s):
        """
        :type s: str
        :rtype: str
        """
        dp = [[0] * len(s) for _ in range(len(s))]
        max_length = 1
        x = y = 0
        for l in range(1, len(s)+1):
            for i in range(len(s)-l+1):
                j = i+l-1
                if l == 1:
                    dp[i][i] = 1
                elif l == 2:
                    dp[i][j] = 2 if s[i] == s[j] else 0
                elif s[i] == s[j]:
                    dp[i][j] = dp[i+1][j-1] + 2 if not dp[i+1][j-1] == 0 else 0
                else:
                    dp[i][j] = 0
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    x, y = i, j
        return s[x:y+1]


    def longestPalindromicSubsequence(self, s):
        """https://www.youtube.com/watch?v=_nCsPn7_OgI
        - http://www.acmerblog.com/longest-palindromic-subsequence-5721.html
        - Given a string, find the length of longest palindromic subsequence in this string.
        :type s: str
        :rtype: int
        """
        # def recursion(s, lo, hi):
        #     # assert lo >= 0 and hi <= len(s)-1
        #     if lo > hi: return 0
        #     elif lo == hi: return 1
        #     elif s[lo] == s[hi]: return recursion(s, lo+1, hi-1) + 2
        #     else: return max(recursion(s, lo, hi-1), recursion(s, lo+1, hi))

        dp = [[0] * len(s) for _ in range(len(s))]
        for l in range(1, len(s)+1):
            for i in range(len(s)-l+1):
                if l == 1:
                    dp[i][i] = 1
                elif s[i] == s[i+l-1]:
                    dp[i][i+l-1] = 2 + dp[i+1][i+l-2]
                else:
                    dp[i][i+l-1] = max(dp[i][i+l-2], dp[i+1][i+l-1])
        return dp[0][-1]


if __name__ == '__main__':
    p = Palindrome()
    # print p.longestpalindromicSubsequence('asicubi8wiubwdfkaygfewiuqhfi')
    # print p.longestPalindrome('asicubi8wiuaabccbaafkaygfewiuqhfi')
    print p.longestPalindrome('abaxabaxabb')
    print p.longestPalindrome('aabccbaaf')

