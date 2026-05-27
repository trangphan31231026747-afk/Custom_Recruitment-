from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment


class WebsiteJobApplicationBlacklist(WebsiteHrRecruitment):

    def _get_post_value(self, post, *keys):
        for key in keys:
            value = post.get(key)
            if value:
                return str(value).strip()
        return False

    def _find_active_blacklist_record(self, post):
        email = self._get_post_value(post, "email", "email_from", "partner_email")
        phone = self._get_post_value(post, "phone", "partner_phone")
        mobile = self._get_post_value(post, "mobile", "partner_mobile")

        match_domains = []

        if email:
            match_domains.append([("email", "=ilike", email)])

        if phone:
            match_domains.append([("phone", "=", phone)])
            match_domains.append([("mobile", "=", phone)])

        if mobile:
            match_domains.append([("phone", "=", mobile)])
            match_domains.append([("mobile", "=", mobile)])

        if not match_domains:
            return False

        domain = expression.AND([
            [("state", "=", "active")],
            expression.OR(match_domains),
        ])

        return request.env["recruitment.candidate.blacklist"].sudo().search(domain, limit=1)

    @http.route()
    def jobs_apply(self, job, **post):
        if request.httprequest.method == "POST":
            blacklist_record = self._find_active_blacklist_record(post)

            if blacklist_record:
                return request.render("candidate_blacklist.job_application_error_blacklist", {})

        return super().jobs_apply(job, **post)