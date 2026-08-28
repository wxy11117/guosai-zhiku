const routeCatalog = {
  predict: {
    title: "先建立可解释基线",
    copy: "少量数据先看回归或灰色预测；长时间序列再比较 ARIMA 与时序神经网络。",
    models: [["线性回归", "model-linear-reg"], ["灰色预测", "model-grey"], ["ARIMA", "model-arima"], ["LSTM", "model-lstm"]],
  },
  optimize: {
    title: "先写目标函数与约束",
    copy: "变量连续看线性或非线性规划；选与不选用整数规划；多阶段决策再看动态规划。",
    models: [["线性规划", "model-lp"], ["整数规划", "model-ip"], ["动态规划", "model-dp"], ["多目标优化", "model-multiobj"]],
  },
  evaluate: {
    title: "权重与排序要分开解释",
    copy: "先说明指标如何赋权，再说明方案如何排序；主客观权重最好做稳健性对照。",
    models: [["AHP", "model-ahp"], ["熵权法", "model-entropy"], ["TOPSIS", "model-topsis"], ["DEA", "model-dea"]],
  },
  classify: {
    title: "从基线模型开始比较",
    copy: "先用逻辑回归建立解释基线，再用树模型或 SVM 提升效果，并用 ROC/AUC 选阈值。",
    models: [["逻辑回归", "model-logistic"], ["随机森林", "model-rf"], ["SVM", "model-svm"], ["ROC / AUC", "model-roc"]],
  },
  cluster: {
    title: "先确认数据有没有标签",
    copy: "没有标签时先聚类找结构；维度高先用 PCA；形状不规则或有噪声可比较 DBSCAN。",
    models: [["聚类总览", "model-cluster-general"], ["K-Means", "model-kmeans"], ["DBSCAN", "model-dbscan"], ["PCA", "model-pca"]],
  },
  network: {
    title: "先把对象画成点和边",
    copy: "单点到单点看最短路，访问全部节点看 TSP，多车辆配送看 VRP，容量约束看网络流。",
    models: [["最短路径", "model-shortest"], ["最小生成树", "model-mst"], ["TSP", "model-tsp"], ["VRP", "model-vrp"]],
  },
  simulate: {
    title: "解析求解困难时再仿真",
    copy: "随机风险用蒙特卡罗，流程排队用离散事件，反馈系统看系统动力学。",
    models: [["蒙特卡罗", "model-mc"], ["离散事件仿真", "model-des"], ["系统动力学", "model-system-dynamics"], ["多智能体", "model-abm"]],
  },
  mechanism: {
    title: "先写守恒关系，再估参数",
    copy: "把物理过程写成微分方程或差分方程，用最小二乘校准，并补充误差与灵敏度分析。",
    models: [["常微分方程", "model-ode"], ["偏微分方程", "model-pde"], ["最小二乘", "model-least-sq"], ["参数优化", "model-param-opt"]],
  },
};

const courseResources = [
  { order: 1, title: "第1讲 教材和参考资料", file: "lesson-01-textbooks.rar", bytes: 119159653, kind: "RAR", targets: [] },
  { order: 2, title: "第2讲 层次分析法", file: "lesson-02-ahp.rar", bytes: 6767578, kind: "RAR", targets: ["model-ahp"] },
  { order: 3, title: "第3讲 模糊综合评价", file: "lesson-03-fuzzy-evaluation.rar", bytes: 6627680, kind: "RAR", targets: ["model-fuzzy"] },
  { order: 4, title: "第4讲 熵权法", file: "lesson-04-entropy-weight.rar", bytes: 5359024, kind: "RAR", targets: ["model-entropy"] },
  { order: 5, title: "第5讲 TOPSIS", file: "lesson-05-topsis.rar", bytes: 7067999, kind: "RAR", targets: ["model-topsis"] },
  { order: 6, title: "第6讲 灰色关联分析", file: "lesson-06-grey-relational-analysis.rar", bytes: 1481888, kind: "RAR", targets: ["model-corr"] },
  { order: 7, title: "第7讲 线性规划", file: "lesson-07-linear-programming.rar", bytes: 1391163, kind: "RAR", targets: ["model-lp"] },
  { order: 8, title: "第8讲 整数规划", file: "lesson-08-integer-programming.rar", bytes: 1436700, kind: "RAR", targets: ["model-ip"] },
  { order: 9, title: "第9讲 非线性规划", file: "lesson-09-nonlinear-programming.rar", bytes: 1764294, kind: "RAR", targets: ["model-nlp"] },
  { order: 10, title: "第10讲 图论与最短路径算法", file: "lesson-10-graph-shortest-path.rar", bytes: 5594719, kind: "RAR", targets: ["model-shortest"] },
  { order: 11, title: "第11讲 网络最大流问题", file: "lesson-11-maximum-flow.rar", bytes: 1228359, kind: "RAR", targets: ["model-maxflow"] },
  { order: 12, title: "第12讲 最小费用最大流问题", file: "lesson-12-min-cost-max-flow.rar", bytes: 1930513, kind: "RAR", targets: ["model-maxflow"] },
  { order: 13, title: "第13讲 旅行商（TSP）问题", file: "lesson-13-tsp.rar", bytes: 876424, kind: "RAR", targets: ["model-tsp"] },
  { order: 14, title: "第14讲 插值算法", file: "lesson-14-interpolation.rar", bytes: 2379583, kind: "RAR", targets: ["model-interp"] },
  { order: 15, title: "第15讲 拟合算法", file: "lesson-15-curve-fitting.rar", bytes: 1347360, kind: "RAR", targets: ["model-poly-reg"] },
  { order: 16, title: "第16讲 微分方程", file: "lesson-16-differential-equations.rar", bytes: 7079550, kind: "RAR", targets: ["model-ode"] },
  { order: 17, title: "第17讲 时间序列", file: "lesson-17-time-series.rar", bytes: 311084924, kind: "RAR", targets: ["model-arima"] },
  { order: 18, title: "第18讲 聚类分析", file: "lesson-18-clustering.rar", bytes: 1710099, kind: "RAR", targets: ["model-cluster-general"] },
  { order: 19, title: "智能算法课程包", file: "intelligent-algorithms.rar", bytes: 9122802, kind: "RAR", targets: ["model-ga", "model-sa", "model-pso"] },
  { order: 20, title: "智能算法与保命指南", file: "intelligent-algorithms-survival-guide.pdf", bytes: 2209052, kind: "PDF", targets: ["model-sa"] },
].map((resource) => ({ ...resource, href: `assets/learning-packs/${resource.file}` }));

const courseResourceGroups = [
  { title: "入门与综合评价", subtitle: "教材、AHP、模糊评价、熵权、TOPSIS 与灰色关联", orders: [1, 2, 3, 4, 5, 6] },
  { title: "规划与网络优化", subtitle: "线性、整数、非线性规划，以及路径与网络流", orders: [7, 8, 9, 10, 11, 12, 13] },
  { title: "数值计算与数据分析", subtitle: "插值、拟合、微分方程、时间序列与聚类", orders: [14, 15, 16, 17, 18] },
  { title: "智能算法专题", subtitle: "模拟退火等启发式算法与竞赛保命指南", orders: [19, 20] },
];

function formatResourceBytes(bytes) {
  if (bytes >= 1024 ** 3) return `${(bytes / 1024 ** 3).toFixed(1)} GB`;
  if (bytes >= 1024 ** 2) return `${(bytes / 1024 ** 2).toFixed(bytes >= 100 * 1024 ** 2 ? 0 : 1)} MB`;
  return `${Math.max(1, Math.round(bytes / 1024))} KB`;
}

function courseResourceLink(resource, compact = false) {
  return `<a class="${compact ? "model-resource-link" : "course-resource-card"}" href="${resource.href}" download>
    <span class="course-file-kind">${resource.kind}</span>
    <span class="course-file-copy"><strong>${resource.title}</strong><small>${resource.kind === "RAR" ? "课件、案例与配套文件" : "专题学习指南"} · ${formatResourceBytes(resource.bytes)}</small></span>
    <span class="course-download-icon" aria-hidden="true">↓</span>
  </a>`;
}

function injectCourseResources() {
  const library = document.querySelector("#model-library");
  if (library && !document.querySelector("#course-resources")) {
    const resourceCenter = document.createElement("section");
    resourceCenter.id = "course-resources";
    resourceCenter.className = "course-resource-center section-anchor";
    resourceCenter.innerHTML = `
      <div class="course-resource-head">
        <div><span>COURSE DOWNLOADS · 20 FILES</span><h3>课程课件与配套资料</h3><p>按知识路线下载课程包；展开具体模型时，也能在对应知识点直接取得相关资料。</p></div>
        <div class="course-resource-summary"><b>18</b><span>专题课程</span><b>2</b><span>智能算法资料</span></div>
      </div>
      <div class="course-resource-groups">
        ${courseResourceGroups.map((group) => `<section class="course-resource-group">
          <div class="course-group-title"><div><strong>${group.title}</strong><small>${group.subtitle}</small></div><span>${group.orders.length} 份</span></div>
          <div class="course-resource-grid">${group.orders.map((order) => courseResourceLink(courseResources.find((item) => item.order === order))).join("")}</div>
        </section>`).join("")}
      </div>`;
    library.querySelector(":scope > .library-head")?.after(resourceCenter);
  }

  courseResources.forEach((resource) => {
    resource.targets.forEach((targetId) => {
      const modelBody = document.querySelector(`#${CSS.escape(targetId)} .model-body`);
      if (!modelBody) return;
      let resourceBlock = modelBody.querySelector(":scope > .model-learning-resources");
      if (!resourceBlock) {
        resourceBlock = document.createElement("div");
        resourceBlock.className = "model-learning-resources";
        resourceBlock.innerHTML = `<div class="model-resource-head"><div><span>配套课程</span><strong>下载课件与案例文件</strong></div><small>离线学习 · 原始资料包</small></div><div class="model-resource-row"></div>`;
        modelBody.querySelector(":scope > .paper-use")?.before(resourceBlock);
      }
      resourceBlock.querySelector(":scope .model-resource-row")?.insertAdjacentHTML("beforeend", courseResourceLink(resource, true));
    });
  });

  const moduleGrid = document.querySelector(".module-grid");
  if (moduleGrid && !moduleGrid.querySelector("[data-resource-jump]")) {
    const resourceModule = document.createElement("button");
    resourceModule.type = "button";
    resourceModule.className = "module-card module-card-soft module-card-resources";
    resourceModule.dataset.resourceJump = "true";
    resourceModule.innerHTML = `<span class="module-card-top"><i>08</i><em>COURSE FILES</em></span><span class="module-symbol">↓</span><strong>课程资料下载</strong><small>18 讲课程包与智能算法专题资料，按知识点对应整理。</small><span class="module-enter">进入资料中心 <b>→</b></span>`;
    resourceModule.addEventListener("click", () => {
      setKnowledgeView("models", { scroll: false });
      window.setTimeout(() => document.querySelector("#course-resources")?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
    });
    moduleGrid.append(resourceModule);
  }
}

injectCourseResources();

const smartSearch = document.querySelector("#smart-search");
const globalSearch = document.querySelector("#global-search");
const homeSearch = document.querySelector("#home-search");
const sourceSearch = document.querySelector("#search");
const resultCount = document.querySelector("#knowledge-result-count");
const routeAnswer = document.querySelector("#route-answer");
const routeButtons = [...document.querySelectorAll("[data-route]")];
const openViewButtons = [...document.querySelectorAll("[data-open-view]")];
const railButtons = [...document.querySelectorAll(".rail-nav [data-open-view]")];
const moduleBack = document.querySelector("#module-back");
const viewTitle = document.querySelector("#view-title");
const viewKicker = document.querySelector("#view-kicker");
const expandAllButton = document.querySelector("#expandAll");
const modelCategories = [...document.querySelectorAll(".model-category-section")];
const yearSections = [...document.querySelectorAll(".year-section")];

const viewMeta = {
  home: ["智库首页", "KNOWLEDGE HOME"],
  router: ["智能模型选路", "SMART MODEL ROUTER"],
  models: ["模型方法库", "61 METHODS · 9 CATEGORIES"],
  projects: ["学习项目", "PROJECT 01 · RESEARCH VISUALIZATION"],
  ai: ["AI 学习模块", "29 COLLECTIONS · 4 LEARNING ROUTES"],
  archive: ["历年赛题与论文", "CUMCM ARCHIVE · 2015—2025"],
  experience: ["国赛实战指南", "CUMCM PLAYBOOK"],
  guide: ["使用说明", "READ BEFORE USE"],
  search: ["全库搜索", "SEARCH RESULTS"],
};

let activeView = "home";

const projectProgressKey = "modelscore-learning-project-sci-plots-v1";

const aiLessonConcepts = {
  "AI知识共享": ["人工智能任务的分类框架", "数据、模型、损失函数与评价指标", "训练集、验证集和测试集的职责", "可复现实验记录与知识共享规范"],
  "人工智能入门到实战计划": ["Python 与线性代数基础", "数据清洗、特征工程和可视化", "监督学习与无监督学习主线", "从基线模型到完整项目交付"],
  "人工智能学习笔记": ["概念卡片与公式卡片", "代码实验的输入输出记录", "错误案例和调参过程复盘", "从阅读到复现的闭环笔记法"],
  "辅论带你学AI": ["用问题类型选择算法", "用小样本建立可解释基线", "用对照实验判断改进是否有效", "把模型结果写成可验证结论"],
  "挑战 7 周学会人工智能": ["第1周数学与编程", "第2—3周经典机器学习", "第4—5周神经网络与深度学习", "第6—7周项目复现与汇报"],
  "12种人工智能初学者必备素养": ["问题拆解与数据意识", "代码阅读与调试能力", "实验对照与结果质疑", "伦理、版权与数据安全意识"],
  "6大人工智能重要学习阶段": ["数学和编程准备", "数据处理与统计基础", "经典机器学习", "深度学习、工程部署与专题研究"],
  "人工智能全网最纯干货": ["回归、分类、聚类和降维", "神经网络训练与正则化", "Transformer、GAN、RAG 与迁移学习", "模型评价、解释和工程实战"],
  "神经网络全解": ["神经元、层和前向传播", "反向传播与梯度下降", "激活函数、损失函数与正则化", "CNN、RNN、Transformer 等典型结构"],
  "机器学习全解": ["线性与逻辑回归", "决策树、随机森林与集成学习", "SVM、KNN、朴素贝叶斯", "聚类、降维和模型评价"],
  "突破100个强大算法模型": ["按任务建立算法谱系", "算法假设与适用数据", "计算复杂度和解释能力", "基线、改进与集成策略"],
  "SHAP全解析": ["局部解释与全局解释", "Shapley 值的边际贡献思想", "特征重要性、依赖图和交互效应", "解释稳定性与误用风险"],
  "突破最强算法模型，XGBoost": ["梯度提升与加法模型", "目标函数、正则项和二阶信息", "树结构参数与学习率", "交叉验证、早停与特征重要性"],
  "卷积神经网络（CNN）详解": ["卷积核、步长和填充", "池化与感受野", "特征图和通道", "分类、检测与迁移学习流程"],
  "FlashAttention-2": ["注意力计算的时间和空间瓶颈", "分块计算与显存访问", "并行度和工作划分", "速度、精度与硬件条件的权衡"],
  "LLM课程大": ["分词、嵌入与 Transformer", "预训练、指令微调和对齐", "推理、上下文窗口和采样", "RAG、工具调用和应用评测"],
  "最全大模型面试": ["Transformer 与注意力机制", "训练、微调和推理差异", "RAG、Agent 与向量检索", "性能、成本、安全和评测"],
  "大模型本地部署教程": ["模型格式、量化和硬件需求", "推理框架与服务接口", "上下文、批处理和显存管理", "日志、监控与隐私边界"],
  "AI最全知识库": ["AI 知识地图的层级设计", "术语、算法和项目之间的关联", "资料可信度与更新记录", "从检索到实践的学习闭环"],
  "AI大模型知识库": ["大模型基础架构", "训练与微调方法", "检索增强和工具使用", "大模型评测、安全与落地"],
  "Agent智能体入门手册": ["目标、状态、记忆和工具", "规划、执行与反馈循环", "单智能体和多智能体协作", "权限、失败恢复和结果验证"],
  "Claude Code 101实战指南": ["任务描述与上下文组织", "代码库检索和改动边界", "测试驱动的迭代流程", "代码审查、回滚和安全检查"],
  "🤖人工智能入门到实战计划": ["选题与需求定义", "数据方案和评价标准", "模型原型与迭代实验", "演示、文档和项目复盘"],
  "人工智能论文合集": ["摘要、问题与贡献定位", "方法假设和实验设计", "基线、消融与统计显著性", "局限性、复现性和延伸问题"],
  "人工智能最全书单": ["数学与统计基础书目", "机器学习和深度学习教材", "工程实践与系统设计", "按目标制定阅读顺序"],
  "科研屋": ["研究问题与可检验假设", "文献检索和证据链", "实验设计与不确定性", "图表、论文结构和学术表达"],
  "AI肺炎诊断案例": ["医学图像预处理", "分类模型与迁移学习", "敏感度、特异度和 AUC", "数据偏差、外部验证与临床边界"],
  "AI产品经理技术合集": ["用户问题与 AI 能力边界", "数据闭环和评价指标", "模型、工作流与交互设计", "成本、风险和上线监控"],
  "AIGC日常盘点": ["文本、图像和多模态生成", "提示、控制和编辑工作流", "质量、事实性与版权风险", "应用场景和效果评估"],
};

const aiGroupProfiles = {
  foundation: {
    label: "FOUNDATION · 入门成长",
    why: "它负责建立可迁移的学习框架，避免只记术语、不会处理真实数据。",
    task: (title) => `围绕“${title}”画一张一页知识地图，再选择一份小数据完成从清洗、建模到评价的最小闭环。`,
    output: "1 张知识地图＋1 份可运行实验记录",
    cumcm: "把学习路线压缩成赛前三周训练表：每个知识点必须对应一道历年题、一次代码复现和一段论文表达。",
    models: [["线性回归", "model-linear-reg"], ["逻辑回归", "model-logistic"], ["聚类总览", "model-cluster-general"]],
  },
  models: {
    label: "MODELS · 模型算法",
    why: "它帮助你理解算法假设、评价方法和改进条件，比赛中才能根据问题选择模型。",
    task: (title) => `为“${title}”建立基线与改进模型，固定数据划分和评价指标，比较精度、稳定性、解释性与运行成本。`,
    output: "1 组对照实验＋1 张结果图＋1 段模型选择说明",
    cumcm: "国赛中先用可解释基线回答问题，再用复杂模型提升效果，并补充交叉验证、灵敏度或误差分析。",
    models: [["随机森林", "model-rf"], ["XGBoost", "model-boosting"], ["SVM", "model-svm"], ["ROC / AUC", "model-roc"]],
  },
  llm: {
    label: "LLM & AGENT · 大模型智能体",
    why: "它把大模型从聊天工具还原为可评估的系统组件，便于理解检索、工具和智能体工作流。",
    task: (title) => `围绕“${title}”设计一个小型本地工作流，明确输入、知识来源、工具权限、输出格式和人工复核点。`,
    output: "1 张系统流程图＋1 份提示/工具规范＋3 个测试案例",
    cumcm: "可把大模型用于资料整理、代码解释和写作检查，但模型结论必须回到数据、公式和可复现实验验证。",
    models: [["文本分类基线", "model-logistic"], ["关联规则", "model-assoc"], ["多智能体", "model-abm"]],
  },
  research: {
    label: "RESEARCH · 科研实践",
    why: "它把算法学习推进到证据、实验、论文和真实场景，重点是结论是否可信。",
    task: (title) => `选择“${title}”中的一个研究问题，整理问题—数据—方法—实验—结论—局限六栏研究卡，并提出一个可复现的改进实验。`,
    output: "1 张研究卡＋1 个复现实验方案＋1 段局限性分析",
    cumcm: "直接迁移到国赛论文结构：摘要闭环、变量定义、模型假设、验证实验、结果解释和优缺点必须前后一致。",
    models: [["方差分析", "model-anova"], ["参数优化", "model-param-opt"], ["蒙特卡罗", "model-mc"]],
  },
};

function initLearningProject() {
  const stageButtons = [...document.querySelectorAll("[data-project-complete]")];
  const resetButton = document.querySelector("[data-project-reset]");
  const value = document.querySelector("#project-progress-value");
  const count = document.querySelector("#project-progress-count");
  const bar = document.querySelector("#project-progress-bar");
  if (!stageButtons.length) return;

  let completed = new Set();
  try {
    const stored = JSON.parse(localStorage.getItem(projectProgressKey) || "[]");
    if (Array.isArray(stored)) completed = new Set(stored);
  } catch (_) {
    completed = new Set();
  }

  const render = () => {
    const done = stageButtons.filter((button) => completed.has(button.dataset.projectComplete)).length;
    const percent = Math.round((done / stageButtons.length) * 100);
    stageButtons.forEach((button) => {
      const isDone = completed.has(button.dataset.projectComplete);
      button.classList.toggle("is-complete", isDone);
      button.setAttribute("aria-pressed", String(isDone));
      button.querySelector("span").textContent = isDone ? "本阶段已完成" : "标记本阶段完成";
      button.closest(".project-stage")?.classList.toggle("is-complete", isDone);
    });
    if (value) value.textContent = `${percent}%`;
    if (count) count.textContent = `${done} / ${stageButtons.length}`;
    if (bar) bar.style.width = `${percent}%`;
    try {
      localStorage.setItem(projectProgressKey, JSON.stringify([...completed]));
    } catch (_) {
      // 本地存储不可用时，进度仍在当前页面会话内有效。
    }
  };

  stageButtons.forEach((button) => button.addEventListener("click", () => {
    const stage = button.dataset.projectComplete;
    if (completed.has(stage)) completed.delete(stage);
    else completed.add(stage);
    render();
  }));
  resetButton?.addEventListener("click", () => {
    completed.clear();
    render();
  });
  render();
}

function initAiLearningLibrary() {
  const cards = [...document.querySelectorAll("[data-ai-collection]")];
  const filterButtons = [...document.querySelectorAll("[data-ai-filter]")];
  const search = document.querySelector("#ai-library-search");
  const empty = document.querySelector("#ai-library-empty");
  const library = document.querySelector("#ai-library");
  const scrollButtons = [...document.querySelectorAll("[data-ai-scroll-library]")];
  const viewer = document.querySelector("#ai-topic-viewer");
  const closeViewer = document.querySelector("[data-ai-close-topic]");
  const topicKicker = document.querySelector("#ai-topic-kicker");
  const topicTitle = document.querySelector("#ai-topic-title");
  const topicSummary = document.querySelector("#ai-topic-summary");
  const topicWhy = document.querySelector("#ai-topic-why");
  const topicConcepts = document.querySelector("#ai-topic-concepts");
  const topicTask = document.querySelector("#ai-topic-task");
  const topicOutput = document.querySelector("#ai-topic-output");
  const topicCumcm = document.querySelector("#ai-topic-cumcm");
  const topicModels = document.querySelector("#ai-topic-models");
  if (!cards.length) return;

  let activeFilter = "all";
  const render = () => {
    const query = search?.value.trim().toLowerCase() || "";
    let visible = 0;
    cards.forEach((card) => {
      const matchesGroup = activeFilter === "all" || card.dataset.aiGroup === activeFilter;
      const haystack = `${card.dataset.aiSearch || ""} ${card.textContent || ""}`.toLowerCase();
      const matchesQuery = !query || haystack.includes(query);
      const show = matchesGroup && matchesQuery;
      card.hidden = !show;
      if (show) visible += 1;
    });
    filterButtons.forEach((button) => button.classList.toggle("active", button.dataset.aiFilter === activeFilter));
    if (empty) empty.hidden = visible !== 0;
  };

  filterButtons.forEach((button) => button.addEventListener("click", () => {
    activeFilter = button.dataset.aiFilter || "all";
    render();
    library?.scrollIntoView({ behavior: "smooth", block: "start" });
  }));
  search?.addEventListener("input", render);
  scrollButtons.forEach((button) => button.addEventListener("click", () => library?.scrollIntoView({ behavior: "smooth", block: "start" })));

  const openLesson = (card) => {
    const title = card.querySelector("strong")?.textContent.trim() || "AI 本地课程";
    const summary = card.querySelector("small")?.textContent.trim() || "围绕本主题建立可复现的学习与实践闭环。";
    const group = card.dataset.aiGroup || "foundation";
    const profile = aiGroupProfiles[group] || aiGroupProfiles.foundation;
    const concepts = aiLessonConcepts[title] || ["问题定义", "数据准备", "模型方法", "结果验证"];
    if (topicKicker) topicKicker.textContent = profile.label;
    if (topicTitle) topicTitle.textContent = title;
    if (topicSummary) topicSummary.textContent = summary;
    if (topicWhy) topicWhy.textContent = `${summary}。${profile.why}`;
    if (topicConcepts) topicConcepts.innerHTML = concepts.map((item) => `<li>${item}</li>`).join("");
    if (topicTask) topicTask.textContent = profile.task(title);
    if (topicOutput) topicOutput.textContent = profile.output;
    if (topicCumcm) topicCumcm.textContent = profile.cumcm;
    if (topicModels) topicModels.innerHTML = profile.models.map(([label, id]) => `<a href="#${id}" data-open-model="${id}">${label} <b>→</b></a>`).join("");
    viewer?.removeAttribute("hidden");
    cards.forEach((item) => item.classList.toggle("is-open", item === card));
    window.setTimeout(() => viewer?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
  };

  cards.forEach((card) => card.addEventListener("click", (event) => {
    event.preventDefault();
    openLesson(card);
  }));
  closeViewer?.addEventListener("click", () => {
    viewer?.setAttribute("hidden", "");
    cards.forEach((card) => card.classList.remove("is-open"));
    library?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  render();
}

function renderRoute(routeKey) {
  const route = routeCatalog[routeKey] || routeCatalog.predict;
  routeAnswer.innerHTML = `
    <div class="route-answer-copy">
      <strong>${route.title}</strong>
      <p>${route.copy}</p>
    </div>
    <div class="route-models">
      ${route.models.map(([label, id]) => `<a href="#${id}" data-open-model="${id}">${label}</a>`).join("")}
    </div>`;
}

function visibleKnowledgeCount() {
  const visible = [...document.querySelectorAll(".searchable")].filter((item) => item.style.display !== "none");
  return {
    total: visible.length,
    models: visible.filter((item) => item.classList.contains("model-detail")).length,
    papers: visible.filter((item) => item.classList.contains("paper-card")).length,
  };
}

function syncResultCount() {
  if (!resultCount) return;
  const count = visibleKnowledgeCount();
  resultCount.textContent = sourceSearch?.value.trim()
    ? `找到 ${count.models} 个模型 · ${count.papers} 篇论文`
    : `${count.total} 个知识条目已就绪`;
  resultCount.classList.remove("knowledge-result-pulse");
  requestAnimationFrame(() => resultCount.classList.add("knowledge-result-pulse"));
}

function runKnowledgeSearch(value) {
  if (!sourceSearch) return;
  sourceSearch.value = value;
  [smartSearch, globalSearch, homeSearch].forEach((input) => {
    if (input && input.value !== value) input.value = value;
  });
  sourceSearch.dispatchEvent(new Event("input", { bubbles: true }));
  syncResultCount();
}

function setSectionCollapsed(section, collapsed) {
  section.classList.toggle("section-collapsed", collapsed);
  const banner = section.querySelector(":scope > .model-category-banner, :scope > .year-banner");
  banner?.setAttribute("aria-expanded", String(!collapsed));
}

function prepareHierarchies() {
  modelCategories.forEach((section, index) => {
    const banner = section.querySelector(":scope > .model-category-banner");
    banner?.setAttribute("role", "button");
    banner?.setAttribute("tabindex", "0");
    banner?.addEventListener("click", () => setSectionCollapsed(section, !section.classList.contains("section-collapsed")));
    banner?.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        banner.click();
      }
    });
    setSectionCollapsed(section, index !== 0);
  });

  yearSections.forEach((section, index) => {
    const banner = section.querySelector(":scope > .year-banner");
    banner?.setAttribute("role", "button");
    banner?.setAttribute("tabindex", "0");
    banner?.addEventListener("click", (event) => {
      if (event.target.closest("a")) return;
      setSectionCollapsed(section, !section.classList.contains("section-collapsed"));
    });
    banner?.addEventListener("keydown", (event) => {
      if ((event.key === "Enter" || event.key === " ") && event.target === banner) {
        event.preventDefault();
        banner.click();
      }
    });
    setSectionCollapsed(section, index !== 0);
  });
}

function configureViewHierarchy(view) {
  if (view === "search") {
    modelCategories.forEach((section) => setSectionCollapsed(section, false));
    yearSections.forEach((section) => setSectionCollapsed(section, false));
  } else if (view === "models" && !location.hash.startsWith("#model-")) {
    modelCategories.forEach((section, index) => setSectionCollapsed(section, index !== 0));
  } else if (view === "archive" && !/^#(?:p-|q-|year-)/.test(location.hash)) {
    yearSections.forEach((section, index) => setSectionCollapsed(section, index !== 0));
  }
}

function setKnowledgeView(view, options = {}) {
  const nextView = viewMeta[view] ? view : "home";
  const { historyMode = "push", scroll = true } = options;
  activeView = nextView;
  document.body.dataset.knowledgeView = nextView;
  const [title, kicker] = viewMeta[nextView];
  if (viewTitle) viewTitle.textContent = title;
  if (viewKicker) viewKicker.textContent = kicker;
  if (moduleBack) moduleBack.style.display = nextView === "home" ? "none" : "grid";
  railButtons.forEach((button) => button.classList.toggle("active", button.dataset.openView === nextView));
  if (expandAllButton) {
    expandAllButton.hidden = !["models", "archive", "search"].includes(nextView);
    expandAllButton.textContent = nextView === "archive" ? "展开全部年份" : "展开全部分类";
  }
  configureViewHierarchy(nextView);
  if (historyMode !== "none") {
    const targetHash = `#${nextView}`;
    if (historyMode === "replace") history.replaceState({ knowledgeView: nextView }, "", targetHash);
    else if (location.hash !== targetHash) history.pushState({ knowledgeView: nextView }, "", targetHash);
  }
  if (scroll) window.scrollTo({ top: 0, behavior: "smooth" });
}

function viewFromHash(hash = location.hash) {
  const key = hash.replace(/^#/, "");
  if (viewMeta[key]) return key;
  if (key.startsWith("model-")) return "models";
  if (/^(?:p-|q-|year-)/.test(key)) return "archive";
  if (key === "experience") return "experience";
  if (key === "before-use") return "guide";
  if (key === "model-map") return "router";
  return "home";
}

function openSearchResults(value) {
  runKnowledgeSearch(value);
  setKnowledgeView(value.trim() ? "search" : "home");
}

[smartSearch, globalSearch, homeSearch].forEach((input) => {
  input?.addEventListener("input", (event) => openSearchResults(event.target.value));
});
sourceSearch?.addEventListener("input", () => {
  [smartSearch, globalSearch, homeSearch].forEach((input) => {
    if (input && input.value !== sourceSearch.value) input.value = sourceSearch.value;
  });
  syncResultCount();
});

openViewButtons.forEach((button) => button.addEventListener("click", () => setKnowledgeView(button.dataset.openView)));

routeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    routeButtons.forEach((item) => item.classList.toggle("active", item === button));
    renderRoute(button.dataset.route);
  });
});

document.addEventListener("click", (event) => {
  const modelLink = event.target.closest("[data-open-model]");
  if (modelLink) {
    const model = document.querySelector(`#${CSS.escape(modelLink.dataset.openModel)} details`);
    const category = model?.closest(".model-category-section");
    if (category) setSectionCollapsed(category, false);
    setKnowledgeView("models", { historyMode: "none", scroll: false });
    if (model) model.open = true;
  }
  const anchor = event.target.closest("a[href^='#']");
  const href = anchor?.getAttribute("href") || "";
  if (href.startsWith("#p-") || href.startsWith("#q-") || href.startsWith("#year-")) {
    const target = document.querySelector(href);
    const year = target?.closest(".year-section");
    if (year) setSectionCollapsed(year, false);
    setKnowledgeView("archive", { historyMode: "none", scroll: false });
  } else if (href === "#experience") {
    setKnowledgeView("experience", { historyMode: "none", scroll: false });
  } else if (href === "#before-use") {
    setKnowledgeView("guide", { historyMode: "none", scroll: false });
  } else if (href === "#model-map") {
    setKnowledgeView("router", { historyMode: "none", scroll: false });
  }
  if (event.target.closest(".quick") || event.target.closest("#clearSearch")) setTimeout(syncResultCount, 0);
});

expandAllButton?.addEventListener("click", () => {
  const sections = activeView === "archive" ? yearSections : modelCategories;
  const shouldExpand = sections.some((section) => section.classList.contains("section-collapsed"));
  sections.forEach((section) => setSectionCollapsed(section, !shouldExpand));
  expandAllButton.textContent = shouldExpand ? "收起全部" : (activeView === "archive" ? "展开全部年份" : "展开全部分类");
});

document.addEventListener("keydown", (event) => {
  const tag = event.target.tagName?.toLowerCase();
  const editing = tag === "input" || tag === "textarea" || event.target.isContentEditable;
  if (event.key === "/" && !editing) {
    event.preventDefault();
    globalSearch?.focus();
  }
  if (event.key === "Escape" && [smartSearch, globalSearch, homeSearch].includes(document.activeElement)) {
    runKnowledgeSearch("");
    document.activeElement.blur();
    if (activeView === "search") setKnowledgeView("home");
  }
});

const progress = document.createElement("div");
progress.className = "knowledge-progress";
document.body.append(progress);
window.addEventListener("scroll", () => {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0}%`;
}, { passive: true });

prepareHierarchies();
initLearningProject();
initAiLearningLibrary();
const initialView = viewFromHash();
setKnowledgeView(initialView, { historyMode: "replace", scroll: false });
if (location.hash.startsWith("#model-")) {
  const model = document.querySelector(`${location.hash} details`);
  if (model) {
    setSectionCollapsed(model.closest(".model-category-section"), false);
    model.setAttribute("open", "");
  }
}

window.addEventListener("popstate", () => setKnowledgeView(viewFromHash(), { historyMode: "none", scroll: false }));
window.addEventListener("hashchange", () => {
  const view = viewFromHash();
  if (view !== activeView) setKnowledgeView(view, { historyMode: "none", scroll: false });
});
renderRoute("predict");
syncResultCount();
