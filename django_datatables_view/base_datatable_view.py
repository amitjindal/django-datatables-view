# -*- coding: utf-8 -*-
import re

from .mixins import JSONResponseView


class DatatableMixin(object):
    """ JSON data for datatables
    """
    model = None
    columns = []
    order_columns = []
    max_display_length = 100  # max limit of records returned, do not allow to kill our server by huge sets of data

    def initialize(*args, **kwargs):
        pass

    def get_order_columns(self):
        """ Return list of columns used for ordering
        """
        return self.order_columns

    def get_columns(self):
        """ Returns the list of columns that are returned in the result set
        """
        return self.columns

    def render_column(self, row, column):
        """ Renders a column on a row
        """
        if hasattr(row, 'get_%s_display' % column):
            # It's a choice field
            text = getattr(row, 'get_%s_display' % column)()
        else:
            try:
                text = getattr(row, column)
            except AttributeError:
                obj = row
                for part in column.split('.'):
                    if obj is None:
                        break
                    obj = getattr(obj, part)

                text = obj

        if hasattr(row, 'get_absolute_url'):
            return '<a href="%s">%s</a>' % (row.get_absolute_url(), text)
        else:
            return text

    def ordering(self, qs):
        """ Get parameters from the request and prepare order by clause
        """
        request = self.request
        pre_camel_case_notation = True

        if not request.POST.get('iSortingCols'):
            pre_camel_case_notation = False

        # Number of columns that are used in sorting
        try:
            if pre_camel_case_notation:
                sorting_cols = int(request.REQUEST.get('iSortingCols', 0))
            else:
                sorting_cols = len([(key, value) for key, value in self.request.POST.iteritems() if re.search(r'order.\d+..column.', key)])
        except ValueError:
            sorting_cols = 0

        order = []
        order_columns = self.get_order_columns()

        for i in range(sorting_cols):
            # sorting column
            try:
                if pre_camel_case_notation:
                    sort_col = int(request.REQUEST.get('iSortCol_%s' % i))
                    # sorting order
                    sort_dir = request.REQUEST.get('sSortDir_%s' % i)
                else:
                    sort_col = int(request.REQUEST.get('order[%s][column]' % i))
                    # sorting order
                    sort_dir = request.REQUEST.get('order[%s][dir]' % i)
            except ValueError:
                sort_col = 0

            sdir = '-' if sort_dir == 'desc' else ''
            sortcol = order_columns[sort_col]

            if isinstance(sortcol, list):
                for sc in sortcol:
                    order.append('%s%s' % (sdir, sc.replace('.', '__')))
            else:
                order.append('%s%s' % (sdir, sortcol.replace('.', '__')))
        if order:
            return qs.order_by(*order)
        return qs

    def paging(self, qs):
        """ Paging
        """
        request = self.request
        pre_camel_case_notation = True

        if not request.POST.get('iSortingCols'):
            pre_camel_case_notation = False

        if pre_camel_case_notation:
            limit = min(int(self.request.REQUEST.get('iDisplayLength', 10)), self.max_display_length)
            start = int(self.request.REQUEST.get('iDisplayStart', 0))
        else:
            limit = min(int(self.request.REQUEST.get('length', 10)), self.max_display_length)
            start = int(self.request.REQUEST.get('start', 0))
        
        # if pagination is disabled ("paging": false)
        if limit == -1:
            return qs

        offset = start + limit
        
        return qs[start:offset]

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError("Need to provide a model or implement get_initial_queryset!")
        return self.model.objects.all()

    def filter_queryset(self, qs):
        return qs

    def prepare_results(self, qs):
        data = []
        for item in qs:
            data.append([self.render_column(item, column) for column in self.get_columns()])
        return data

    def get_context_data(self, *args, **kwargs):
        request = self.request
        pre_camel_case_notation = True
        self.initialize(*args, **kwargs)

        if not request.POST.get('iSortingCols'):
            pre_camel_case_notation = False

        qs = self.get_initial_queryset()

        # number of records before filtering
        total_records = qs.count()

        qs = self.filter_queryset(qs)

        # number of records after filtering
        total_display_records = qs.count()

        qs = self.ordering(qs)
        qs = self.paging(qs)

        # prepare output data
        if pre_camel_case_notation:
            aaData = self.prepare_results(qs)

            ret = {'sEcho': int(request.REQUEST.get('sEcho', 0)),
                   'iTotalRecords': total_records,
                   'iTotalDisplayRecords': total_display_records,
                   'aaData': aaData
            }
        else:
            aaData = self.prepare_results(qs)

            ret = {'draw': int(request.REQUEST.get('draw', 0)),
                   'iTotalRecords': total_records,
                   'iTotalDisplayRecords': total_display_records,
                   'data': aaData
            }

        return ret


class BaseDatatableView(DatatableMixin, JSONResponseView):
    pass