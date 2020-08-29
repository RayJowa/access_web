
$(document).ready(function () {
    // $('#city').change(function () {
    //     console.log(this.val());
    // });


})

function fetchSuburbs(city) {
    console.log(city);

    $('#suburb-select-div').removeClass('col-sm-12')
    .addClass('col-sm-10');
    $('#suburb-spinner').toggle();
    $('#suburb-error').empty()


    $.ajax({
        url: '/fetch_suburbs',
        method: 'post',
        data: {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'city': city,

        },
        dataType: 'json',
        success: function (data) {

            $('#suburb-select-div').removeClass('col-sm-10')
            .addClass('col-sm-12');
            $('#suburb-spinner').toggle();

            //clear select to make way for new options
            $('#suburb').empty();

            if(data.suburbs){
                //Load new suburbs into select
                $.each(data.suburbs, function (i, suburb) {
                    console.log(`${suburb.suburbid} - ${suburb.name}`);
                    $('#suburb').append(`<option value="${suburb.suburbid}">${suburb.name}</option>`);
                });
            }else {
                $('#suburb').append(`<option value="">Select suburb</option>`);
                $('#suburb-error').text(data.error_message);
            }

        }
      });
}

function fetchSuburbsSearch(city) {
    console.log(city);

    $('#suburb-select-div').removeClass('col-sm-12')
    .addClass('col-sm-10');
    $('#suburb-spinner').toggle();
    $('#suburb-error').empty()


    $.ajax({
        url: '/fetch_suburbs',
        method: 'post',
        data: {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
            'city': city,

        },
        dataType: 'json',
        success: function (data) {

            $('#suburb-select-div').removeClass('col-sm-10')
            .addClass('col-sm-12');
            $('#suburb-spinner').toggle();

            //clear select to make way for new options
            $('#suburb').empty();

            if(data.suburbs){
                //Load new suburbs into select
                $('#suburb').append(`<option value="">(All suburbs)</option>`);
                $.each(data.suburbs, function (i, suburb) {
                    $('#suburb').append(`<option value="${suburb.name}">${suburb.name}</option>`);
                });
            }else {
                $('#suburb').append(`<option value="">Select suburb</option>`);
                $('#suburb-error').text(data.error_message);
            }

        }
      });
}