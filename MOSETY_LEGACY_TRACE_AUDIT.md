# MOSETY LEGACY TRACE AUDIT (P010 / AG002)

**Audit Date**: 28 September 2026  
**Scope**: All tracked files, templates, migrations, media filenames, database tables, and rendered outputs for Mosety Boat Rides Naivasha.  
**Release Gate Requirement**: "NO UNVERIFIED FACTS. NO UNINTENDED LEGACY TRACE."

---

## 1. Source Code & Template Matches

| File Path | Match Content | Category | Required Disposition |
| :--- | :--- | :--- | :--- |
| `templates/blog/post_detail.html:4` | `{% block meta_title %}{{ post.title }} \| Legacy Boat Rides Journal{% endblock %}` | Page Title | **REPLACE** with `Mosety Boat Rides Field Journal` |
| `templates/blog/post_detail.html:15` | `...by Legacy Boat Rides.` | Meta Description | **REPLACE** with `...by Mosety Boat Rides.` |
| `templates/blog/post_detail.html:59, 126` | `"name": "Legacy Boat Rides Naivasha"` | Schema Publisher | **REPLACE** with `"name": "{{ site.business_name }}"` |
| `templates/blog/post_detail.html:60, 127` | `"url": "{{ site.base_url }}{% static 'images/legacy-logo.jpeg' %}"` | Schema Logo | **REPLACE** with dynamic `site.logo.url` fallback |
| `templates/bookings/tour_detail.html:208` | `<h2 ...>More Legacy Boat Rides Tours</h2>` | Section Heading | **REPLACE** with `More Mosety Boat Rides` |
| `templates/bookings/tour_detail.html:236` | `"name": "Legacy Boat Rides Naivasha"` | Schema Provider | **REPLACE** with `"name": "{{ site.business_name }}"` |
| `templates/bookings/tour_list.html:4` | `{% block meta_title %}Lake Naivasha Boat Rides & Tours \| Legacy Boat Rides{% endblock %}` | Page Title | **REPLACE** with `Mosety Boat Rides Naivasha` |
| `templates/dashboard/dashboard.html:4` | `{% block meta_title %}Business Dashboard \| Legacy Boat Rides{% endblock %}` | Page Title | **REPLACE** with `Mosety Boat Rides Dashboard` |
| `templates/jobs/job_list.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/loyalty/signup.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/reputation/dashboard.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/reputation/leaderboard.html:4, 18` | `...make Legacy Boat Rides the top-rated...` | Page Title / Copy | **REPLACE** with `Mosety Boat Rides` |
| `templates/reputation/profile.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/reputation/rate.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/reputation/success.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/seo/detail.html:4` | `{% block meta_title %}{{ page.effective_seo_title }} \| Legacy Boat Rides{% endblock %}` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/seo/detail.html:164, 175` | `"name": "Legacy Boat Rides Naivasha"`, `legacy-logo.jpeg` | Schema Publisher | **REPLACE** with dynamic `site.business_name` & logo |
| `templates/seo/list.html:4` | `... \| Legacy Boat Rides` | Page Title | **REPLACE** with `Mosety Boat Rides` |
| `templates/services/service_detail.html:4` | `... \| Legacy Boat Rides Naivasha` | Page Title | **REPLACE** with `Mosety Boat Rides Naivasha` |
| `templates/services/service_list.html:4, 7` | `...offered by Legacy Boat Rides...` | Meta / Heading | **REPLACE** with `Mosety Boat Rides` |
| `templates/testimonials/testimonial_list.html:4, 7` | `...with Legacy Boat Rides.` | Meta / Heading | **REPLACE** with `Mosety Boat Rides` |
| `utils.py:10, 11` | `# phrase such as "Legacy Boat Rides"...` | Code Comments | **REMOVE** or neutralize comment |

---

## 2. Database Record Matches

| Model | Record Count with Match | Field Names Affected | Required Action |
| :--- | :--- | :--- | :--- |
| `Tour` | 5 | `description`, `short_description`, `meta_description` | **UPDATE**: Replace with Mosety brand copy via management script |
| `FAQ` | 208 | `question`, `answer` | **UPDATE**: Programmatic replacement of brand tokens |
| `FAQItem` | 153 | `question`, `answer` | **UPDATE**: Programmatic replacement of brand tokens |
| `LocalPage` | 996 | `title`, `meta_description`, `content` | **UPDATE**: Programmatic replacement of brand tokens |
| `Post` | 66 | `title`, `content`, `excerpt`, `meta_description` | **UPDATE**: Programmatic replacement of brand tokens |
| `GuidePage` | 100 | `title`, `content` | **UPDATE**: Programmatic replacement of brand tokens |
| `Testimonial` | 19 | `text`, `reviewer_title` | **AUDIT**: Re-align or purge unverified placeholder testimonials |
| `PartnerHotel` | 2 | `description` | **UPDATE**: Neutralize brand references |
| `InternalLink` | 4 | `anchor_text`, `target_title` | **UPDATE**: Neutralize brand references |
| `User` | 1 (`id=7`, `legacy-editor`) | `username`, `email` | **UPDATE**: Rename to `mosety-editor`, email `editor@mosety.co.ke` |

---

## 3. Media & Static Files

- `static/images/legacy-logo.jpeg`: Verify whether this file exists in filesystem.
- Replace any static template references with `SiteSettings.get_solo().logo` or a brand-neutral SVG placeholder.
- Verify no image filenames contain `legacy`.

---

## 4. Decontamination Verification Strategy

1. Run `python manage.py clean_legacy_traces` management command.
2. Re-run `git grep -i "legacy"` across all code, templates, and scripts (excluding this audit document and migrations history where historical class names exist).
3. Execute database query verifying 0 records match `legacy` in user-facing tables.
4. Add automated test `test_brand_integrity.py` asserting zero `legacy` tokens in any public HTTP response.
