function send(url,form_id,result_div) {
    // Отсылаем паметры
    $.ajax({
            type: "POST",
            url:  url,
            data: $("#"+form_id).serialize(),
            // Выводим то что вернул PHP
            success: function(html)
            {
                    $("#"+result_div).empty();
                    $("#"+result_div).append(html);
                    // скрываем форму поставщика, открываем заказа и т.п.
                    send_and_show();
                    // Для удаления ошибки при загрузке поля со значением
                    check_contractor();
            },
            error: function()
            {
                $("#"+result_div).empty();
                $("#"+result_div).append("Ошибка!");
            }
            }); 
}
function send_and_show() {
    //показываем форму ввода счёта
    $("#content_to_hide").show();
    var c_id = $("#c_id").val()
    var c_name = $("#c_name").val()
    $("#contractor").val(c_name)
    $("#contractor_id").val(c_id)
    // удаляем старый список поставщиков
    $("#contractors_list").empty();
    // перезагружаем новый, со значением по умолчанию
    // замена нужна для русского языка, может быть только под Windows7
    var contractor_name = $("#id_name").val().replace(/ /g,"%20")
    $("#contractors_list").load("/api/get_contractors_list/"+contractor_name+"/");
    // удаляем форму ввода поставщика
    $("#additional_content").empty();
}


