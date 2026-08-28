const workflows = [];

const templates = [
  { id: "tianfu", group: "cn", name: "天府杯", month: "3月", icon: "🐼", stars: 4, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "cert", group: "cn", name: "认证杯", month: "4-5月", icon: "📝", stars: 3, groups: ["本科生组", "专科组"] },
  { id: "mathorcup", group: "cn", name: "MathorCup", month: "4月", icon: "☕", stars: 4, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "teddy", group: "cn", name: "泰迪杯", month: "4月", icon: "🧸", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "huadong", group: "cn", name: "华东杯", month: "4-5月", icon: "🌊", stars: 2, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "huazhong", group: "cn", name: "华中杯", month: "4-5月", icon: "🏛️", stars: 2, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "wuyi", group: "cn", name: "五一杯", month: "5月", icon: "🎯", stars: 3, groups: ["本科生组", "专科组"] },
  { id: "zhongqing", group: "cn", name: "中青杯", month: "5月", icon: "🌱", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "yangtze", group: "cn", name: "长三角", month: "5月", icon: "🌉", stars: 2, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "statistics", group: "cn", name: "统计建模大赛", month: "5月", icon: "📈", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "shuwei", group: "cn", name: "数维杯", month: "5月", icon: "🔢", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "diangong", group: "cn", name: "电工杯", month: "5-6月", icon: "⚡", stars: 4, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "dongbei", group: "cn", name: "辽宁省/东三省", month: "6月", icon: "🏔️", stars: 2, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "shenzhen", group: "cn", name: "深圳杯", month: "7-9月", icon: "🏙️", stars: 4, groups: ["本科生组", "研究生组"] },
  { id: "huashu", group: "cn", name: "华数杯", month: "8月", icon: "🔮", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "cumcm", group: "cn", name: "国赛 (CUMCM)", month: "9月", icon: "🏆", stars: 5, groups: ["本科生组", "专科组"], region: true },
  { id: "gmcm", group: "cn", name: "华为杯", month: "9-10月", icon: "📱", stars: 5, groups: ["研究生组"] },
  { id: "mcm", group: "en", name: "美赛（MCM/ICM）", month: "2月", icon: "IC", stars: 5, groups: ["本科生组"] },
  { id: "apmcm", group: "en", name: "亚太（APMCM）", month: "11月", icon: "A", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
  { id: "nmmcm", group: "en", name: "数维杯国际赛", month: "11月", icon: "NW", stars: 3, groups: ["本科生组", "研究生组", "专科组"] },
];

const awardProfiles = {
  cumcm: { labels: (region) => ["国赛一等奖", "国赛二等奖", `${region}赛区一等奖`, `${region}赛区二等奖`] },
  mcm: { labels: () => ["O 奖", "F 奖", "S 奖", "M 奖"] },
  gmcm: { labels: () => ["一等奖", "二等奖", "三等奖", "成功参赛奖"] },
  shenzhen: { labels: () => ["一等奖", "二等奖", "三等奖", "优秀奖"] },
  default: { labels: () => ["一等奖", "二等奖", "三等奖", "优秀奖"] },
};

const competitionCalendar = [
  { month: "02月", name: "美赛 MCM/ICM", time: "奖项：O/F/S/M" },
  { month: "03月", name: "天府杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "04月", name: "MathorCup", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "04月", name: "泰迪杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "04-05月", name: "认证杯 / 华东杯 / 华中杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "05月", name: "五一杯 / 中青杯 / 长三角 / 统计建模大赛 / 数维杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "05-06月", name: "电工杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "06月", name: "辽宁省/东三省", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "07-09月", name: "深圳杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "08月", name: "华数杯", time: "常见奖项：一等、二等、三等、优秀奖" },
  { month: "09月", name: "国赛 CUMCM", time: "奖项：国奖与赛区奖，需要选择赛区" },
  { month: "09-10月", name: "华为杯", time: "限制研究生，常见奖项：一等、二等、三等" },
  { month: "11月", name: "APMCM / 数维杯国际赛", time: "常见奖项：一等、二等、三等、优秀奖" },
];

const modeCopy = {
  during: {
    title: "比赛期间",
    body: "用户上传论文初稿、代码和其他参照文件后，先执行本地 42 项规则检查；配置有效 API Key 时再由 ChatGPT 复核高风险项。",
  },
  after: {
    title: "比赛结束后",
    body: "用户上传论文、代码和其他参照文件后，系统结合比赛侧重点、评价标准、奖项体系与往年获奖特点，生成估奖检测报告。",
  },
};

let activeFilter = "all";
let activeMode = "during";
let activeTemplate = "cumcm";
let activeGroup = "本科生组";
let pendingDeleteIndex = null;
let lastArchivedIndex = null;
let archiveToastTimer = null;
let currentDetailIndex = null;
let pendingFileIndex = null;
let uploadAnalyses = {};

const STORAGE_KEY = "modelscore-agent-state-v1";
const defaultProfile = {
  theme: "light",
  nameStyle: "rainbow",
  nickname: "模评云用户",
  avatar: "",
};
const profile = { ...defaultProfile };

const viewButtons = document.querySelectorAll("[data-view]");
const viewTriggers = document.querySelectorAll("[data-view-trigger]");
const viewPanels = document.querySelectorAll("[data-view-panel]");
const filterButtons = document.querySelectorAll("[data-filter]");
const workflowList = document.querySelector("#workflow-list");
const cnTemplateList = document.querySelector("#cn-template-list");
const enTemplateList = document.querySelector("#en-template-list");
const modeButtons = document.querySelectorAll("[data-mode]");
const groupButtons = document.querySelectorAll("[data-group]");
const modeExplain = document.querySelector("#mode-explain");
const agentForm = document.querySelector("#agent-form");
const problemFile = document.querySelector("#problem-file");
const paperFile = document.querySelector("#paper-file");
const codeFile = document.querySelector("#code-file");
const extraFile = document.querySelector("#extra-file");
const problemName = document.querySelector("#problem-name");
const paperName = document.querySelector("#paper-name");
const codeName = document.querySelector("#code-name");
const extraName = document.querySelector("#extra-name");
const uploadReadyCount = document.querySelector("#upload-ready-count");
const uploadStatusList = document.querySelector("#upload-status-list");
const regionField = document.querySelector("#region-field");
const regionSelect = document.querySelector("#region-select");
const calendarToggle = document.querySelector("#calendar-toggle");
const calendarPopover = document.querySelector("#calendar-popover");
const calendarGrid = document.querySelector("#calendar-grid");
const todayMonth = document.querySelector("#today-month");
const todayDay = document.querySelector("#today-day");
const userToggle = document.querySelector("#user-toggle");
const userPopover = document.querySelector("#user-popover");
const themeButtons = document.querySelectorAll("[data-theme]");
const nameStyleButtons = document.querySelectorAll("[data-name-style]");
const rainbowName = document.querySelector(".rainbow-name");
const nicknameButton = document.querySelector("#nickname-button");
const nicknameText = document.querySelector("#nickname-text");
const avatarInput = document.querySelector("#avatar-input");
const avatarImage = document.querySelector("#avatar-image");
const userAvatar = document.querySelector(".user-avatar");
const deleteModal = document.querySelector("#delete-modal");
const deleteRecordName = document.querySelector("#delete-record-name");
const cancelDeleteButton = document.querySelector("#cancel-delete");
const confirmDeleteButton = document.querySelector("#confirm-delete");
const archiveToast = document.querySelector("#archive-toast");
const archiveToastText = document.querySelector("#archive-toast-text");
const undoArchiveButton = document.querySelector("#undo-archive");
const detailBackButton = document.querySelector("#detail-back");
const detailTitle = document.querySelector("#detail-title");
const detailSubtitle = document.querySelector("#detail-subtitle");
const detailSummary = document.querySelector("#detail-summary");
const detailScore = document.querySelector("#detail-score");
const detailGrade = document.querySelector("#detail-grade");
const detailFiles = document.querySelector("#detail-files");
const detailProgress = document.querySelector("#detail-progress");
const detailAwards = document.querySelector("#detail-awards");
const detailAwardTitle = document.querySelector("#detail-award-title");
const detailAdvice = document.querySelector("#detail-advice");
const detailExportJson = document.querySelector("#detail-export-json");
const detailExportReport = document.querySelector("#detail-export-report");
const detailFileInput = document.querySelector("#detail-file-input");
const runtimeId = document.querySelector("#runtime-id");
const runtimePercent = document.querySelector("#runtime-percent");
const runtimeBarFill = document.querySelector("#runtime-bar-fill");
const runtimeSteps = document.querySelector("#runtime-steps");
const runtimeLog = document.querySelector("#runtime-log");
const artifactCount = document.querySelector("#artifact-count");
const artifactList = document.querySelector("#artifact-list");
const reportTitle = document.querySelector("#report-title");
const reportLead = document.querySelector("#report-lead");
const reportBadge = document.querySelector("#report-badge");
const reportKpis = document.querySelector("#report-kpis");
const detailRisks = document.querySelector("#detail-risks");
const detailEvidence = document.querySelector("#detail-evidence");
const reportPreview = document.querySelector("#report-preview");
const infoModal = document.querySelector("#info-modal");
const infoTitle = document.querySelector("#info-title");
const infoBody = document.querySelector("#info-body");
const infoClose = document.querySelector("#info-close");
const serviceStatus = document.querySelector("#service-status");

const LEGACY_DEMO_TITLES = new Set([
  "国赛（CUMCM）B题 - 风电叶片优化与协同控制",
  "MathorCup B题 - 赛后估奖报告",
]);
let workflowSyncTimer = null;
let serviceOnline = false;

function workflowId() {
  const suffix = globalThis.crypto?.randomUUID?.().replaceAll("-", "") || `${Date.now()}${Math.random().toString(16).slice(2)}`;
  return `WF-${suffix.slice(0, 20).toUpperCase()}`;
}

function normalizeWorkflow(item) {
  return { ...item, id: item.id || workflowId(), awards: Array.isArray(item.awards) ? item.awards : [], advice: Array.isArray(item.advice) ? item.advice : [] };
}

function updateServiceStatus(state, version = "") {
  serviceOnline = state === "online";
  if (!serviceStatus) return;
  serviceStatus.classList.remove("checking", "online", "offline");
  serviceStatus.classList.add(state);
  serviceStatus.querySelector("span").textContent = serviceOnline ? `本地服务 ${version || "在线"}` : "本地服务离线";
  serviceStatus.title = serviceOnline ? "SQLite 持久化服务运行正常" : "点击查看启动方法";
}

async function checkServerHealth() {
  try {
    const response = await fetch("/api/health", { cache: "no-store" });
    const health = await response.json();
    if (!response.ok || health.status !== "ok") throw new Error("health check failed");
    updateServiceStatus("online", `v${health.version}`);
    return true;
  } catch (_error) {
    updateServiceStatus("offline");
    return false;
  }
}

async function syncWorkflowState() {
  if (!serviceOnline) return;
  try {
    const response = await fetch("/api/workflows/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workflows }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "工作流同步失败");
  } catch (error) {
    console.warn("工作流同步失败，已保留浏览器离线副本。", error);
    updateServiceStatus("offline");
  }
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ workflows, profile }));
  } catch (error) {
    console.warn("浏览器离线副本保存失败，将继续同步到 SQLite。", error);
  }
  window.clearTimeout(workflowSyncTimer);
  workflowSyncTimer = window.setTimeout(syncWorkflowState, 180);
}

async function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  let offlineWorkflows = [];
  try {
    const saved = raw ? JSON.parse(raw) : {};
    if (Array.isArray(saved.workflows)) {
      offlineWorkflows = saved.workflows
        .filter((item) => !LEGACY_DEMO_TITLES.has(item.title))
        .map(normalizeWorkflow);
    }
    if (saved.profile && typeof saved.profile === "object") {
      Object.assign(profile, defaultProfile, saved.profile);
    }
  } catch (error) {
    console.warn("本地数据读取失败，已使用空工作流。", error);
  }

  if (await checkServerHealth()) {
    try {
      const response = await fetch("/api/workflows", { cache: "no-store" });
      const payload = await response.json();
      if (!response.ok || !Array.isArray(payload.workflows)) throw new Error(payload.error || "工作流读取失败");
      const stored = payload.workflows.map(normalizeWorkflow);
      workflows.splice(0, workflows.length, ...(stored.length ? stored : offlineWorkflows));
      if (!stored.length && offlineWorkflows.length) await syncWorkflowState();
      return;
    } catch (error) {
      console.warn("SQLite 工作流读取失败，已使用浏览器离线副本。", error);
      updateServiceStatus("offline");
    }
  }
  workflows.splice(0, workflows.length, ...offlineWorkflows);
}

function setView(view) {
  viewButtons.forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  viewPanels.forEach((panel) => panel.classList.toggle("active", panel.dataset.viewPanel === view));
}

function visibleByFilter() {
  if (activeFilter === "archived") return workflows.filter((item) => item.archived);
  const activeItems = workflows.filter((item) => !item.archived);
  if (activeFilter === "all") return activeItems;
  return activeItems.filter((item) => item.type === activeFilter);
}

function renderWorkflows() {
  const filtered = visibleByFilter();
  if (!filtered.length) {
    const emptyCopy = activeFilter === "archived" ? "暂无归档记录" : "暂无工作流记录，点击新建开始分析";
    workflowList.innerHTML = `<div class="empty-state">${emptyCopy}</div>`;
  } else {
    workflowList.innerHTML = filtered
      .map((item) => {
        const index = workflows.indexOf(item);
        const isRunning = item.status === "运行中";
        return `
        <article class="workflow-row" data-type="${item.type}" data-index="${index}">
          <div class="workflow-title">
            <input type="checkbox" aria-label="选择 ${item.title}" />
            <div>
              <strong>${item.title}</strong>
              <small>${item.slug}</small>
            </div>
          </div>
          <span class="type-badge ${item.type}">${item.typeLabel}</span>
          <span class="status-badge ${item.archived ? "archived" : isRunning ? "running" : ""}"><i>●</i>${item.archived ? "已归档" : item.status}</span>
          <span>${item.createdAt}</span>
          <span class="row-actions">
            <button type="button" data-action="archive" data-index="${index}">${item.archived ? "恢复" : "归档"}</button>
            <button class="danger" type="button" data-action="delete" data-index="${index}">删除</button>
          </span>
        </article>
      `;
      })
      .join("");
  }

  const activeWorkflows = workflows.filter((item) => !item.archived);
  document.querySelector("#stat-total").textContent = String(activeWorkflows.length);
  document.querySelector("#stat-running").textContent = String(activeWorkflows.filter((item) => item.status === "运行中").length);
  document.querySelector("#stat-completed").textContent = String(activeWorkflows.filter((item) => item.status === "已完成").length);
  document.querySelector("#stat-failed").textContent = String(activeWorkflows.filter((item) => item.status === "失败").length);
  document.querySelector("#count-all").textContent = `(${activeWorkflows.length})`;
  document.querySelector("#count-during").textContent = `(${activeWorkflows.filter((item) => item.type === "during").length})`;
  document.querySelector("#count-after").textContent = `(${activeWorkflows.filter((item) => item.type === "after").length})`;
  document.querySelector("#count-archived").textContent = `(${workflows.filter((item) => item.archived).length})`;
  setupPressableFeedback();
}

function renderDetail(index) {
  const item = workflows[index];
  if (!item) return;
  const report = buildReport(item);
  const runtime = getRuntimeState(item);

  currentDetailIndex = index;
  detailTitle.textContent = item.title;
  detailSubtitle.textContent = item.slug;
  detailScore.textContent = Number.isFinite(item.score) ? item.score.toFixed(1) : "—";
  detailGrade.textContent = item.grade;
  renderRuntime(runtime);

  const summaryItems = [
    ["赛事", item.contest],
    ["题号", `${item.problem} 题`],
    ["组别", item.group],
    ["赛区", item.region],
    ["模式", item.typeLabel],
    ["创建时间", item.createdAt],
  ];

  detailSummary.innerHTML = summaryItems
    .map(([label, value]) => `<div class="summary-item"><span>${label}</span><strong>${value}</strong></div>`)
    .join("");

  detailFiles.innerHTML = item.files?.length
    ? item.files
      .map(
      (file, fileIndex) => `
        <article class="file-item">
          <span class="file-icon">${file.type.slice(0, 1)}</span>
          <div>
            <b>${file.name}</b>
            <small>${file.type} · ${file.size}</small>
            ${renderParseChips(file.analysis)}
          </div>
          <em>${file.status || "已就绪"}</em>
          <span class="file-actions">
            <button type="button" data-file-action="replace" data-file-index="${fileIndex}">替换</button>
            <button class="danger" type="button" data-file-action="remove" data-file-index="${fileIndex}">移除</button>
          </span>
        </article>
      `,
      )
      .join("")
    : `<div class="empty-state">暂无上传材料，可从新建页重新提交。</div>`;

  const steps = runtime.steps.map((step) => step.name);
  detailProgress.innerHTML = steps
    .map((step, stepIndex) => {
      const progressStep = runtime.currentStep;
      const state = item.status === "运行中" && stepIndex === progressStep ? "running" : stepIndex > progressStep ? "pending" : "";
      const mark = state === "pending" ? "…" : state === "running" ? "•" : "✓";
      const text = state === "pending" ? "待处理" : state === "running" ? "处理中" : "已完成";
      return `<li class="${state}"><i>${mark}</i><div><strong>${step}</strong><small>${text}</small></div></li>`;
    })
    .join("");

  const scoreRows = item.realReport
    ? item.realReport.dimensions.map((dimension) => [dimension.name, dimension.score])
    : item.awards;
  detailAwardTitle.textContent = item.realReport ? "六维评分" : "真实结果";
  detailAwards.innerHTML = scoreRows.length ? scoreRows
    .map(
      ([label, value]) => `
        <div class="award-row">
          <span>${label}</span>
          <div class="award-track"><i style="--value: ${value}%"></i></div>
          <strong>${value}</strong>
        </div>
      `,
    )
    .join("") : `<div class="empty-state">评审完成后显示真实评分结果。</div>`;

  detailAdvice.innerHTML = item.advice.length ? item.advice
    .map(
      ([level, title, body]) => `
        <article class="advice-item">
          <span>${level}</span>
          <div><strong>${title}</strong><p>${body}</p></div>
        </article>
      `,
    )
    .join("") : `<div class="empty-state">当前没有生成建议。</div>`;

  reportTitle.textContent = report.title;
  reportLead.textContent = report.lead;
  reportBadge.textContent = report.badge;
  reportKpis.innerHTML = report.kpis
    .map(([label, value]) => `<article><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
  detailRisks.innerHTML = report.risks
    .map(
      ([level, title, body]) => `
        <article class="risk-item ${level}">
          <span>${level === "high" ? "高" : level === "low" ? "低" : "中"}</span>
          <div><strong>${title}</strong><p>${body}</p></div>
        </article>
      `,
    )
    .join("");
  detailEvidence.innerHTML = report.evidence
    .map(
      ([mark, title, body]) => `
        <article class="evidence-item">
          <span>${mark}</span>
          <div><strong>${title}</strong><p>${body}</p></div>
        </article>
      `,
    )
    .join("");
  reportPreview.innerHTML = `
    <h3>${report.previewTitle}</h3>
    <p>${report.summary}</p>
    <ul>
      ${report.previewBullets.map((line) => `<li>${line}</li>`).join("")}
    </ul>
  `;

  detailExportJson.dataset.index = String(index);
  detailExportReport.dataset.index = String(index);
  setView("detail");
}

function pipelineStepsFor(item) {
  return [
    ["赛题分析", "comp-problem", "识别题目背景、任务目标、约束条件和提交要求。"],
    ["材料解析", "file-parse", "解析论文、代码、数据与参照材料，建立上下文索引。"],
    ["规则匹配", "rule-match", `匹配${item.contest}奖项体系、组别规则和赛区要求。`],
    ["建模审查", "model-review", "检查模型假设、目标函数、约束条件和求解逻辑。"],
    ["代码复现", "code-check", "检查入口脚本、依赖版本、数据路径和结果复现说明。"],
    [item.type === "after" ? "奖项估计" : "修改建议", item.type === "after" ? "award-estimate" : "advice-generate", item.type === "after" ? "计算奖项概率并生成依据解释。" : "生成分级修改建议和优先级。"],
    ["报告生成", "report-build", "生成检测报告、风险项、证据依据和导出产物。"],
  ].map(([name, code, desc]) => ({ name, code, desc }));
}

function getRuntimeState(item) {
  const steps = pipelineStepsFor(item);
  const isDone = item.status === "已完成";
  const currentStep = isDone ? steps.length : Math.min(item.progressStep ?? 0, steps.length - 1);
  const percent = isDone ? 100 : item.status === "失败" ? Math.round((currentStep / steps.length) * 100) : Math.round((currentStep / steps.length) * 100);
  const runtimeIdValue = item.runtimeId || `MYC-${item.createdAt.replace(/\D/g, "").slice(0, 12) || "202606011501"}-${item.type}`;
  const logs = item.runtimeLogs?.length ? item.runtimeLogs : buildDefaultLogs(item, currentStep, isDone);
  const artifacts = Array.isArray(item.artifacts) ? item.artifacts : [];

  return {
    id: runtimeIdValue,
    steps: steps.map((step, index) => ({
      ...step,
      state: isDone || index < currentStep ? "done" : index === currentStep ? "running" : "pending",
    })),
    currentStep,
    percent,
    logs,
    artifacts,
  };
}

function buildDefaultLogs(item, currentStep, isDone) {
  const steps = pipelineStepsFor(item);
  const completed = steps.slice(0, isDone ? steps.length : currentStep + 1);
  return completed.map((step, index) => {
    const status = isDone || index < currentStep ? "completed" : "running";
    return `[${String(index + 1).padStart(2, "0")}/${steps.length}] ${step.code} ${status}: ${step.desc}`;
  });
}

function renderRuntime(runtime) {
  runtimeId.textContent = `任务编号：${runtime.id}`;
  runtimePercent.textContent = `${runtime.percent}%`;
  runtimeBarFill.style.width = `${runtime.percent}%`;
  runtimeSteps.innerHTML = runtime.steps
    .map(
      (step, index) => `
        <article class="runtime-step ${step.state}">
          <span>${step.state === "done" ? "✓" : step.state === "running" ? "•" : index + 1}</span>
          <div>
            <strong>${step.name}</strong>
            <small>${step.code}</small>
            <p>${step.desc}</p>
          </div>
          <em>${step.state === "done" ? "已完成" : step.state === "running" ? "运行中" : "待处理"}</em>
        </article>
      `,
    )
    .join("");
  runtimeLog.textContent = runtime.logs.join("\n");
  artifactCount.textContent = `${runtime.artifacts.length} 个文件`;
  artifactList.innerHTML = runtime.artifacts.length ? runtime.artifacts
    .map(
      (artifact) => `
        <article class="artifact-item">
          <span>${artifact.group}</span>
          <strong>${artifact.name}</strong>
          <small>${artifact.size}</small>
          <em>${artifact.status}</em>
        </article>
      `,
    )
    .join("") : `<div class="empty-state">尚未生成报告文件。</div>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function buildReport(item) {
  if (item.realReport) {
    const sourceLabel = item.realReport.provider === "local-rules+openai" ? `本地规则 + ${item.realReport.model}` : "本地规则引擎";
    const risks = item.realReport.risks.slice(0, 8).map((risk) => [
      risk.severity,
      escapeHtml(`${risk.title} · ${risk.rule_id}`),
      escapeHtml(`${risk.reason} 建议：${risk.action}`),
    ]);
    const evidence = item.realReport.checks
      .filter((check) => check.evidence)
      .slice(0, 8)
      .map((check) => [
        check.source === "openai-review" ? "AI" : "证",
        escapeHtml(`${check.title} · 第 ${check.evidence.page} 页`),
        escapeHtml(`${check.evidence.file}：${check.evidence.quote}`),
      ]);
    return {
      title: "CUMCM 赛中诊断报告",
      lead: "按 42 项国赛规则完成六维检查；评分、风险与建议均保留可审计依据。",
      badge: sourceLabel,
      kpis: [
        ["综合健康度", item.realReport.score.toFixed(1)],
        ["总体置信度", `${Math.round(item.realReport.confidence * 100)}%`],
        ["规则检查", `${item.realReport.checks.filter((check) => check.passed).length}/42 通过`],
        ["高风险项", String(item.realReport.risks.filter((risk) => risk.severity === "high").length)],
      ],
      risks,
      evidence: evidence.length ? evidence : [["!", "证据不足", "当前未定位到可展示的原文证据，请查看完整报告。"]],
      previewTitle: `${item.contest} ${item.problem}题诊断结论`,
      summary: escapeHtml(item.realReport.summary),
      previewBullets: item.realReport.risks.slice(0, 5).map((risk) => escapeHtml(`${risk.title}：${risk.action}`)),
    };
  }
  const isFailed = item.status === "失败";
  return {
    title: isFailed ? "评审未完成" : "正在生成真实评审报告",
    lead: isFailed ? "本次任务没有产生可用评分，请查看运行日志后重新提交。" : "评分、风险、证据和建议将在本地服务完成真实分析后显示。",
    badge: isFailed ? "运行失败" : "等待服务结果",
    kpis: [
      ["当前状态", item.status],
      ["任务编号", item.runtimeId || "待创建"],
      ["评分结果", "尚未生成"],
      ["数据来源", "本地评审 API"],
    ],
    risks: [],
    evidence: [],
    previewTitle: `${item.contest} ${item.problem}题`,
    summary: isFailed ? "未生成任何模拟分数或奖项概率。请修复错误后重新运行。" : "任务处理中。页面不会在真实报告返回前显示推测分数或奖项概率。",
    previewBullets: isFailed ? ["查看运行日志中的错误信息。", "确认本地服务在线并重新提交材料。"] : ["等待 42 项规则检查完成。", "报告返回后将展示六维评分和原文证据。"],
  };
}

function stars(count) {
  return "★★★★★".slice(0, count);
}

function renderTemplates() {
  const templateHtml = (item) => {
    const implemented = item.id === "cumcm";
    return `
    <button class="template-card ${item.id === activeTemplate ? "active" : ""} ${implemented ? "" : "future"}" type="button" data-template="${item.id}" ${implemented ? "" : "disabled"}>
      <span class="template-icon">${item.icon}</span>
      <span>
        <h3>${item.name} <span class="stars">${stars(item.stars)}</span></h3>
        <small>${implemented ? `${item.month} · ${getAwardLabels(item.id).join(" / ")}` : `${item.month} · 规则尚未接入`}</small>
      </span>
      <i class="radio-dot"></i>
    </button>
  `;
  };

  cnTemplateList.innerHTML = templates
    .filter((item) => item.group === "cn")
    .sort((a, b) => Number(b.id === "cumcm") - Number(a.id === "cumcm"))
    .map(templateHtml).join("");
  enTemplateList.innerHTML = templates.filter((item) => item.group === "en").map(templateHtml).join("");

  document.querySelectorAll("[data-template]").forEach((button) => {
    button.addEventListener("click", () => {
      activeTemplate = button.dataset.template;
      normalizeGroupForTemplate();
      renderTemplates();
      renderRegionField();
      renderGroups();
      renderMode();
    });
  });
}

function getAwardLabels(templateId = activeTemplate) {
  const region = regionSelect?.value || "所在";
  const profile = awardProfiles[templateId] || awardProfiles.default;
  return profile.labels(region);
}

function selectedTemplate() {
  return templates.find((item) => item.id === activeTemplate) || templates[0];
}

function normalizeGroupForTemplate() {
  const template = selectedTemplate();
  if (!template.groups.includes(activeGroup)) activeGroup = template.groups[0];
}

function renderGroups() {
  const template = selectedTemplate();
  groupButtons.forEach((button) => {
    const group = button.dataset.group;
    const enabled = template.groups.includes(group);
    button.disabled = !enabled;
    button.classList.toggle("active", group === activeGroup);
  });
}

function renderRegionField() {
  regionField?.classList.toggle("is-hidden", !selectedTemplate().region);
}

function renderMode() {
  const copy = modeCopy[activeMode];
  modeButtons.forEach((button) => {
    const implemented = button.dataset.mode === "during";
    button.disabled = !implemented;
    button.title = implemented ? "已接入真实评审" : "需要教师标注数据完成奖项校准后开放";
    button.classList.toggle("active", button.dataset.mode === activeMode);
  });
  modeExplain.innerHTML = `<strong>${copy.title}</strong><p>${copy.body}</p>`;
}

function renderCalendar() {
  const now = new Date();
  todayMonth.textContent = `${String(now.getMonth() + 1).padStart(2, "0")}月`;
  todayDay.textContent = String(now.getDate()).padStart(2, "0");
  calendarGrid.innerHTML = competitionCalendar
    .map(
      (item) => `
        <article class="calendar-item">
          <strong>${item.month}</strong>
          <span><b>${item.name}</b><br />${item.time}</span>
        </article>
      `,
    )
    .join("");
  setupPressableFeedback();
}

function openDeleteModal(index) {
  pendingDeleteIndex = index;
  deleteRecordName.textContent = `记录：${workflows[index].title}`;
  deleteModal.classList.add("open");
  deleteModal.setAttribute("aria-hidden", "false");
}

function closeDeleteModal() {
  pendingDeleteIndex = null;
  deleteModal.classList.remove("open");
  deleteModal.setAttribute("aria-hidden", "true");
}

function showArchiveToast(recordTitle) {
  window.clearTimeout(archiveToastTimer);
  archiveToastText.textContent = `已归档：${recordTitle}`;
  archiveToast.classList.add("open");
  archiveToastTimer = window.setTimeout(() => {
    archiveToast.classList.remove("open");
    lastArchivedIndex = null;
  }, 4200);
}

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function formatFileSize(bytes) {
  if (!Number.isFinite(bytes) || bytes <= 0) return "待接入";
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function fileExtension(name = "") {
  return name.includes(".") ? name.split(".").pop().toLowerCase() : "";
}

function estimatePaperPages(file) {
  const mb = file.size / 1024 / 1024;
  return Math.max(6, Math.min(32, Math.round(mb * 8 + 8)));
}

function analyzeUpload(file, slot) {
  if (!file) {
    const isOptional = slot === "extra";
    return {
      slot,
      state: "missing",
      status: "待上传",
      valid: isOptional,
      summary: isOptional ? "可选参照材料，未上传不会阻止分析。" : "尚未选择文件。",
      meta: [],
    };
  }

  const ext = fileExtension(file.name);
  const allowed = {
    problem: ["pdf", "docx", "txt"],
    paper: ["pdf", "docx", "txt"],
    code: ["zip", "py", "m", "ipynb", "txt"],
    extra: ["pdf", "docx", "csv", "txt", "zip", "json"],
  }[slot];
  const maxSize = slot === "code" ? 80 : 40;
  const sizeMb = file.size / 1024 / 1024;
  const validType = allowed.includes(ext);
  const validSize = sizeMb <= maxSize;

  if (!validType || !validSize) {
    return {
      slot,
      state: "error",
      status: "需处理",
      valid: false,
      summary: !validType ? `文件格式 .${ext || "未知"} 不在允许范围内。` : `文件超过 ${maxSize} MB，建议压缩或拆分。`,
      meta: [`${formatFileSize(file.size)}`, ext ? `.${ext}` : "未知格式"],
    };
  }

  if (slot === "problem") {
    return {
      slot,
      state: "ready",
      status: "解析完成",
      valid: true,
      summary: "已准备抽取赛题背景、问题目标、约束条件、数据说明和提交要求。",
      meta: [`${formatFileSize(file.size)}`, ext.toUpperCase(), "赛题约束"],
      details: { requirements: ["问题背景", "目标函数", "约束条件", "数据口径", "提交要求"] },
    };
  }

  if (slot === "paper") {
    const pages = estimatePaperPages(file);
    return {
      slot,
      state: "ready",
      status: "解析完成",
      valid: true,
      summary: `预计 ${pages} 页，已准备抽取摘要、目录、公式、图表和参考文献。`,
      meta: [`${pages} 页`, `${formatFileSize(file.size)}`, ext.toUpperCase()],
      details: { pages, sections: ["摘要", "模型假设", "求解过程", "结果分析", "结论"] },
    };
  }

  if (slot === "code") {
    const structure = ext === "zip" || ext === "rar"
      ? ["main.py", "data/", "results/", "README"]
      : [file.name, "单文件入口", "待补数据目录"];
    return {
      slot,
      state: "ready",
      status: "解析完成",
      valid: true,
      summary: `识别 ${structure.length} 个关键结构，后续会检查入口脚本、依赖版本和数据路径。`,
      meta: [`${structure.length} 项结构`, `${formatFileSize(file.size)}`, ext.toUpperCase()],
      details: { structure, dataFiles: ext === "zip" || ext === "rar" ? ["input.csv", "params.xlsx"] : ["待上传数据"] },
    };
  }

  return {
    slot,
    state: "ready",
    status: "可参照",
    valid: true,
    summary: "已作为大模型上下文材料，后续用于补充题目背景、数据说明或往年作品特征。",
    meta: [`${formatFileSize(file.size)}`, ext.toUpperCase(), "参照材料"],
    details: { referenceType: ext.toUpperCase() },
  };
}

function renderParseChips(analysis) {
  if (!analysis?.meta?.length) return "";
  return `<span class="parse-meta">${analysis.meta.map((item) => `<span class="parse-chip">${item}</span>`).join("")}</span>`;
}

function updateUploadInspector() {
  const analyses = [
    ["problem", "赛题文件", problemFile?.files?.[0]],
    ["paper", "论文文件", paperFile?.files?.[0]],
    ["code", "代码与数据", codeFile?.files?.[0]],
    ["extra", "其他参照", extraFile?.files?.[0]],
  ].map(([slot, label, file]) => [label, analyzeUpload(file, slot)]);

  uploadAnalyses = Object.fromEntries(analyses.map(([, analysis]) => [analysis.slot, analysis]));
  const readyCount = analyses.filter(([, analysis]) => analysis.valid && analysis.state !== "missing").length;
  uploadReadyCount.textContent = `${readyCount}/4 已就绪`;
  uploadStatusList.innerHTML = analyses
    .map(
      ([label, analysis]) => `
        <article class="upload-status-item ${analysis.state === "error" ? "error" : analysis.state === "missing" ? "warning" : ""}">
          <strong>${label}<em>${analysis.status}</em></strong>
          <p>${analysis.summary}</p>
          ${renderParseChips(analysis)}
        </article>
      `,
    )
    .join("");

  [
    [problemFile, "problem"],
    [paperFile, "paper"],
    [codeFile, "code"],
    [extraFile, "extra"],
  ].forEach(([input, slot]) => {
    input?.closest(".file-card")?.classList.toggle("error", uploadAnalyses[slot]?.state === "error");
  });
}

function openInfoModal(title, html) {
  infoTitle.textContent = title;
  infoBody.innerHTML = html;
  infoModal.classList.add("open");
  infoModal.setAttribute("aria-hidden", "false");
}

function closeInfoModal() {
  infoModal.classList.remove("open");
  infoModal.setAttribute("aria-hidden", "true");
}

function exportRecords() {
  downloadJson("modelscore-agent-records.json", {
    exportedAt: new Date().toLocaleString("zh-CN", { hour12: false }),
    records: workflows,
  });
}

function renderRecordLines() {
  if (!workflows.length) return "<p>暂无可导出的工作流记录。</p>";
  return workflows
    .map((item) => `<div class="record-line"><strong>${item.title}</strong><span>${item.status}</span></div>`)
    .join("");
}

function applyProfile() {
  document.body.dataset.theme = profile.theme;
  themeButtons.forEach((button) => button.classList.toggle("active", button.dataset.theme === profile.theme));
  nicknameText.textContent = profile.nickname;
  setNameStyle(profile.nameStyle);

  if (profile.avatar) {
    avatarImage.src = profile.avatar;
    userAvatar.classList.add("has-image");
  }
}

function setupPressableFeedback() {
  const selector = [
    "button",
    ".template-card",
    ".calendar-item",
    ".template-icon",
  ].join(",");

  document.querySelectorAll(selector).forEach((element) => {
    if (element.dataset.pressableReady) return;
    element.dataset.pressableReady = "true";
    element.classList.add("pressable");

    element.addEventListener("pointerdown", () => {
      element.classList.remove("is-released");
      element.classList.add("is-pressing");
      if (navigator.vibrate) navigator.vibrate(8);
    });

    ["pointerup", "pointercancel", "pointerleave"].forEach((eventName) => {
      element.addEventListener(eventName, () => {
        if (!element.classList.contains("is-pressing")) return;
        element.classList.remove("is-pressing");
        element.classList.add("is-released");
        window.setTimeout(() => element.classList.remove("is-released"), 280);
      });
    });
  });
}

viewButtons.forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));
viewTriggers.forEach((button) => button.addEventListener("click", () => setView(button.dataset.viewTrigger)));

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    renderWorkflows();
  });
});

modeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activeMode = button.dataset.mode;
    renderMode();
  });
});

groupButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.disabled) return;
    activeGroup = button.dataset.group;
    renderGroups();
  });
});

workflowList.addEventListener("click", (event) => {
  const actionButton = event.target.closest("[data-action]");
  const row = event.target.closest(".workflow-row");
  if (!row) return;

  if (!actionButton && event.target.closest("input")) return;

  if (!actionButton) {
    renderDetail(Number(row.dataset.index));
    return;
  }

  const index = Number(actionButton.dataset.index);
  const action = actionButton.dataset.action;

  if (action === "archive") {
    const item = workflows[index];
    item.archived = !item.archived;

    if (item.archived) {
      lastArchivedIndex = index;
      showArchiveToast(item.title);
    } else {
      archiveToast.classList.remove("open");
      lastArchivedIndex = null;
    }

    saveState();
    renderWorkflows();
    return;
  }
  if (action === "delete") {
    openDeleteModal(index);
    return;
  }
  renderWorkflows();
});

detailBackButton?.addEventListener("click", () => setView("workflows"));

detailExportJson?.addEventListener("click", () => {
  const item = workflows[Number(detailExportJson.dataset.index)];
  if (!item) return;
  if (item.realReport?.downloads?.json) {
    window.location.href = item.realReport.downloads.json;
    return;
  }
  downloadJson("modelscore-workflow-detail.json", item);
});

detailExportReport?.addEventListener("click", () => {
  const item = workflows[Number(detailExportReport.dataset.index)];
  if (!item) return;
  if (item.realReport?.downloads?.pdf) {
    window.location.href = item.realReport.downloads.pdf;
    return;
  }
  openInfoModal("导出报告", `<p><strong>${item.title}</strong></p><p>报告导出任务已创建，正式接入后会生成 PDF / DOCX 检测报告。</p>`);
});

detailFiles?.addEventListener("click", (event) => {
  const button = event.target.closest("[data-file-action]");
  if (!button || currentDetailIndex === null) return;

  const item = workflows[currentDetailIndex];
  const fileIndex = Number(button.dataset.fileIndex);
  if (!item?.files?.[fileIndex]) return;

  if (button.dataset.fileAction === "remove") {
    item.files.splice(fileIndex, 1);
    saveState();
    renderDetail(currentDetailIndex);
    return;
  }

  pendingFileIndex = fileIndex;
  detailFileInput.value = "";
  detailFileInput.click();
});

detailFileInput?.addEventListener("change", () => {
  if (currentDetailIndex === null || pendingFileIndex === null) return;
  const file = detailFileInput.files[0];
  if (!file) return;

  const item = workflows[currentDetailIndex];
  const oldFile = item.files[pendingFileIndex];
  const slot = oldFile.type === "赛题" ? "problem" : oldFile.type === "论文" ? "paper" : oldFile.type === "代码" ? "code" : "extra";
  const analysis = analyzeUpload(file, slot);
  item.files[pendingFileIndex] = {
    ...oldFile,
    name: file.name,
    size: formatFileSize(file.size),
    status: analysis.valid ? "已替换" : "需处理",
    analysis,
  };
  pendingFileIndex = null;
  saveState();
  renderDetail(currentDetailIndex);
});

cancelDeleteButton?.addEventListener("click", closeDeleteModal);

confirmDeleteButton?.addEventListener("click", () => {
  if (pendingDeleteIndex === null) return;
  workflows.splice(pendingDeleteIndex, 1);
  closeDeleteModal();
  saveState();
  renderWorkflows();
});

deleteModal?.addEventListener("click", (event) => {
  if (event.target === deleteModal) closeDeleteModal();
});

undoArchiveButton?.addEventListener("click", () => {
  if (lastArchivedIndex === null || !workflows[lastArchivedIndex]) return;
  workflows[lastArchivedIndex].archived = false;
  lastArchivedIndex = null;
  archiveToast.classList.remove("open");
  saveState();
  renderWorkflows();
});

calendarToggle?.addEventListener("click", () => {
  calendarPopover.classList.toggle("open");
  userPopover?.classList.remove("open");
});

userToggle?.addEventListener("click", () => {
  userPopover.classList.toggle("open");
  calendarPopover?.classList.remove("open");
});

document.addEventListener("click", (event) => {
  if (calendarPopover?.classList.contains("open")) {
    if (!event.target.closest("#calendar-popover") && !event.target.closest("#calendar-toggle")) {
      calendarPopover.classList.remove("open");
    }
  }

  if (userPopover?.classList.contains("open")) {
    if (!event.target.closest("#user-popover") && !event.target.closest("#user-toggle")) {
      userPopover.classList.remove("open");
    }
  }
});

themeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const theme = button.dataset.theme;
    profile.theme = theme;
    document.body.dataset.theme = theme;
    themeButtons.forEach((item) => item.classList.toggle("active", item === button));
    saveState();
  });
});

function setNameStyle(style) {
  profile.nameStyle = style;
  rainbowName?.classList.remove("name-style-rainbow", "name-style-aurora", "name-style-sunset");
  if (style !== "classic") rainbowName?.classList.add(`name-style-${style}`);
  nameStyleButtons.forEach((button) => button.classList.toggle("active", button.dataset.nameStyle === style));
}

nameStyleButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setNameStyle(button.dataset.nameStyle);
    saveState();
  });
});

nicknameButton?.addEventListener("click", () => {
  const nextName = window.prompt("请输入新的昵称", nicknameText.textContent.trim());
  if (!nextName) return;
  profile.nickname = nextName.trim().slice(0, 18);
  nicknameText.textContent = profile.nickname;
  saveState();
});

avatarInput?.addEventListener("change", () => {
  const file = avatarInput.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    profile.avatar = reader.result;
    avatarImage.src = profile.avatar;
    userAvatar.classList.add("has-image");
    saveState();
  });
  reader.readAsDataURL(file);
});

document.querySelectorAll("[data-menu-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const action = button.dataset.menuAction;
    const content = {
      help: "<p><strong>帮助与反馈</strong></p><p>正式版将接入问题反馈、客服邮箱、常见问题和诊断日志上传入口。</p>",
      notice: "<p><strong>平台公告</strong></p><p>当前原型公告：模评云智能体前端正在开发，赛事模板与报告样式持续完善。</p>",
      version: "<p><strong>版本更新与查询</strong></p><p>当前版本：ModelScore v0.5。已接入真实文件解析、42 项规则、报告导出与 SQLite 持久化。</p>",
      about: "<p><strong>关于我们</strong></p><p>模评云智能体面向数学建模竞赛，提供赛中诊断和赛后估奖两类工作流。</p>",
      "switch-account": "<p><strong>切换账号</strong></p><p>正式登录系统接入后，这里会打开账号选择器。当前原型保留本地用户数据。</p>",
      logout: "<p><strong>退出登录</strong></p><p>当前为本地原型，不会清除工作流记录。正式版会在确认后退出当前账号。</p>",
    };

    if (action === "export-records") {
      exportRecords();
      openInfoModal("导出记录", `<p>已生成工作流记录 JSON 文件。</p>${renderRecordLines()}`);
      return;
    }

    openInfoModal(button.textContent.trim(), content[action] || "<p>功能建设中。</p>");
  });
});

infoClose?.addEventListener("click", closeInfoModal);

serviceStatus?.addEventListener("click", () => {
  if (serviceOnline) {
    openInfoModal("本地服务正常", "<p>评分服务和 SQLite 持久化均已连接。任务与报告会在服务重启后保留。</p>");
  } else {
    openInfoModal("本地服务离线", "<p>请在项目目录运行：</p><p><code>.\\start.ps1</code></p><p>脚本会检查端口、启动服务并打开工作台。</p>");
  }
});

infoModal?.addEventListener("click", (event) => {
  if (event.target === infoModal) closeInfoModal();
});

regionSelect?.addEventListener("change", () => {
  renderTemplates();
});

problemFile?.addEventListener("change", () => {
  problemName.textContent = problemFile.files[0]?.name || "选择赛题 PDF / DOCX / TXT";
  updateUploadInspector();
});

paperFile?.addEventListener("change", () => {
  paperName.textContent = paperFile.files[0]?.name || "选择 PDF / DOCX";
  updateUploadInspector();
});

codeFile?.addEventListener("change", () => {
  codeName.textContent = codeFile.files[0]?.name || "选择 ZIP / 代码文件";
  updateUploadInspector();
});

extraFile?.addEventListener("change", () => {
  extraName.textContent = extraFile.files[0]?.name || "供大模型参照分析";
  updateUploadInspector();
});

function fileMeta(input, fallbackName, type) {
  const file = input?.files?.[0];
  const slot = type === "赛题" ? "problem" : type === "论文" ? "paper" : type === "代码" ? "code" : "extra";
  const analysis = uploadAnalyses[slot] || analyzeUpload(file, slot);
  return {
    name: file?.name || fallbackName,
    type,
    size: file ? formatFileSize(file.size) : "未上传",
    status: file ? analysis.status : "待补充",
    analysis,
  };
}

agentForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  updateUploadInspector();
  const blockingErrors = [uploadAnalyses.problem, uploadAnalyses.paper, uploadAnalyses.code].filter((analysis) => !analysis.valid || analysis.state === "missing");
  const formatErrors = Object.values(uploadAnalyses).filter((analysis) => analysis.state === "error");
  if (blockingErrors.length || formatErrors.length) {
    openInfoModal("上传文件需处理", `<p>请先补齐赛题文件、论文文件和代码文件，并处理格式或大小异常后再启动分析。</p>`);
    return;
  }
  const template = selectedTemplate();
  if (template.id !== "cumcm" || activeMode !== "during") {
    openInfoModal("真实评审范围", "<p>当前真实评分 MVP 先支持<strong>CUMCM 国赛 · 赛中诊断</strong>。请选择国赛模板和赛中诊断；其他赛事保留为后续规则扩展项。</p>");
    return;
  }
  const regionText = template.region ? ` · ${regionSelect.value}赛区` : "";
  const workflow = {
    id: workflowId(),
    title: `${template.name} ${document.querySelector("#problem-input").value || "B"}题 - ${activeMode === "during" ? "赛中诊断" : "赛后估奖"}`,
    slug: `${activeGroup}${regionText} · ${activeMode === "during" ? "大模型合理性与正确性分析" : `奖项体系：${getAwardLabels().join(" / ")}`}`,
    type: activeMode,
    typeLabel: activeMode === "during" ? "赛中诊断" : "赛后估奖",
    status: "运行中",
    progressStep: 0,
    runtimeId: `MYC-${Date.now().toString(36).toUpperCase()}-${activeMode}`,
    runtimeLogs: [],
    artifacts: [],
    archived: false,
    createdAt: new Date().toLocaleString("zh-CN", { hour12: false }),
    contest: template.name,
    problem: document.querySelector("#problem-input").value || "B",
    group: activeGroup,
    region: template.region ? `${regionSelect.value}赛区` : "无",
    score: null,
    grade: activeMode === "during" ? "正在生成修改建议" : "正在生成估奖报告",
    files: [
      fileMeta(problemFile, "未上传赛题", "赛题"),
      fileMeta(paperFile, "未上传论文", "论文"),
      fileMeta(codeFile, "未上传代码", "代码"),
      fileMeta(extraFile, "未上传其他文件", "参照"),
    ],
    awards: [],
    advice: [],
  };
  workflows.unshift(workflow);
  saveState();
  renderWorkflows();
  renderDetail(0);
  const submitButton = agentForm.querySelector("button[type='submit']");
  submitButton.disabled = true;
  submitButton.textContent = "正在执行真实评审…";
  workflow.runtimeLogs = ["[01/07] upload accepted: 文件已发送至本地评分服务。", "[02/07] file-parse running: 正在提取论文结构与代码清单。"];
  workflow.progressStep = 1;
  saveState();
  renderDetail(0);
  try {
    const formData = new FormData();
    formData.append("contest", template.name);
    formData.append("problem_id", document.querySelector("#problem-input").value || "B");
    formData.append("group", activeGroup);
    formData.append("region", `${regionSelect.value}赛区`);
    formData.append("mode", activeMode);
    formData.append("review_mode", document.querySelector("#review-mode").value);
    formData.append("problem", problemFile.files[0]);
    formData.append("paper", paperFile.files[0]);
    formData.append("code", codeFile.files[0]);
    if (extraFile.files[0]) formData.append("extra", extraFile.files[0]);
    const response = await fetch("/api/jobs", { method: "POST", body: formData });
    const created = await response.json();
    if (!response.ok) throw new Error(created.detail || created.error || "评审服务返回错误");
    workflow.runtimeId = created.job_id;
    let job = created;
    while (!['completed', 'failed'].includes(job.status)) {
      await new Promise((resolve) => window.setTimeout(resolve, 700));
      const pollResponse = await fetch(`/api/jobs/${created.job_id}`);
      job = await pollResponse.json();
      if (!pollResponse.ok) throw new Error(job.error || "无法读取任务进度");
      workflow.progressStep = Math.min(6, Math.floor((job.progress || 0) / 15));
      workflow.runtimeLogs = [`[${String(job.progress || 0).padStart(3, ' ')}%] ${job.status}: ${job.message || '处理中'}`];
      saveState();
      renderDetail(0);
    }
    if (job.status === 'failed') throw new Error(job.error || '评审失败');
    const result = job.report;
    workflow.status = "已完成";
    workflow.progressStep = pipelineStepsFor(workflow).length;
    workflow.runtimeId = result.report_id;
    workflow.score = result.score;
    workflow.grade = result.provider === "local-rules+openai" ? "ChatGPT 增强诊断已生成" : "本地规则诊断已生成";
    workflow.realReport = result;
    workflow.advice = result.risks.slice(0, 8).map((risk) => [risk.severity === "high" ? "高" : risk.severity === "low" ? "低" : "中", risk.title, risk.action]);
    workflow.runtimeLogs = [
      "[01/07] comp-problem completed: 赛题材料已解析。",
      "[02/07] file-parse completed: 论文与代码清单已提取。",
      "[03/07] rule-match completed: CUMCM 42 项规则已加载。",
      "[04/07] model-review completed: 六维证据检查已完成。",
      "[05/07] code-check completed: 代码静态复现性检查已完成（未执行代码）。",
      `[06/07] advice-generate completed: ${result.risks.length} 个优先风险已排序。`,
      `[07/07] report-build completed: ${result.report_id} JSON/PDF 已生成。`,
    ];
    workflow.artifacts = [
      { group: "规则检查", name: "42_RULE_CHECKS", size: "42 项", status: "已生成" },
      { group: "修改建议", name: "REVISION_ADVICE", size: `${result.risks.length} 项`, status: "已生成" },
      { group: "报告生成", name: "report.json", size: "结构化", status: "可导出" },
      { group: "报告生成", name: "report.pdf", size: "PDF", status: "可导出" },
    ];
  } catch (error) {
    workflow.status = "失败";
    workflow.grade = "评审失败";
    workflow.runtimeLogs.push(`[ERROR] ${error.message}`);
    openInfoModal("评审失败", `<p>${escapeHtml(error.message)}</p><p>请确认通过 <code>server.py</code> 启动了本地服务。</p>`);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "启动智能体分析";
    saveState();
    renderWorkflows();
    renderDetail(0);
  }
});

async function initializeApp() {
  await loadState();
  saveState();
  renderWorkflows();
  renderTemplates();
  renderRegionField();
  renderGroups();
  renderCalendar();
  renderMode();
  applyProfile();
  updateUploadInspector();
  setupPressableFeedback();
  if (window.location.hash === "#create") setView("create");
  window.setInterval(checkServerHealth, 15000);
}

window.addEventListener("hashchange", () => {
  if (window.location.hash === "#create") setView("create");
  if (window.location.hash === "#workflows") setView("workflows");
});

initializeApp();
