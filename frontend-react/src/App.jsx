import React from 'react';

export default function App() {
  const handleBrandInstaClick = () => {
    window.open('https://instagram.com/thedaily.poshan', '_blank', 'noreferrer');
  };

  const handleFounderInstaClick = () => {
    window.open('https://instagram.com/prem.fya', '_blank', 'noreferrer');
  };

  const handleScrollToMenu = () => {
    document.getElementById('signature-menu')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleScrollToStory = () => {
    document.getElementById('brand-story')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="landing-container">
      <div className="ambient-glow" />

      {/* Header */}
      <header className="site-header">
        <div className="header-brand">
          <div className="brand-logo-mark">🍃</div>
          <div className="brand-info">
            <span className="brand-name">Daily Poshan</span>
            <span className="brand-handle">@thedaily.poshan</span>
          </div>
        </div>

        <div className="header-actions">
          <button type="button" className="insta-pill" onClick={handleBrandInstaClick}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
              <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
            <span>@thedaily.poshan</span>
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-dot" />
            <span>Pure Veg & High-Protein Jar Salads</span>
          </div>
          <h1 className="hero-title">
            Your daily dose of poshan, <span className="gradient-text">packed fresh in every jar</span>.
          </h1>
          <p className="hero-subtext">
            <strong>Daily Poshan</strong> (<a href="https://instagram.com/thedaily.poshan" target="_blank" rel="noreferrer" className="brand-handle">@thedaily.poshan</a>) delivers ready-to-eat, nutrient-dense jar salads designed for fitness lovers, busy professionals, and clean eaters. 100% vegetarian, plant-forward protein, and zero preservatives.
          </p>
          <div className="hero-actions-group">
            <button type="button" className="btn-primary" onClick={handleBrandInstaClick}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
              <span>Follow @thedaily.poshan</span>
            </button>
            <button type="button" className="btn-secondary" onClick={handleScrollToMenu}>
              <span>Explore Signature Menu ↓</span>
            </button>
          </div>
        </div>

        <div className="hero-card-wrapper">
          <div className="hero-portrait-card">
            <div className="portrait-img-box">
              <img src="/muscle_fuel_jar.png" alt="Daily Poshan Muscle Fuel Jar" className="portrait-img" />
              <div className="portrait-tag">Flagship: Muscle Fuel Jar</div>
            </div>
            <div className="card-author-details">
              <div>
                <div className="card-author-name">Daily Poshan</div>
                <div className="card-author-role">Founded by Prem (<a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-pink)' }}>@prem.fya</a>)</div>
              </div>
              <a 
                href="https://instagram.com/thedaily.poshan" 
                target="_blank" 
                rel="noreferrer" 
                className="card-social-handle"
              >
                @thedaily.poshan
              </a>
            </div>
          </div>

          <div className="floating-stat-badge">
            <span className="stat-icon">💪</span>
            <div>
              <div className="stat-num">22g Protein</div>
              <div className="stat-lbl">Muscle Fuel Jar</div>
            </div>
          </div>
        </div>
      </section>

      {/* Signature Menu Section */}
      <section className="section-wrapper" id="signature-menu">
        <div className="section-header">
          <span className="section-eyebrow">OUR MENU</span>
          <h2 className="section-title">Handcrafted Nutrient-Dense Jar Salads</h2>
          <p className="section-subtitle">
            Freshly prepared with organic greens, high-protein paneer, sprouts, seeds, and signature house dressings.
          </p>
        </div>

        <div className="menu-grid">
          {/* Muscle Fuel Jar */}
          <div className="menu-card highlight-menu-card">
            <div className="menu-card-header">
              <span className="project-tag tag-emerald">FLAGSHIP HIGH-PROTEIN</span>
              <span className="menu-price">₹250</span>
            </div>
            <h3>Muscle Fuel Jar 🥗</h3>
            <p className="menu-tagline">High-protein, plant-forward power bowl for strength & recovery.</p>
            <p className="menu-desc">
              Loaded with fresh paneer cubes, sprouted lentils, roasted seeds, crunchy cucumber, and mixed greens with clean mint dressing.
            </p>
            <div className="menu-stats">
              <span><strong>22g</strong> Protein</span>
              <span><strong>320</strong> Calories</span>
              <span><strong>Pure Veg</strong></span>
            </div>
          </div>

          {/* Chatori Jar */}
          <div className="menu-card">
            <div className="menu-card-header">
              <span className="project-tag tag-amber">DESI TWIST</span>
              <span className="menu-price">₹250</span>
            </div>
            <h3>Chatori Jar 🌶️</h3>
            <p className="menu-tagline">Chatpata, desi twist with a healthy crunch.</p>
            <p className="menu-desc">
              A vibrant crunchy salad jar packed with chaat spices, baked sev, chickpeas, garden veggies, and tangy tamarind-mint dressing.
            </p>
            <div className="menu-stats">
              <span><strong>8g</strong> Protein</span>
              <span><strong>270</strong> Calories</span>
              <span><strong>Tangy</strong></span>
            </div>
          </div>

          {/* Glow & Flow Jar */}
          <div className="menu-card">
            <div className="menu-card-header">
              <span className="project-tag tag-purple">RADIANCE SPECIAL</span>
              <span className="menu-price">₹250</span>
            </div>
            <h3>Glow & Flow Jar ✨</h3>
            <p className="menu-tagline">Special salad for natural glow, balance & vital energy.</p>
            <p className="menu-desc">
              Radiance jar crafted with antioxidant-rich berries, avocado, chia & pumpkin seeds, spinach, and lemon tahini dressing.
            </p>
            <div className="menu-stats">
              <span><strong>10g</strong> Protein</span>
              <span><strong>280</strong> Calories</span>
              <span><strong>Antioxidant</strong></span>
            </div>
          </div>

          {/* Extra Dips */}
          <div className="menu-card">
            <div className="menu-card-header">
              <span className="project-tag tag-cyan">ADD-ON DRESSINGS</span>
              <span className="menu-price">₹25</span>
            </div>
            <h3>Signature Extra Dips 🥣</h3>
            <p className="menu-tagline">Artisanal dressings made fresh daily.</p>
            <p className="menu-desc">
              Choose from freshly whipped mint chutney, creamy tahini sesame dip, or spicy schezwan sauce to elevate your jar.
            </p>
            <div className="menu-stats">
              <span><strong>0g</strong> Preservatives</span>
              <span><strong>35</strong> Calories</span>
              <span><strong>Fresh</strong></span>
            </div>
          </div>
        </div>
      </section>

      {/* Brand Story & Founder Journey */}
      <section className="section-wrapper" id="brand-story">
        <div className="section-header">
          <span className="section-eyebrow">THE BRAND STORY</span>
          <h2 className="section-title">The Origin of Daily Poshan</h2>
          <p className="section-subtitle">
            Founded by <strong>Prem</strong> (<a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-pink)' }}>@prem.fya</a>) as an entrepreneurial D2C startup experiment to redefine convenient vegetarian nutrition.
          </p>
        </div>

        <div className="about-card">
          <div className="about-bio">
            <h3>Building a Better Meal Jar 🌿</h3>
            <p>
              <strong>Daily Poshan</strong> was born from a simple realization: fitness enthusiasts and health-conscious individuals who prefer pure vegetarian food struggle to find quick, high-protein, ready-to-eat meals.
            </p>
            <p>
              Founder <strong>Prem</strong> (<a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-pink)' }}>@prem.fya</a>) took Daily Poshan through the complete venture development cycle — developing the signature Muscle Fuel Jar recipe, designing consumer sticker labels, creating social ad campaigns, and architecting a modern digital web platform.
            </p>
            <div className="skills-pill-group">
              <span className="skill-pill">Pure Vegetarian</span>
              <span className="skill-pill">High Protein</span>
              <span className="skill-pill">Ready to Eat</span>
              <span className="skill-pill">Zero Preservatives</span>
              <span className="skill-pill">Eco Glass Jars</span>
              <span className="skill-pill">WhatsApp Ordering</span>
            </div>
          </div>

          <div className="about-highlights-grid">
            <div className="highlight-box">
              <div className="highlight-box-icon">💡</div>
              <div className="highlight-box-title">Problem Identification</div>
              <div className="highlight-box-desc">Solving the vegetarian protein gap with ready, convenient jar salads.</div>
            </div>
            <div className="highlight-box">
              <div className="highlight-box-icon">🥗</div>
              <div className="highlight-box-title">Product R&D</div>
              <div className="highlight-box-desc">Formulating the Muscle Fuel Jar with 22g clean plant-forward protein.</div>
            </div>
            <div className="highlight-box">
              <div className="highlight-box-icon">🏷️</div>
              <div className="highlight-box-title">Brand & Packaging</div>
              <div className="highlight-box-desc">Designing custom sticker graphics for consumer-ready jar packaging.</div>
            </div>
            <div className="highlight-box">
              <div className="highlight-box-icon">📱</div>
              <div className="highlight-box-title">Digital Ordering</div>
              <div className="highlight-box-desc">Building a seamless React & Django web app with instant WhatsApp ordering.</div>
            </div>
          </div>
        </div>
      </section>

      {/* Brand Values */}
      <section className="section-wrapper">
        <div className="section-header">
          <span className="section-eyebrow">OUR PROMISE</span>
          <h2 className="section-title">Why Daily Poshan?</h2>
        </div>

        <div className="projects-grid">
          <div className="project-card">
            <div>
              <span className="project-tag tag-emerald">100% PURE VEG</span>
              <h3>Wholesome Plant Nutrition</h3>
              <p>
                Every jar is crafted with fresh greens, sprouted legumes, paneer, and superfood seeds — zero meat, zero artificial add-ons.
              </p>
            </div>
          </div>

          <div className="project-card">
            <div>
              <span className="project-tag tag-cyan">READY TO EAT</span>
              <h3>Ultimate Convenience</h3>
              <p>
                No cooking, no chopping, no prep needed. Simply pop open a fresh Daily Poshan jar and enjoy nutritious poshan anywhere.
              </p>
            </div>
          </div>

          <div className="project-card">
            <div>
              <span className="project-tag tag-purple">ECO PACKAGING</span>
              <h3>Freshness Sealed Jars</h3>
              <p>
                Packaged in reusable glass jars with leak-proof seals, keeping ingredients fresh, crisp, and nutrient-rich for longer.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Brand Instagram Banner */}
      <section className="insta-banner-card">
        <div className="insta-banner-content">
          <h3>Follow @thedaily.poshan on Instagram</h3>
          <p>
            Stay connected with <strong>Daily Poshan</strong> (<a href="https://instagram.com/thedaily.poshan" target="_blank" rel="noreferrer" style={{ textDecoration: 'underline', fontWeight: 700 }}>@thedaily.poshan</a>) for fresh jar drops, health tips, and behind-the-scenes startup updates!
          </p>
          <div style={{ marginTop: '12px', fontSize: '14px', opacity: 0.9 }}>
            Founded & Created by Prem (<a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer" style={{ textDecoration: 'underline', color: '#ffffff' }}>@prem.fya</a>)
          </div>
        </div>
        <button type="button" className="insta-big-btn" onClick={handleBrandInstaClick}>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
          </svg>
          <span>Follow @thedaily.poshan</span>
        </button>
      </section>

      {/* Footer */}
      <footer className="site-footer">
        <div className="footer-brand">
          Daily Poshan &bull; <span style={{ color: 'var(--accent-pink)' }}>@thedaily.poshan</span>
        </div>
        <div>
          &copy; {new Date().getFullYear()} Daily Poshan &bull; Founded by Prem (<a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-purple)' }}>@prem.fya</a>)
        </div>
        <div className="footer-links">
          <a href="https://instagram.com/thedaily.poshan" target="_blank" rel="noreferrer">Instagram (@thedaily.poshan)</a>
          <a href="https://instagram.com/prem.fya" target="_blank" rel="noreferrer">Founder (@prem.fya)</a>
        </div>
      </footer>
    </div>
  );
}
