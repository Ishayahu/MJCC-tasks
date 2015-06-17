/**
 * Created by Ishayahu on 16.06.2015.
 * ��� ������� ��������� ������:
 * ����������/�������������� ���������
 */

/**
 * ���������� ���������
 * @param id ����� ���������, ������ ����� ������
 * @param elem_id id ��������, ����������� �����
 */
function save_draft(id,elem_id){
    var text = document.getElementById(elem_id).value
    localStorage.setItem("draft_"+id,text);
}

/**
 * �������� ���������
 * @param id ����� ���������, ������ ����� ������
 */
function delete_draft(id){
    localStorage.removeItem("draft_"+id);
}

/**
 * �������������� ���������
 * @param id ����� ���������, ������ ����� ������
 * @param elem_id id ��������, ����������� �����
 */
function restore_draft(id,elem_id){
    var text = localStorage.getItem("draft_"+id);
    if (text!=null) {
        document.getElementById(elem_id).value = text;
    }

}

/**
 * ������������ ���������� ���������
 * @param id ����� ���������, ������ ����� ������
 * @param elem_id id ��������, ����������� �����
 */
function register_draft_saver(id,elem_id) {
    //$("#"+elem_id).keydown(save_draft(id,elem_id));
    $("#"+elem_id).bind('input propertychange',function(){
        save_draft(id,elem_id);
    });
}

function register_draft_cleaner(id,elem_id) {
    $('#'+elem_id).submit(function(){
        delete_draft(id);
    });
}

