function CheckTab(e){
    if(e.keyCode == '9'){
        return false;
    }
}
function list_down2(dropdown_id) {
    // скрыть/показать список возможных вариантов
    var a = document.getElementById(dropdown_id);
        if ( a.style.display == 'none' )
        a.style.display = 'block'
    else
        if ( a.style.display == 'block' )
        a.style.display = 'none';
};
function list_on_change(item_list,input_field_id,dropdown_field_id,error_field_id,confirm_message,field_to_hide_id,filed_to_load_id,url_to_load_prefix,url_to_load_element_id,url_to_load_postfix) {
    // if (!if_not_new_callback) {
       // if_not_new_callback =function (){}
    // }
    function wrapped(e) {
        // Изменение списка возможных вариантов в соответствии с введёнными в input_field_id символами
        var e = e||window.event;
        if (e.keyCode == 9 || e.keyCode == 13) {
            // если энтер или таб - добавить нового поставщика
            // TODO: а если мышкой увели фокус?
            // TODO: при энтере отправляется форма
            // формируем url с которого должна загрузиться форма для ввода нового значения(?)
            url_to_load = url_to_load_prefix + document.getElementById(url_to_load_element_id).value.replace(/ /g,'%20') + url_to_load_postfix
            // проверяем, является ли значение новым или нет
            check_contractor(item_list,input_field_id,dropdown_field_id,error_field_id,confirm_message,field_to_hide_id,filed_to_load_id,url_to_load)
        } else {
            //var inputed = $("#contractor").val()
            var inputed = $("#"+input_field_id).val()
            for (x=0;x<$("#"+dropdown_field_id).find('li').length;x++) {
                if ($("#"+dropdown_field_id).find('li')[x].innerHTML.toLowerCase().indexOf(inputed.toLowerCase())==-1) {
                    $("#"+dropdown_field_id).find('li')[x].hidden=true
                } else {
                    $("#"+dropdown_field_id).find('li')[x].hidden=false
                }
            }
        }
    }
    return wrapped
};
function select_element(id,value,input_field_id,id_field_id,error_field_id,dropdown_id,if_not_new_callback){
    // Вводит в поле ввода выбранное из списка значение
    if (!if_not_new_callback) {
       if_not_new_callback =function (){}
    }
    var b = document.getElementById(input_field_id);
    var c = document.getElementById(id_field_id);
    b.value=value;
    c.value=id;
    list_down2(dropdown_id);
    //check_contractor(); // а зачем? ведь выбрано то и так из имеющихся!
    //Чтобы убрать ошибку "поле должно быть обязательным"
    var b = document.getElementById(input_field_id);
    // Если значение не пустое - удаляем сообщение об ошибке. Если пустое - добавляем
    if (b.value) {
        $("#"+error_field_id).empty()
    } else {
        $("#"+error_field_id).html("<li>Обязательное поле.</li>")
    }
    if_not_new_callback()
}
function check_contractor(item_list,input_field_id,dropdown_field_id,error_field_id,confirm_message,field_to_hide_id,field_to_load_id,url_to_load) {
    // Проверяем введённое значение если был выбран элемент
    // if (!if_not_new_callback) {
       // if_not_new_callback =function (){}
    // }
    var a = document.getElementById(dropdown_field_id);
    if ( a.style.display == 'block' )
        a.style.display = 'none';
    var b = document.getElementById(input_field_id);
    // Если значение не пустое - удаляем сообщение об ошибке. Если пустое - добавляем
    if (b.value) {
        $("#"+error_field_id).empty()
    } else {
        $("#"+error_field_id).html("<li>Обязательное поле.</li>")
    }
    // Если ввели нового поставщика
    if (c_list.indexOf(b.value)==-1) {
        if (confirm (confirm_message)) {
            // скрываем поле счёта
            $("#"+field_to_hide_id).hide();
            // загружаем форму добавления новго поставщика
            // замена нужна для русского языка, может быть только под Windows7
            //var contractor_name=b.value.replace(/ /g,"%20")
            $("#"+field_to_load_id).load(url_to_load);
            event.preventDefault();
            event.stopPropagation();
        }
    // } else {
        // if_not_new_callback()
    }
    
}
// функция для загрузки последней цены, срока гарантии + установка статуса в {статус по умолчанию} и места в {место по умолчанию} из настроек раздела [cashless]
function autocompletion(number,dp,ds,model_value){
    contractor_value = $("#contractor").val()
    csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]")[0].value
    id_cp = 'id_'+number+'_current_place'
    id_s = 'id_'+number+'_status'
    id_p = 'id_'+number+'_price'
    id_w = 'id_'+number+'_guarantee_period'
    // сюда поставить загрузку из БД
    $.post( "/api/json/get/price_and_warranty/", { 'model': model_value, 'contractor': contractor_value, 'csrfmiddlewaretoken': csrfmiddlewaretoken })
      .done(function( data ) {
        console.log( data );
        $("#"+id_p).val(data.price)
        $("#"+id_w).val(data.warranty)
      });
    // тут ставим место и статус
    $("#"+id_cp+" :contains('"+dp+"')").attr("selected", "selected");
    $("#"+id_s+" :contains('"+ds+"')").attr("selected", "selected");
}
