<p align="center">
  <h1 align="center">SciVoyage</h1>
  <p align="center">科研风旅行组图排版 · Kimi Code Skill</p>
</p>

<p align="center">
  <a href="#功能特性">功能特性</a> •
  <a href="#效果预览">效果预览</a> •
  <a href="#安装">安装</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#使用示例">使用示例</a> •
  <a href="#项目结构">项目结构</a> •
  <a href="#许可证">许可证</a>
</p>

---

## 简介

**SciVoyage** 是一个 Kimi Code Skill，用于将一组旅行照片和对应的中文说明，自动整理排版成一张**看起来像论文 Figure 1 的社交媒体长图**。

它解决的问题：

- 旅行照片多、叙事散，直接发社交媒体显得杂乱
- 想做出论文 Figure 风格的 `(a)(b)(c)` 子图编号 + `Fig. 1.` 整体图注
- 中文说明需要翻译成适合海外平台的英文图注
- 需要在图上用红色箭头、虚线、实线框等元素标注重点

## 功能特性

- **子图自动编号**：按 `(a)`、`(b)`、`(c)` … 顺序编号
- **中译英图注**：把每张照片的 1-2 句中文说明翻译成科研风英文，拼接成完整 `Fig. 1.` 图注
- **智能布局推荐**：根据子图数量选择最优布局
  - 2-3 张：单行等宽
  - 4-6 张：2×2 或 2×3 网格
  - 7-10 张：不规则网格
  - 含地图：左上角放地图，其余放照片
- **红色标记系统**：
  - 粗实线红色箭头：方向、路线、流程
  - 红色虚线：关联、引导、区域边界
  - 红色实线矩形框：突出关键区域
  - 红色细箭头 + 文字标签：标注地名、峰名、建筑名
  - 实线小框 + 虚线延长线 + 虚线放大图边框：远景与近景放大联动
- **字体风格统一**：子图编号使用 Arial/Helvetica Bold 加白色方块背景，整体图注使用 Times New Roman 衬线字体
- **社交媒体适配**：默认输出单张竖版长图，宽度建议 1080 px，适合小红书 / Instagram / 朋友圈
- **多种输出格式**：PNG/JPG 图片、Python matplotlib/Pillow 脚本、Markdown 排版方案、HTML 网页、LaTeX `subfigure` 代码

## 效果预览

项目目录中提供了风格参考和测试输出：

| 文件 | 说明 |
|------|------|
| [`0ed7fc829c6875461cee53faa078b726.jpg`](./0ed7fc829c6875461cee53faa078b726.jpg) | 黄山徒步参考风格（10 子图 + 红色标记） |
| [`test_trip/final_composite.jpg`](./test_trip/final_composite.jpg) | 测试合成效果示例 |

> 实际输出为模型根据 `SKILL.md` 规则生成的单张长图。

## 环境要求

- Kimi Code CLI（用于加载并执行本 Skill）

## 安装

### 方式一：作为独立项目克隆

```bash
git clone <your-repo-url>
cd xjpaper
```

Kimi Code 启动后会自动加载 `skills/scivoyage/SKILL.md`。

### 方式二：复制到现有项目

```bash
# 在你的项目下创建 skills 目录
mkdir -p skills

# 复制 SciVoyage skill
cp -r /path/to/xjpaper/skills/scivoyage skills/
```

### 验证安装

在 Kimi Code 中提问，若模型读取了 `skills/scivoyage/SKILL.md` 并按其中流程执行，即表示安装成功。

## 快速开始

1. 准备旅行照片和每张照片的 1-2 句中文说明
2. 在 Kimi Code 中输入：

```text
请使用 SciVoyage skill，帮我做一张旅行组图。
```

3. 按提示提供：
   - **主题标题**：整张图想表达什么
   - **子图素材**：照片内容及顺序
   - **中文子图说明**：每张照片的 1-2 句解释
   - **可选标注**：是否需要红框、虚线、箭头、文字标注
   - **输出格式**：图片（默认）/ Python 脚本 / Markdown / HTML / LaTeX

## 使用示例

### 示例 1：新疆伊犁环线

```text
请使用 SciVoyage skill，帮我做一张新疆旅行组图。

主题：新疆伊犁环线 7 日旅行亮点

照片顺序如下：
1. 赛里木湖日出全景
2. 果子沟大桥
3. 夏塔古道徒步
4. 琼库什台村落
5. 那拉提草原
6. 巴音布鲁克九曲十八弯
7. 独库公路

中文说明：
1. 赛里木湖清晨，湖面如镜，远处雪山倒映其中。
2. 果子沟大桥横跨山谷，宛如一条银色丝带。
3. 夏塔古道沿途可见原始森林与雪山同框。
4. 琼库什台是哈萨克族传统村落，木屋错落有致。
5. 那拉提草原上牛羊成群，空中草原视野开阔。
6. 巴音布鲁克日落时分，九曲十八弯倒映九个太阳。
7. 独库公路一日历四季，沿途风景壮丽多变。

输出：一张 1080px 宽、可直接发朋友圈的 JPG 长图。
```

### 示例 2：黄山徒步（Markdown 方案输出）

**输入：**

```text
主题：黄山徒步
照片 4 张：天都峰远眺、迎客松、西海大峡谷、光明顶日落

说明：
1. 天都峰险峻陡峭，是黄山三大主峰之一。
2. 迎客松姿态优美，是黄山标志性景观。
3. 西海大峡谷云雾缭绕，奇峰林立。
4. 光明顶日落金光洒满群山。

请生成论文 Figure 风格的英文图注。
```

**输出：**

```markdown
## 多面板展示图排版方案：黄山徒步

### 布局（共 4 张子图）

┌─────────────────┬─────────────────┐
│   (a) 天都峰    │   (b) 迎客松    │
├─────────────────┼─────────────────┤
│ (c) 西海大峡谷  │ (d) 光明顶日落  │
└─────────────────┴─────────────────┘

### 整体图注

**Fig. 1.** Highlights of the Huangshan Hiking Trip. (a) Tiandu Peak, one of the three main peaks of Huangshan, features steep and rugged cliffs. (b) The Guest-Greeting Pine, with its elegant posture, serves as an iconic landmark of Huangshan. (c) The West Sea Grand Canyon is shrouded in mist and dotted with peculiar peaks. (d) The sunset at Bright Summit bathes the surrounding mountains in golden light.
```

## 支持的输出格式

| 格式 | 扩展名 | 适用场景 |
|------|--------|----------|
| 图片 | `.png` / `.jpg` | 直接发朋友圈 / 小红书 / Instagram |
| Python 脚本 | `.py` | 想手动调整布局时使用 |
| Markdown | `.md` | 仅需排版方案说明 |
| HTML | `.html` | 网页展示 |
| LaTeX | `.tex` | 论文 subfigure 代码 |

## 项目结构

```text
.
├── LICENSE              # MIT 许可证
├── README.md            # 项目说明（本文件）
├── skills/scivoyage/
│   ├── SKILL.md         # Skill 核心规则与执行流程
│   └── ...
├── test_trip/           # 测试样例
└── xinjiang_trip/       # 新疆旅行示例
```

## 贡献指南

欢迎提交 Issue 和 Pull Request。在提交前请确保：

1. 描述清楚问题或改进点
2. 保持与现有 `SKILL.md` 的风格和定位一致
3. 不要添加超出本 Skill 定位的功能

## 许可证

本项目采用 [MIT](./LICENSE) 许可证开源。
