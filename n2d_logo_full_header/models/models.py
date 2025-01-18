# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_image = fields.Binary(string='Image Logo')


class BaseDocumentLayout(models.TransientModel):
    """
    Customise the company document layout and display a live preview
    """

    _inherit = 'base.document.layout'
    logo_image = fields.Binary(string='Image Logo', related='company_id.logo_image')
