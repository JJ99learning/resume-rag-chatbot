# AI Engineer Transition Roadmap

> "The algorithm: delete requirements, simplify, optimize, accelerate, automate. In that order. Skipping steps is how you end up with a bad product." — Musk

**Start:** 2026-06-13 | **Deadline:** 2026-07-11 **(4 weeks. Not 6. Obviously.)**  
**From:** Java Engineer | **To:** Shipped AI project + first interview  
**Rule:** "理解X" 不是任务。能跑的代码才是任务。

---

## Launch Control Dashboard

| Week | Mission | Status | Proof of Completion |
|------|---------|--------|---------------------|
| Week 1 | API接通 + RAG跑起来 | 🔄 In Progress | PDF问答在终端能跑 |
| Week 2 | UI上线 + GitHub公开 + 开始投简历 | ⬜ Not Started | 有可访问URL + 第一封简历发出去 |
| Week 3 | Agent工具调用 + 项目升维 | ⬜ Not Started | Bot能主动调用≥2个工具 |
| Week 4 | 面试冲刺 + 拿到机会 | ⬜ Not Started | ≥1个面试邀约 |

**Status:** ⬜ Not Started | 🔄 In Progress | ✅ Done | ❌ Blocked (fix in 30min or ask Claude)

---

## Week 1 — 接通引擎 + RAG链路

> "Fail fast. An explosion is a test result." 卡住30分钟 = 立刻问Claude，不是死磕。

### Days 1-2 — 今晚开始，不是"这周"

- [X] `python --version` 确认环境存在（conda env: `ai-engineer`）
- [X] `pip install sentence-transformers chromadb python-dotenv pypdf streamlit`
- [X] 写 `hello_claude.py`：用 `subprocess` 调 `claude -p`，发一条消息，打印回复 → **跑起来**
- [X] 改成多轮对话：本地维持 `conversation_history` list，每次把历史拼进 prompt 发给 `claude -p` → **跑起来**

**LLM 调用方式（不用 API Key，走 Pro Plan）：**
```python
import subprocess

def ask_claude(prompt: str) -> str:
    result = subprocess.run(
        ['claude', '-p', prompt],
        capture_output=True, text=True, encoding='utf-8'
    )
    return result.stdout.strip()
```

**Day 2 结束标准：** 终端里能和 Claude 连续聊5句话，历史对话被记住

### Days 3-5 — RAG 完整链路

- [X] 准备一个测试文件（自己的简历 PDF 或任意 TXT）
- [X] 写 `ingestor.py`：读文件 → 切 chunks（每块500字）→ 打印出来
- [X] 把 chunks embed → 存入 ChromaDB（本地文件夹）
- [X] 写 `retriever.py`：输入问题 → 搜出最相关3个chunks → 打印出来
- [X] 写 `rag.py`：把chunks塞进prompt → 问Claude → 打印回答
- [X] 测试：问一个文件里有的问题，确认答案来自文件内容

**Day 5 结束标准：** `python rag.py` → 问 → 得到基于文件的回答。就这一件事。

### Days 6-7 — 代码整理 + Git

- [ ] 创建 `rag-chatbot/` 子目录，整理文件结构
- [ ] 写 `.gitignore`（排除 `.env`、`chroma_db/`、`__pycache__/`）
- [ ] `git init` + 推到 GitHub（public repo）
- [ ] 写 README 第一版：一句话描述 + 怎么跑

**Week 1 结束标准：** GitHub 上有代码，README 能让陌生人知道这是什么

---

## Week 2 — UI上线 + 开始求职（并行，不是串行）

> "Ship imperfect. OTA update later. Time is the real scarce resource."

### Days 1-3 — Streamlit UI（10行代码的事）

- [ ] `pip install streamlit`
- [ ] 写 `app.py`：文件上传 + 对话框 + 对话历史显示
- [ ] 本地 `streamlit run app.py` 跑起来，截图
- [ ] `pip freeze > requirements.txt`
- [ ] 推到 GitHub

### Days 4-5 — 部署（今天必须上线）

- [ ] 去 Streamlit Cloud（share.streamlit.io）免费部署
- [ ] 配置环境变量 `ANTHROPIC_API_KEY`
- [ ] 修依赖问题（大概率遇到，30分钟内解决）
- [ ] 拿到公开URL，写进 README

**Day 5 结束标准：** 有一个链接，发给任何人能直接用

### Days 6-7 — 求职启动（这周就开始，不等Week 6）

- [ ] 简历加入这个项目（项目名 + 技术栈 + GitHub + URL）
- [ ] LinkedIn 加关键词：`Python` `LLM` `RAG` `AI Engineer`
- [ ] 搜索目标JD：`AI Engineer` `LLM` `RAG` `Python`
- [ ] 发出去 ≥3封简历（内转 or 外投都算）

**Week 2 结束标准：** URL存在 + 简历发出去了。两件事。

---

## Week 3 — Agent升维

> "Obviously the next step is giving it tools. A chatbot that can only talk is like a Tesla with no autopilot."

### Tool Use 核心循环

```
用户问题 → Claude思考 → 决定调用哪个工具 → 执行工具 → 拿到结果 → 继续思考 → 最终回答
```

### Atomic Tasks

- [ ] 读 Anthropic Tool Use 文档（看代码示例，不是全文）
- [ ] 给 Claude 定义第一个工具：`search_web(query)` 或 `get_current_date()`
- [ ] 实现工具执行逻辑 + 把结果塞回给 Claude
- [ ] 测试：问一个需要工具的问题，确认 Claude 主动调用了
- [ ] 加第二个工具（`calculate()` 或 `read_file(path)`）
- [ ] 更新 README：加架构图（ASCII文字图就够）
- [ ] 推 GitHub + 更新线上部署

**Week 3 结束标准：** Bot能主动决定用工具还是直接回答

---

## Week 4 — 面试冲刺

> "You don't need to know everything. You need to know your thing cold."

### 必须能张口就答（不能卡顿）

- [ ] 什么是 RAG？为什么不把整个文档直接塞给LLM？（答：token limit + 精准度）
- [ ] Embedding 是什么？（答：把文字映射成向量，相似的文字向量距离近）
- [ ] 你的项目架构？（画出来：用户→Streamlit→RAG链路→Claude→回答）
- [ ] Tool Use 和普通调用有什么区别？（答：Claude自主决定是否调用，ReAct循环）
- [ ] 为什么选 ChromaDB 不选 Pinecone？（答：本地零配置，demo够用）

### 求职加速

- [ ] 每天投 ≥2家（包括内转申请）
- [ ] 在 LinkedIn 发一条帖子展示项目（截图 + URL + 学到什么）
- [ ] 找到 ≥1个 AI 工程师 做 coffee chat（LinkedIn DM）

**Week 4 结束标准：** ≥1个面试邀约。这是唯一指标。

---

## The Algorithm（每天早上对照）

```
1. DELETE   今天的任务里，哪些是没有具体输出的？删掉。
2. SIMPLIFY 剩下的任务，能合并的合并，能简化的简化。
3. OPTIMIZE 从最重要的任务开始，不从最容易的开始。
4. ACCELERATE 设一个"不可能"的完成时间，然后试图达到它。
5. AUTOMATE 现在不管自动化，那是Week 3以后的事。
```

---

## Tech Stack（5个库，不多）

```
claude -p (subprocess)   LLM调用，走 Pro Plan $20额度，无需 API Key
chromadb                 向量数据库（本地，零配置）
sentence-transformers    Embedding（本地CPU跑，all-MiniLM-L6-v2）
streamlit                UI（10行出界面）
pypdf                    读取简历 PDF
python-dotenv            .env管理（部署阶段用）
```

---

##傻瓜规则

任何超过30分钟没有进展的任务 = 立刻问Claude。  
"我想先研究清楚再做" = 傻瓜规则触发。直接做，研究在做的过程中完成。  
代码不完美没关系。线上能跑才是完美。
