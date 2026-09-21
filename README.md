<h1 align="center">
  <img src="assets/hero.svg" alt="Kumar Abhinash: Full-Stack Developer, AI Builder, Software Engineer in Progress, Product Builder" width="100%">
</h1>

<p align="center">
  <a href="#featured-projects">Projects</a> ·
  <a href="#ai-engineering">AI &amp; Engineering</a> ·
  <a href="#tech-stack">Stack</a> ·
  <a href="#github-stats">Stats</a> ·
  <a href="#open-source">Open Source</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#contact">Contact</a>
</p>

<div align="center">

<!-- BEGIN:SOCIAL -->
[![GitHub — Profile](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abhiraj66369-commits)
<!-- END:SOCIAL -->

</div>

> **Hi, I'm Kumar Abhinash.**
> I build full-stack web apps and AI-powered tools: a bilingual agriculture assistant, a learning platform for a coaching institute, a business management platform, and an operating-systems simulator.
> I'm growing from student projects into production-minded software engineering, with a focus on the full stack, LLM applications and clean automation.

<img src="assets/divider.svg" alt="" width="100%">

## 🔭 Current Focus

<!-- BEGIN:FOCUS -->
- 🔭 Evolving AgroMind AI, a bilingual agriculture assistant built on the Gemini API
- 🔭 Full-stack product engineering with React, Node.js and PostgreSQL (Supabase)
- 🔭 Automating my own workflow with GitHub Actions
<!-- END:FOCUS -->

<img src="assets/divider.svg" alt="" width="100%">

<a id="featured-projects"></a>

## 🗂️ Featured Projects

<!-- BEGIN:PROJECTS -->
| Project | What it does | Tech | Status | Demo |
|---|---|---|---|---|
| [🌾 AgroMind AI](https://github.com/abhiraj66369-commits/agromind-ai) | Agriculture-only chatbot for farmers, in Hindi and English. Gemini-backed Express API with rate limiting, Helmet and CORS, plus a React chat UI with history and dark/light mode. | React • Tailwind CSS • Node.js • Express • Gemini API | 🚧 In progress | [Live ↗](https://agromind.vercel.app) |
| [🎓 Target Bio Classes](https://github.com/abhiraj66369-commits/TARGETBIO-CLASSES) | EdTech learning platform for a coaching institute: OTP login, student registration, course demos, paid access, teacher dashboard, video/notes/DPP uploads, payment verification and an enquiry panel. | React • Node.js | 🚧 In progress | [Live ↗](https://targetbio-classes.vercel.app) |
| [🏢 Arvika Tech](https://github.com/abhiraj66369-commits/arvika--tech) | Business management platform with CEO, client and employee dashboards: projects, payment proofs, salary records, attendance and messaging. JWT auth on a PostgreSQL (Supabase) backend. | React • Vite • Node.js • PostgreSQL • Supabase • Cloudinary | 🚧 In progress | [Live ↗](https://arvikatech.vercel.app) |
| [🧵 Multi-threaded Simulator](https://github.com/abhiraj66369-commits/multi-threaded-simulator) | Real-time simulator for multithreading models (many-to-one, one-to-one, many-to-many), CPU scheduling and semaphore/monitor synchronization, with thread-state timelines and interactive controls. | HTML | 📄 Report included | — |

More repositories: [WEB-LEARN](https://github.com/abhiraj66369-commits/WEB-LEARN) (learning platform) · [STUDENT-DETAILS](https://github.com/abhiraj66369-commits/STUDENT-DETAILS) (student details devops demo)
<!-- END:PROJECTS -->

### 📈 Repository health

Live numbers pulled from the GitHub API by the [profile-update workflow](.github/workflows/profile-update.yml). Nothing here is typed by hand.

<!-- BEGIN:HEALTH -->
| Repository | ★ Stars | Forks | Open issues + PRs | CI | Latest release | Last push | Main language |
|---|---|---|---|---|---|---|---|
| [agromind-ai](https://github.com/abhiraj66369-commits/agromind-ai) | 0 | 0 | 0 | — | — | 2026-05-10 | JavaScript |
| [TARGETBIO-CLASSES](https://github.com/abhiraj66369-commits/TARGETBIO-CLASSES) | 0 | 0 | 0 | — | — | 2026-02-03 | JavaScript |
| [arvika--tech](https://github.com/abhiraj66369-commits/arvika--tech) | 1 | 0 | 0 | — | — | 2026-08-23 | JavaScript |
| [multi-threaded-simulator](https://github.com/abhiraj66369-commits/multi-threaded-simulator) | 1 | 0 | 0 | — | — | 2025-12-21 | HTML |

<sub>Real numbers only; — means not available. Stars across these repositories: 2. Snapshot date: 2026-09-21.</sub>
<!-- END:HEALTH -->

<details>
<summary><b>🏛️ Architecture: AgroMind AI</b> (solid = built, dashed = planned)</summary>

```mermaid
flowchart TD
    F["Farmer<br/>Hindi or English"] --> UI["React + Tailwind chat UI<br/>client-side topic pre-check"]
    UI -->|REST| API["Express API<br/>rate limit, CORS, Helmet, input limits"]
    API --> LLM["Gemini API<br/>agriculture-only system prompt"]
    LLM --> OUT["Markdown answer<br/>tables, lists, copy button"]
    CTX["Location and crop context"]:::planned -.-> API
    WX["Weather data"]:::planned -.-> API
    KB["Agricultural knowledge base<br/>retrieval (RAG)"]:::planned -.-> API
    classDef planned stroke-dasharray:5 5,color:#8b949e
```

The solid path is what the repository implements today: a React client talking to an Express proxy that keeps the Gemini API key server-side. Location, weather and retrieval are on the [roadmap](#roadmap) and are not implemented yet.

</details>

<details>
<summary><b>🏛️ Architecture: Arvika Tech</b></summary>

```mermaid
flowchart LR
    U["CEO, client, employee"] --> FE["React (Vite)<br/>deployed on Vercel"]
    FE -->|REST + JWT| BE["Node.js API<br/>deployed on Render"]
    BE --> DB[("PostgreSQL<br/>Supabase")]
    BE --> IMG["Cloudinary<br/>image storage"]
```

</details>

<img src="assets/divider.svg" alt="" width="100%">

<a id="ai-engineering"></a>

## 🤖 AI &amp; Engineering Focus

| Capability | Status | Where |
|---|---|---|
| LLM API integration (Gemini) behind a server-side proxy | ✅ Built | AgroMind AI |
| System-prompt scoping and topic filtering | ✅ Built | AgroMind AI |
| Bilingual Hindi / English chat UX | ✅ Built | AgroMind AI |
| Retrieval-augmented generation, embeddings, vector search | 🗺️ Planned | AgroMind AI |

**Engineering practices I can point to in real repositories:**

<!-- BEGIN:PRACTICES -->
| Practice | Where it shows up |
|---|---|
| Server-side secrets | AgroMind AI keeps the Gemini API key on the backend and ships a .env.example |
| API hardening | AgroMind AI: rate limiting, Helmet security headers, CORS restricted to the frontend, input sanitization and length limits |
| Authentication and roles | Arvika Tech: JWT auth with CEO / client / employee dashboards |
| Database setup scripts | Arvika Tech: repeatable setup-db script for PostgreSQL tables and constraints |
| Automation | This profile repo: GitHub Actions for snake, metrics, README refresh and quality checks |
<!-- END:PRACTICES -->

## 🧰 Developer Tools

<!-- BEGIN:DEVTOOLS -->
| Tool | What it is |
|---|---|
| [multi-threaded-simulator](https://github.com/abhiraj66369-commits/multi-threaded-simulator) | Interactive teaching tool for operating-system concepts: thread models, CPU scheduling, synchronization. |
| [WEB-LEARN](https://github.com/abhiraj66369-commits/WEB-LEARN) | Learning platform experiments in plain HTML. |
<!-- END:DEVTOOLS -->

<a id="open-source"></a>

## 🌍 Open Source

<!-- BEGIN:OSS -->
**Open Source Journey.** Merged upstream contributions will be listed here, with real PR links only. Until then, my public repositories above are the work to look at.
<!-- END:OSS -->

## 🌐 Portfolio &amp; Resume

Portfolio and resume links appear in the badges at the top of this page as soon as they are added to [`data/profile.json`](data/profile.json). Until then the pinned repositories above are the best view of my work.

<img src="assets/divider.svg" alt="" width="100%">

<a id="tech-stack"></a>

## 💻 Tech Stack

Only technologies that appear in my repositories are listed.

<!-- BEGIN:STACK -->
| Area | Technologies |
|---|---|
| **Languages** | ![Languages technology icons](https://skillicons.dev/icons?i=js,html,css&theme=dark&perline=10)<br/>JavaScript · HTML · CSS |
| **Frontend** | ![Frontend technology icons](https://skillicons.dev/icons?i=react,tailwind,vite&theme=dark&perline=10)<br/>React · Tailwind CSS · Vite |
| **Backend** | ![Backend technology icons](https://skillicons.dev/icons?i=nodejs,express&theme=dark&perline=10)<br/>Node.js · Express · REST APIs · JWT auth |
| **Database** | ![Database technology icons](https://skillicons.dev/icons?i=postgres,supabase&theme=dark&perline=10)<br/>PostgreSQL · Supabase |
| **AI / LLM** | Gemini API · Prompt design (system prompts) |
| **DevOps** | ![DevOps technology icons](https://skillicons.dev/icons?i=git,githubactions&theme=dark&perline=10)<br/>Git · GitHub Actions |
| **Cloud / Deployment** | ![Cloud / Deployment technology icons](https://skillicons.dev/icons?i=vercel&theme=dark&perline=10)<br/>Vercel · Render · Cloudinary |
| **Tools** | ![Tools technology icons](https://skillicons.dev/icons?i=github,vscode&theme=dark&perline=10)<br/>GitHub · VS Code |
<!-- END:STACK -->

<a id="github-stats"></a>

## 📊 GitHub Stats

All cards below are generated by the [Metrics workflow](.github/workflows/metrics.yml) and committed to this repository, so they load fast and never depend on a third-party server being up.

![GitHub metrics overview: repositories, activity and community summary](metrics/github-metrics.svg)

![Most-used programming languages across my repositories](metrics/languages.svg)

### 🔥 Contribution Streak

![Current and longest contribution streak](metrics/streak.svg)

### 🏅 DSA &amp; Coding Platforms

<!-- BEGIN:CODING -->
*Add your LeetCode / CodeChef / HackerRank / Codeforces profile links here. Statistics are only shown when they can be fetched reliably.*
<!-- END:CODING -->

### 🏆 Certifications

<!-- BEGIN:CERTS -->
*Add verified certifications here.*
<!-- END:CERTS -->

Certificate files, if any, live in [`certificates/`](certificates/).

### 🎖️ Achievements

![GitHub achievements earned so far](metrics/achievements.svg)

<details>
<summary><b>📈 Detailed metrics, calendar and habits (click to expand)</b></summary>

### 📅 Isometric Contribution Calendar

![Isometric view of my last year of contributions](metrics/isocalendar.svg)

### 💡 Coding Habits

![Coding habits: when and how I commit](metrics/habits.svg)

### 📌 Starred Topics

![Topics of the repositories I have starred](metrics/topics.svg)

</details>

### 🐍 Watch the Snake Eat My Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/abhiraj66369-commits/abhiraj66369-commits/output/github-snake-dark.svg">
  <img alt="Snake animation eating through my GitHub contribution graph" src="https://raw.githubusercontent.com/abhiraj66369-commits/abhiraj66369-commits/output/github-snake.svg" width="100%">
</picture>

<img src="assets/divider.svg" alt="" width="100%">

## 🌱 Currently Learning

<!-- BEGIN:LEARNING -->
*Add what you are actively learning here (data/profile.json → learning).*
<!-- END:LEARNING -->

<a id="roadmap"></a>

## 🗺️ Roadmap

<!-- BEGIN:ROADMAP -->
- [ ] AgroMind AI: ground answers with retrieval over an agricultural knowledge base (RAG) *(planned)*
- [ ] AgroMind AI: location, crop and weather context *(planned)*
- [ ] Screenshots and architecture docs for every flagship repo *(planned)*
- [ ] Automated tests and CI on flagship repos *(planned)*
<!-- END:ROADMAP -->

<a id="contact"></a>

## 📬 Contact

<!-- BEGIN:CONTACT -->
[![GitHub — Profile](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abhiraj66369-commits)
<!-- END:CONTACT -->

<p align="center">
  <img src="assets/footer.svg" alt="Thanks for visiting. Let's build something useful." width="100%">
</p>
