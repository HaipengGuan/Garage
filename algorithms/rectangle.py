class Rectangle(object):

    def largestRectangleArea(self, heights):
        """https://leetcode.com/problems/largest-rectangle-in-histogram/
        :type heights: List[int]
        :rtype: int
        """
        stact = []
        max_area = 0
        heights.append(0)
        current_index = 0
        while current_index < len(heights):
            if len(stact) == 0 or heights[current_index] >= heights[stact[-1]]:
                stact.append(current_index)
                current_index += 1
            else:
                height = heights[stact.pop(-1)]
                width = current_index if stact == [] else current_index - 1 - stact[-1]
                max_area = max(max_area, height * width)
        return max_area

    def maximalRectangle(self, matrix):
        """https://leetcode.com/problems/maximal-rectangle/
        :type matrix: List[List[str]]
        :rtype: int
        """
        # ------------- using DP ------------------
        if len(matrix) == 0 or len(matrix[0]) == 0: return 0
        x_size , y_size = len(matrix[0]), len(matrix)
        max_area = 0
        left, height = [[0 for _ in range(x_size)] for _ in range(2)]
        right = [x_size for _ in range(x_size)]
        for i in range(y_size):
            current_left, current_right = 0, x_size
            for j in range(x_size):
                if matrix[i][j] == '1': height[j] += 1
                else: height[j] = 0
            for j in range(x_size):
                if matrix[i][j] == '1': left[j] = max(left[j], current_left)
                else: left[j], current_left = 0, j+1
            for j in reversed(range(x_size)):
                if matrix[i][j] == '1': right[j] = min(right[j], current_right)
                else: right[j], current_right = x_size, j
            for j in range(x_size):
                max_area = max(max_area, (right[j] - left[j]) * height[j])
        return max_area
        # -------- using largestRectangleArea -------
        # if len(matrix) == 0 or len(matrix[0]) == 0: return 0
        # x_size , y_size = len(matrix[0]), len(matrix)
        # max_area = 0
        # height = [0 for _ in range(x_size)]
        # for i in range(y_size):
        #     for j in range(x_size):
        #         height[j] = height[j] + 1 if matrix[i][j] == '1' else 0
        #     max_area = max(max_area, self.largestRectangleArea(height))
        # return max_area


    def maximalSquare(self, matrix):
        """https://leetcode.com/problems/maximal-square/
        :type matrix: List[List[str]]
        :rtype: int
        """
        if len(matrix) == 0 or len(matrix[0]) == 0: return 0
        x_size, y_size = len(matrix[0]), len(matrix)
        max_area = 0
        left, height = [[0 for _ in range(x_size)] for _ in range(2)]
        right = [x_size for _ in range(x_size)]
        for i in range(y_size):
            current_left, current_right = 0, x_size
            for j in range(x_size):
                if matrix[i][j] == '1': height[j] += 1
                else: height[j] = 0
            for j in range(x_size):
                if matrix[i][j] == '1': left[j] = max(left[j], current_left)
                else: left[j], current_left = 0, j+1
            for j in reversed(range(x_size)):
                if matrix[i][j] == '1': right[j] = min(right[j], current_right)
                else: right[j], current_right = x_size, j
            for j in range(x_size):
                # if (right[j] - left[j]) == height[j]:
                max_area = max(max_area, min(right[j] - left[j], height[j])**2)
        return max_area



