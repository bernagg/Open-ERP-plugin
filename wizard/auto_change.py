# -*- coding: utf-8 -*-

from osv import osv, fields


class auto_change(osv.osv_memory):
    _name = 'academy.auto_change'
    _columns = {
      'info_updates': fields.integer('Number of updated classrooms', readonly=True),
      'classroom_capacity': fields.integer('Capacity of the classroom to search', required=True),
      'new_capacity': fields.integer('New capacity', required=True),
      'state': fields.selection([('init', 'Init'), ('done', 'Done'), ], 'State', readonly=True)
    }

    _defaults = {
    'state': lambda *a: 'init'
    }


def assign_classroom_capacity_capacity(self, cr, uid, ids, data, context=None):
    form = self.browse(cr, uid, ids[0])
    classroom_capacity = form.classroom_capacity
    new_capacity = form.new_capacity
    classroom_obj = self.pool.get('academy.classroom')
    classroom_ids = classroom_obj.search(cr, uid, [('capacity', '=', classroom_capacity)])
    values = {'capacity': new_capacity}
    classroom_obj.write(cr, uid, classroom_ids, values)
    values = {'state': 'done', 'info_updates': len(classroom_ids), }
    self.write(cr, uid, ids, values)
    return True

auto_change()