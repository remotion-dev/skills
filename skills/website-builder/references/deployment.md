# Deployment — GitHub + Vercel

Ship flow for any static or Next.js site Graeham builds. Source lives in GitHub, hosting is Vercel, domain is attached in Vercel's dashboard.

## One-time Vercel setup (user-owned, skip if done)

Graeham needs to do this once per account. These steps require account creation and permission grants — do not automate them.

1. Sign in at vercel.com with GitHub.
2. Authorize Vercel to read GitHub repos.
3. Custom domain: add DNS records from Vercel's "Domains" panel to wherever Graeham's DNS lives (GoDaddy, Cloudflare, etc.).

## Repo creation

Create a fresh repo for each site. Reuse existing repos only when updating an existing project.

```bash
PAT=$(cat outputs/.claude-credentials/github-pat.txt)
REPO_NAME="site-name-here"
# Create the repo via GitHub's API:
curl -s -X POST -H "Authorization: token $PAT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"private\":true,\"auto_init\":false}" | jq -r '.ssh_url, .clone_url'
```

If `api.github.com` is blocked in the sandbox, fall back to pushing to an existing repo or have the user create the repo manually.

## Local scaffold

For static sites (most of Graeham's builds), no build step needed. Vercel serves HTML/CSS/JS directly.

```
site-name/
├── index.html
├── assets/
│   ├── images/
│   └── fonts/
├── styles/           (optional if CSS inlined)
├── scripts/          (optional if JS inlined)
├── vercel.json       (optional routing/redirects)
└── README.md
```

Minimal `vercel.json` for a static site with clean URLs:

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    { "source": "/(.*)", "headers": [
      { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
      { "key": "X-Content-Type-Options", "value": "nosniff" }
    ]}
  ]
}
```

For Next.js sites (PropIQ/PropertyOS), the default scaffold ships with `next.config.js` — no extra `vercel.json` needed.

## First push

```bash
cd /tmp/site-name
git init
git add .
git commit -m "Initial scaffold"
git branch -M main
git remote add origin https://${PAT}@github.com/Graehamwatts/${REPO_NAME}.git
git push -u origin main
```

Never commit the PAT itself into the repo. The PAT in the remote URL is only in your local `.git/config`, not in the pushed history.

## Vercel import

After the first push, the user imports the repo into Vercel:

1. Vercel dashboard → Add New → Project → Select the GitHub repo.
2. For static sites: framework preset = "Other", root directory = `./`, no build command. Output directory = `./`.
3. For Next.js: framework auto-detected. Leave defaults.
4. Click Deploy.

Vercel will auto-deploy on every push to `main` from this point.

## Preview deploys

Every PR gets an auto-generated preview URL. Use this for client review before merging.

```bash
git checkout -b feat/new-hero
# edit files
git commit -am "New hero variant"
git push origin feat/new-hero
# Open a PR on GitHub — Vercel will post the preview URL as a comment.
```

## Custom domain

Graeham configures this in Vercel's domain panel. DNS records typically:
- A record for apex: `76.76.21.21`
- CNAME for `www`: `cname.vercel-dns.com`

Vercel will show exact records after adding the domain.

## SSL / HTTPS

Vercel provisions SSL automatically via Let's Encrypt. Nothing to configure. HTTPS is enforced by default.

## Environment variables

Any secrets (API keys, database URLs) go in Vercel's Environment Variables panel, not in the repo. Reference in code via `process.env.VAR_NAME`.

For static sites, avoid env vars entirely — they'll be exposed in the built HTML.

## Analytics

Vercel has built-in analytics on the paid tier. Free alternative: add Plausible or Umami via a single script tag in `<head>`.

Do not use Google Analytics as the default. GDPR cookie banner requirements will kneecap the page's polish.

## Rollback

Every deploy is preserved. To roll back:

1. Vercel dashboard → Project → Deployments.
2. Find a previous deploy → click "Promote to Production".

Roll back in the dashboard, not via `git revert`, when the issue is urgent.

## Build-free vs Next.js tradeoff

Most of Graeham's sites should be single-file HTML or a small static folder. Reasons to upgrade to Next.js:

- Dynamic routes based on data (listing pages from an MLS feed, blog posts from markdown).
- API routes (lead capture, form submissions).
- Team contributors who want React components.

If none of those apply, stay on static HTML. Faster to iterate, faster to deploy, less to maintain.

## Checklist before shipping to production

- `<title>` and `<meta description>` filled and specific.
- Open Graph meta tags for social sharing (`og:title`, `og:description`, `og:image`).
- Favicon present (ICO or PNG, at least 32x32).
- All `<a>` tags point somewhere real (no `#` placeholders).
- Form submissions wired to an actual endpoint (Formspree, Netlify Forms, a custom API route).
- Mobile layout verified at 375px width.
- Lighthouse score checked (accessibility ≥ 90, performance ≥ 80).
- Legal footer present if the site collects data (privacy policy link).
