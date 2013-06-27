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
                    send_and_show()
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
    // удаляем старый список поставщиков
    $("#contractors_list").empty();
    // перезагружаем новый, со значением по умолчанию
    // TODO: получать значение через $("#"+result_div)
    var contractor_name = $("#id_name").val()
    $("#contractors_list").load("/api/get_contractors_list/"+contractor_name+"/");
    // удаляем форму ввода поставщика
    $("#additional_content").empty();
}


