# codex-zotero

一个专门用于整理 **合成生物学 / 代谢工程** Zotero 文献的轻量工具仓库。

## 能做什么

- 读取 Zotero 导出的 **BibTeX (.bib)** 和 **RIS (.ris)** 文件
- 自动提取题名、作者、年份、期刊、DOI、关键词
- 按合成生物学研究方向自动分成 4 个二级标签
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

## 5. 当前二级分类

### 1. Chassis engineering / 底盘工程
关注宿主与底盘本身的改造，例如：
- Yarrowia lipolytica
- Bacillus subtilis
- genome engineering / genome refactoring
- microbial chassis
- adaptive laboratory evolution

### 2. Pathway optimization / 代谢通路优化
关注代谢流、前体、辅因子与通路重构，例如：
- metabolic engineering
- pathway engineering
- precursor supply
- redox / cofactor balance
- central carbon metabolism
- Ehrlich pathway

### 3. Expression & regulation tools / 表达调控工具
关注表达元件和动态调控，例如：
- promoter
- transcriptional regulation
- antisense transcription
- transcription-factor-based biosensor
- dynamic regulation

### 4. Natural product biosynthesis / 天然产物生物合成
关注目标产物及细胞工厂生产，例如：
- natural product biosynthesis
- de novo production
- gastrodin
- sakuranetin
- flavonoids
- 2-phenylethanol
- microbial cell factory

未匹配到上述关键词的文献归入 **Other**。

## 6. 与顾洋老师论文的对应关系

这 4 个标签可以基本覆盖你目前关注的论文脉络：

- **底盘工程**：Y. lipolytica / B. subtilis 底盘构建与系统重构
- **代谢通路优化**：Ehrlich pathway、中心碳代谢、前体与氧化还原调控
- **表达调控工具**：启动子、反义转录调控、转录因子型生物传感器
- **天然产物生物合成**：gastrodin、sakuranetin、芳香族天然产物等

## 7. 推荐工作流

Zotero → 导出 BibTeX/RIS → 放入 `data/` → 运行脚本 → 在 `output/` 查看分类结果和重复项。

后续可继续扩展 Zotero Web API 同步、自动读取摘要、按导师/课题组建立子标签，以及自动生成文献阅读卡片。
