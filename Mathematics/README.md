# 《数学》 For OI —— 合并教材

把 OI-Docs 的《数论》教师版、《博弈论》教师版，与新写的第一部分（基础数学）、
第三部分（组合数学）、第四部分后半（概率论）合并成一部按“部分—章”组织的教材。

## 文件

| 文件 | 内容 |
| --- | --- |
| `main.tex` | 唯一起点文件：导言区、`\PartPage` 部分页机制、前置部分（封面／阅读说明／记号速查表／教学分层／目录）、五个部分的入口、附录开关 |
| `part1.tex` | 第一部分 基础数学（自写，6 章） |
| `part2.tex` | 第二部分 数论（由 `assemble.py` 从 `Number Theory/number_theory_teacher.tex` 抽取，第 0–15 章） |
| `part3.tex` | 第三部分 组合数学（自写，7 章） |
| `part4a.tex` | 第四部分 博弈论（由 `assemble.py` 从 `Game Theory/game_theory_teacher.tex` 抽取，第 1–7 章） |
| `part4b.tex` | 第四部分 概率论（自写，第 8–10 章） |
| `part5.tex` | 第五部分 多项式与生成函数（**占位骨架，正文由使用者提供**） |
| `appendix.tex` | 附录 A–D（数论附录 A/B/C + 博弈论附录） |
| `assemble.py` | 从 OI-Docs 原稿重新生成 `part2.tex`、`part4a.tex`、`appendix.tex` |

`part2.tex` / `part4a.tex` / `appendix.tex` 顶部都写着“由 assemble.py 生成，请勿手改”，
改动原稿后请重新运行 `python3 assemble.py` 再编译。

## 编译

```
cd Mathematics
xelatex main.tex
xelatex main.tex
```

需要 **XeLaTeX 编译两遍**：第一遍生成目录与交叉引用，第二遍稳定页码与链接。
依赖：`ctex`（`fontset=fandol`）、`amsmath`/`amsthm`/`mathtools`、`tcolorbox[most]`、
`tikz`、`fancyhdr`、`listings`、`booktabs`、`longtable`、`enumitem`、`hyperref`、`emptypage`。

全部插图都是 TikZ 矢量图，**没有外部图片依赖**。

## 结构约定

- 每部分开头是一张**部分页**：右下角是 TikZ 绘制的旋转叠加图案，左下角是罗马数字、
  部分名称与部分标题。图案形状与几何参数按使用者提供的模板逐字保留。
- `\BeginPart{形状编号}{副本数 n}{罗马数字}{部分名称}{标题}` 负责：递增内部 `partno`
  计数器、把章号计数器归零、画部分页、写目录项。
- 章号在每部分重新从 1 开始；第二部分额外 `\setcounter{chapter}{-1}`，保留原稿的“第 0 章”。
- `\theHchapter = <partno>.<chapter>`（附录改为 `\Alph{chapter}`），保证 hyperref 锚点唯一。
- `\comparisonfalse`：每个部分页都从右页（奇数页）开始，中间用空白页补齐。
  想要连续排版就把 `main.tex` 里那一行改成 `\comparisontrue`。

## 各部分记号

全书统一记号见 `main.tex` 前置部分的“统一记号速查表”。数论宏：`\Z \N \Pp \eps \one
\id \ord \lcm \rad \iva \floor \ceil`；博弈论宏：`\mex \SG \Np \topbit \dep \Val`；
概率论宏：`\E \Var \Cov \Bern \Bin \Pois \Geom \Harm`。新宏请加到 `main.tex` 的
“简写命令”一节，不要在各部分文件里重复定义。
