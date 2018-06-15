# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class CheckoutChecklist(models.TransientModel):
    """ The summary line for a class docstring should fit on one line.

    """

    _name = 'checkout.checklist'
    _description = u'Checkout Checklist'

    period_id = fields.Many2one('finance.period', u'结账会计期间', domain="[('is_closed','=',False)]", required=True)
    company_id = fields.Many2one(
        'res.company',
        string=u'公司',
        change_default=True,
        default=lambda self: self.env['res.company']._company_default_get())

    check_voucher_depreciation = fields.Boolean(string=u'计提折旧', readonly=True)
    check_voucher_exchange = fields.Boolean(string=u'期末调汇', readonly=True)
    check_voucher_profit = fields.Boolean(string=u'收支结转', readonly=True)
    check_trial_balance = fields.Boolean(string=u'试算平衡', readonly=True)
    check_balance_sheet = fields.Boolean(string=u'资产负债表', readonly=True)
    check_account_cash = fields.Boolean(string=u'现金', readonly=True)
    check_account_bank = fields.Boolean(string=u'银行存款', readonly=True)
    check_account_good = fields.Boolean(string=u'存货', readonly=True)
    check_account_fixed_asset = fields.Boolean(string=u'固定资产', readonly=True)
    check_account_intangible_asset = fields.Boolean(string=u'无形资产', readonly=True)

    msg_voucher_depreciation = fields.Selection(
        string=u'计提折旧', selection=[('ok', u'正常'), ('error', u'未结转')], default='ok', readonly=True)
    msg_voucher_exchange = fields.Selection(
        string=u'期末调汇', selection=[('ok', u'正常'), ('error', u'未结转')], default='ok', readonly=True)
    msg_voucher_profit = fields.Selection(
        string=u'收支结转', selection=[('ok', u'正常'), ('error', u'未结转')], default='ok', readonly=True)
    msg_trial_balance = fields.Selection(
        string=u'试算平衡', selection=[('ok', u'正常'), ('error', u'不平衡')], default='ok', readonly=True)
    msg_balance_sheet = fields.Selection(
        string=u'资产负债表', selection=[('ok', u'正常'), ('error', u'不平衡')], default='ok', readonly=True)
    msg_account_cash = fields.Selection(
        string=u'现金', selection=[('ok', u'正常'), ('error', u'有赤字')], default='ok', readonly=True)
    msg_account_bank = fields.Selection(
        string=u'银行存款', selection=[('ok', u'正常'), ('error', u'有赤字')], default='ok', readonly=True)
    msg_account_good = fields.Selection(
        string=u'存货', selection=[('ok', u'正常'), ('error', u'存货 –  存货跌价准备 < 0')], default='ok', readonly=True)
    msg_account_fixed_asset = fields.Selection(
        string=u'固定资产', selection=[('ok', u'正常'), ('error', u'固定资产 – 累计折旧 < 0')], default='ok', readonly=True)
    msg_account_intangible_asset = fields.Selection(
        string=u'无形资产', selection=[('ok', u'正常'), ('error', u'有赤字')], default='ok', readonly=True)

    result = fields.Selection(
        string=u'结果', selection=[('ok', u'检查通过，可以结账'), ('error', u'检查未通过，请核实后再结账')], compute='_compute_result')

    @api.depends('check_voucher_depreciation', 'check_voucher_exchange', 'check_voucher_profit', 'check_trial_balance',
                 'check_balance_sheet', 'check_account_cash', 'check_account_bank', 'check_account_good',
                 'check_account_fixed_asset', 'check_account_intangible_asset')
    def _compute_result(self):
        for record in self:
            ok = record.check_voucher_depreciation and record.check_voucher_exchange and record.check_voucher_profit and record.check_trial_balance and record.check_balance_sheet and record.check_account_cash and record.check_account_bank and record.check_account_good and record.check_account_fixed_asset and record.check_account_intangible_asset

            if ok:
                record.result = 'ok'
            else:
                record.result = 'error'

    @api.model
    def default_get(self, fields):
        res = super(CheckoutChecklist, self).default_get(fields)

        check_voucher_depreciation = False
        check_voucher_exchange = False
        check_voucher_profit = False
        check_trial_balance = False
        check_balance_sheet = False
        check_account_cash = False
        check_account_bank = False
        check_account_good = False
        check_account_fixed_asset = False
        check_account_intangible_asset = False

        res.update({
            'check_voucher_depreciation': check_voucher_depreciation,
            'check_voucher_exchange': check_voucher_exchange,
            'check_voucher_profit': check_voucher_profit,
            'check_trial_balance': check_trial_balance,
            'check_balance_sheet': check_balance_sheet,
            'check_account_cash': check_account_cash,
            'check_account_bank': check_account_bank,
            'check_account_good': check_account_good,
            'check_account_fixed_asset': check_account_fixed_asset,
            'check_account_intangible_asset': check_account_intangible_asset,
            'msg_voucher_depreciation': 'error' if not check_voucher_depreciation else 'ok',
            'msg_voucher_exchange': 'error' if not check_voucher_exchange else 'ok',
            'msg_voucher_profit': 'error' if not check_voucher_profit else 'ok',
            'msg_trial_balance': 'error' if not check_trial_balance else 'ok',
            'msg_balance_sheet': 'error' if not check_balance_sheet else 'ok',
            'msg_account_cash': 'error' if not check_account_cash else 'ok',
            'msg_account_bank': 'error' if not check_account_bank else 'ok',
            'msg_account_good': 'error' if not check_account_good else 'ok',
            'msg_account_fixed_asset': 'error' if not check_account_fixed_asset else 'ok',
            'msg_account_intangible_asset': 'error' if not check_account_intangible_asset else 'ok',
        })

        return res

    @api.onchange('check_voucher_depreciation')
    def _onchange_check_voucher_depreciation(self):
        if not self.check_voucher_depreciation:
            self.msg_voucher_depreciation = 'error'
        else:
            self.msg_voucher_depreciation = 'ok'

    @api.onchange('check_voucher_exchange')
    def _onchange_check_voucher_exchange(self):
        if not self.check_voucher_exchange:
            self.msg_voucher_exchange = 'error'
        else:
            self.msg_voucher_exchange = 'ok'

    @api.onchange('check_voucher_profit')
    def _onchange_check_voucher_profit(self):
        if not self.check_voucher_profit:
            self.msg_voucher_profit = 'error'
        else:
            self.msg_voucher_profit = 'ok'

    @api.onchange('check_trial_balance')
    def _onchange_check_trial_balance(self):
        if not self.check_trial_balance:
            self.msg_trial_balance = 'error'
        else:
            self.msg_trial_balance = 'ok'

    @api.onchange('check_balance_sheet')
    def _onchange_check_balance_sheet(self):
        if not self.check_balance_sheet:
            self.msg_balance_sheet = 'error'
        else:
            self.msg_balance_sheet = 'ok'

    @api.onchange('check_account_cash')
    def _onchange_check_account_cash(self):
        if not self.check_account_cash:
            self.msg_account_cash = 'error'
        else:
            self.msg_account_cash = 'ok'

    @api.onchange('check_account_bank')
    def _onchange_check_account_bank(self):
        if not self.check_account_bank:
            self.msg_account_bank = 'error'
        else:
            self.msg_account_bank = 'ok'

    @api.onchange('check_account_good')
    def _onchange_check_account_good(self):
        if not self.check_account_good:
            self.msg_account_good = 'error'
        else:
            self.msg_account_good = 'ok'

    @api.onchange('check_account_fixed_asset')
    def _onchange_check_account_fixed_asset(self):
        if not self.check_account_fixed_asset:
            self.msg_account_fixed_asset = 'error'
        else:
            self.msg_account_fixed_asset = 'ok'

    @api.onchange('check_account_intangible_asset')
    def _onchange_check_account_intangible_asset(self):
        if not self.check_account_intangible_asset:
            self.msg_account_intangible_asset = 'error'
        else:
            self.msg_account_intangible_asset = 'ok'

    @api.onchange('period_id')
    def _onchange_peroid_id(self):
        def set_value(self):
            self.check_voucher_depreciation = self._check_voucher_depreciation()
            self.check_voucher_exchange = self._check_voucher_exchange()
            self.check_voucher_profit = self._check_voucher_profit()
            self.check_trial_balance = self._check_trial_balance()
            self.check_balance_sheet = self._check_balance_sheet()
            self.check_account_cash = self._check_account('1001')
            self.check_account_bank = self._check_account('1002')
            self.check_account_good = self._check_account_good()
            self.check_account_fixed_asset = self._check_account_fixed_asset()
            self.check_account_intangible_asset = self._check_account_intangible_asset()

        if self.period_id:
            trial_balance_items = self.env['trial.balance'].search([('period_id', '=', self.period_id.id)])
            account_ids = self.env['finance.account'].search([])
            if len(trial_balance_items) != len(account_ids):
                period_id = self.period_id
                self.period_id = False
                set_value(self)
                return {
                    'warning': {
                        'title': u'错误',
                        'message': u'期间%s，没有运行科目余额表，请至菜单 账簿 > 科目余额表，查看科目余额表！' % period_id.name
                    }
                }

        set_value(self)

    @api.multi
    def _check_voucher_depreciation(self):
        self.ensure_one()
        if not self.period_id:
            return False

        fixed_assets = self.env['asset'].search([
            ('no_depreciation', '=', False),  # 提折旧的
            ('state', '=', 'done'),  # 已确认
            ('period_id', '!=', self.period_id.id)
        ])

        depreciations = self.env['asset.line'].search([('period_id', '!=', self.period_id.id)])

        if len(depreciations) != len(fixed_assets):
            return False

        depreciation_voucher = self.env['voucher.line'].search([('period_id', '=', self.period_id.id), ('name', '=',
                                                                                                        u'固定资产折旧')])
        if 'draft' in depreciation_voucher.mapped('state'):
            return False

        return True

    @api.multi
    def _check_voucher_exchange(self):
        self.ensure_one()
        if not self.period_id:
            return False
        need_create_exchange_voucher = False
        if self.env['finance.account'].search([('currency_id', '!=', self.env.user.company_id.currency_id.id),
                                               ('currency_id', '!=', False), ('exchange', '=', True)]):
            need_create_exchange_voucher = True

        vouch_obj = self.env['voucher'].search(
            [('is_exchange', '=', True), ('period_id', '=', self.period_id.id)], order="create_date desc", limit=1)
        if need_create_exchange_voucher and not vouch_obj:
            return False

        return True

    @api.multi
    def _check_voucher_profit(self):
        self.ensure_one()
        if not self.period_id:
            return False

        voucher = self.env['voucher'].search(
            [('is_checkout', '=', True), ('period_id', '=', self.period_id.id)], order="create_date desc", limit=1)

        if not voucher:
            return False

        return True

    @api.multi
    def _check_trial_balance(self):
        self.ensure_one()
        if not self.period_id:
            return False
        trial_balance_items = self.env['trial.balance'].search([('period_id', '=', self.period_id.id)])
        active_id = False
        if trial_balance_items:
            active_id = trial_balance_items.ids[0]
        else:
            return False

        if active_id:
            check_wizard_model = self.env['check.trial.balance.wizard'].with_context(active_id=active_id)
            default_values = check_wizard_model.default_get(['is_balance'])
            if not default_values['is_balance']:
                return False
            else:
                return True
        else:
            return False

        return True

    @api.multi
    def _check_balance_sheet(self):
        self.ensure_one()
        if not self.period_id:
            return False

        # create_balance_sheet_wizard = self.env['create.balance.sheet.wizard'].create({ 'period_id': self.period_id.id
        #     })
        # create_balance_sheet_wizard.create_balance_sheet()
        balance_sheet_lines = self.env['balance.sheet'].search([])
        last_line = balance_sheet_lines[-1]
        if (datetime.utcnow() -
                datetime.strptime(last_line.write_date, DEFAULT_SERVER_DATETIME_FORMAT)).seconds > 8 * 3600:
            raise UserError(u'资产负债表是8小时前更新，太旧了，请至 菜单 账簿 > 资产负债表 更新资产负债表！')

        if last_line.ending_balance != last_line.ending_balance_two:
            return False

        return True

    @api.multi
    def _check_account(self, account_code):
        self.ensure_one()
        if not self.period_id:
            return False

        account_id = self.env['finance.account'].search([('code', '=', account_code)])
        child_account_ids = self.env['finance.account'].search([('id', 'child_of', account_id.id)])
        for child_account_id in child_account_ids:
            trial_balance_item = self.env['trial.balance'].search([('subject_name_id', '=', child_account_id.id),
                                                                   ('period_id', '=', self.period_id.id)])
            if trial_balance_item.ending_balance_credit < 0:
                return False

        return True

    @api.multi
    def _check_account_good(self):
        self.ensure_one()
        if not self.period_id:
            return False

        account_id = self.env['finance.account'].search([('code', '=', '1201')])
        trial_balance_item = self.env['trial.balance'].search([('subject_name_id', '=', account_id.id),
                                                               ('period_id', '=', self.period_id.id)])
        counterpart_account_id = self.env['finance.account'].search([('code', '=', '1202')])
        counterpart_trial_balance_item = self.env['trial.balance'].search(
            [('subject_name_id', '=', counterpart_account_id.id), ('period_id', '=', self.period_id.id)])

        if trial_balance_item.ending_balance_debit - counterpart_trial_balance_item.ending_balance_credit < 0:
            return False

        return True

    @api.multi
    def _check_account_fixed_asset(self):
        self.ensure_one()
        if not self.period_id:
            return False

        account_id = self.env['finance.account'].search([('code', '=', '1501')])
        trial_balance_item = self.env['trial.balance'].search([('subject_name_id', '=', account_id.id),
                                                               ('period_id', '=', self.period_id.id)])
        counterpart_account_id = self.env['finance.account'].search([('code', '=', '1502')])
        counterpart_trial_balance_item = self.env['trial.balance'].search(
            [('subject_name_id', '=', counterpart_account_id.id), ('period_id', '=', self.period_id.id)])

        if trial_balance_item.ending_balance_debit - counterpart_trial_balance_item.ending_balance_credit < 0:
            return False

        return True

    @api.multi
    def _check_account_intangible_asset(self):
        self.ensure_one()
        if not self.period_id:
            return False

        account_id = self.env['finance.account'].search([('code', '=', '1601')])
        child_account_ids = self.env['finance.account'].search([('id', 'child_of', account_id.id)])
        for child_account_id in child_account_ids:
            trial_balance_item = self.env['trial.balance'].search([('subject_name_id', '=', child_account_id.id),
                                                                   ('period_id', '=', self.period_id.id)])
            if trial_balance_item.ending_balance_credit < 0:
                return False

        return True

    @api.multi
    def close_period(self):
        self.ensure_one()

        self.period_id.is_closed = True
