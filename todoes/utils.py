# -*- coding:utf-8 -*-
# coding=<utf8>

from todoes.models import Note, Task,RegularTask
# метод постороения дерева заметок
def build_note_tree(root_note,notes,current_indent):
    childrens = Note.objects.filter(parent_note=root_note).\
        order_by('timestamp')
    for note in childrens:
        notes.append(note_with_indent(note,current_indent))
        build_note_tree(note,notes,current_indent+1)
# класс для заметки с отступом
class note_with_indent():
    def __init__(self, note, indent):
        self.note = note.note
        self.id = note.id
        self.author = note.author
        self.timestamp = note.timestamp
        self.indent = '&#9676;'*indent
        self.indent_pix = 4*indent
# получение всех заметок для заявки
def get_all_notes(root_note,notes):
    childrens = Note.objects.filter(parent_note=root_note).\
        order_by('timestamp')
    for note in childrens:
        notes.append(note)
        get_all_notes(note,notes)
def build_tasks_tree(root_task,tasks,current_indent):
    # class_dict = {str(RegularTask):RegularTask,
    #               str(Task):Task}
    if str(root_task.__class__)==str(Task):
        childrens = Task.objects.filter(parent_task=root_task).order_by('start_date')
    elif str(root_task.__class__)==str(RegularTask):
        childrens = Task.objects.filter(parent_regular_task=root_task).order_by('start_date')
    for task in childrens:
        task.indent_pix = 4*current_indent
        tasks.append(task)
        build_tasks_tree(task,tasks,current_indent+1)
