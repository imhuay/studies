## 字符串的排列（全排列）
<!--START_SECTION:badge-->

![last modify](https://img.shields.io/static/v1?label=last%20modify&message=2025-07-08%2016%3A53%3A13&color=yellowgreen&style=flat-square)
[![](https://img.shields.io/static/v1?label=&message=%E4%B8%AD%E7%AD%89&color=yellow&style=flat-square)](../../../README.md#中等)
[![](https://img.shields.io/static/v1?label=&message=%E5%89%91%E6%8C%87Offer&color=green&style=flat-square)](../../../README.md#剑指offer)
[![](https://img.shields.io/static/v1?label=&message=%E6%B7%B1%E5%BA%A6%E4%BC%98%E5%85%88%E6%90%9C%E7%B4%A2&color=blue&style=flat-square)](../../../README.md#深度优先搜索)
[![](https://img.shields.io/static/v1?label=&message=%E7%BB%8F%E5%85%B8&color=blue&style=flat-square)](../../../README.md#经典)

<!--END_SECTION:badge-->
<!--info
tags: [DFS+剪枝, 经典]
source: 剑指Offer
level: 中等
number: '3800'
name: 字符串的排列（全排列）
companies: []
-->

<summary><b>问题简述</b></summary>

```txt
输入一个字符串，打印出该字符串中字符的所有排列。
```

<details><summary><b>详细描述</b></summary>

```txt
输入一个字符串，打印出该字符串中字符的所有排列。

你可以以任意顺序返回这个字符串数组，但里面不能有重复元素。

示例:
    输入：s = "abc"
    输出：["abc","acb","bac","bca","cab","cba"]

限制：
    1 <= s 的长度 <= 8

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```

</details>

<!-- <div align="center"><img src="../../../_assets/xxx.png" height="300" /></div> -->

<summary><b>思路1：DFS树状遍历+剪枝</b></summary>

- 深度优先求全排列的过程实际上相当于是一个**多叉树的先序遍历过程**；
    - 假设共有 `n` 种状态都不重复，则：
    - 第一层有 `n` 种选择；
    - 第二层有 `n - 1` 种选择；
    - ...
    - 共有 `n!` 种可能；

    <details><summary><b>图示</b></summary>

    <div align="center"><img src="../../../_assets/剑指Offer_0038_中等_字符串的排列.png" height="200" /></div>

    </details>

**本题的难点是如何过滤重复的状态**

- **写法1）** 遍历所有状态，直接用 `set` 保存结果（不剪枝）：

    <details><summary><b>Python</b></summary>

    ```python
    class Solution:
        def permutation(self, s: str) -> List[str]:

            N = len(s)
            buf = []
            ret = set()
            visited = [False] * N
            def dfs(deep):
                if deep == N:
                    ret.add(''.join(buf))
                    return

                for i in range(N):
                    if not visited[i]:
                        # 标记
                        buf.append(s[i])
                        visited[i] = True
                        # 进入下一层
                        dfs(deep + 1)
                        # 回溯（撤销标记）
                        buf.pop()  
                        visited[i] = False
            
            dfs(0)
            return list(ret)
    ```

    </details>

- **写法2）** 跳过重复字符（需排序）：
    - 其中用于剪枝的代码不太好理解，其解析详见：[「代码随想录」剑指 Offer 38. 字符串的排列](https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof/solution/dai-ma-sui-xiang-lu-jian-zhi-offer-38-zi-gwt6/)
  
        ```python
        if not visited[i - 1] and i > 0 and s[i] == s[i - 1]: 
            continue
        ```

    <details><summary><b>Python</b></summary>

    ```python
    class Solution:
        def permutation(self, s: str) -> List[str]:

            s = sorted(s)  # 排序，使相同字符在一起
            N = len(s)
            ret = []  # 保存结果
            buf = []  # 临时结果
            visited = [False] * N  # 记录是否访问
            def dfs(deep):  # 传入递归深度
                if deep == N:
                    ret.append(''.join(buf))
                    return

                for i in range(N):
                    # 剪枝
                    if visited[i - 1] is False and i > 0 and s[i] == s[i - 1]:
                        continue

                    # 下面的代码居然可以（区别仅在于 visited[i - 1] 的状态），
                    # 但是效率不如上面的，具体解析可参考：[「代码随想录」剑指 Offer 38. 字符串的排列](https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof/solution/dai-ma-sui-xiang-lu-jian-zhi-offer-38-zi-gwt6/)
                    # if visited[i - 1] is True and i > 0 and s[i] == s[i - 1]:
                    #     continue

                    if not visited[i]:  # 如果当前位置还没访问过
                        # 标记当前位置
                        visited[i] = True
                        buf.append(s[i])
                        # 下一个位置
                        dfs(deep + 1)
                        # 回溯
                        buf.pop()
                        visited[i] = False

            dfs(0)
            return ret
    ```

    </details>

- **写法3）** 在每一层用一个 `set` 保存已经用过的字符（不排序）：

    <details><summary><b>Python</b></summary>

    ```python
    class Solution:
        def permutation(self, s: str) -> List[str]:

            N = len(s)
            buf = []
            ret = set()
            visited = [False] * N
            def dfs(deep):
                if deep == N:
                    ret.add(''.join(buf))
                    return

                used = set()  # 记录用过的字符
                for i in range(N):
                    if s[i] in used:  # 如果是已经用过的
                        continue

                    if not visited[i]:
                        # 标记
                        used.add(s[i])
                        buf.append(s[i])
                        visited[i] = True
                        # 进入下一层
                        dfs(deep + 1)
                        # 回溯（撤销标记）
                        buf.pop()  
                        visited[i] = False
            
            dfs(0)
            return list(ret)
    ```

    </details>

- **写法2）** 原地交换
    > [剑指 Offer 38. 字符串的排列（回溯法，清晰图解）](https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof/solution/mian-shi-ti-38-zi-fu-chuan-de-pai-lie-hui-su-fa-by/)

    - 这个写法有点像“下一个排列”，只是没有使用字典序；

    <details><summary><b>Python</b></summary>

    ```python
    class Solution:
        def permutation(self, s: str) -> List[str]:
            N = len(s)
            buf = list(s)
            ret = []

            def dfs(deep):
                if deep == N - 1:
                    ret.append(''.join(buf))   # 添加排列方案
                    return

                used = set()
                for i in range(deep, N):  # 注意遍历范围，类似选择排序
                    if buf[i] in used:  # 已经用过的状态
                        continue

                    used.add(buf[i])
                    buf[deep], buf[i] = buf[i], buf[deep]  # 交换，将 buf[i] 固定在第 deep 位
                    dfs(deep + 1)               # 开启固定第 x + 1 位字符
                    buf[deep], buf[i] = buf[i], buf[deep]  # 恢复交换

            dfs(0)
            return ret
    ```

    </details>


<summary><b>思路2：下一个排列</b></summary>

> [字符串的排列](https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof/solution/zi-fu-chuan-de-pai-lie-by-leetcode-solut-hhvs/)

- 先排序得到最小的字典序结果；
- 循环直到不存在下一个更大的排列；

<details><summary><b>Python</b></summary>

```python
class Solution:
    def permutation(self, s: str) -> List[str]:
        
        def nextPermutation(nums: List[str]) -> bool:
            i = len(nums) - 2
            while i >= 0 and nums[i] >= nums[i + 1]:
                i -= 1

            if i < 0:
                return False
            else:
                j = len(nums) - 1
                while j >= 0 and nums[i] >= nums[j]:
                    j -= 1
                nums[i], nums[j] = nums[j], nums[i]

            left, right = i + 1, len(nums) - 1
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

            return True

        buf = sorted(s)
        ret = [''.join(buf)]
        while nextPermutation(buf):
            ret.append(''.join(buf))

        return ret
```

</details>
