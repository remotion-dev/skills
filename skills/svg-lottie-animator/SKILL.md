---
name: svg-lottie-animator
description: 将静态 SVG 插画转换为 Lottie 动画。输入一个 SVG 文件和对应的 Lottie 结构 JSON，根据用户描述的动画需求，生成带有关键帧动画的 Lottie JSON 和 HTML 预览文件。当用户要求为 SVG 元素添加动画、创建 Lottie 动画、从静态插画生成动效、或需要动画预览时触发此技能。触发关键词：SVG动画、Lottie、关键帧动画、motion path、动效生成。
---

# SVG Lottie 动画生成器

将静态 SVG 元素根据 Lottie JSON 结构和用户动画需求，生成关键帧动画 Lottie JSON + HTML 预览。

## 工作流程

### 第一步：解析输入文件

1. **读取 SVG 文件**：识别可动画化元素（形状、路径、组等）
2. **读取 Lottie 结构 JSON**：理解图层层级、预合成、元素位置

输入 JSON 通常从 Figma/Sketch/AE 导出，`a: 0` 表示静态属性。

### 第二步：动画哲学 (必须)

在写任何代码前，先定义：
1. **品牌个性**: 专业/活泼/优雅/有力
2. **情感响应**: 信任/兴奋/平静/紧迫
3. **运动隐喻**: 像水一样流畅 / 像弹簧一样弹性 / 像空气一样轻盈

### 第三步：选择动画策略

| 策略 | 适用场景 | 技术 |
|------|---------|------|
| Pop-In 弹入 | Logo、按钮 | Scale + Opacity |
| Draw-On 绘制 | 描边图标 | Trim Path |
| Morph 形变 | 图标切换 | Path 关键帧 (需相同顶点数) |
| Stagger 交错 | 多元素 | 延迟 st/ip |
| Character 角色 | 人物、吉祥物 | Parenting + 骨骼层级 |
| Frame-by-Frame | 走路/跑步循环 | ip/op 图层切换 |

### 第四步：生成动画 Lottie JSON

#### 4.1 基本参数

```json
{"v":"5.12.1","fr":30,"ip":0,"op":90,"w":750,"h":720,"nm":"动画名称","ddd":0}
```

#### 4.2 元素引用方式

| 方式 | 何时使用 |
|------|---------|
| 矢量形状图层 (ty:4) | 需要形变动画的元素 |
| 图片图层 (ty:2) | 复杂元素的整体运动 |
| 预合成 (ty:0) | 组合多个子图层 |

#### 4.3 关键帧动画

将属性 `a` 从 `0` 改为 `1`，提供 `k` 关键帧数组。**必须使用专业缓动曲线**，见 [references/bezier-easing.md](references/bezier-easing.md)。

**位置动画** (含运动路径弧线):
```json
"p": {"a":1,"k":[
  {"t":0,"s":[100,200,0],"o":{"x":[0.33],"y":[0]},"i":{"x":[0.67],"y":[1]},
   "to":[50,-100,0],"ti":[-50,100,0]},
  {"t":30,"s":[400,200,0]}
]}
```
`to`/`ti` = 运动路径贝塞尔切线，使轨迹变为抛物线弧线。

**旋转/缩放/透明度**: 类似结构，单值用数组 `[value]`。

#### 4.4 图层类型速查

| ty | 类型 | 特有属性 |
|----|------|---------|
| 0 | 预合成 | `refId`, `w`, `h` |
| 1 | 纯色 | `sw`, `sh`, `sc` |
| 2 | 图片 | `refId` |
| 4 | 形状 | `shapes` |

#### 4.5 遮罩 (Track Matte)

```json
{"ind":1,"ty":4,"nm":"遮罩","td":1, "shapes":[...]},
{"ind":2,"ty":4,"nm":"内容","tt":1, "shapes":[...]}
```

| tt | 模式 |
|----|------|
| 1 | Alpha 遮罩 |
| 2 | Alpha 反转 |

### 第五步：应用动画原则

**必须应用以下原则**，详见 [references/advanced-techniques.md](references/advanced-techniques.md)：

1. **Anticipation (预备动作)**: 跳跃前先下蹲，移动前先反向
2. **Squash & Stretch**: 保持体积守恒 `X * Y ≈ 10000`
3. **Follow-Through**: 到达目标后过冲再回弹 (Elastic Settle)
4. **Staggered Timing**: 多元素交错入场 `st: 0, 3, 6, 9`
5. **Layer Parenting**: 骨骼层级 `"parent": ind` 控制角色动画

**Squash & Stretch 示例**:
```json
"s": {"a":1,"k":[
  {"t":0, "s":[100,100]},
  {"t":8, "s":[110,91]},     // 蓄力压扁 (110×91=10010)
  {"t":15,"s":[85,118]},     // 腾空拉伸 (85×118=10030)
  {"t":20,"s":[125,80]},     // 落地砸扁 (125×80=10000)
  {"t":30,"s":[100,100]}     // 恢复
]}
```

### 第六步：形状修饰器

**Trim Path** (描边绘制动画):
```json
{"ty":"tm","s":{"a":0,"k":0},
 "e":{"a":1,"k":[{"t":0,"s":[0]},{"t":45,"s":[100]}]},
 "o":{"a":0,"k":0},"m":1}
```

**Repeater** (重复排列):
```json
{"ty":"rp","c":{"a":0,"k":8},"tr":{"r":{"a":0,"k":45}}}
```

### 第七步：生成 HTML 预览

```bash
python scripts/generate_preview.py <lottie_json_path> <output_html_path>
```

或手动使用 `assets/preview-template.html` 模板。

### 第八步：验证与迭代

1. 在浏览器中打开 HTML 验证动画效果
2. 检查流畅性、时间节奏、运动轨迹
3. 根据用户反馈迭代

## 参考文档

- [专业缓动曲线库](references/bezier-easing.md) — **关键帧必须使用专业缓动**
- [高级动画技术](references/advanced-techniques.md) — 动画原则、骨骼层级、逐帧动画
- [Lottie JSON 格式](references/lottie-format.md) — 完整数据结构参考
- [输入输出映射示例](references/example-mapping.md) — 真实案例
