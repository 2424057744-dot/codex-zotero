# codex-zotero

一个专门用于整理 **合成生物学 / 代谢工程** Zotero 文献的轻量工具仓库。

## 能做什么

- 读取 Zotero 导出的 **BibTeX (.bib)** 和 **RIS (.ris)** 文件
- 自动提取题名、作者、年份、期刊、DOI、关键词
- 判断文献是否属于 **Synthetic biology / metabolic engineering**
- 检测可能的重复文献（优先 DOI，其次标准化题名）
- 输出便于 Excel / Python / ChatGPT 继续处理的 CSV 文件

## 目录

```text
codex-zotero/
├─ data/
│  └─ .gitkeep
├─ output/
│  └─ .gitkeep
├─ src/
│  └─ zotero_manager.py
├─ categories.json
├─ requirements.txt
└─ README.md
```

## 1. 从 Zotero 导出

在 Zotero 中：

1. 选中“我的文库”或某个分类
2. 右键 → **导出文库 / 导出分类**
3. 推荐选择 BibTeX（`.bib`）或 RIS（`.ris`）
4. 把导出的文件放进本仓库的 `data/` 文件夹

> 不建议把 Zotero 原始 `zotero.sqlite` 数据库直接上传到 GitHub。

## 2. 安装

需要 Python 3.10+。

```bash
pip install -r requirements.txt
```

## 3. 使用

BibTeX：

```bash
python src/zotero_manager.py data/library.bib
```

RIS：

```bash
python src/zotero_manager.py data/library.ris
```

指定输出文件：

```bash
python src/zotero_manager.py data/library.bib --output output/library_clean.csv
```

## 4. 输出字段

- title
- authors
- year
- journal
- doi
- keywords
- category
- duplicate_key
- possible_duplicate

## 5. 当前分类

只保留：

- **Synthetic biology / metabolic engineering**
- **Other**（未匹配到合成生物学关键词的文献）

关键词规则位于 `categories.json`，当前重点覆盖：

- synthetic biology
- metabolic engineering
- microbial cell factory
- Yarrowia lipolytica
- genome engineering / genome refactoring
- pathway engineering
- promoter / transcriptional regulation
- biosensor
- natural product biosynthesis
- yeast chassis
- Bacillus subtilis

## 6. 推荐工作流

Zotero → 导出 BibTeX/RIS → 放入 `data/` → 运行脚本 → 在 `output/` 查看筛选结果和重复项。

后续可以继续扩展为 Zotero Web API 同步、自动阅读摘要、细分“底盘工程 / 代谢通路 / 调控工具 / 天然产物生物合成”等二级标签。
