function job_type(job_type) {
    document.getElementById('location').value = '';
    let param = 'job_type=' + job_type;
    send_request_reverse_recipe(param);
}

function sort_jobs(sort_type) {
    document.getElementById('location').value = '';
    let param = 'sort_jobs=' + sort_type;
    send_request_reverse_recipe(param);
}

function find_location() {
    let location = document.getElementById('location').value;
    let param = 'location=' + location;
    send_request_reverse_recipe(param);
}

function send_request_reverse_recipe() {
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/reverse_recipe',
        beforeSend: function () {
            console.log('before send');
        },
        success: function (result) {
            console.log(result);
            update_table_recipe(result);
        },
        error: function () {
            console.log('error');
        }
    });
}

function send_request_fridge() {
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/foods',
        beforeSend: function () {
            console.log('before send');
        },
        success: function (result) {
            console.log(result);
            update_list_foods(result);
        },
        error: function () {
            console.log('error');
        }
    });
}

function update_list_foods(data) {
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = '<li>' + elem['name'] + '</li>';
        all_rows = all_rows + row;
    });
    $('#myFridge').html(all_rows);
}


function update_table_recipe(data) {
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = '<tr><td>' + elem['title'] + '</td>' + '<td><img src=' + elem['image'] + 'width="100" height="100" alt="recipe"></td>' + '<td>';
        elem['usedIngredients'].forEach(key => {
            // console.log(key['name'])
            row += key['name'] + ',';
        })
        row += '</td>' + '</tr>';
        all_rows = all_rows + row;
    });
    $('#myTable tbody').html(all_rows);
}