var asset_form_number=0;
function add_asset(asset_type_id) {
    asset_form_number++;
    // добавляем в конец в div.id=bill_assets форму нового актива + поле для его количества
    var url = "/api/get_asset_add_form/"+asset_type_id+"/"+asset_form_number+"/";
    var form_name = "asset_form_"+asset_form_number;
    $("#bill_assets").append("<div id='"+form_name+"'><br /></div>");
    $("#"+form_name).load(url,function(result){
        // кнопка удаления формы    
        $("#"+form_name).append('<input type="number" value="1" name="count_of_asset'+asset_form_number+'" /><input type="button" value="X" onclick="delete_asset_form('+asset_form_number+')" />');
        $("#max_asset_form_number").val(asset_form_number);
    });
}
function delete_asset_form(id) {
    var form_name = "asset_form_"+id;
    $("#"+form_name).remove();
}