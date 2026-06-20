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

/** A `<meta>` tag (name or property), or "" when the content is empty. */
function metaTag(attr, key, content) {
  return content ? `<meta ${attr}="${key}" content="${esc(content)}">` : "";
}
const metaName = (key, content) => metaTag("name", key, content);
const metaProp = (key, content) => metaTag("property", key, content);

/** JSON-LD `<script>` tag for the config (also feeds GEO/ASO). */
function jsonLdTag(cfg) {
  return `<script type="application/ld+json">${JSON.stringify(prune(buildJsonLd(cfg)))}</script>`;
}

/**
 * Render the full `<head>` SEO fragment as an HTML string. Description and image
 * fall back through page → site. Build-time-injectable; empty-valued tags drop.
 */
export function renderHead(cfg) {
  const desc = cfg.description || cfg.siteDescription;
  const image = cfg.image || cfg.siteImage;
  const handle = cfg.twitterUser ? `@${esc(cfg.twitterUser)}` : "";
  const titled = cfg.siteName ? `${esc(cfg.title)} | ${esc(cfg.siteName)}` : esc(cfg.title);

  const tags = [
    `<title>${titled}</title>`,
    `<meta name="viewport" content="width=device-width, initial-scale=1.0">`,
    metaName("description", desc),
    metaName("author", cfg.author?.name),
    metaName("keywords", cfg.keywords),
    `<meta name="robots" content="index, follow">`,
    cfg.url ? `<link rel="canonical" href="${esc(cfg.url)}">` : "",
    metaProp("og:title", cfg.title),
    metaProp("og:description", desc),
    metaProp("og:url", cfg.url),
    metaProp("og:site_name", cfg.siteName),
    metaProp("og:type", isArticle(cfg) ? "article" : "website"),
    metaProp("og:locale", cfg.locale || "en_US"),
    metaProp("og:image", image),
    metaName("twitter:card", cfg.twitterCard || "summary"),
    metaName("twitter:site", handle),
    metaName("twitter:creator", handle),
    metaName("twitter:title", cfg.title),
    metaName("twitter:description", desc),
    metaName("twitter:image", image),
    jsonLdTag(cfg),
  ];
  return tags.filter(Boolean).join("\n") + "\n";
}
