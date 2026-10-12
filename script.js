const translations = {
  en: {
    skip: "Skip to content",
    navWork: "Work",
    navAbout: "About",
    navContact: "Contact",
    menu: "Menu",
    homeLabel: "Chengchun Liu, home",
    primaryNav: "Primary navigation",
    sections: "Sections",
    mobileSections: "Mobile sections",
    profileSummary: "Profile summary",
    portraitAlt: "Portrait of Chengchun Liu",
    researchAreas: "Research areas",
    topics: "Topics",
    spectroVisualLabel: "An original diagram of multimodal spectra, a molecular hypothesis, and constrained refinement",
    candidateMolecule: "Candidate molecular structure",
    geoFigureLabel: "A conceptual diagram of single-step molecular geometry refinement",
    geoVisualLabel: "A rough molecule transformed into a refined geometry",
    uhsrAlt: "Unsupervised hierarchical symbolic regression framework",
    chromVisualLabel: "An original multiscale diagram for AI-powered chromatography",
    irVisualLabel: "Stylized infrared spectrum",
    irSpectrumLabel: "A stylized infrared spectrum with highlighted functional-group region",
    paradigmVisualLabel: "Research paradigm moving from manual work to autonomous science",
    educationExperience: "Education and experience",
    heroLine1: "AI for chemistry.",
    heroLine2: "Built to reason.",
    heroIntro:
      "I build scientific AI systems that move between spectra, molecular structure, and chemical experiments — with physical constraints and interpretability kept in the loop.",
    exploreWork: "Explore selected work",
    profileRole: "Ph.D. researcher · Peking University",
    profileStatus: "ByteDance Seed · STEM Scientist Program",
    profileLocation: "Beijing, China · UTC+8",
    focusLabel: "Research focus",
    focus1: "Scientific agents",
    focus2: "Molecular spectra",
    focus3: "Geometric learning",
    focus4: "Autonomous chemistry",
    workLabel: "Selected work",
    workHeading: "First- and co-first-author research",
    workIntro:
      "A focused selection of work I led across molecular structure elucidation, quantum geometry, interpretable learning, and chemical automation.",
    roleCoFirstLead: "Co-first author · listed first",
    roleCoFirst: "Co-first author",
    roleFirst: "First author",
    roleFirstAccount: "First author · Account",
    roleFirstPerspective: "First author · Perspective",
    spectroDesc:
      "A hypothesis-and-refinement system that proposes molecular structures from multimodal spectra, then repairs them with formula-, exact-mass-, and unsaturation-aware molecular generation.",
    tagMultimodal: "Multimodal spectra",
    tagElucidation: "Structure elucidation",
    tagGen: "Generative models",
    viewPaper: "View paper",
    viewCode: "View code",
    spectroCaption: "Spectra → hypothesis → constrained refinement",
    hypothesis: "Hypothesis",
    refine: "Constrained refinement",
    formula: "Formula",
    mass: "Exact mass",
    dbe: "Unsaturation",
    geoDesc:
      "GeoOpt-Net uses SE(3)-equivariant, multifidelity learning to map inexpensive force-field conformers directly toward DFT-quality molecular geometries in one deterministic forward pass.",
    tagGeometry: "Molecular geometry",
    tagQuantum: "Quantum chemistry",
    geoInput: "Force-field conformer",
    geoOutput: "DFT-quality geometry",
    geoCaption: "One deterministic refinement step",
    symbolicDesc:
      "A layered symbolic-learning framework that turns complex multivariable relationships into compact, chemically interpretable equations.",
    uhsrCredit: "Figure from Lou et al., Advanced Science 2026, e21200; resized.",
    chromDesc:
      "A research perspective connecting automated experimentation, retention prediction, condition optimization, and closed-loop chromatographic separation.",
    scaleMolecule: "Molecule",
    scaleSurface: "Surface",
    scaleColumn: "Column",
    scaleLoop: "Closed loop",
    chromCaption: "From molecular interactions to closed-loop separation",
    neighborChip: "Structural neighborhood",
    irDesc:
      "A functional-group-centered learning strategy that uses local structural context to improve the accuracy, robustness, and interpretability of infrared-spectrum prediction.",
    manual: "Manual",
    manualDetail: "Expert iteration",
    automated: "Automated",
    automatedDetail: "Data + robotics",
    agentic: "Agentic",
    agenticDetail: "Closed-loop reasoning",
    paradigmDesc:
      "A forward-looking framework for moving organic chemistry from manual workflows toward the productive intersection of automation and artificial intelligence.",
    scholarCallout: "Looking for the complete publication record, including collaborative work?",
    openScholar: "Open Google Scholar",
    aboutLabel: "About",
    aboutHeading: "Chemistry, computation, and systems that can close the loop.",
    aboutP1:
      "I am a Ph.D. researcher in Materials Physics and Chemistry at Peking University, advised by Prof. Fanyang Mo. Before that, I studied chemistry at Nankai University.",
    aboutP2:
      "My research asks how AI can work with the evidence chemists actually use: spectra, three-dimensional structures, physical constraints, experimental conditions, and iterative feedback.",
    aboutP3:
      "Since 2026, I have also been part of ByteDance Seed's STEM Scientist Program as an intern with the Seed Edge team, exploring scientific agents and AI-driven research workflows.",
    present: "Present",
    expected: "expected",
    seedRole: "Seed Edge intern · STEM Scientist Program",
    pku: "Peking University",
    pkuRole: "Graduate training in Materials Physics and Chemistry · Ph.D. stage since Sep 2024",
    nankai: "Nankai University",
    nankaiRole: "B.Sc. in Chemistry",
    contactLabel: "Contact",
    contactHeading: "Let’s talk about scientific AI.",
    contactIntro:
      "I’m interested in collaborations around molecular reasoning, chemistry agents, spectroscopy, geometric learning, and research automation.",
    footerLine: "AI for chemistry · Beijing",
    backTop: "Back to top",
  },
  zh: {
    skip: "跳至主要内容",
    navWork: "代表工作",
    navAbout: "关于我",
    navContact: "联系",
    menu: "菜单",
    homeLabel: "刘丞军个人主页",
    primaryNav: "主导航",
    sections: "页面栏目",
    mobileSections: "手机端页面栏目",
    profileSummary: "个人简介",
    portraitAlt: "刘丞军肖像照",
    researchAreas: "研究方向",
    topics: "研究主题",
    spectroVisualLabel: "多模态光谱、分子结构假设与约束修正的原创示意图",
    candidateMolecule: "候选分子结构",
    geoFigureLabel: "单步分子几何精修概念示意图",
    geoVisualLabel: "从初始分子构象到精修几何的原创示意图",
    uhsrAlt: "无监督层次符号回归研究框架",
    chromVisualLabel: "人工智能驱动色谱的原创跨尺度示意图",
    irVisualLabel: "红外光谱与结构邻近机制示意图",
    irSpectrumLabel: "突出官能团区域的红外光谱示意图",
    paradigmVisualLabel: "从人工研究到自动化与科学智能体的研究范式示意图",
    educationExperience: "教育与经历",
    heroLine1: "人工智能 × 化学。",
    heroLine2: "让机器学会推理。",
    heroIntro:
      "我构建能够在光谱、分子结构与化学实验之间进行推理的科学智能系统，并把物理约束与可解释性保留在闭环之中。",
    exploreWork: "查看代表工作",
    profileRole: "博士研究生 · 北京大学",
    profileStatus: "字节跳动 Seed · STEM 科学家计划",
    profileLocation: "中国北京 · UTC+8",
    focusLabel: "研究方向",
    focus1: "科学智能体",
    focus2: "分子光谱",
    focus3: "几何学习",
    focus4: "自主化学研究",
    workLabel: "代表工作",
    workHeading: "一作与共一代表成果",
    workIntro: "聚焦我主导的分子结构解析、量子几何、可解释学习与化学自动化研究。",
    roleCoFirstLead: "共同第一作者 · 排名第 1",
    roleCoFirst: "共同第一作者",
    roleFirst: "第一作者",
    roleFirstAccount: "第一作者 · Account 综述",
    roleFirstPerspective: "第一作者 · Perspective 观点",
    spectroDesc:
      "从多模态光谱提出分子结构假设，再利用分子式、精确质量与不饱和度约束的生成模型迭代修正候选结构。",
    tagMultimodal: "多模态光谱",
    tagElucidation: "结构解析",
    tagGen: "生成模型",
    viewPaper: "查看论文",
    viewCode: "查看代码",
    spectroCaption: "光谱 → 假设生成 → 约束修正",
    hypothesis: "结构假设",
    refine: "约束修正",
    formula: "分子式",
    mass: "精确质量",
    dbe: "不饱和度",
    geoDesc:
      "GeoOpt-Net 通过 SE(3) 等变与多保真学习，在一次确定性前向推理中把低成本力场构象直接精修至接近 DFT 水平的分子几何。",
    tagGeometry: "分子几何",
    tagQuantum: "量子化学",
    geoInput: "力场初始构象",
    geoOutput: "DFT 水平几何",
    geoCaption: "单步确定性几何精修",
    symbolicDesc: "以层次化符号学习把复杂多变量关系转化为紧凑、具有化学可解释性的显式方程。",
    uhsrCredit: "图源：Lou 等，Advanced Science 2026，e21200；已缩放。",
    chromDesc: "系统连接自动化实验、保留行为预测、条件优化与闭环色谱分离，梳理智能色谱的发展路径。",
    scaleMolecule: "分子",
    scaleSurface: "界面",
    scaleColumn: "色谱柱",
    scaleLoop: "闭环系统",
    chromCaption: "从分子相互作用到闭环分离",
    neighborChip: "结构邻近机制",
    irDesc: "围绕官能团局部化学环境建模，提升红外光谱预测的准确性、稳健性与可解释性。",
    manual: "人工",
    manualDetail: "专家迭代",
    automated: "自动化",
    automatedDetail: "数据 + 机器人",
    agentic: "智能体",
    agenticDetail: "闭环推理",
    paradigmDesc: "面向未来的研究框架：推动有机化学从手工流程走向自动化与人工智能深度协同。",
    scholarCallout: "希望查看包含合作成果在内的完整论文记录？",
    openScholar: "打开 Google Scholar",
    aboutLabel: "关于我",
    aboutHeading: "连接化学、计算与能够闭环运行的科学系统。",
    aboutP1: "我在北京大学攻读材料物理与化学博士学位，导师为莫凡洋教授；本科毕业于南开大学化学学院。",
    aboutP2:
      "我的研究关注人工智能如何真正使用化学家依赖的证据：光谱、三维结构、物理约束、实验条件与迭代反馈。",
    aboutP3:
      "自 2026 年起，我在字节跳动 Seed Edge 团队参与 STEM 科学家计划实习，探索科学智能体与 AI 驱动的科研工作流。",
    present: "至今",
    expected: "预计",
    seedRole: "Seed Edge 实习生 · STEM 科学家计划",
    pku: "北京大学",
    pkuRole: "材料物理与化学 · 硕博连读（2024.09 进入博士阶段）",
    nankai: "南开大学",
    nankaiRole: "化学 · 理学学士",
    contactLabel: "联系",
    contactHeading: "一起聊聊科学智能。",
    contactIntro: "欢迎围绕分子推理、化学智能体、光谱学、几何学习与科研自动化开展交流与合作。",
    footerLine: "人工智能 × 化学 · 北京",
    backTop: "返回顶部",
  },
};

const languageButton = document.querySelector(".language-toggle");
const languageCurrent = document.querySelector(".language-current");
const languageOther = document.querySelector(".language-other");
const translatableElements = document.querySelectorAll("[data-i18n]");
const translatableAltElements = document.querySelectorAll("[data-i18n-alt]");
const translatableAriaElements = document.querySelectorAll("[data-i18n-aria-label]");

function saveLanguage(language) {
  try {
    window.localStorage.setItem("portfolio-language", language);
  } catch (_error) {
    // The language switch remains functional when storage is unavailable.
  }
}

function readSavedLanguage() {
  try {
    return window.localStorage.getItem("portfolio-language");
  } catch (_error) {
    return null;
  }
}

function applyLanguage(language) {
  const copy = translations[language];

  translatableElements.forEach((element) => {
    const key = element.dataset.i18n;
    if (copy[key]) {
      element.textContent = copy[key];
    }
  });

  translatableAltElements.forEach((element) => {
    const key = element.dataset.i18nAlt;
    if (copy[key]) element.setAttribute("alt", copy[key]);
  });

  translatableAriaElements.forEach((element) => {
    const key = element.dataset.i18nAriaLabel;
    if (copy[key]) element.setAttribute("aria-label", copy[key]);
  });

  const isChinese = language === "zh";
  document.documentElement.lang = isChinese ? "zh-CN" : "en";
  document.title = isChinese
    ? "刘丞军 — 人工智能与化学"
    : "Chengchun Liu — AI for Chemistry";
  languageCurrent.textContent = isChinese ? "中" : "EN";
  languageOther.textContent = isChinese ? "EN" : "中";
  languageButton.setAttribute("aria-pressed", String(isChinese));
  languageButton.setAttribute("aria-label", isChinese ? "Switch to English" : "切换为中文");
  saveLanguage(language);
}

languageButton.addEventListener("click", () => {
  applyLanguage(document.documentElement.lang.startsWith("zh") ? "en" : "zh");
});

const savedLanguage = readSavedLanguage();
const preferredLanguage = navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
applyLanguage(savedLanguage || preferredLanguage);

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -40px" },
);

document.documentElement.classList.add("motion-ready");

document.querySelectorAll(".reveal").forEach((element, index) => {
  element.style.transitionDelay = `${Math.min(index % 3, 2) * 80}ms`;
  revealObserver.observe(element);
});

document.querySelectorAll('a[href="#top"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}#top`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});
