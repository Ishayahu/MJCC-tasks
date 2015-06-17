/**
 * Created by Ishayahu on 16.06.2015.
 * ƒл€ функций редактора текста:
 * сохранение/восстановление черновика
 */

/**
 * —охранение черновика
 * @param id номер черновика, обычно номер задачи
 * @param elem_id id элемента, содержащего текст
 */
function save_draft(id,elem_id){
    var text = document.getElementById(elem_id).value
    localStorage.setItem("draft_"+id,text);
}

/**
 * ”даление черновика
 * @param id номер черновика, обычно номер задачи
 */
function delete_draft(id){
    localStorage.removeItem("draft_"+id);
}

/**
 * ¬осстановление черновика
 * @param id номер черновика, обычно номер задачи
 * @param elem_id id элемента, содержащего текст
 */
function restore_draft(id,elem_id){
    var text = localStorage.getItem("draft_"+id);
    if (text!=null) {
        document.getElementById(elem_id).value = text;
    }

}

/**
 * –егистрирует сохранение черновика
 * @param id номер черновика, обычно номер задачи
 * @param elem_id id элемента, содержащего текст
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

