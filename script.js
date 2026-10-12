const supportedLanguages = ["en", "zh-Hans", "zh-Hant"];
const languageStorageKey = "ccl-portfolio-language";

function normalizeCopy(value) {
  return value.trim().replace(/\s+/g, " ");
}

function readDefaultCopy() {
  const copy = {};

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (!(key in copy)) copy[key] = normalizeCopy(element.textContent);
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    const key = element.dataset.i18nAriaLabel;
    if (!(key in copy)) copy[key] = element.getAttribute("aria-label") || "";
  });

  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    const key = element.dataset.i18nAlt;
    if (!(key in copy)) copy[key] = element.getAttribute("alt") || "";
  });

  document.querySelectorAll("[data-i18n-content]").forEach((element) => {
    const key = element.dataset.i18nContent;
    if (!(key in copy)) copy[key] = element.getAttribute("content") || "";
  });

  return copy;
}

const defaultCopy = readDefaultCopy();

const translations = {
  en: defaultCopy,
  "zh-Hans": {
    pageTitle: "刘丞军 — 化学人工智能",
    displayName: "刘丞军",
    metaDescription: "刘丞军是北京大学博士候选人，研究方向包括化学人工智能、分子光谱、分子几何精修与科学智能体。",
    socialDescription: "聚焦人工智能与化学交叉领域的研究。",
    ogLocale: "zh_CN",
    socialImageAlt: "刘丞军的化学人工智能学术主页",
    skip: "跳至主要内容",
    sectionGuide: "分区导航",
    navIntro: "首页",
    navWork: "研究成果",
    navAbout: "关于我",
    navContact: "联系",
    primaryNav: "主导航",
    homeLabel: "刘丞军，返回首页",
    sections: "页面分区",
    languageSelector: "语言",
    menu: "菜单",
    mobileSections: "移动端分区导航",
    heroLine1: "AI 赋能化学。",
    heroLine2: "为推理而生。",
    heroIntro: "迈向贯通测量、机理与发现的科学人工智能。",
    exploreWork: "浏览代表成果",
    profileSummary: "个人简介",
    portraitAlt: "刘丞军的个人照片",
    profileRole: "博士候选人",
    pku: "北京大学",
    researchAreas: "研究领域",
    focusLabel: "研究方向",
    focus1: "科学智能体",
    focus2: "分子光谱",
    focus3: "几何学习",
    focus4: "自主化学",
    workLabel: "代表成果",
    workHeading: "代表论文",
    workIntro: "研究涵盖分子结构解析、量子几何、可解释学习与化学自动化。",
    topics: "主题",
    spectroDesc: "一个“假设—精修”系统：先依据多模态光谱提出分子结构假设，再以同时考虑分子式、精确质量与不饱和度的分子生成模型加以修正。",
    tagMultimodal: "多模态光谱",
    tagElucidation: "结构解析",
    tagGen: "生成模型",
    viewPaper: "查看论文",
    spectroVisualLabel: "多模态光谱、分子结构假设与约束精修的原创示意图",
    hypothesis: "结构假设",
    candidateMolecule: "候选分子结构",
    refine: "约束精修",
    formula: "分子式",
    mass: "精确质量",
    dbe: "不饱和度",
    spectroCaption: "光谱 → 假设 → 精修",
    geoDesc: "GeoOpt-Net 采用 SE(3) 等变多保真学习，在一次确定性前向传播中，将低成本生成的力场构象直接映射为具 DFT 级精度的分子几何结构。",
    tagGeometry: "分子几何",
    tagQuantum: "量子化学",
    viewCode: "查看代码",
    geoFigureLabel: "单步分子几何精修概念图",
    geoInput: "力场构象",
    geoOutput: "DFT 级几何结构",
    geoVisualLabel: "粗略分子构型转化为精修后的几何结构",
    geoCaption: "单步确定性精修",
    symbolicVisualLabel: "展示复杂变量如何经由分层符号学习组合为可解释方程的抽象示意图",
    symbolicSystem: "多变量系统",
    symbolicDiscovery: "分层发现",
    symbolicLaw: "可解释规律",
    symbolicQualities: "紧凑 · 显式 · 可解释",
    symbolicCaption: "多变量 → 分层发现 → 紧凑方程",
    symbolicDesc: "一种分层符号学习框架，将复杂的多变量关系转化为紧凑且具化学可解释性的方程。",
    chromVisualLabel: "人工智能赋能色谱的原创多尺度示意图",
    scaleMolecule: "分子",
    scaleSurface: "表面",
    scaleColumn: "色谱柱",
    scaleClosedLoop: "闭环",
    scaleAutomation: "人工智能 + 自动化",
    chromCaption: "从分子相互作用到闭环分离",
    chromDesc: "一篇串联自动化实验、保留行为预测、条件优化与闭环色谱分离的研究展望。",
    irVisualLabel: "风格化红外光谱",
    irSpectrumLabel: "突出显示官能团区的风格化红外光谱",
    functionalRegion: "官能团区",
    wavenumber: "波数",
    neighborChip: "结构邻域",
    irDesc: "一种以官能团为中心的学习策略，利用局部结构信息，提高红外光谱预测的准确性、稳健性与可解释性。",
    equalContribution: "这些作者对本研究贡献同等。",
    scholarCallout: "想查看包括合作成果在内的完整发表记录？",
    openScholar: "打开 Google Scholar",
    aboutLabel: "关于我",
    aboutHeading: "化学、计算，以及能够实现闭环的系统。",
    aboutP1: "我是北京大学材料物理与化学专业的博士候选人，导师为莫凡洋教授。本科就读于南开大学化学专业。",
    aboutP2: "我的研究关注人工智能如何结合化学家实际使用的各类证据：光谱、三维结构、物理约束、实验条件与迭代反馈。",
    educationExperience: "教育与经历",
    seedPeriod: "2026年8月—至今",
    seedOrg: "字节跳动 Seed",
    seedRole: "Seed Edge 实习生 · STEM 科学家项目",
    pkuPeriod: "2022年9月—至今",
    pkuRole: "材料物理与化学博士候选人 · 预计毕业：2027年6月",
    nankaiPeriod: "2018年9月—2022年6月",
    nankai: "南开大学",
    nankaiRole: "化学学士",
    contactLabel: "联系",
    contactHeading: "期待与你交流科学人工智能。",
    contactIntro: "我期待在分子推理、化学智能体、光谱学、几何学习与科研自动化等方向开展合作。",
    emailLinkLabel: "发送邮件至刘丞军：liuchengchun@stu.pku.edu.cn",
    footerLine: "化学人工智能 · 北京",
    backTop: "返回顶部",
  },
  "zh-Hant": {
    pageTitle: "劉丞軍 — 化學人工智慧",
    displayName: "劉丞軍",
    metaDescription: "劉丞軍是北京大學博士候選人，研究方向包括化學人工智慧、分子光譜、分子幾何精修與科學智能體。",
    socialDescription: "聚焦人工智慧與化學交叉領域的研究。",
    ogLocale: "zh_TW",
    socialImageAlt: "劉丞軍的化學人工智慧學術網站",
    skip: "跳至主要內容",
    sectionGuide: "分區導覽",
    navIntro: "首頁",
    navWork: "研究成果",
    navAbout: "關於我",
    navContact: "聯絡",
    primaryNav: "主要導覽",
    homeLabel: "劉丞軍，返回首頁",
    sections: "頁面分區",
    languageSelector: "語言",
    menu: "選單",
    mobileSections: "行動版分區導覽",
    heroLine1: "AI 賦能化學。",
    heroLine2: "為推理而生。",
    heroIntro: "邁向串聯量測、機理與發現的科學人工智慧。",
    exploreWork: "瀏覽代表成果",
    profileSummary: "個人簡介",
    portraitAlt: "劉丞軍的個人照片",
    profileRole: "博士候選人",
    pku: "北京大學",
    researchAreas: "研究領域",
    focusLabel: "研究方向",
    focus1: "科學智能體",
    focus2: "分子光譜",
    focus3: "幾何學習",
    focus4: "自主化學",
    workLabel: "代表成果",
    workHeading: "代表論文",
    workIntro: "研究涵蓋分子結構解析、量子幾何、可解釋學習與化學自動化。",
    topics: "主題",
    spectroDesc: "一套「假設—精修」系統：先依據多模態光譜提出分子結構假設，再以同時納入分子式、精確質量與不飽和度的分子生成模型加以修正。",
    tagMultimodal: "多模態光譜",
    tagElucidation: "結構解析",
    tagGen: "生成模型",
    viewPaper: "查看論文",
    spectroVisualLabel: "多模態光譜、分子結構假設與約束精修的原創示意圖",
    hypothesis: "結構假設",
    candidateMolecule: "候選分子結構",
    refine: "約束精修",
    formula: "分子式",
    mass: "精確質量",
    dbe: "不飽和度",
    spectroCaption: "光譜 → 假設 → 精修",
    geoDesc: "GeoOpt-Net 採用 SE(3) 等變多保真學習，在一次確定性的前向傳播中，將低成本生成的力場構象直接映射為具 DFT 級精度的分子幾何結構。",
    tagGeometry: "分子幾何",
    tagQuantum: "量子化學",
    viewCode: "查看程式碼",
    geoFigureLabel: "單步分子幾何精修概念圖",
    geoInput: "力場構象",
    geoOutput: "DFT 級幾何結構",
    geoVisualLabel: "粗略分子構型轉化為精修後的幾何結構",
    geoCaption: "單步確定性精修",
    symbolicVisualLabel: "展示複雜變數如何經由分層符號學習組合為可解釋方程式的抽象示意圖",
    symbolicSystem: "多變數系統",
    symbolicDiscovery: "分層發現",
    symbolicLaw: "可解釋規律",
    symbolicQualities: "簡潔 · 顯式 · 可解釋",
    symbolicCaption: "多變數 → 分層發現 → 簡潔方程式",
    symbolicDesc: "一種分層符號學習框架，將複雜的多變數關係轉化為簡潔且具化學可解釋性的方程式。",
    chromVisualLabel: "人工智慧驅動層析的原創多尺度示意圖",
    scaleMolecule: "分子",
    scaleSurface: "表面",
    scaleColumn: "層析管柱",
    scaleClosedLoop: "閉環",
    scaleAutomation: "人工智慧 + 自動化",
    chromCaption: "從分子相互作用到閉環分離",
    chromDesc: "一篇串聯自動化實驗、保留行為預測、條件最佳化與閉環層析分離的研究展望。",
    irVisualLabel: "風格化紅外光譜",
    irSpectrumLabel: "突顯官能基區的風格化紅外光譜",
    functionalRegion: "官能基區",
    wavenumber: "波數",
    neighborChip: "結構鄰域",
    irDesc: "一種以官能基為核心的學習策略，利用局部結構資訊，提升紅外光譜預測的準確性、穩健性與可解釋性。",
    equalContribution: "這些作者對本研究貢獻同等。",
    scholarCallout: "想查看包含合作成果在內的完整發表紀錄？",
    openScholar: "開啟 Google Scholar",
    aboutLabel: "關於我",
    aboutHeading: "化學、計算，以及能夠實現閉環的系統。",
    aboutP1: "我是北京大學材料物理與化學專業的博士候選人，指導教授為莫凡洋教授。大學期間就讀於南開大學化學專業。",
    aboutP2: "我的研究關注人工智慧如何結合化學家實際使用的各類證據：光譜、三維結構、物理約束、實驗條件與迭代回饋。",
    educationExperience: "教育與經歷",
    seedPeriod: "2026年8月—至今",
    seedOrg: "字節跳動 Seed",
    seedRole: "Seed Edge 實習生 · STEM 科學家計畫",
    pkuPeriod: "2022年9月—至今",
    pkuRole: "材料物理與化學博士候選人 · 預計畢業：2027年6月",
    nankaiPeriod: "2018年9月—2022年6月",
    nankai: "南開大學",
    nankaiRole: "化學學士",
    contactLabel: "聯絡",
    contactHeading: "期待與你交流科學人工智慧。",
    contactIntro: "我期待在分子推理、化學智能體、光譜學、幾何學習與科研自動化等方向展開合作。",
    emailLinkLabel: "寄送電子郵件給劉丞軍：liuchengchun@stu.pku.edu.cn",
    footerLine: "化學人工智慧 · 北京",
    backTop: "返回頂端",
  },
};

function normalizeLanguage(language) {
  const aliases = {
    "zh-CN": "zh-Hans",
    "zh-SG": "zh-Hans",
    zh: "zh-Hans",
    "zh-TW": "zh-Hant",
    "zh-HK": "zh-Hant",
    "zh-MO": "zh-Hant",
  };
  const normalized = aliases[language] || language;
  return supportedLanguages.includes(normalized) ? normalized : null;
}

function readStoredLanguage() {
  try {
    return normalizeLanguage(window.localStorage.getItem(languageStorageKey));
  } catch {
    return null;
  }
}

function storeLanguage(language) {
  try {
    window.localStorage.setItem(languageStorageKey, language);
  } catch {
    // The site still works when storage is unavailable.
  }
}

function languageFromUrl() {
  return normalizeLanguage(new URLSearchParams(window.location.search).get("lang"));
}

function updateLanguageUrl(language) {
  const url = new URL(window.location.href);
  if (language === "en") {
    url.searchParams.delete("lang");
  } else {
    url.searchParams.set("lang", language);
  }
  window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
}

function applyLanguage(language, { persist = false, updateUrl = false } = {}) {
  const selectedLanguage = normalizeLanguage(language) || "en";
  const copy = { ...defaultCopy, ...translations[selectedLanguage] };

  document.documentElement.lang = selectedLanguage;
  document.documentElement.dataset.language = selectedLanguage;

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const translation = copy[element.dataset.i18n];
    if (translation !== undefined) element.textContent = translation;
  });

  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    const translation = copy[element.dataset.i18nAriaLabel];
    if (translation !== undefined) element.setAttribute("aria-label", translation);
  });

  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    const translation = copy[element.dataset.i18nAlt];
    if (translation !== undefined) element.setAttribute("alt", translation);
  });

  document.querySelectorAll("[data-i18n-content]").forEach((element) => {
    const translation = copy[element.dataset.i18nContent];
    if (translation !== undefined) element.setAttribute("content", translation);
  });

  document.querySelectorAll("button[data-language]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.language === selectedLanguage));
  });

  if (persist) storeLanguage(selectedLanguage);
  if (updateUrl) updateLanguageUrl(selectedLanguage);
}

const initialLanguage = languageFromUrl() || readStoredLanguage() || "en";
applyLanguage(initialLanguage);

document.querySelectorAll("button[data-language]").forEach((button) => {
  button.addEventListener("click", () => {
    applyLanguage(button.dataset.language, { persist: true, updateUrl: true });
  });
});

window.addEventListener("popstate", () => {
  applyLanguage(languageFromUrl() || readStoredLanguage() || "en");
});

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

const sideGuideLinks = Array.from(document.querySelectorAll(".side-guide [data-guide-target]"));
const sideGuideSections = sideGuideLinks
  .map((link) => ({ link, section: document.getElementById(link.dataset.guideTarget) }))
  .filter(({ section }) => section);

function updateSideGuide() {
  if (!sideGuideSections.length) return;

  const probe = window.scrollY + window.innerHeight * 0.34;
  let activeId = sideGuideSections[0].section.id;

  sideGuideSections.forEach(({ section }) => {
    if (section.offsetTop <= probe) activeId = section.id;
  });

  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 8) {
    activeId = sideGuideSections[sideGuideSections.length - 1].section.id;
  }

  sideGuideSections.forEach(({ link, section }) => {
    const isActive = section.id === activeId;
    link.classList.toggle("is-active", isActive);
    if (isActive) {
      link.setAttribute("aria-current", "location");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

let sideGuideFrame = null;

function requestSideGuideUpdate() {
  if (sideGuideFrame !== null) return;
  sideGuideFrame = window.requestAnimationFrame(() => {
    updateSideGuide();
    sideGuideFrame = null;
  });
}

window.addEventListener("scroll", requestSideGuideUpdate, { passive: true });
window.addEventListener("resize", requestSideGuideUpdate);
updateSideGuide();

document.querySelectorAll('a[href="#top"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}#top`);
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});

document.querySelectorAll(".mobile-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    link.closest("details")?.removeAttribute("open");
  });
});
