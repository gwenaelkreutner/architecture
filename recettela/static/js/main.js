function find_location() {
    let location = document.getElementById('location').value;
    let param = 'query=' + location;
    search_recipe(param);
}

function send_request_reverse_recipe() {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/reverse_recipe',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
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

function search_recipe(query) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/search_recipe/?' + query,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (result) {
            console.log(result);
            update_table_recipe(result, false);
        },
        error: function () {
            console.log('error');
        }
    });
}


function send_request_fridge(isDelete = true) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/foodsUser',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (result) {
            update_list_foods(result, isDelete);
        },
        error: function () {
            console.log('error');
        }
    });
}


function delete_food(pk) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: 'http://127.0.0.1:8000/api/foods/' + pk + '/',
        type: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
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

function recipe_information(pk) {
    $.ajax({
        url: 'https://api.spoonacular.com/recipes/' + pk + '/information?apiKey=04a5aef53bd442d28f3338d9b852be8b',
        type: 'GET',
        success: function (result) {
            window.open(result['spoonacularSourceUrl'], '_blank');
            ;
        },
        error: function () {
            console.log('error');
        }
    });
}

$("#formAdd").submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var csrftoken = getCookie('csrftoken');
    var form = $(this);
    var ingredient = document.getElementById("inputIngredient").value;
    var date = document.getElementById("inputDate").value;
    var url = 'http://127.0.0.1:8000/api/foods/';
    console.log(form.serialize());

    $.ajax({
        type: "POST",
        url: url,
        data: {name: ingredient, expiration_date: date, calories: 0}, // serializes the form's elements.
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);

        },
        success: function (result) {
            update_list_foods(result);
        },
    });


});

function update_list_foods(data, isDelete = true) {
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = '<tr><td>' + elem['name'] + '</td>' + '<td>Expiration date : ' + elem['expiration_date'] + '</td>';
        if (isDelete) row += '<td><button type="button" class="btn btn-danger" onclick="delete_food(' + elem['id'] + ')">DELETE</button></td>';
        row += '</tr>';
        all_rows = all_rows + row;
    });
    $('#myFridge tbody').html(all_rows);
}


function update_table_recipe(data, isReverse = true) {
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        row = '<tr><td>' + elem['title'] + '</td>' + '<td><img src=' + elem['image'] + 'width="100" height="100" alt="recipe"></td>' + '<td>';
        if (isReverse) {
            elem['usedIngredients'].forEach(key => {
                row += key['name'] + ',';
            })
        }

        row += '</td>' + '<td><u onclick="recipe_information(' + elem['id'] + ')">Link</u></td>' + '</tr>';
        all_rows = all_rows + row;
    });
    $('#myTable tbody').html(all_rows);
}

function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}