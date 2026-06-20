// seo.js — qte77 portable SEO head builder (no-build ES module).
//
// Emits the same head tags a Jekyll `jekyll-seo-tag` site produces (meta +
// Open Graph + Twitter Card + JSON-LD), but framework-free — so the no-build /
// Vite GUIs get parity with qte77.github.io. Intended as a BUILD-TIME helper
// (run under Node to emit static `<head>` HTML), not a runtime injector —
// crawlers shouldn't depend on JS to see your meta. See seo.html for the
// authored-template alternative.
//
// The JSON-LD also feeds GEO + ASO (see DISCOVERABILITY.md).

/** Escape a string for safe use inside an HTML double-quoted attribute. */
export function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

const isArticle = (cfg) => cfg.type === "article" || cfg.type === "post";

/**
 * Build the schema.org JSON-LD object: `BlogPosting` for an article, else a
 * `WebSite` with an `author` Person. Pure — returns a plain object.
 */
export function buildJsonLd(cfg) {
  const author = {
    "@type": "Person",
    name: cfg.author?.name,
    url: cfg.author?.url || cfg.siteUrl,
  };
  if (cfg.author?.sameAs?.length) author.sameAs = cfg.author.sameAs;
  if (cfg.author?.image) {
    author.image = { "@type": "ImageObject", url: cfg.author.image };
  }

  if (!isArticle(cfg)) {
    return {
      "@context": "https://schema.org",
      "@type": "WebSite",
      name: cfg.siteName || cfg.title,
      url: cfg.siteUrl || cfg.url,
      description: cfg.description,
      author,
    };
  }

  return {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    mainEntityOfPage: { "@type": "WebPage", "@id": cfg.url },
    headline: cfg.title,
    description: cfg.description,
    image: cfg.image || cfg.siteImage,
    datePublished: cfg.datePublished,
    dateModified: cfg.dateModified || cfg.datePublished,
    author: { "@type": "Person", name: cfg.author?.name, url: cfg.author?.url },
    publisher: {
      "@type": "Organization",
      name: cfg.siteName || cfg.title,
      logo: { "@type": "ImageObject", url: cfg.logo || cfg.siteImage },
    },
  };
}

/** Drop keys whose value is undefined/null (so optional fields vanish cleanly). */
function prune(obj) {
  if (Array.isArray(obj)) return obj.map(prune);
  if (obj && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj)
        .filter(([, v]) => v !== undefined && v !== null)
        .map(([k, v]) => [k, prune(v)]),
    );
  }
  return obj;
}

/**
 * Render the full `<head>` SEO fragment as an HTML string. Description and image
 * fall back through page → site. Returns build-time-injectable HTML.
 */
export function renderHead(cfg) {
  const desc = cfg.description || cfg.siteDescription;
  const image = cfg.image || cfg.siteImage;
  const ogType = isArticle(cfg) ? "article" : "website";
  const m = (l) => l.filter(Boolean).join("\n");

  const tags = [
    `<title>${esc(cfg.title)}${cfg.siteName ? ` | ${esc(cfg.siteName)}` : ""}</title>`,
    `<meta name="viewport" content="width=device-width, initial-scale=1.0">`,
    desc && `<meta name="description" content="${esc(desc)}">`,
    cfg.author?.name && `<meta name="author" content="${esc(cfg.author.name)}">`,
    cfg.keywords && `<meta name="keywords" content="${esc(cfg.keywords)}">`,
    `<meta name="robots" content="index, follow">`,
    cfg.url && `<link rel="canonical" href="${esc(cfg.url)}">`,
    // Open Graph
    `<meta property="og:title" content="${esc(cfg.title)}">`,
    desc && `<meta property="og:description" content="${esc(desc)}">`,
    cfg.url && `<meta property="og:url" content="${esc(cfg.url)}">`,
    cfg.siteName && `<meta property="og:site_name" content="${esc(cfg.siteName)}">`,
    `<meta property="og:type" content="${ogType}">`,
    `<meta property="og:locale" content="${esc(cfg.locale || "en_US")}">`,
    image && `<meta property="og:image" content="${esc(image)}">`,
    // Twitter Card
    `<meta name="twitter:card" content="${esc(cfg.twitterCard || "summary")}">`,
    cfg.twitterUser && `<meta name="twitter:site" content="@${esc(cfg.twitterUser)}">`,
    cfg.twitterUser && `<meta name="twitter:creator" content="@${esc(cfg.twitterUser)}">`,
    `<meta name="twitter:title" content="${esc(cfg.title)}">`,
    desc && `<meta name="twitter:description" content="${esc(desc)}">`,
    image && `<meta name="twitter:image" content="${esc(image)}">`,
    // JSON-LD (also feeds GEO/ASO)
    `<script type="application/ld+json">${JSON.stringify(prune(buildJsonLd(cfg)))}</script>`,
  ];
  return m(tags) + "\n";
}
