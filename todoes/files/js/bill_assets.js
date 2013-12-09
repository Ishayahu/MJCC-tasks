var asset_form_number=0;
function add_asset(asset_type_id) {
    asset_form_number++;
    // добавляем в конец в div.id=bill_assets форму нового актива + поле для его количества
    var url = "/api/get_asset_add_form/"+asset_type_id+"/"+asset_form_number+"/";
    var url2 = "/api/get_asset_add_form_script/"+asset_type_id+"/"+asset_form_number+"/";
    var form_name = "asset_form_"+asset_form_number;
    if (asset_form_number==1) {
        $("#bill_assets").append("<table border='1' id='bill_assets_table'><tr id='table_header'></tr></table>");
        $("#table_header").load("/api/get_asset_add_form_header/",function(result){
        });
    }
    $("#bill_assets_table").append("<tr id='"+form_name+"'><br /></tr>");
    $("#"+form_name).load(url,function(result){
        // кнопка удаления формы    
        //$("#"+form_name).append('<input type="number" value="1" name="count_of_asset'+asset_form_number+'" /><input type="button" value="X" onclick="delete_asset_form('+asset_form_number+')" />');
        $("#max_asset_form_number").val(asset_form_number);
    });
    $("#bill_assets").append("<div id='script_for_form_"+form_name+"'></div>")
    $("#script_for_form_"+form_name).load(url2,function(result){
                                                });
    }
function delete_asset_form(id) {
    var form_name = "asset_form_"+id;
    $("#"+form_name).remove();
}