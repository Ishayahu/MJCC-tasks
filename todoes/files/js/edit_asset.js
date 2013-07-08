function send(url,form_id,asset_id,result_div) {
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
                    //send_and_show();
                    // Для удаления ошибки при загрузке поля со значением
                    //check_contractor();
            },
            error: function()
            {
                $("#"+result_div).empty();
                $("#"+result_div).append("Ошибка!");
            }
            }); 
}