# -*- coding:utf-8 -*-
# coding=<utf8>

from todoes.models import Note
# метод постороения дерева заметок
def build_note_tree(root_note,notes,current_indent):
    childrens = Note.objects.filter(parent_note=root_note).order_by('timestamp')
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
    childrens = Note.objects.filter(parent_note=root_note).order_by('timestamp')
    for note in childrens:
        notes.append(note)
        get_all_notes(note,notes)