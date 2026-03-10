import { writeFileSync } from "node:fs";
import path from "node:path";

function normalizeSiteUrl(value) {
  const trimmed = (value ?? "").trim();
  if (!trimmed) return null;

  const withoutTrailingSlash = trimmed.replace(/\/+$/, "");
  if (!/^https?:\/\//i.test(withoutTrailingSlash)) {
    throw new Error(`SITE_URL must include protocol (got: ${value})`);
  }

  return withoutTrailingSlash;
}

const siteUrl =
  normalizeSiteUrl(process.env.SITE_URL) ??
  normalizeSiteUrl(process.env.VITE_SITE_URL) ??
  "https://differentiation-algorithms-research.vercel.app";

const lastmod = new Date().toISOString().slice(0, 10);

const urls = [
  {
    loc: `${siteUrl}/`,
    lastmod,
    changefreq: "daily",
    priority: "1.0",
  },
];

const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(
    (url) => `  <url>
    <loc>${url.loc}</loc>
    <lastmod>${url.lastmod}</lastmod>
    <changefreq>${url.changefreq}</changefreq>
    <priority>${url.priority}</priority>
  </url>`
  )
  .join("\n")}
</urlset>
`;

const robotsTxt = `User-agent: *
Allow: /

# Block non-content endpoints.
Disallow: /api/
Disallow: /_vercel/

Sitemap: ${siteUrl}/sitemap.xml
`;

const publicDir = path.join(process.cwd(), "public");
writeFileSync(path.join(publicDir, "sitemap.xml"), sitemapXml, "utf8");
writeFileSync(path.join(publicDir, "robots.txt"), robotsTxt, "utf8");
