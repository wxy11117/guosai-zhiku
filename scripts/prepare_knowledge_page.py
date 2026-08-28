from pathlib import Path


ROOT = Path.cwd()
TARGET = ROOT / "knowledge.html"


def replace_once(text: str, old: str, new: str, marker: str | None = None) -> str:
    if (marker or new) in text:
        return text
    if old not in text:
        raise RuntimeError(f"Missing expected marker: {old[:80]}")
    return text.replace(old, new, 1)


page = TARGET.read_text(encoding="utf-8")
page = page.replace("assets/logo-mark.svg", "assets/qions-model-logo.png")
page = page.replace('type="image/svg+xml"', 'type="image/png"')
page = page.replace(
    '<span class="rail-logo">M</span>',
    '<span class="rail-logo"><img src="assets/qions-model-logo.png" alt=""/></span>',
)
page = page.replace("佳子（保研版）", "violet")
page = page.replace("violet·", "violet ·")
page = page.replace(
    '可以添加微信：<b style="color:#214f82">baoyanjiazi</b>',
    '可以添加 QQ：<b style="color:#214f82">2934935729</b>',
)
page = page.replace(
    '也可以通过微信 <b>baoyanjiazi</b> 反馈',
    '也可以通过 QQ <b>2934935729</b> 反馈',
)
page = page.replace('<b>微信：</b>baoyanjiazi', '<b>QQ：</b>2934935729')
page = page.replace('<a href="app.html#create">新建</a>', '<a href="index.html">模评云官网</a>')
page = page.replace(
    'class="knowledge-workspace-link" href="app.html#create"',
    'class="knowledge-workspace-link" href="index.html"',
)
page = page.replace(
    'class="rail-diagnose" href="app.html#create"',
    'class="rail-diagnose" href="index.html"',
)
page = page.replace("knowledge.css?v=cloud1", "knowledge.css?v=modules2")
page = page.replace("knowledge.js?v=cloud1", "knowledge.js?v=modules2")
page = page.replace("knowledge.css?v=modules2", "knowledge.css?v=modules3")
page = page.replace("knowledge.js?v=modules2", "knowledge.js?v=modules3")
page = page.replace("knowledge.css?v=modules3", "knowledge.css?v=modules4")
page = page.replace("knowledge.js?v=modules3", "knowledge.js?v=modules4")
page = page.replace("knowledge.css?v=modules4", "knowledge.css?v=modules5")
page = page.replace("knowledge.js?v=modules4", "knowledge.js?v=modules5")
page = page.replace("knowledge.css?v=modules5", "knowledge.css?v=modules6")
page = page.replace("knowledge.js?v=modules5", "knowledge.js?v=modules6")
page = page.replace("knowledge.css?v=modules6", "knowledge.css?v=modules7")
page = page.replace("knowledge.css?v=modules7", "knowledge.css?v=modules8")
page = replace_once(
    page,
    "<title>CUMCM 2015–2025 国赛优秀论文方法库</title>",
    """<title>国赛智库 | 模评云智能体</title>
<meta name="description" content="模评云国赛智库：61 个建模方法、92 篇优秀论文与 2015—2025 历年赛题的智能学习工作台。"/>
<link rel="icon" href="assets/qions-model-logo.png" type="image/png"/>""",
)
page = replace_once(
    page,
    "</style>\n</head>",
    "</style>\n<link rel=\"stylesheet\" href=\"knowledge.css?v=modules8\"/>\n</head>",
)
page = replace_once(
    page,
    "<body>\n<div class=\"app\">",
    """<body>
<header class="knowledge-header">
  <a class="knowledge-brand" href="app.html" aria-label="返回模评云智能体">
    <span class="knowledge-brand-mark"><img src="assets/qions-model-logo.png" alt=""/></span>
    <span><strong>模评云智能体</strong><small>ModelScore Agent</small></span>
  </a>
  <nav class="knowledge-global-nav" aria-label="模评云主导航">
    <a href="app.html">工作流</a>
    <a href="index.html">模评云官网</a>
    <a href="corpus.html">语料库</a>
    <a class="active" href="knowledge.html" aria-current="page">国赛智库</a>
  </nav>
  <div class="knowledge-header-actions">
    <span class="knowledge-live"><i></i> 本地知识库</span>
    <a class="knowledge-workspace-link" href="index.html">开始论文诊断 <span>→</span></a>
  </div>
</header>
<div class="app">""",
)
page = replace_once(
    page,
    "<aside class=\"sidebar\">\n  <div class=\"brand\">",
    """<aside class="sidebar">
  <div class="app-rail">
    <button class="rail-identity" type="button" data-open-view="home">
      <span class="rail-logo"><img src="assets/qions-model-logo.png" alt=""/></span>
      <span><strong>国赛智库</strong><small>CUMCM · 2015—2025</small></span>
    </button>
    <nav class="rail-nav" aria-label="国赛智库模块">
      <button class="active" type="button" data-open-view="home"><span class="rail-icon">⌂</span><span>智库首页</span></button>
      <button type="button" data-open-view="router"><span class="rail-icon">✦</span><span>智能选路</span><em>AI</em></button>
      <button type="button" data-open-view="models"><span class="rail-icon">∑</span><span>模型方法库</span><em>61</em></button>
      <button type="button" data-open-view="archive"><span class="rail-icon">▤</span><span>赛题与论文</span><em>92</em></button>
      <button type="button" data-open-view="experience"><span class="rail-icon">✓</span><span>国赛实战指南</span></button>
      <button type="button" data-open-view="guide"><span class="rail-icon">i</span><span>使用说明</span></button>
    </nav>
    <div class="rail-summary">
      <div><span>知识覆盖</span><strong>153</strong></div>
      <p>61 个模型方法<br/>92 篇优秀论文</p>
    </div>
    <a class="rail-diagnose" href="index.html"><span>＋</span> 开始论文诊断</a>
  </div>
  <div class="brand">""",
    marker='<div class="app-rail">',
)
page = replace_once(
    page,
    '      <button type="button" data-open-view="models"><span class="rail-icon">∑</span><span>模型方法库</span><em>61</em></button>\n',
    '      <button type="button" data-open-view="models"><span class="rail-icon">∑</span><span>模型方法库</span><em>61</em></button>\n'
    '      <button type="button" data-open-view="projects"><span class="rail-icon">◇</span><span>学习项目</span><em>NEW</em></button>\n',
    marker='data-open-view="projects"><span class="rail-icon">◇</span>',
)
page = replace_once(
    page,
    '      <button type="button" data-open-view="projects"><span class="rail-icon">◇</span><span>学习项目</span><em>NEW</em></button>\n',
    '      <button type="button" data-open-view="projects"><span class="rail-icon">◇</span><span>学习项目</span><em>NEW</em></button>\n'
    '      <button type="button" data-open-view="ai"><span class="rail-icon">AI</span><span>AI 学习</span><em>29</em></button>\n',
    marker='data-open-view="ai"><span class="rail-icon">AI</span>',
)
page = replace_once(
    page,
    """<div class="topbar"><div class="crumb">CUMCM / NATIONAL MATHEMATICAL MODELING ARCHIVE</div><div class="actions"><button id="expandAll">展开目录</button><button onclick="window.print()">打印 / PDF</button></div></div>""",
    """<div class="topbar">
    <div class="view-heading">
      <button class="module-back" id="module-back" type="button" data-open-view="home" aria-label="返回智库首页">←</button>
      <div><span id="view-kicker">KNOWLEDGE HOME</span><strong id="view-title">智库首页</strong></div>
    </div>
    <label class="toolbar-search" for="global-search"><span>⌕</span><input id="global-search" type="search" placeholder="搜索模型、赛题或论文编号" autocomplete="off"/><kbd>/</kbd></label>
    <div class="actions"><button id="expandAll">展开当前分类</button><button onclick="window.print()">打印 / PDF</button></div>
  </div>""",
)
page = replace_once(
    page,
    """<div class="stat"><b>61</b><span>核心模型详解</span></div></div></header>

    <section id="before-use" class="before-use">""",
    """<div class="stat"><b>61</b><span>核心模型详解</span></div></div></header>

    <section class="knowledge-command" aria-labelledby="route-title">
      <div class="command-copy">
        <div class="command-eyebrow"><span></span> SMART MODEL ROUTER</div>
        <h2 id="route-title">先描述问题，再选择模型</h2>
        <p>把题目关键词、研究目标或论文编号交给智库。它会在模型详解、历年赛题和优秀论文之间同步检索。</p>
        <label class="command-search" for="smart-search">
          <span aria-hidden="true">⌕</span>
          <input id="smart-search" type="search" placeholder="例如：路径规划、时间序列、C038、农作物…" autocomplete="off"/>
          <kbd>/</kbd>
        </label>
        <div class="command-meta">
          <span id="knowledge-result-count">153 个知识条目已就绪</span>
          <a href="#experience">先看实战指南 →</a>
        </div>
      </div>
      <div class="route-agent" aria-live="polite">
        <div class="route-agent-head">
          <span><i></i> 模评云选路助手</span>
          <small>LOCAL · RULE BASED</small>
        </div>
        <p class="route-prompt">这道题最接近哪类任务？</p>
        <div class="route-intents" role="list" aria-label="问题类型">
          <button class="active" type="button" data-route="predict">预测趋势</button>
          <button type="button" data-route="optimize">寻找最优</button>
          <button type="button" data-route="evaluate">评价排序</button>
          <button type="button" data-route="classify">分类判别</button>
          <button type="button" data-route="cluster">发现结构</button>
          <button type="button" data-route="network">路径网络</button>
          <button type="button" data-route="simulate">系统仿真</button>
          <button type="button" data-route="mechanism">机理方程</button>
        </div>
        <div class="route-answer" id="route-answer"></div>
      </div>
    </section>

    <section id="before-use" class="before-use">""",
    marker='<section class="knowledge-command"',
)
page = replace_once(
    page,
    """</div></div></header>

    <section class="knowledge-command" aria-labelledby="route-title">""",
    """</div></div></header>

    <section class="module-dashboard" aria-labelledby="module-dashboard-title">
      <div class="dashboard-heading">
        <div><span>KNOWLEDGE WORKSPACE</span><h2 id="module-dashboard-title">今天想从哪里开始？</h2><p>先选择任务，再进入分类列表和具体内容；首页不再堆叠全部目录。</p></div>
        <label class="dashboard-search" for="home-search"><span>⌕</span><input id="home-search" type="search" placeholder="搜索模型、赛题、论文编号…" autocomplete="off"/><kbd>/</kbd></label>
      </div>
      <div class="module-grid">
        <button class="module-card module-card-featured" type="button" data-open-view="router">
          <span class="module-card-top"><i>01</i><em>SMART ROUTER</em></span>
          <span class="module-visual" aria-hidden="true"><i></i><i></i><i></i><i></i><b>题目</b></span>
          <strong>智能模型选路</strong>
          <small>从问题类型倒推模型主线，快速建立“题目—模型—验证”路径。</small>
          <span class="module-enter">开始选路 <b>→</b></span>
        </button>
        <button class="module-card" type="button" data-open-view="models">
          <span class="module-card-top"><i>02</i><em>METHODS</em></span>
          <span class="module-metric"><b>61</b><small>个方法</small></span>
          <strong>模型方法库</strong>
          <small>9 大类型，从直觉、公式到国赛写法和常见坑。</small>
          <span class="module-enter">进入模型库 <b>→</b></span>
        </button>
        <button class="module-card" type="button" data-open-view="archive">
          <span class="module-card-top"><i>03</i><em>ARCHIVE</em></span>
          <span class="module-metric"><b>92</b><small>篇论文</small></span>
          <strong>历年赛题与论文</strong>
          <small>按年份、题号和论文三级展开，适合同题横向对照。</small>
          <span class="module-enter">浏览资料档案 <b>→</b></span>
        </button>
        <button class="module-card module-card-soft" type="button" data-open-view="experience">
          <span class="module-card-top"><i>04</i><em>PLAYBOOK</em></span>
          <span class="module-symbol">✓</span>
          <strong>国赛实战指南</strong>
          <small>摘要、选题、验证、协作与比赛节奏。</small>
          <span class="module-enter">查看指南 <b>→</b></span>
        </button>
        <button class="module-card module-card-soft" type="button" data-open-view="guide">
          <span class="module-card-top"><i>05</i><em>START HERE</em></span>
          <span class="module-symbol">i</span>
          <strong>使用说明</strong>
          <small>资料边界、推荐顺序、AI 使用和学习建议。</small>
          <span class="module-enter">阅读说明 <b>→</b></span>
        </button>
      </div>
    </section>

    <section class="knowledge-command" aria-labelledby="route-title">""",
    marker='class="module-dashboard"',
)
page = replace_once(
    page,
    '''        <button class="module-card module-card-soft" type="button" data-open-view="guide">
          <span class="module-card-top"><i>05</i><em>START HERE</em></span>
          <span class="module-symbol">i</span>
          <strong>使用说明</strong>
          <small>资料边界、推荐顺序、AI 使用和学习建议。</small>
          <span class="module-enter">阅读说明 <b>→</b></span>
        </button>''',
    '''        <button class="module-card module-card-soft" type="button" data-open-view="guide">
          <span class="module-card-top"><i>05</i><em>START HERE</em></span>
          <span class="module-symbol">i</span>
          <strong>使用说明</strong>
          <small>资料边界、推荐顺序、AI 使用和学习建议。</small>
          <span class="module-enter">阅读说明 <b>→</b></span>
        </button>
        <button class="module-card module-card-project" type="button" data-open-view="projects">
          <span class="module-card-top"><i>06</i><em>LEARNING PROJECT</em></span>
          <span class="module-metric"><b>18</b><small>类科研图表</small></span>
          <strong>科研绘图实战</strong>
          <small>按四个阶段复现 SCI 常用图表，再迁移到国赛论文结果展示。</small>
          <span class="module-enter">进入学习项目 <b>→</b></span>
        </button>''',
    marker='class="module-card module-card-project"',
)
page = replace_once(
    page,
    '''        <button class="module-card module-card-project" type="button" data-open-view="projects">
          <span class="module-card-top"><i>06</i><em>LEARNING PROJECT</em></span>
          <span class="module-metric"><b>18</b><small>类科研图表</small></span>
          <strong>科研绘图实战</strong>
          <small>按四个阶段复现 SCI 常用图表，再迁移到国赛论文结果展示。</small>
          <span class="module-enter">进入学习项目 <b>→</b></span>
        </button>''',
    '''        <button class="module-card module-card-project" type="button" data-open-view="projects">
          <span class="module-card-top"><i>06</i><em>LEARNING PROJECT</em></span>
          <span class="module-metric"><b>18</b><small>类科研图表</small></span>
          <strong>科研绘图实战</strong>
          <small>按四个阶段复现 SCI 常用图表，再迁移到国赛论文结果展示。</small>
          <span class="module-enter">进入学习项目 <b>→</b></span>
        </button>
        <button class="module-card module-card-ai" type="button" data-open-view="ai">
          <span class="module-card-top"><i>07</i><em>AI LEARNING HUB</em></span>
          <span class="module-metric"><b>29</b><small>个知识集合</small></span>
          <strong>AI 学习模块</strong>
          <small>从入门、机器学习到大模型与科研实践，按路线浏览飞书公开知识空间。</small>
          <span class="module-enter">进入 AI 学习中心 <b>→</b></span>
        </button>''',
    marker='class="module-card module-card-ai"',
)
page = replace_once(
    page,
    '    <section class="knowledge-command" aria-labelledby="route-title">',
    '''    <section id="learning-projects" class="learning-projects" aria-labelledby="project-title">
      <header class="project-hero">
        <div class="project-hero-copy">
          <span>LEARNING PROJECT 01 · RESEARCH VISUALIZATION</span>
          <h2 id="project-title">科研绘图实战：18 类 SCI 常用图表</h2>
          <p>从“能运行示例”进阶到“能解释模型结果”。本项目按表达目标重新整理原网页目录，建议每完成一个阶段，就换成自己的建模数据复现一次。</p>
          <div class="project-actions">
            <a class="project-source" href="https://kwz55xptfhg.feishu.cn/wiki/Eujxw97tAi0qRMkaV6PckVzGnVc" target="_blank" rel="noopener noreferrer">打开飞书原学习页面 ↗</a>
            <button type="button" data-project-reset>重置学习进度</button>
          </div>
        </div>
        <div class="project-progress-panel" aria-label="学习项目进度">
          <div><span>项目进度</span><strong id="project-progress-value">0%</strong></div>
          <div class="project-progress-track"><i id="project-progress-bar"></i></div>
          <p><b id="project-progress-count">0 / 4</b> 个阶段已完成</p>
          <div class="project-stats"><span><b>18</b> 图表</span><span><b>4</b> 阶段</span><span><b>Python</b> 工具</span></div>
        </div>
      </header>

      <section class="project-brief">
        <div><span>项目目标</span><p>判断数据关系与论文叙事需求，为趋势、分布、对比、空间结构选择合适图表。</p></div>
        <div><span>建议产出</span><p>18 份可运行代码、4 张竞赛数据改造图、1 页统一配色与图注规范。</p></div>
        <div><span>完成标准</span><p>每张图都能回答“展示什么、为何用它、评委应看到什么结论”。</p></div>
      </section>

      <div class="project-stage-grid">
        <article class="project-stage" data-project-stage="foundation">
          <div class="project-stage-head"><span>STAGE 01 · 基础表达</span><em>4 类</em></div>
          <h3>先把趋势、离散关系和组间差异画清楚</h3>
          <p>适合绝大多数数据探索与论文结果页，是后续复杂图形的表达基础。</p>
          <div class="project-chart-list"><span>折线图</span><span>散点图</span><span>条形图</span><span>直方图</span></div>
          <div class="project-stage-task"><b>阶段任务</b><p>用同一份数据分别画趋势图、关系图和分布图，并写出各图不可替代的结论。</p></div>
          <button type="button" class="project-complete" data-project-complete="foundation" aria-pressed="false"><i>✓</i><span>标记本阶段完成</span></button>
        </article>

        <article class="project-stage" data-project-stage="distribution">
          <div class="project-stage-head"><span>STAGE 02 · 分布与关系</span><em>4 类</em></div>
          <h3>识别相关结构、异常值与类别分布</h3>
          <p>适合特征分析、模型前的数据洞察，以及对结果稳定性的辅助说明。</p>
          <div class="project-chart-list"><span>热力图</span><span>箱线图</span><span>小提琴图</span><span>成对关系图</span></div>
          <div class="project-stage-task"><b>阶段任务</b><p>对一组多指标数据完成相关性热力图与分布对比，说明异常值是否需要处理。</p></div>
          <button type="button" class="project-complete" data-project-complete="distribution" aria-pressed="false"><i>✓</i><span>标记本阶段完成</span></button>
        </article>

        <article class="project-stage" data-project-stage="composite">
          <div class="project-stage-head"><span>STAGE 03 · 组合与空间</span><em>6 类</em></div>
          <h3>表达多维指标、区间变化和空间层次</h3>
          <p>这些图信息密度更高，使用时必须控制指标数量、颜色和坐标尺度。</p>
          <div class="project-chart-list"><span>蜘蛛图</span><span>双轴图</span><span>面积图</span><span>带状图</span><span>等高线图</span><span>极坐标图</span></div>
          <div class="project-stage-task"><b>阶段任务</b><p>任选一种多指标评价结果，比较蜘蛛图与标准条形图，保留更清晰的一版并解释选择。</p></div>
          <button type="button" class="project-complete" data-project-complete="composite" aria-pressed="false"><i>✓</i><span>标记本阶段完成</span></button>
        </article>

        <article class="project-stage" data-project-stage="advanced">
          <div class="project-stage-head"><span>STAGE 04 · 立体与分面</span><em>4 类</em></div>
          <h3>呈现三维曲面与多组条件下的重复关系</h3>
          <p>适合参数搜索、响应面和分组对比；只有三维结构确实重要时再使用 3D。</p>
          <div class="project-chart-list"><span>3D 曲面图</span><span>3D 散点图</span><span>3D 条形图</span><span>Facet Grid</span></div>
          <div class="project-stage-task"><b>阶段任务</b><p>把二维参数扫描结果绘成响应面，再补一张等高线图，比较哪一张更利于读出最优区间。</p></div>
          <button type="button" class="project-complete" data-project-complete="advanced" aria-pressed="false"><i>✓</i><span>标记本阶段完成</span></button>
        </article>
      </div>

      <section class="project-transfer">
        <div class="project-transfer-copy"><span>TRANSFER TO CUMCM</span><h3>把绘图练习迁移到一篇国赛论文</h3><p>选一个你正在学习的模型，重画其核心结果图。图题写结论，坐标写单位，颜色只承担一种语义，并在正文解释图表支持了哪条判断。</p></div>
        <div class="project-transfer-links">
          <a href="#model-corr" data-open-model="model-corr"><span>相关分析</span><small>热力图与散点关系 →</small></a>
          <a href="#model-cluster-general" data-open-model="model-cluster-general"><span>聚类分析</span><small>分组分布与降维展示 →</small></a>
          <a href="#archive" data-open-view="archive"><span>优秀论文库</span><small>观察结果图如何服务论证 →</small></a>
        </div>
      </section>

      <aside class="project-source-note"><b>资料说明</b><p>本学习项目依据公开飞书页面的图表目录进行重组与学习路线提炼；示例代码、图片与后续更新请以原页面为准。</p></aside>
    </section>

    <section class="knowledge-command" aria-labelledby="route-title">''',
    marker='id="learning-projects"',
)
page = replace_once(
    page,
    '''      <aside class="project-source-note"><b>资料说明</b><p>本学习项目依据公开飞书页面的图表目录进行重组与学习路线提炼；示例代码、图片与后续更新请以原页面为准。</p></aside>
    </section>

    <section class="knowledge-command" aria-labelledby="route-title">''',
    '''      <aside class="project-source-note"><b>资料说明</b><p>本学习项目依据公开飞书页面的图表目录进行重组与学习路线提炼；示例代码、图片与后续更新请以原页面为准。</p></aside>
    </section>

    <section id="ai-learning" class="ai-learning" aria-labelledby="ai-learning-title">
      <header class="ai-hero">
        <div class="ai-hero-copy">
          <span>AI LEARNING HUB · FEDERATED KNOWLEDGE</span>
          <h2 id="ai-learning-title">从 AI 入门到模型实战</h2>
          <p>将“AI知识共享”公开空间的 29 个目录集合接入国赛智库，按学习阶段重新分组。本站提供路线、索引与国赛模型关联，原始文章、代码和持续更新保留在飞书知识空间。</p>
          <div class="ai-hero-actions">
            <a href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer">打开完整飞书知识空间 ↗</a>
            <button type="button" data-ai-scroll-library>浏览全部 29 个集合</button>
          </div>
        </div>
        <div class="ai-hero-matrix" aria-label="AI 学习模块概览">
          <div><strong>29</strong><span>目录集合</span></div><div><strong>4</strong><span>学习路线</span></div><div><strong>AI ×</strong><span>国赛建模</span></div><div><strong>LIVE</strong><span>原空间更新</span></div>
        </div>
      </header>

      <section class="ai-roadmap" aria-labelledby="ai-roadmap-title">
        <div class="ai-section-heading"><span>LEARNING ROUTES</span><h3 id="ai-roadmap-title">先选目标，再进入知识集合</h3><p>不要从第一篇顺序看到最后一篇；按当前任务选择路线，学完立即用国赛数据复现。</p></div>
        <div class="ai-roadmap-grid">
          <button type="button" data-ai-filter="foundation"><i>01</i><strong>入门与成长路线</strong><small>素养、阶段、7 周计划与系统学习笔记</small><span>7 个集合 →</span></button>
          <button type="button" data-ai-filter="models"><i>02</i><strong>机器学习与深度学习</strong><small>算法、神经网络、SHAP、CNN 与 XGBoost</small><span>8 个集合 →</span></button>
          <button type="button" data-ai-filter="llm"><i>03</i><strong>大模型与智能体</strong><small>LLM、部署、面试、Agent 与 Claude Code</small><span>8 个集合 →</span></button>
          <button type="button" data-ai-filter="research"><i>04</i><strong>科研与行业实践</strong><small>论文、书单、科研案例、产品与 AIGC</small><span>6 个集合 →</span></button>
        </div>
      </section>

      <section class="ai-model-bridge">
        <div><span>AI × CUMCM</span><h3>把 AI 专题接到国赛模型学习</h3><p>先在 AI 模块理解算法，再回到国赛模型库查看适用场景、论文写法和关联赛题。</p></div>
        <div class="ai-model-links"><a href="#model-rf" data-open-model="model-rf">随机森林 <b>→</b></a><a href="#model-boosting" data-open-model="model-boosting">XGBoost <b>→</b></a><a href="#model-svm" data-open-model="model-svm">SVM <b>→</b></a><a href="#model-cluster-general" data-open-model="model-cluster-general">聚类分析 <b>→</b></a></div>
      </section>

      <section class="ai-library" id="ai-library" aria-labelledby="ai-library-title">
        <div class="ai-library-head">
          <div><span>COMPLETE DIRECTORY</span><h3 id="ai-library-title">AI 知识集合目录</h3><p>完整保留当前公开空间可见的 29 个一级目录入口；输入关键词或按路线筛选。</p></div>
          <label for="ai-library-search"><span>⌕</span><input id="ai-library-search" type="search" placeholder="搜索：机器学习、LLM、论文、部署…" autocomplete="off"/></label>
        </div>
        <div class="ai-filter-bar" role="group" aria-label="AI 知识集合筛选">
          <button class="active" type="button" data-ai-filter="all">全部 <em>29</em></button><button type="button" data-ai-filter="foundation">入门成长 <em>7</em></button><button type="button" data-ai-filter="models">模型算法 <em>8</em></button><button type="button" data-ai-filter="llm">大模型智能体 <em>8</em></button><button type="button" data-ai-filter="research">科研实践 <em>6</em></button>
        </div>

        <div class="ai-collection-grid">
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="AI知识共享 愿景 入口" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>START</span><strong>AI知识共享</strong><small>知识空间总入口与共享愿景</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="人工智能入门到实战计划 学习路线" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>ROADMAP</span><strong>人工智能入门到实战计划</strong><small>从基础认知到项目实践的主路线</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="人工智能学习笔记 笔记" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>NOTES</span><strong>人工智能学习笔记</strong><small>概念、方法与学习过程记录</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="辅论带你学AI 教程" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>GUIDE</span><strong>辅论带你学AI</strong><small>面向初学者的系列教程</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="挑战7周学会人工智能 7 周" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>7 WEEKS</span><strong>挑战 7 周学会人工智能</strong><small>按周推进的阶段学习安排</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="12种人工智能初学者必备素养 素养" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>SKILLS</span><strong>12种人工智能初学者必备素养</strong><small>建立有效学习与实践习惯</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="foundation" data-ai-search="6大人工智能重要学习阶段 阶段" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>STAGES</span><strong>6大人工智能重要学习阶段</strong><small>从数学、代码到模型应用的阶段框架</small><b>打开集合 ↗</b></a>

          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="人工智能全网最纯干货 算法 深度学习 机器学习" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>FEATURED</span><strong>人工智能全网最纯干货</strong><small>算法、训练、评估与模型实战长目录</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="神经网络全解 深度学习" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>DEEP LEARNING</span><strong>神经网络全解</strong><small>结构、训练、压缩与经典网络</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="机器学习全解 分类 回归 聚类" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>MACHINE LEARNING</span><strong>机器学习全解</strong><small>分类、回归、聚类与模型评价</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="突破100个强大算法模型 算法" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>100 MODELS</span><strong>突破100个强大算法模型</strong><small>按专题扩展算法工具箱</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="SHAP 模型解释 机器学习 深度学习" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>EXPLAINABLE AI</span><strong>SHAP全解析</strong><small>机器学习与深度学习模型解释教程</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="XGBoost 提升树 集成学习" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>BOOSTING</span><strong>突破最强算法模型，XGBoost</strong><small>原理、调参与项目应用</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="卷积神经网络 CNN 原理" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>VISION</span><strong>卷积神经网络（CNN）详解</strong><small>结构原理与图像任务基础</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="models" data-ai-search="FlashAttention-2 Faster Attention 并行 注意力" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>ATTENTION</span><strong>FlashAttention-2</strong><small>注意力计算、并行与工作划分</small><b>打开集合 ↗</b></a>

          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="LLM课程 大语言模型 课程" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>LLM COURSE</span><strong>LLM课程大</strong><small>大语言模型系统课程入口</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="最全大模型面试 面试题" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>INTERVIEW</span><strong>最全大模型面试</strong><small>概念、工程与应用面试准备</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="大模型本地部署教程 部署" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>DEPLOYMENT</span><strong>大模型本地部署教程</strong><small>环境、推理与本地运行流程</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="AI最全知识库 大模型 人工智能" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>KNOWLEDGE BASE</span><strong>AI最全知识库</strong><small>综合 AI 主题目录与资料入口</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="AI大模型知识库 LLM" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>LLM LIBRARY</span><strong>AI大模型知识库</strong><small>LLM 原理、应用与生态资料</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="Agent智能体入门手册 AI自动化" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>AGENT</span><strong>Agent智能体入门手册</strong><small>解锁 AI 自动化与智能体基础</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="Claude Code 101 实战指南 编程" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>CODING AGENT</span><strong>Claude Code 101实战指南</strong><small>AI 编程助手的基础工作流</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="llm" data-ai-search="人工智能入门到实战计划 智能体 进阶" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>ADVANCED PLAN</span><strong>🤖人工智能入门到实战计划</strong><small>知识空间中的进阶实战目录入口</small><b>打开集合 ↗</b></a>

          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="人工智能论文合集 论文 科研" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>PAPERS</span><strong>人工智能论文合集</strong><small>论文阅读与前沿研究入口</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="人工智能最全书单 书籍" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>BOOKS</span><strong>人工智能最全书单</strong><small>按方向补足理论与工程基础</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="科研屋 学术 前沿" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>RESEARCH</span><strong>科研屋</strong><small>科研案例与学术前沿专题</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="AI肺炎诊断 医疗 分类 95.5" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>CASE STUDY</span><strong>AI肺炎诊断案例</strong><small>医疗图像分类的四步实践案例</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="AI产品经理技术合集 产品 技术" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>AI PRODUCT</span><strong>AI产品经理技术合集</strong><small>产品视角理解模型与落地链路</small><b>打开集合 ↗</b></a>
          <a class="ai-collection-card" data-ai-collection data-ai-group="research" data-ai-search="AIGC日常盘点 生成式AI" href="https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home" target="_blank" rel="noopener noreferrer"><span>AIGC</span><strong>AIGC日常盘点</strong><small>生成式 AI 动态与应用主题整理</small><b>打开集合 ↗</b></a>
        </div>
        <p class="ai-library-empty" id="ai-library-empty" hidden>没有匹配的 AI 知识集合，请换一个关键词。</p>
      </section>

      <aside class="ai-source-note"><b>收录方式</b><p>国赛智库提供目录级索引、学习路线和模型关联，不复制第三方文章全文。飞书空间中的子文章、代码、插图及后续更新均以原知识空间为准。</p></aside>
    </section>

    <section class="knowledge-command" aria-labelledby="route-title">''',
    marker='id="ai-learning"',
)
ai_space_url = "https://kwz55xptfhg.feishu.cn/wiki/space/7398415988541702147?ccm_open_type=lark_wiki_spaceLink&amp;open_tab_from=wiki_home"
page = page.replace(
    f'<a href="{ai_space_url}" target="_blank" rel="noopener noreferrer">打开完整飞书知识空间 ↗</a>',
    '<button type="button" data-ai-scroll-library>浏览全部本地课程</button>',
)
if 'id="ai-learning"' in page:
    ai_start = page.index('<section id="ai-learning"')
    ai_end = page.index('<section class="knowledge-command"', ai_start)
    ai_segment = page[ai_start:ai_end]
    ai_segment = ai_segment.replace(
        f'href="{ai_space_url}" target="_blank" rel="noopener noreferrer"',
        'href="#ai-topic-viewer" data-ai-open',
    )
    ai_segment = ai_segment.replace(
        "将“AI知识共享”公开空间的 29 个目录集合接入国赛智库，按学习阶段重新分组。本站提供路线、索引与国赛模型关联，原始文章、代码和持续更新保留在飞书知识空间。",
        "将 29 个 AI 知识集合改写为国赛智库内可直接学习的本地课程，按阶段重新分组。每课包含知识目标、核心概念、实践任务和国赛迁移建议，不再依赖外部文档。",
    )
    ai_segment = ai_segment.replace(
        "完整保留当前公开空间可见的 29 个一级目录入口；输入关键词或按路线筛选。",
        "29 个自主整理的本地课程；输入关键词或按路线筛选，点击后直接在智库内学习。",
    )
    ai_segment = ai_segment.replace("在原空间查找 ↗", "打开本地课程 →")
    page = page[:ai_start] + ai_segment + page[ai_end:]
page = replace_once(
    page,
    '''      <aside class="ai-source-note"><b>收录方式</b><p>国赛智库提供目录级索引、学习路线和模型关联，不复制第三方文章全文。飞书空间中的子文章、代码、插图及后续更新均以原知识空间为准。</p></aside>''',
    '''      <section class="ai-topic-viewer" id="ai-topic-viewer" hidden aria-live="polite">
        <header class="ai-topic-head">
          <div><span id="ai-topic-kicker">LOCAL AI COURSE</span><h3 id="ai-topic-title">选择一门课程开始学习</h3><p id="ai-topic-summary">点击上方任一知识集合，这里会展开完整的本地学习单元。</p></div>
          <button type="button" data-ai-close-topic aria-label="关闭当前课程">×</button>
        </header>
        <div class="ai-topic-layout">
          <article class="ai-topic-intro"><span>WHY IT MATTERS</span><h4>为什么要学</h4><p id="ai-topic-why"></p></article>
          <article class="ai-topic-concepts"><span>CORE KNOWLEDGE</span><h4>核心知识清单</h4><ol id="ai-topic-concepts"></ol></article>
          <article class="ai-topic-task"><span>PRACTICE</span><h4>本课实践任务</h4><p id="ai-topic-task"></p><div><b>建议产出</b><span id="ai-topic-output"></span></div></article>
          <article class="ai-topic-cumcm"><span>TRANSFER TO CUMCM</span><h4>如何迁移到国赛</h4><p id="ai-topic-cumcm"></p><div class="ai-topic-models" id="ai-topic-models"></div></article>
        </div>
      </section>

      <aside class="ai-source-note"><b>课程说明</b><p>本模块为 violet 自主整理的本地学习内容，依据公开目录主题重新组织，不复制第三方文章、代码或图片。课程可直接在国赛智库内学习，并与模型库和优秀论文模块相互跳转。</p></aside>''',
    marker='id="ai-topic-viewer"',
)
page = replace_once(
    page,
    "</script>\n</body></html>",
    "</script>\n<script src=\"knowledge.js?v=modules6\"></script>\n</body></html>",
)
page = replace_once(
    page,
    """    <div class="problem-order-note"><b>阅读顺序：</b>每道题先展开“完整赛题（官方原文入口）”查看题目和附件，再看模型路线与优秀论文。这样能把每篇论文的方法选择放回具体题目约束中理解。</div>""",
    """    <section class="archive-module-head">
      <div><span>CUMCM ARCHIVE · 2015—2025</span><h2>历年赛题与优秀论文</h2><p>先按年份进入，再展开题目与论文；适合同题路线比较、模型复盘与论文结构学习。</p></div>
      <div class="archive-module-stats"><span><b>11</b> 届竞赛</span><span><b>46</b> 道赛题</span><span><b>92</b> 篇论文</span></div>
    </section>
    <div class="problem-order-note"><b>阅读顺序：</b>每道题先展开“完整赛题（官方原文入口）”查看题目和附件，再看模型路线与优秀论文。这样能把每篇论文的方法选择放回具体题目约束中理解。</div>""",
)
TARGET.write_text(page, encoding="utf-8", newline="\n")
print(f"Prepared {TARGET} ({len(page)} chars)")
