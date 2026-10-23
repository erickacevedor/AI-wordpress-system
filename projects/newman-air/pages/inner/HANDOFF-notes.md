# Newman Air: inner pages handoff

**Status (2026-10-23):** 34 pages built and imported on the Windows Local copy `newman-air`
(localhost:10028), all published, none linked from the front page (the splash is still the front
page). Nothing on Flywheel yet.

| Group | Pages (Local IDs) |
|---|---|
| Hubs | Services 42, Service Area 41 |
| Services (`/services/...`) | AC Installation 44, AC Repair 45, Air Cleaners 46, Air Handlers 47, Commercial 49, Cooling 50, Ductless 51, Ductwork 52, Germicidal Lights 54, Heat Pumps 57, Heating Installation 58, Heating Repair 59, Indoor Air Quality 60, Maintenance 64, Thermostats 67 |
| Cities (`/service-area/...`) | Bristol 48, Elizabethton 53, Gray 55, Greeneville 56, Johnson City 61, Jonesborough 62, Kingsport 63 |
| Company | About Us 43, Contact Us 70, Financing 68, Maintenance Plan 69 |
| Utility | Privacy Policy 3 (was WordPress's default draft), Terms and Conditions 66, A2P Submission 71, Sitemap 72, Thank You 73, Confirmed 74 |

Slugs and parents are the old site's, so a path-preserving 301 from callbestinshow.com lands on the
same page. Old `/services/mini-splits/` already redirected to `/services/ductless/` there; no page here.

## Pipeline

```bash
# 1. old pages (public HTML) -> outlines           content/source/md/*.md
#    (content/source/html is gitignored: re-download with curl and a browser User-Agent)
python projects/newman-air/tools/extract-source.py
# 2. outlines -> rebranded content + review list    content/pages/*.json, content/REVIEW.md
python projects/newman-air/tools/make-content.py
# 3. content -> Elementor pages + import manifest   pages/inner/out/*.json, pages/inner/pages.json
python projects/newman-air/pages/inner/build.py
python projects/newman-air/tools/port-css.py && bash projects/newman-air/deploy-plugin.sh
# 4. import (idempotent, by path) and condition header/footer to every _newman_core page
W eval-file projects/newman-air/tools/import-pages.php projects/newman-air/pages/inner/pages.json
W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/_theme/header.json newman-header "<include/singular/page/ID,...>"
W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/_theme/footer.json newman-footer "<same list>"
W elementor flush-css
```

Financing, Maintenance Plan, Contact, A2P, Sitemap, Thank You and Confirmed are written in
`build.py` (from their docs or the old page); the rest come from `content/pages/`.

## What changed from the old pages (all listed in content/REVIEW.md)

- Best in Show -> Newman Air; dog-show idioms (Top-Dog, best-in-show, pure-bred, paws down,
  blue ribbon, first-place, standing ovation, pedigree, medal-worthy) -> neutral wording in
  headlines (Erick, 2026-10-23: no bear in headlines; list them in the ClickUp comment):
  AC Installation H1 "Professional AC Installation in Johnson City, TN" and closing "Ready for
  Better Cooling?"; AC Repair H1 "Professional AC Repair in Johnson City, TN"; Cooling H1
  "Professional AC Services in Johnson City, TN" and closing "Ready for Better Cooling?";
  Ductless closing "Ready for Better Ductless Comfort?"; Indoor Air Quality H2 "See What our
  Customers Say About Our Service"; About H1 "Trusted Comfort Since 1994" and H3 "Your Comfort
  Deserves a Team You Can Trust"; Cooling/Ductless body lead-in "Trusted Comfort Since 1994";
  Thank You/Confirmed teaser; blog "Ductless Mini-Split vs. Central AC" H2 "Finding the Right
  Cooling Option for You". Body text keeps a few bear words where the old copy had dog ones
  (e.g. "bear-strong technicians"). Winner's Circle -> Bear Necessities.
- Public email on Contact, Privacy and Terms: dispatch@newmanair.com (Erick, 2026-10-23; the old
  pages said office@newmanheatandair.com). The Maintenance Plan form still sends to office@ (Alexis's doc).
- Hearth added next to GoodLeap and Synchrony (86bcan2a2); Ruud added where brands are listed (86bcajgzg).
- $75 diagnostic FAQ added to AC Repair, Ductwork and Heating Repair (86bcajgu6), answer from the approved homepage FAQ.
- About: "(formerly Best in Show Heating & Cooling)" in the first paragraph (DJ's plan doc v2, Phase B).
- Contact: the old "Plumbing Repair & Installation Services" heading was a template leftover; now "We Offer a Full Range of HVAC Services".
- Old global blocks dropped and replaced by the V2.1 bands: sidebar menu + form (now hero form + sidebar), Winner's Circle band (now Bear Necessities), reviews shortcodes (live widget still pending, as on the homepage).
- Source bugs fixed: list items split in two (e.g. "Short cycling, where the" / "system turns on...").
- New UI labels (not in any doc): breadcrumb, sidebar "Talk to Our Team" / "Our Services" / "Service Areas", A2P H1 "Text Message Opt-In", form card titles "Lock In Your Coverage" (plan) and "Contact Newman Air Today!" (old Contact h2).

## Open items

- **SEO meta:** stored as Rank Math post meta (`rank_math_title`, `rank_math_description`, `rank_math_robots` noindex on Thank You, Confirmed, A2P). Rank Math is not installed on Local; it applies once it is. Cooling's old title duplicates AC Installation's ("AC Installation in Johnson City, TN"), kept as is.
- **Financing:** Hearth application URL missing in Dani's doc: button goes to `#hearth-link-pending` with a yellow note.
- **Maintenance Plan:** built with the sign-up form (entries to office@newmanheatandair.com, Alexis's comment). Megan never chose form vs call (86bcg1f4b); remove the form card if she picks call only.
- **Form routing** (recipients, SMTP, spam) is Esteban's task (86bcajgud).
- **A2P:** same LeadConnector form embed as the old page; its content (and the Privacy/Terms SMS wording) belongs to Esteban's A2P update.
- **Header/footer** are conditioned page by page; switch to Entire Site at launch only if every page then carries `_newman_core`.
- **Indoor Air Quality** had a reviews embed under "See What our Customers Say..."; dropped like the other review shortcodes.

## Blog (2026-10-23)

12 posts from callbestinshow.com, same slugs, dates and categories (HVAC 4, Uncategorized 8),
URLs `/blog/<slug>/` (permalink structure set to `/blog/%postname%/` on Local, as on the old
site). Index page `/blog/` (page 156, Posts widget; the old site had no index). Theme Builder
single-post template 157 (`pages/blog/build.py`, condition include/singular/post). Header and
footer conditions include all posts.

```bash
python projects/newman-air/tools/make-blog.py        # posts -> content/blog/*.json + content/BLOG-REVIEW.md
python projects/newman-air/pages/blog/build.py       # single-post template
W eval-file projects/newman-air/tools/import-posts.php "<abs path>/projects/newman-air/content" 1
W eval-file projects/newman-air/tools/import-template.php projects/newman-air/pages/blog/single-post.json newman-single-post include/singular/post
```

- Images: featured and inline images live in the Media Library now (22 files; the old Gutenberg
  posts hot-linked bannerbear and a Google "temp_images" URL). Five carried the old brand
  (a "Best In Show / callbestinshow.com" stamp or footer): cropped off; originals kept locally in
  `content/source/blog-img-orig/` (gitignored). One long file name was shortened (Windows path limit).
- Authors: the old authors do not exist on the new install; posts are by user 1.
- WordPress's "Hello world!" (post 1) is excluded from the index; delete it before launch.
- Category archives (`/blog/category/...`) have no Newman template; nothing links to them.
- In Git Bash, run WP-CLI with `MSYS_NO_PATHCONV=1` and a `C:/` PHP path when an argument starts with `/`
  (Git Bash turned `/blog/%postname%/` into `C:/Program Files/Git/blog/...` once; fixed).
