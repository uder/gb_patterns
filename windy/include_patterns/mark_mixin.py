import windy.include_patterns.unit_of_work as unit_of_work


class MarkMixin:
    def mark_new(self):
        unit_of_work.UnitOfWork.get_current().add_new(self)

    def mark_dirty(self):
        unit_of_work.UnitOfWork.get_current().add_dirty(self)

    def mark_remove(self):
        unit_of_work.UnitOfWork.get_current().add_remove(self)
