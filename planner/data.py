from datetime import timedelta


class TaskError(Exception):
    pass


class ScheduleError(Exception):
    pass


class Task:
    def __init__(self, name, begins, ends):
        if ends < begins:
            raise TaskError('The begin time must precede the end time')
        if ends - begins < timedelta(minutes=5):
            raise TaskError('The minimum duration is 5 minutes')
        self.name = name
        self.begins = begins
        self.ends = ends

    def excludes(self, other):
        return NotImplemented

    def overlaps(self, other):
        if other.begins < self.begins:
            return other.ends > self.begins
        elif other.ends > self.ends:
            return other.begins < self.ends
        else:
            return True

    def __repr__(self):
        return '<{} {} {}>'.format(self.name,
                                   self.begins.isoformat(),
                                   self.ends.isoformat())


class Activity(Task):
    def excludes(self, other):
        return isinstance(other, Activity)


class Status(Task):
    def excludes(self, other):
        return False


class Schedule:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        for contained in self.tasks:
            if task.overlaps(contained):
                if task.exclude(contained) or contained.exclude(task):
                    raise ScheduleError(task, contained)
        self.tasks.append(task)

    def remove(self, task):
        try:
            self.tasks.remove(task)
        except ValueError:
            pass

    def __contains__(self, task):
        return task in self.tasks
