---
title: Testing All Markdown Styles
slug: markdown-style-test
tags: ['Design', 'CSS', 'Markdown']
---

# Testing All Markdown Styles

这篇文章展示了所有可用的 Markdown 样式效果。让我们一起来看看每个元素的渲染效果吧！

## 1. 文本格式化

普通段落文本看起来是这样的。这是一个比较长的段落，用于测试行距和段落间距的效果。段落之间应该有合适的间距，确保阅读体验良好。

*这是斜体文本* 和 **这是粗体文本**

***这是粗斜体文本***

## 2. 列表展示

### 无序列表
* 第一个列表项
* 第二个列表项
  * 嵌套的列表项
  * 另一个嵌套项
* 第三个列表项

### 有序列表
1. 第一步
2. 第二步
   1. 子步骤 1
   2. 子步骤 2
3. 第三步

## 3. 代码展示

行内代码看起来是这样的：`print("Hello World")`

代码块示例：

```python
def hello_world():
    """这是一个简单的函数"""
    message = "Hello, World!"
    print(message)
    return message

# 调用函数
hello_world()
```

```javascript
// JavaScript示例
const greeting = (name) => {
    return `Hello, ${name}!`;
};

console.log(greeting("Developer"));
```

## 4. 引用效果

> 这是一段引用文本。它应该有一个漂亮的左边框和稍微的缩进。
> 
> 这是引用的第二段，用来测试多段引用的效果。

## 5. 链接和图片

这是一个[链接示例](https://example.com)。

这是另一个[带有标题的链接](https://example.com "悬停显示的标题")。

## 6. 表格展示

| 标题 1 | 标题 2 | 标题 3 |
|--------|--------|--------|
| 内容 1 | 内容 2 | 内容 3 |
| 示例 A | 示例 B | 示例 C |

## 7. 水平分割线

下面是一条水平分割线：

---

## 8. 复杂嵌套示例

1. 第一个主要点
   > 这是第一点的补充说明，使用引用格式
   ```python
   # 这是相关的代码示例
   def example():
       return "示例代码"
   ```

2. 第二个主要点
   * 要点 A
   * 要点 B
     1. 详细说明 1
     2. 详细说明 2
   * 要点 C

## 总结

这个文档包含了所有主要的 Markdown 元素，可以用来测试样式表的效果。通过这个测试文档，我们可以：

1. 验证所有样式是否正确渲染
2. 检查元素间距是否合适
3. 确保响应式设计正常工作
4. 测试暗色主题的显示效果