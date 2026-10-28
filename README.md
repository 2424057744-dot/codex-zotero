# codex-zotero

一个用于整理 Zotero 导出文献的轻量工具仓库。

## 能做什么

- 读取 Zotero 导出的 **BibTeX (.bib)** 和 **RIS (.ris)** 文件
- 自动提取题名、作者、年份、期刊、DOI、关键词
- 按研究主题进行初步分类
- 检测可能的重复文献（优先 DOI，其次标准化题名）
- 输出一个便于 Excel / Python / ChatGPT 继续处理的 CSV 文件

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
3. 推荐选择：
   - BibTeX：`.bib`
   - RIS：`.ris`
4. 把导出的文件放进本仓库的 `data/` 文件夹

> 暂时不要把 Zotero 的原始 `zotero.sqlite` 数据库直接上传到 GitHub。

## 2. 安装

需要 Python 3.10+。

```bash
pip install -r requirements.txt
```

## 3. 使用

处理 BibTeX：

```bash
python src/zotero_manager.py data/library.bib
```

处理 RIS：

```bash
python src/zotero_manager.py data/library.ris
```

指定输出文件：

```bash
python src/zotero_manager.py data/library.bib --output output/library_clean.csv
```

## 4. 输出

默认输出到：

```text
output/zotero_clean.csv
```

字段包括：

- title
- authors
- year
- journal
- doi
- keywords
- category
- duplicate_key
- possible_duplicate

## 5. 当前分类规则

默认规则写在 `categories.json`，可自行修改关键词。

目前包含：

- Grain storage CFD / ventilation
- Wheat hyperspectral / seed vigor
- Grain pest control / inert dust
- Mycotoxin sensing / MOF / aptamer
- Food biotechnology / fermentation
- Synthetic biology / metabolic engineering
- Other

## 6. 推荐工作流

Zotero → 导出 BibTeX/RIS → 放入 `data/` → 运行脚本 → 在 `output/` 查看分类和重复项。

后续可以继续扩展为：

- Zotero Web API 同步
- 自动补 DOI / PMID
- 自动生成文献阅读笔记
- 按课题生成 Collections 建议
- 根据摘要自动分类
- 生成 GB/T 7714、APA、Elsevier 等参考文献格式
