const organizationUrl = "https://github.com/Quick-Red-Tech";

const downloadCards = [
  {
    platform: "Windows Version",
    artifact: ".exe build",
    copy:
      "Download the Windows desktop release for classrooms, labs, and revision systems that need a direct executable build.",
    cta: "Get Windows .exe",
  },
  {
    platform: "macOS Version",
    artifact: ".dmg package",
    copy:
      "Download the macOS release as a disk image package, which is the standard Mac delivery format for this GUI app.",
    cta: "Get macOS .dmg",
  },
];

const featureCards = [
  {
    title: "Three focused workspaces",
    copy:
      "Guide students through structured polynomials, radical equations, or worksheet-style typed expressions without mixing the mental models.",
  },
  {
    title: "Readable symbols on screen",
    copy:
      "The app now uses clearer mathematical symbols like √, ∛, superscripts, and symbolic derivatives so students can understand what they are seeing.",
  },
  {
    title: "Desktop shell that feels complete",
    copy:
      "Menu bar, toolbar, status area, help/about flows, and workspace guides make the app feel like a proper product instead of a raw prototype.",
  },
];

const workflowSteps = [
  {
    step: "01",
    title: "Choose the right workspace",
    copy:
      "Use Polynomial for multi-term power-rule work, Roots for guided radicals, and Expressions for broader worksheet questions.",
  },
  {
    step: "02",
    title: "Review the interpreted math",
    copy:
      "Students can see the original equation, the normalized power-rule interpretation, and the result with clearer mathematical symbols.",
  },
  {
    step: "03",
    title: "Teach from a clean output panel",
    copy:
      "The result layout is built for explanation: readable preview blocks, scrollable long expressions, and clearer derivative output.",
  },
];

const exampleCards = [
  {
    mode: "Polynomial",
    equation: "y = x⁴ + 3x² − 7",
    derivative: "y′ = 4x³ + 6x",
  },
  {
    mode: "Roots",
    equation: "y = √x − 3",
    derivative: "y′ = 1 / (2√x)",
  },
  {
    mode: "Expressions",
    equation: "y = 4x − 1/x²",
    derivative: "y′ = 4 + 2/x³",
  },
];

const milestones = [
  {
    date: "May 2022",
    title: "Project start",
    copy:
      "Chisom Life Eke, CEO of Quick Red Tech, started building the differentiation project in May 2022.",
  },
  {
    date: "2022 to 2025",
    title: "Long bug-fixing stretch",
    copy:
      "The product direction stayed alive, but repeated bugs and interface issues slowed delivery and forced several rebuilds.",
  },
  {
    date: "Late February 2026",
    title: "Version 1 completed",
    copy:
      "The desktop app was finished in late February 2026 with guided tabs, clearer symbols, and a stronger product shell.",
  },
];

const faqs = [
  {
    question: "Where do I get the downloads quickly?",
    answer:
      "Both the Windows .exe release and the macOS .dmg package are promoted through the Quick Red Tech organization on GitHub.",
  },
  {
    question: "Who started the project?",
    answer:
      "The project story on this site credits Chisom Life Eke, CEO of Quick Red Tech, with starting the build in May 2022 and completing version 1 in late February 2026.",
  },
  {
    question: "Why keep multiple tabs instead of one large calculator?",
    answer:
      "Because the learning flow changes by problem type. Structured tabs reduce mistakes and make each rule set easier to teach.",
  },
  {
    question: "Can the product handle mixed worksheet questions?",
    answer:
      "Yes. The Expressions workspace now supports typed inputs that mix roots, reciprocal powers, shifted terms, and standard powers in one line.",
  },
];

function App() {
  return (
    <div className="site-shell">
      <header className="masthead">
        <nav className="topbar">
          <a className="brand" href="#top">
            <span className="brand-mark" aria-hidden="true">
              d/dx
            </span>
            <span className="brand-copy">
              <strong>QuickRed Tech</strong>
              <span>Differentiator</span>
            </span>
          </a>

          <div className="nav-links">
            <a href="#downloads">Downloads</a>
            <a href="#features">Features</a>
            <a href="#story">Story</a>
            <a href="#faq">FAQ</a>
          </div>

          <a className="nav-cta" href={organizationUrl} target="_blank" rel="noreferrer">
            Quick Red Tech
          </a>
        </nav>

        <section className="hero" id="top">
          <div className="hero-copy">
            <p className="eyebrow">Desktop differentiation software for real teaching flow</p>
            <h1>Launch a clearer power-rule workspace on Windows and macOS.</h1>
            <p className="hero-text">
              QuickRed Tech Differentiator packages guided polynomial work, radical questions, and mixed expression solving into
              one desktop product with clearer math symbols, stronger UI structure, and release-ready download targets.
            </p>

            <div className="hero-actions">
              <a className="button button-primary" href="#downloads">
                View download versions
              </a>
              <a className="button button-secondary" href={organizationUrl} target="_blank" rel="noreferrer">
                Open Quick Red Tech
              </a>
            </div>

            <div className="hero-metrics">
              <article>
                <strong>2</strong>
                <span>desktop release targets: Windows .exe and macOS .dmg</span>
              </article>
              <article>
                <strong>3</strong>
                <span>guided workspaces for different differentiation question types</span>
              </article>
              <article>
                <strong>2022 → 2026</strong>
                <span>product journey from initial build to completed version 1</span>
              </article>
            </div>
          </div>

          <div className="hero-visual" aria-label="Application preview">
            <div className="orb orb-one" />
            <div className="orb orb-two" />

            <div className="product-window">
              <div className="window-chrome">
                <div className="window-dots">
                  <span />
                  <span />
                  <span />
                </div>
                <p>QuickRed Tech Differentiator</p>
              </div>

              <div className="window-tabs">
                <span className="active">Polynomial</span>
                <span>Roots</span>
                <span>Expressions</span>
              </div>

              <div className="window-grid">
                <section className="demo-card tone-deep">
                  <p className="demo-label">Builder</p>
                  <h2>Equation workspace</h2>
                  <ul>
                    <li>x⁴ + 3x² − 7</li>
                    <li>√x − 3</li>
                    <li>4x − 1/x²</li>
                  </ul>
                </section>

                <section className="demo-card tone-light">
                  <p className="demo-label">Interpretation</p>
                  <h3>Readable symbolic math</h3>
                  <p>y = x^(1/2) − 3</p>
                  <p>y′ = 1 / (2√x)</p>
                </section>

                <section className="demo-card tone-accent">
                  <p className="demo-label">Release story</p>
                  <h3>Now packaged for desktop delivery</h3>
                  <p>Windows .exe release</p>
                  <p>macOS .dmg package</p>
                </section>
              </div>
            </div>
          </div>
        </section>
      </header>

      <main>
        <section className="section downloads-section" id="downloads">
          <div className="section-head">
            <p className="eyebrow">Downloads</p>
            <h2>Promote both desktop versions clearly so users know what they can install.</h2>
          </div>

          <div className="download-grid">
            {downloadCards.map((card) => (
              <article key={card.platform} className="download-card">
                <p className="example-mode">{card.platform}</p>
                <h3>{card.artifact}</h3>
                <p>{card.copy}</p>
                <a className="button button-primary" href={organizationUrl} target="_blank" rel="noreferrer">
                  {card.cta}
                </a>
              </article>
            ))}
          </div>

          <p className="download-note">
            Quick access link:{" "}
            <a href={organizationUrl} target="_blank" rel="noreferrer">
              {organizationUrl}
            </a>
          </p>
        </section>

        <section className="section feature-section" id="features">
          <div className="section-head">
            <p className="eyebrow">Why it feels like a product</p>
            <h2>Professional interface decisions now support the math, the lesson flow, and the release story.</h2>
          </div>

          <div className="feature-grid">
            {featureCards.map((card, index) => (
              <article key={card.title} className="feature-card">
                <span className="feature-index">0{index + 1}</span>
                <h3>{card.title}</h3>
                <p>{card.copy}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section workflow-section" id="workflow">
          <div className="section-head narrow">
            <p className="eyebrow">Teaching workflow</p>
            <h2>Built for the real sequence of explanation, checking, and showing the final derivative.</h2>
          </div>

          <div className="workflow-list">
            {workflowSteps.map((item) => (
              <article key={item.step} className="workflow-card">
                <span>{item.step}</span>
                <div>
                  <h3>{item.title}</h3>
                  <p>{item.copy}</p>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="section equation-section" id="equations">
          <div className="section-head">
            <p className="eyebrow">Coverage examples</p>
            <h2>The product now covers the main problem families users actually ask for.</h2>
          </div>

          <div className="example-grid">
            {exampleCards.map((card) => (
              <article key={card.mode} className="example-card">
                <p className="example-mode">{card.mode}</p>
                <h3>{card.equation}</h3>
                <p>{card.derivative}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section story-section" id="story">
          <div className="section-head">
            <p className="eyebrow">Founder story</p>
            <h2>Chisom Life Eke started the project in May 2022 and carried it through bugs to a finished v1 in late February 2026.</h2>
          </div>

          <div className="timeline-list">
            {milestones.map((item) => (
              <article key={item.date} className="timeline-card">
                <p className="timeline-date">{item.date}</p>
                <h3>{item.title}</h3>
                <p>{item.copy}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section quote-section">
          <div className="quote-panel">
            <p className="quote-mark">“</p>
            <blockquote>
              A good differentiation tool should not only compute the answer. It should make the rule visible.
            </blockquote>
            <p className="quote-caption">Product principle behind QuickRed Tech Differentiator version 1</p>
          </div>
        </section>

        <section className="section faq-section" id="faq">
          <div className="section-head narrow">
            <p className="eyebrow">FAQ</p>
            <h2>Questions users, tutors, and school leads will ask before installing the app.</h2>
          </div>

          <div className="faq-list">
            {faqs.map((item) => (
              <article key={item.question} className="faq-card">
                <h3>{item.question}</h3>
                <p>{item.answer}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section launch-section" id="launch">
          <div className="launch-card">
            <div>
              <p className="eyebrow">Quick Red Tech organization</p>
              <h2>Use the organization page as the fast path to the project story, release builds, and future updates.</h2>
            </div>

            <div className="launch-actions">
              <a className="button button-primary" href={organizationUrl} target="_blank" rel="noreferrer">
                Open Quick Red Tech
              </a>
              <a className="button button-secondary" href="#top">
                Back to top
              </a>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>QuickRed Tech Differentiator</p>
        <p>
          Windows .exe and macOS .dmg desktop releases promoted through the{" "}
          <a href={organizationUrl} target="_blank" rel="noreferrer">
            Quick Red Tech organization
          </a>
          .
        </p>
      </footer>
    </div>
  );
}

export default App;
