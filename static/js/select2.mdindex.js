// 指标表的select

selecthtml = '<div class="form-row select2_englishname"><div><label class="" for="id_searchname">搜索指标:</label><select id="column_search"><option value="" selected="selected">输入库/表/字段名搜索</option></select></div></div>'

function formatRepoSelection(data){
    if(data.name){
        name = data.name;
        sel = name.split(',');
        var arrEntities={'lt':'<','gt':'>','nbsp':' ','amp':'&','quot':'"'};
        coltype = sel[0].replace(/&(lt|gt|nbsp|amp|quot);/ig,function(all,t){return arrEntities[t]});
        table = sel[1];
        table = table.split('.');

        jQuery('#id_index_name').val(table[2]);
        jQuery('#id_data_type').val(coltype);
        jQuery('#id_source_table').val(table[0] + "." + table[1]);
    }
    

    return data.name || '';
}

function formatSelect2Result(repo) {
    if (repo.loading) return repo.text;
    var markup = repo.name;
    return markup;
}


function formatRepoSelectionInParent(data){
    if(data.name){
        name = data.name;
        sel = name.split(',');
        var arrEntities={'lt':'<','gt':'>','nbsp':' ','amp':'&','quot':'"'};
        coltype = sel[0].replace(/&(lt|gt|nbsp|amp|quot);/ig,function(all,t){return arrEntities[t]});
        table = sel[1];
        table = table.split('.');

        // bd = jQuery(this).parent('.dynamic-mdindexparent_set');
        // console.log(jQuery(this));
        // bd.find('.field-index_name input').val(table[2])
        // bd.find('.field-source_table input').val(table[0] + "." + table[1])
    }
    

    return data.name || '';
}

jQuery(document).ready(function(){
    jQuery('fieldset.module_0').prepend(selecthtml);
    

    jQuery("#column_search").select2({
        width:'700px',
        allowClear: true,
        placeholder: "输入库/表/字段名搜索",
        language: "zh-CN",
        ajax: {
            url: "/ajax/search_basic_column_info/",
            dataType: 'json',
            type: "get",
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page || 1
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data.items,
                    pagination: {
                        more: false
                    }
                };
            },
            cache: true
        },
        minimumInputLength: 3,
        escapeMarkup: function (markup) {
            return markup;
        },
        templateSelection: formatRepoSelection,
        templateResult: formatSelect2Result,
    });


    jQuery('.field-parent select').select2({
        width:'500px',
        allowClear: true,
        placeholder: "输入库/表/字段名搜索",
        language: "zh-CN",
        ajax: {
            url: "/ajax/search_basic_column_info/",
            dataType: 'json',
            type: "get",
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page || 1
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data.items,
                    pagination: {
                        more: false
                    }
                };
            },
            cache: true
        },
        minimumInputLength: 3,
        escapeMarkup: function (markup) {
            return markup;
        },
        templateSelection: formatRepoSelectionInParent,
        templateResult: formatSelect2Result,
    });   

    jQuery('.field-parent select').on("change", function(e) {  
        bd = jQuery(this).parents('.dynamic-mdindexparent_set');
        bd.find('.field-index_name input').val(table[2])
        bd.find('.field-source_table input').val(table[0] + "." + table[1])
        bd.find('.field-parent select').val('1');
    })

    setTimeout(function(){ 
        jQuery('.add-row').remove()
    }, 2000);


})




