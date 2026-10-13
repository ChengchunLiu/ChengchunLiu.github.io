# 搜索收录与个人平台清单

更新日期：2026-10-13

网站内部的三语静态页面、论文详情页、结构化数据、canonical、hreflang 与 sitemap 已由构建脚本维护。以下项目需要 Chengchun Liu 本人登录相应账号完成；不包含北京大学官网或莫课题组网站的任何改动请求。

## 1. Google Search Console

1. 添加网址前缀资源：`https://chengchunliu.github.io/`。
2. 选择 HTML 标记验证，并复制 `content="..."` 中的验证码。
3. 将验证码交给 Codex；验证码会保存到公开的 `src/google-site-verification.txt` 并重新构建。也可以临时执行：

   ```bash
   python3 scripts/build_site.py --google-site-verification YOUR_TOKEN
   ```

4. 部署后完成验证。
5. 在 **Sitemaps** 提交：`https://chengchunliu.github.io/sitemap.xml`。
6. 用网址检查工具依次请求收录三个首页和五个英文研究页；之后让 Google 通过 `hreflang` 发现两套中文页面。

## 2. Google Scholar

- 确认个人资料为公开状态。
- Homepage 填写 `https://chengchunliu.github.io/`。
- 姓名、单位、研究领域与 Portfolio 保持一致。
- 检查五篇代表论文是否均归入本人资料，合并重复记录，但不要合并不同版本或不同论文。

## 3. ORCID

- 在 Websites & social links 中加入 Portfolio、GitHub、LinkedIn。
- 将可公开的论文记录补齐 DOI，并统一使用 `0009-0002-5550-4145`。
- 在个人简介或关键词中使用与网站一致的方向：AI for chemistry、molecular spectroscopy、scientific agents、molecular geometry refinement。

## 4. GitHub

- Profile 的 Website 填写 `https://chengchunliu.github.io/`。
- 为 `ChengchunLiu.github.io` 仓库添加简洁 description 和相关 topics。
- 如创建个人 Profile README，将 Portfolio、Google Scholar、ORCID 放在靠前位置，并链接 GeoOpt-Net 与 IR-DIAZO-KETONE。

## 5. LinkedIn

- 在 Contact info 中加入 Portfolio。
- 在 Featured 区加入 Portfolio 和最重要的代表论文或代码仓库。
- 标题、博士候选人身份、预计毕业时间和研究关键词与网站保持一致。

## 6. Instagram

- 在个人简介链接中加入 Portfolio。
- 若发布科研内容，使用稳定的个人姓名、论文标题和 Portfolio 链接，避免每次使用不同的人名拼写。

## 建议复查节奏

- 上线后第 1 周：检查 Search Console 是否发现 sitemap 与研究页。
- 上线后第 2–4 周：检查页面是否被收录，以及搜索结果中的标题和描述是否正确。
- 每新增一篇代表作：更新 `src/papers.json`，重新构建、部署并在 Search Console 请求收录。
