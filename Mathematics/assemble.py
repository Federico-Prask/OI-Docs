#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 OI-Docs 原稿中抽取章节，组装成《数学》For OI 的各部分。

抽取原则：
  * 只删去每份原稿的导言区（\documentclass 到 \mainmatter 之前）与 \end{document}；
  * 只删去与原稿独立成册有关的页码重置（\renewcommand{\thepage}、\setcounter{page}）；
  * 章节正文、交叉引用、\label/\ref 一律原样保留。
"""
import io
import os

ROOT = "/home/user/OI-Docs"
OUT = os.path.join(ROOT, "Mathematics")
NT = os.path.join(ROOT, "Number Theory", "number_theory_teacher.tex")
GT = os.path.join(ROOT, "Game Theory", "game_theory_teacher.tex")

BANNER = ("% !TeX program = xelatex\n"
          "% 本文件由 assemble.py 自 OI-Docs 原稿抽取生成，请勿手改（会被覆盖）。\n"
          "% 源文件：%s\n"
          "% 源行号：%s\n"
          "% 说明：已删去独立成册所需的导言区与页码重置；章节正文与交叉引用原样保留。\n\n")


def banner(src, rng):
    return (BANNER.replace("%s", "{}").format(os.path.relpath(src, ROOT), rng))


def lines_of(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def slice_lines(src, lo, hi):
    """取第 lo..hi 行（1 起，闭区间）。"""
    return src[lo - 1:hi]


def write(path, header_src, header_range, body_lines):
    text = banner(header_src, header_range) + "\n".join(body_lines)
    if not text.endswith("\n"):
        text += "\n"
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %-28s %5d lines" % (os.path.basename(path), len(body_lines)))


nt = lines_of(NT)
gt = lines_of(GT)

# ---------------------------------------------------------------- 第二部分 --
# 正文：第 169 行（"第 0 章为预备章"注释）到 3761 行（附录之前）。
# 第 3762 行起是原稿的附录 A/B/C，统一移到全书的 global appendix（见下），
# 因此这里绝不能取到 4639 行，否则附录三章会在 part2 与 appendix 中各出现一次。
# 删除 3756--3761（\clearpage / \cleardoublepage / \appendix / 页码重置）。
nt_body = [l for i, l in enumerate(slice_lines(nt, 169, 3761), start=169)
           if i not in set(range(3756, 3762))]
write(os.path.join(OUT, "part2.tex"), NT, "169--3761（已删 3756-3761 的 \\appendix 与页码重置）", nt_body)

# ------------------------------------------------------- 附录 A/B/C（数论）--
ap_a = slice_lines(nt, 3762, 4149)
ap_b = slice_lines(nt, 4152, 4350)
ap_c = slice_lines(nt, 4353, 4639)

# ---------------------------------------------------------------- 第四部分 --
# 博弈论正文：第 143 行到 1641 行（第 7 章末尾的 teach 框）。
drop_gt = {1638}  # 原稿独立成册用的 \appendix
gt_body = [l for i, l in enumerate(slice_lines(gt, 143, 1641), start=143) if i not in drop_gt]
write(os.path.join(OUT, "part4a.tex"), GT, "143--1641（已删 1638 的 \\appendix）", gt_body)

# ------------------------------------------------------ 附录 D（博弈模板）---
ap_d = slice_lines(gt, 1642, 1728)

# ------------------------------------------------------------------ 附录 ----
NOTE_B = r"""
\begin{tip}[代码与验证脚本的位置]
本附录摘录的模板，完整 C++17 实现在资料包的 \texttt{Number Theory/code/number\_theory.hpp}；
测试程序为 \texttt{Number Theory/code/selftest.cpp}；数学验证脚本为
\texttt{Number Theory/validation/verify\_math.py}、\texttt{check\_happy.py}
与 \texttt{Number Theory/code/vieta\_construct.py}。
这些文件相对本书源码目录的上一级，编译本书本身不需要它们。
\end{tip}
"""

NOTE_D = r"""
\begin{tip}[代码与验证脚本的位置]
本附录摘录的判定模板，完整 C++17 实现在资料包的 \texttt{Game Theory/code/selftest.cpp}。
自测程序对有限范围的随机与穷举数据，把每个公式与暴力搜索逐点比对；
它相对本书源码目录的上一级，编译本书本身不需要它。
\end{tip}
"""

ap_lines = []
ap_lines.append("% " + "=" * 74)
ap_lines.append("% 附录：A--D。章号由 main.tex 中的 \\appendix 切换为 A、B、C、D。")
ap_lines.append("% " + "=" * 74)
ap_lines.append("")
ap_lines += ap_a
ap_lines.append("")
ap_lines += ap_b
ap_lines.append(NOTE_B.rstrip("\n"))
ap_lines.append("")
ap_lines += ap_c
ap_lines.append("")
ap_lines.append("% " + "-" * 74)
ap_lines.append("% 附录 D：来自《博弈论》教师版的“核心判定模板与接口”。")
ap_lines.append("% " + "-" * 74)
ap_lines += ap_d
ap_lines.append(NOTE_D.rstrip("\n"))

with io.open(os.path.join(OUT, "appendix.tex"), "w", encoding="utf-8") as fh:
    fh.write(banner(NT, "3762-4149 / 4152-4350 / 4353-4639（数论）+ 1642-1728（博弈）")
             + "\n".join(ap_lines) + "\n")
print("wrote appendix.tex              %5d lines" % len(ap_lines))
