# QuickRed Tech Differentiator Website

This folder contains the React marketing site for the desktop differentiation app.

## Quick link

- Quick Red Tech organization: `https://github.com/Quick-Red-Tech`

## Commands

```bash
npm install
npm run dev
npm run build
```

## SEO files

- `public/robots.txt`
- `public/sitemap.xml`

## Deployment note

The SEO files are generated via `npm run generate:seo` (runs automatically on `npm run build`).
If you deploy under a different hostname, set `SITE_URL` before building so the generated URLs match your domain.

The landing page itself links users to the Quick Red Tech organization on GitHub for the Windows `.exe` and macOS `.dmg` release path.
