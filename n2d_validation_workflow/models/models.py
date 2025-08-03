from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Override the entire state field to change the order of states
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('validated', 'Validated'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_validate_quotation(self):
        """Move quotation to validated state"""
        for order in self:
            order.write({'state': 'validated'})
        return True
        
    def action_quotation_send(self):
        """Override to ensure proper state transition flow"""
        self.ensure_one()
        # Check if state is validated before allowing to send
        if self.state == 'draft':
            raise models.UserError('Quotation must be validated before sending.')
        # Call original method from super
        return super(SaleOrder, self).action_quotation_send()


    def write(self, vals):
        # Allow state changes and system fields always
        state_change_only = vals.keys() == {'state'} or (len(vals.keys()) == 2 and set(vals.keys()) == {'state', 'write_date'})
        
        # Also allow changes needed for confirmation process
        confirmation_fields = {'state', 'date_order', 'write_date', 'confirmation_date', 'user_id', 'validity_date', 'commitment_date'}
        is_confirmation = all(field in confirmation_fields for field in vals.keys())
        
        # Check if we can bypass protection
        if state_change_only or is_confirmation:
            return super().write(vals)
            
        # Normal protection for other field changes
        for order in self:
            if order.state != 'draft':
                # No one can edit non-draft quotations (including validated ones)
                raise UserError(_("This quotation cannot be modified because it is not in 'Draft' state. Only quotations in 'Draft' state can be modified."))
        
        return super().write(vals)
        
    def action_confirm(self):
        """Override to allow direct confirmation from validated state"""
        # Create a copy of self to avoid modifying the original recordset during iteration
        orders_to_confirm = self.env['sale.order']
        
        for order in self:
            # Only allow confirming validated quotations
            if order.state != 'validated':
                raise UserError(_("Quotation must be validated before confirmation."))
            orders_to_confirm += order
        
        # If no orders to confirm, return
        if not orders_to_confirm:
            return True
            
        # For each order, directly set state to 'sale' using SQL to bypass restrictions
        for order in orders_to_confirm:
            self.env.cr.execute(
                "UPDATE sale_order SET state = 'sale' WHERE id = %s",
                (order.id,)
            )
        
        # Force reload from database
        self.env.cr.commit()
        
        # Return success message
        return {
            "type": "ir.actions.client", 
            "tag": "reload"
        }

    
    def action_reset_to_draft(self):
        """Reset a validated quotation back to draft state for editing"""
        orders_to_reset = self.env['sale.order']
        
        for order in self:
            if order.state == 'validated':
                orders_to_reset += order
            else:
                raise UserError(_("Only validated quotations can be reset to draft."))
        
        # If no orders to reset, return
        if not orders_to_reset:
            return True
            
        # For each order, directly set state to 'draft' using SQL to bypass restrictions
        for order in orders_to_reset:
            self.env.cr.execute(
                "UPDATE sale_order SET state = 'draft' WHERE id = %s",
                (order.id,)
            )
            
        # Force reload from database
        self.env.cr.commit()
        
        # Return refresh action
        return {
            "type": "ir.actions.client", 
            "tag": "reload"
        }
