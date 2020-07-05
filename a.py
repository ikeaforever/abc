class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        i, j, i_star, j_star, m, n = 0, 0, -1, -1, len(s), len(p)
        while i < m:
            if j < n:
                if s[i] == p[j] or p[j] == "?":
                    i += 1
                    j += 1
                elif p[j] == "*":
                    j_star = j
                    j += 1
                elif j_star >= 0:
                    i += 1
                    j = j_star + 1
                else:
                    return False
            else:
                if j_star >= 0:
                    i += 1
                    j = j_star + 1
                else:
                    return False

        for k in range(j, n):
            if p[k] != "*":
                return False

        return True


if __name__ == '__main__':
    s = Solution()
    print(s.isMatch("aaaa", "***a"))
