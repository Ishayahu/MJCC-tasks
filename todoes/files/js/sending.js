function send2(url,form_id,hide_id,show_id,message_id,dropdown_id) {
    // url - url �� �������� ���������� ������,
    // form_id - id ����� �� ������� ������������ ������,
    // hide_id - id ����, ������� ���� ������ (��� ������� ������ (��������, ����� ������)),
    // show_id - id ����, ������� ���� �������� (�� ����, ������� ���� �������� ������ (��������, ����)),
    // message_id - id ����, � ������� ��������� ��������� �� ������/������
    // dropdown_id - id ���� � ������� ��� ����������� ������

    // �������� �������
    $.ajax({
            type: "POST",
            url:  url,
            data: $("#"+form_id).serialize(),
            // ������� �� ��� ������ PHP
            success: function(html)
            {
                    // ������� ���������� ���������
                    $("#"+message_id).empty();
                    $("#"+message_id).append(html);
                    // �������� ����� ����������, ��������� ������ � �.�.
                    send_and_show2(hide_id,show_id,dropdown_id);
                    // ��� �������� ������ ��� �������� ���� �� ��������� - ����� workaround, ��� ��� �� ����� ����� ���� ����������. ������, ������ ���������� �� ������ � ���������� �������. ����, ������ �����, ���� �� �����
                    //check_contractor();
            },
            error: function()
            {
                $("#"+message_id).empty();
                $("#"+message_id).append("������!");
            }
            });
}
function send_and_show2(hide_id,show_id,dropdown_id) {
    // ���������� ��, ��� ���� ��������
    $("#"+show_id).show();
    // ������ ��� ����� ������������� ������ ��� ����������� ������
    //??????????? � ���������� ������ ��� ����������� ������ (����� ��? ���� ��� � ��� ��� ����)

    // ������������� ������ ��� ����������� ������
    //$("#"+dropdown_id).load("/api/get_contractors_list/"+contractor_name+"/");
    // ���� ������ ����? �� ����� ���� ��� �����, ���� ��� ����
    // ����� ����� - ��������, ��� �������

    // ������� ����� � ������� ������� �� ����� ������
    $("#"+hide_id).empty();
}
