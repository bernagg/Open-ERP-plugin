# -*- coding: utf-8 -*-

from osv import osv, fields


class academy_classroom(osv.osv):
    """Classroom defined for the current academy"""
    _name = 'academy.classroom'
    _columns = {
        'name': fields.char('Course', size=32, required=True, help='This is the name of the classroom'),
        'address_id': fields.many2one('res.partner.address', 'Address'),
        'phone': fields.related('adress_id', 'phone', type='char', size=64, string='Phone', store=False, readonly=True),
        'street': fields.related('adress_id', 'street', type='char', size=30, string='Street', store=False, readonly=True),
        'city': fields.related('adress_id', 'city', type='char', size=15, string='City', store=False, readonly=True),
        'capacity': fields.integer('Capacity'),
        'state': fields.selection([('usable', 'Usable'), ('under_construction', 'Under Construction')], 'State'),
        'course_id': fields.one2many('academy.course', 'classroom_id', 'Courses'),
    }

    _defaults = {
        'state': 'usable',
        'capacity': 10,
        }

    def _check_capacity(self, cr, uid, ids):
        for classroom in self.browse(cr, uid, ids):
            if classroom.capacity and (classroom.capacity < 10 or classroom.capacity > 100):
                return False
        return True

    _constraints = [(_check_capacity, 'The capacity is not between 10 and 100', ['capacity'])]
academy_classroom()


class academy_courses(osv.osv):
    """Courses defined for the current academy"""

    def _code_name(self, cr, uid, ids, field_name, arg, context):
        result = {}
        for r in self.browse(cr, uid, ids, context=context):
            result[r.id] = str(r.course_code) + ' ' + r.name
        return result

    def _check_code(self, cr, uid, ids):
        for course in self.browse(cr, uid, ids):
            if len(self.search(cr, uid, [('course_code', 'ilike', course.course_code)])) > 1:
            	return False
        return True

    _name = 'academy.course'
    _columns = {
        'course_code': fields.char('Code', required=True, size=32),
        'name': fields.char('Course', size=32, required=True, help='This is the name of the course'),
        'difficulty': fields.selection([('easy', 'Easy'), ('intermediate', 'Intermediate'), ('insane', 'Insane')], 'Difficulty'),
        'hours': fields.integer('Hours'),
        'description': fields.text('Description'),
        'state': fields.selection([('draft', 'Draft'), ('testing', 'Testing'), ('stable', 'Stable')], 'State'),
        'classroom_id': fields.many2one('academy.classroom', 'Classroom', required=True),
        'category_id': fields.many2one('academy.category', 'Category', required=True),
        'code_name': fields.function(_code_name, type='char', size=96, readonly='True', string='Code name'),
        }
    _defaults = {
        'difficulty': 'easy',
        'state': 'draft',
        }

    def _check_name(self, cr, uid, ids):
        for courses in self.browse(cr, uid, ids):
            if courses.name and len(courses.name) < 10:
                return False
        return True

    def _check_hours(self, cr, uid, ids):
        for course in self.browse(cr, uid, ids):
            if course and (course.hours < 5 or course.hours > 200):
                return False
        return True

    def onchange_name(self, cr, uid, ids, name, description):
        if not description and name:
            return {'value': {'description': name}}
        return {'value': {}}

    _constraints = [
        (_check_name, 'The name has at least 10 characters', ['name']),
        (_check_hours, 'The hours are not between 5 and 200', ['hours']),
        ]
academy_courses()


class academy_category(osv.osv):
    """Courses defined for the current school"""
    _name = 'academy.category'
    _columns = {
        'name': fields.char('Category', size=32, required=True, help='This is the name of the category'),
        'courses_id': fields.one2many('academy.course', 'category_id', 'Courses'),
        }

    def _check_name(self, cr, uid, ids):
        for category in self.browse(cr, uid, ids):
            if category.name and len(category.name) < 3:
                return False
        return True

    _constraints = [(_check_name, 'The name has at least 3 characters', ['name'])]
academy_category()