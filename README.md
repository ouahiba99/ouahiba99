<style>
  .matrix-shell {
    --bg: #020b08;
    --bg-2: #071a14;
    --panel: rgba(10, 22, 18, 0.9);
    --panel-2: rgba(10, 28, 22, 0.86);
    --border: rgba(111, 255, 188, 0.45);
    --text: #d9ffe7;
    --muted: #a8f8d0;
    --green: #61ffb5;
    --green-2: #7ef9c6;
    --green-3: #1ade89;
    --shadow: rgba(97, 255, 181, 0.32);
  }

  .matrix-shell {
    max-width: 1200px;
    margin: 0 auto;
    background:
      linear-gradient(180deg, rgba(8, 18, 14, 0.98), rgba(2, 11, 8, 0.98)),
      radial-gradient(circle at top, rgba(35, 255, 170, 0.12), transparent 40%);
    border: 1px solid var(--border);
    border-radius: 22px;
    box-shadow: 0 0 0 1px rgba(87, 255, 184, 0.12), 0 25px 60px rgba(0, 0, 0, 0.65), inset 0 0 28px rgba(81, 255, 162, 0.05);
    overflow: hidden;
    position: relative;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  }

  .matrix-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      180deg,
      rgba(113, 255, 190, 0.04),
      rgba(113, 255, 190, 0.04) 1px,
      transparent 1px,
      transparent 4px
    );
    pointer-events: none;
    animation: scan 11s linear infinite;
  }

  .matrix-shell > * {
    position: relative;
    z-index: 1;
  }

  .matrix-window {
    padding: 0;
  }

  .matrix-header,
  .matrix-section-title,
  .matrix-project-title,
  .matrix-phase {
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .matrix-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    border-bottom: 1px solid rgba(126, 249, 198, 0.24);
    background: rgba(9, 20, 15, 0.9);
    color: var(--text);
    font-size: 12px;
    font-weight: 700;
  }

  .window-dots {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .window-dots span {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 10px rgba(255,255,255,0.18);
  }

  .window-dots .red { background: #ff5f57; }
  .window-dots .yellow { background: #ffbd2e; }
  .window-dots .green { background: #28c840; }

  .matrix-body {
    padding: 22px 22px 18px;
    color: var(--text);
    background: rgba(2, 11, 8, 0.84);
  }

  .matrix-line {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    min-height: 31px;
    font-size: 15px;
    color: var(--muted);
  }

  .prompt {
    color: var(--green-2);
    font-weight: 700;
  }

  .command {
    color: #dfffea;
    text-shadow: 0 0 12px rgba(126, 249, 198, 0.62);
  }

  .cursor {
    width: 10px;
    height: 18px;
    display: inline-block;
    background: var(--green-2);
    animation: blink 0.9s steps(1) infinite;
    box-shadow: 0 0 10px rgba(126, 249, 198, 0.8);
    vertical-align: middle;
  }

  .matrix-badges {
    margin-top: 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .matrix-badge {
    padding: 7px 12px;
    border: 1px solid rgba(97, 255, 181, 0.34);
    border-radius: 999px;
    background: rgba(10, 22, 18, 0.8);
    color: var(--green-2);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    box-shadow: inset 0 0 14px rgba(97, 255, 181, 0.08);
    animation: pulse 2.6s ease-in-out infinite;
  }

  .matrix-section {
    padding: 18px 22px 10px;
  }

  .matrix-section-title {
    margin: 0 0 16px;
    color: var(--green-2);
    font-size: 13px;
    font-weight: 700;
    border-left: 3px solid var(--green-2);
    padding-left: 12px;
    background: linear-gradient(90deg, rgba(97,255,181,0.12), transparent 70%);
    display: inline-block;
    padding-right: 14px;
    border-radius: 4px 0 0 4px;
  }

  .matrix-panel {
    background: linear-gradient(180deg, rgba(7, 20, 16, 0.9), rgba(4, 12, 10, 0.92));
    border: 1px solid rgba(126, 249, 198, 0.22);
    border-radius: 16px;
    box-shadow: inset 0 0 20px rgba(126, 249, 198, 0.03);
    padding: 18px 18px 14px;
    margin-bottom: 18px;
  }

  .matrix-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
  }

  .matrix-card {
    background: var(--panel-2);
    border: 1px solid rgba(126, 249, 198, 0.18);
    border-radius: 14px;
    padding: 16px;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .matrix-card:hover {
    transform: translateY(-2px);
    border-color: rgba(126, 249, 198, 0.5);
    box-shadow: 0 12px 24px rgba(97,255,181,0.08);
  }

  .matrix-card h3 {
    margin: 0 0 10px;
    color: var(--green-2);
    font-size: 13px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .matrix-card p,
  .matrix-card li,
  .matrix-card span,
  .matrix-card a {
    color: var(--text);
    line-height: 1.6;
    font-size: 14px;
  }

  .matrix-card ul {
    margin: 0;
    padding-left: 18px;
  }

  .matrix-tag-row,
  .matrix-inline {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
  }

  .matrix-tag {
    background: rgba(12, 28, 22, 0.9);
    border: 1px solid rgba(126, 249, 198, 0.24);
    border-radius: 999px;
    padding: 4px 9px;
    font-size: 11px;
    color: var(--green-2);
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .matrix-project {
    margin-bottom: 18px;
    padding: 18px;
    background: rgba(5, 17, 13, 0.9);
    border: 1px solid rgba(126, 249, 198, 0.2);
    border-radius: 14px;
  }

  .matrix-project-title {
    margin: 0 0 10px;
    font-size: 16px;
    color: var(--green-2);
  }

  .matrix-project p {
    color: var(--text);
    line-height: 1.7;
    margin: 0 0 10px;
  }

  .matrix-project ul {
    margin: 10px 0 0;
    padding-left: 18px;
    color: var(--text);
    line-height: 1.7;
  }

  .matrix-status {
    color: var(--green-2);
    font-weight: 700;
    display: inline-block;
    margin-bottom: 8px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 11px;
  }

  .matrix-stats {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    padding: 0 22px 22px;
  }

  .matrix-stats img {
    border-radius: 12px;
    border: 1px solid rgba(126, 249, 198, 0.18);
    background: rgba(8, 18, 15, 0.8);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  }

  .matrix-connect {
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
    padding: 8px 22px 24px;
  }

  .matrix-connect a {
    display: inline-block;
    border: 1px solid rgba(126, 249, 198, 0.25);
    border-radius: 10px;
    background: rgba(9, 20, 15, 0.9);
    padding: 8px 12px;
    color: var(--text);
    text-decoration: none;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
  }

  .matrix-connect a:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(126,249,198,0.18);
  }

  .matrix-footer {
    padding: 0 22px 22px;
    text-align: center;
    color: var(--green-2);
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  @keyframes scan {
    0% { transform: translateY(-14%); }
    100% { transform: translateY(14%); }
  }

  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }

  @keyframes pulse {
    0%, 100% { box-shadow: inset 0 0 8px rgba(126,249,198,0.04); }
    50% { box-shadow: inset 0 0 18px rgba(126,249,198,0.15), 0 0 18px rgba(126,249,198,0.12); }
  }

  @media (max-width: 760px) {
    .matrix-grid {
      grid-template-columns: 1fr;
    }

    .matrix-body {
      padding: 18px 16px 14px;
    }

    .matrix-section {
      padding: 14px 16px 8px;
    }

    .matrix-stats {
      padding-left: 16px;
      padding-right: 16px;
      flex-direction: column;
    }
  }
</style>

<div class="matrix-shell">
  <div class="matrix-window">
    <div class="matrix-header">
      <div class="window-dots">
        <span class="red"></span>
        <span class="yellow"></span>
        <span class="green"></span>
      </div>
      <span>ouahiba@matrix:~$</span>
    </div>

  <div class="matrix-body">
      <div class="matrix-line">
        <span class="prompt">ouahiba99@github:~$</span>
        <span class="command">./welcome --profile</span>
        <span class="cursor"></span>
      </div>
      <div class="matrix-line">
        <span class="prompt">status</span>
        <span class="command">DataOps • Cloud • MLOps • Telecom • Automation</span>
      </div>
      <div class="matrix-badges">
        <span class="matrix-badge">DataOps</span>
        <span class="matrix-badge">Cloud</span>
        <span class="matrix-badge">MLOps</span>
        <span class="matrix-badge">Telecom</span>
        <span class="matrix-badge">Automation</span>
      </div>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[00] identity</div>
    <div class="matrix-panel">
      
<p align="center">
  <img
    src="https://capsule-render.vercel.app/api?type=transparent&height=200&section=header&text=%3E_%20Ouahiba%20Ahmid&fontSize=46&fontColor=7ef9c6&fontAlignY=38&animation=twinkling&color=00000000&desc=&descSize=18&descAlignY=62&descColor=00d4ff"
    alt="Ouahiba Ahmid — DataOps & Cloud Consultant"
    width="90%"
 />
</p>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[01] system overview</div>
    <div class="matrix-panel">
      <p>
        I'm a <strong>Telecom &amp; ICT State Engineer</strong> and <strong>DataOps &amp; Cloud Consultant</strong> focused on building reliable systems at the intersection of <strong>data engineering</strong>, <strong>cloud infrastructure</strong>, <strong>MLOps</strong>, and <strong>telecom operations</strong>.
      </p>
      <p>
        I enjoy turning complex technical requirements into <strong>automated, observable, and production-ready solutions</strong>.
      </p>
      <p align="center">
        <img src="https://www.gitskins.com/api/section/highlights?username=ouahiba99&theme=aurora&avatar=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F59165621%3Fv%3D4&items=Data%20Engineering%3A%3APipelines%20%26%20orchestration%7CCloud%20Infrastructure%3A%3AReliable%20platform%20delivery%7CTelecom%20Operations%3A%3AMonitoring%20%26%20performance&variant=wow&v=ouahiba-focus-1&mode=dark" width="100%" alt="Profile overview" />
      </p>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[02] core capabilities</div>
    <div class="matrix-grid">
      <div class="matrix-card">
        <h3>Data engineering</h3>
        <ul>
          <li>ETL / ELT orchestration</li>
          <li>Python, SQL, Spark</li>
          <li>PostgreSQL, MongoDB, Redis</li>
          <li>Airflow, Prefect</li>
        </ul>
      </div>
      <div class="matrix-card">
        <h3>Cloud infrastructure</h3>
        <ul>
          <li>GCP, Azure</li>
          <li>Docker, Kubernetes</li>
          <li>Linux, Nginx</li>
          <li>Production-ready deployment</li>
        </ul>
      </div>
      <div class="matrix-card">
        <h3>MLOps &amp; automation</h3>
        <ul>
          <li>MLflow, DVC</li>
          <li>FastAPI services</li>
          <li>CI/CD automation</li>
          <li>Operational reliability</li>
        </ul>
      </div>
      <div class="matrix-card">
        <h3>Observability &amp; telecom</h3>
        <ul>
          <li>Prometheus, Grafana</li>
          <li>Kibana &amp; log analysis</li>
          <li>OSS / BSS operations</li>
          <li>Network monitoring and support</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[03] featured projects</div>
    <div class="matrix-project">
      <div class="matrix-status">project 01</div>
      <h3 class="matrix-project-title"><a href="https://github.com/ouahiba99/MLOPS_training">End-to-End MLOps Platform</a></h3>
      <p><strong>Production-oriented ML platform for predicting late e-commerce deliveries.</strong></p>
      <div class="matrix-inline">
        <span class="matrix-tag">Python</span>
        <span class="matrix-tag">PostgreSQL</span>
        <span class="matrix-tag">MLflow</span>
        <span class="matrix-tag">DVC</span>
        <span class="matrix-tag">FastAPI</span>
      </div>
      <ul>
        <li>End-to-end ML lifecycle from training to deployment</li>
        <li>Model registry and champion model workflow</li>
        <li>Artifact tracking with DVC and data validation</li>
        <li>Monitoring, Docker, CI/CD, and cloud integration</li>
      </ul>
    </div>

  <div class="matrix-project">
      <div class="matrix-status">project 02</div>
      <h3 class="matrix-project-title">Telecom Network Operations Platform</h3>
      <p><strong>Engineering platform for simulating, ingesting, processing, and monitoring telecom network data.</strong></p>
      <div class="matrix-inline">
        <span class="matrix-tag">Python</span>
        <span class="matrix-tag">Kafka</span>
        <span class="matrix-tag">PostgreSQL</span>
        <span class="matrix-tag">FastAPI</span>
        <span class="matrix-tag">Grafana</span>
      </div>
      <ul>
        <li>Network KPI and alarm simulation</li>
        <li>Kafka event streaming and operational stores</li>
        <li>Real-time observability dashboards</li>
        <li>Containerized architecture for performant processing</li>
      </ul>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[04] work experience</div>
    <div class="matrix-panel">
      <div class="matrix-card" style="margin-bottom: 12px;">
        <h3>Data / analytics operations</h3>
        <ul>
          <li>Built and maintained production data processing and ETL workflows</li>
          <li>Worked with Python, SQL, Spark, NoSQL, and workflow orchestration</li>
          <li>Supported monitoring, troubleshooting, and incident investigation</li>
          <li>Collaborated with international B2B technical teams</li>
        </ul>
      </div>
      <div class="matrix-card">
        <h3>Telecom network operations</h3>
        <ul>
          <li>Network monitoring and performance analysis across OSS platforms</li>
          <li>Incident investigation and troubleshooting</li>
          <li>Exposure to Nagios, Zabbix, NetAct, ENM, U2020, Jira, and Power BI</li>
          <li>Support for multinational telecom operators and teams</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[05] academy</div>
    <div class="matrix-panel">
      <h3 class="matrix-project-title">ITAAR Academy</h3>
      <p><strong>Founder · Technology &amp; Practical Learning</strong></p>
      <p>ITAAR Academy is a practical learning initiative focused on helping people learn, practice, and share useful skills.</p>
      <div class="matrix-tag-row">
        <span class="matrix-tag">learn</span>
        <span class="matrix-tag">practice</span>
        <span class="matrix-tag">grow</span>
      </div>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[06] github activity</div>
    <div class="matrix-stats">
      <img src="./profile/stats.svg" height="165" alt="GitHub Stats" />
      <img src="./profile/top-langs.svg" height="165" alt="Top Languages" />
    </div>
    <div class="matrix-panel" style="margin-top: 8px; margin-left: 22px; margin-right: 22px;">
      <p align="center">
        <img src="https://github-readme-activity-graph.vercel.app/graph?username=ouahiba99&bg_color=0d1117&color=7ef9c6&line=7ef9c6&point=00d4ff&area=true&hide_border=true" alt="Contribution graph" />
      </p>
      <p align="center">
        <img src="https://streak-stats.demolab.com?user=ouahiba99&hide_border=true&theme=dark" alt="Contribution streak" />
      </p>
      <p align="center">
        <img src="https://raw.githubusercontent.com/ouahiba99/ouahiba99/output/github-contribution-grid-snake.svg" width="90%" alt="GitHub contribution snake" />
      </p>
    </div>
  </div>

  <div class="matrix-section">
    <div class="matrix-section-title">[07] network</div>
    <div class="matrix-connect">
      <a href="https://github.com/ouahiba99">GitHub</a>
      <a href="https://linkedin.com/in/datadrivenmind">LinkedIn</a>
      <a href="mailto:ahmidouahiba@gmail.com">Email</a>
    </div>
  </div>

  <div class="matrix-footer">Building reliable systems. Turning data into scalable solutions.</div>
</div>
