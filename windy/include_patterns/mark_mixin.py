import windy.include_patterns.unit_of_work


class MarkMixin:
    def mark_new(self):
        windy.include_patterns.unit_of_work.UnitOfWork.get_current().add_new(self)

    def mark_dirty(self):
        windy.include_patterns.unit_of_work.UnitOfWork.get_current().add_dirty(self)

    def mark_remove(self):
        windy.include_patterns.unit_of_work.UnitOfWork.get_current().add_remove(self)
