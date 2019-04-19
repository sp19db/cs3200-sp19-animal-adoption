window.onload = function () {
    refreshAnimalsByFilter();
    initMap();
};

$(document).on("click", '.breed a', function () {
    $('#selected-animal-breed').text($(this).text());
    refreshAnimalsByFilter();
});
$('.size a').click(function () {
    $('#selected-animal-size').text($(this).text());
    refreshAnimalsByFilter();
});
$('.gender a').click(function () {
    $('#selected-animal-gender').text($(this).text());
    refreshAnimalsByFilter();
});
$('.age a').click(function () {
    $('#selected-animal-age').text($(this).text());
    refreshAnimalsByFilter();
});
$('.a-type span').click(function (event) {
    var target = $(event.target);
    if (target.hasClass("selected")) {
        target.removeAttr('style');
        target.removeClass("selected").addClass("deselected");
    } else {
        var typeSpan = $('.a-type span');
        typeSpan.removeClass("selected").addClass("deselected");
        typeSpan.removeAttr('style');
        target.css('border-bottom', "3px solid rgb(33, 187, 255)");
        target.removeClass("deselected").addClass("selected");
        breedMenu();
    }
    clearDropdownText();
    refreshAnimalsByFilter();
});

function clearDropdownText() {
    $('#selected-animal-breed').text('Any');
    $('#selected-animal-size').text('Any');
    $('#selected-animal-gender').text('Any');
    $('#selected-animal-age').text('Any');
}

function refreshAnimalsByFilter() {
    var filterUrl = getAnimalFilterUrl();
    getAnimals(filterUrl)
}

function getType() {
    var type_name = "";
    $('.a-type span').each(function () {
        if ($(this).hasClass("selected")) {
            type_name = $(this).attr('id');
        }
    });
    return type_name;
}

function breedMenu() {
    var type_name = getType();
    var menu = document.getElementsByClassName("breed")[0];
    var filterUrl = 'http://127.0.0.1:5000/breeds?type=' + type_name;
    fetch(filterUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (breeds) {
            while (menu.firstChild) {
                menu.removeChild(menu.firstChild);
            }
            for (i = 0; i < breeds.length; i++) {
                var x = document.createElement("li");
                var y = document.createElement("a");
                y.textContent = breeds[i];
                y.setAttribute("href", "#");
                y.className = 'dropdown-item';
                x.appendChild(y);
                menu.appendChild(x);
            }
            var anyLi = document.createElement("li");
            var anyA = document.createElement("a");
            anyA.textContent = "Any";
            anyA.setAttribute("href", "#");
            anyA.className = 'dropdown-item';
            anyLi.appendChild(anyA);
            menu.appendChild(anyLi)
        });
}


function getAnimalFilterUrl() {
    var fieldMap = getFields();
    var filterUrl = createFilter(fieldMap["type"],
        fieldMap["breed"],
        fieldMap["size"],
        fieldMap["gender"],
        fieldMap["age"]);
    return filterUrl;
}

function getFields() {
    var type = "";
    $('.a-type span').each(function () {
        if ($(this).hasClass("selected")) {
            type = $(this).attr('id');
        }
    });
    if (type === "") {
        type = "Any";
    }
    var breed = $('#selected-animal-breed').text();
    var size = $('#selected-animal-size').text();
    var gender = $('#selected-animal-gender').text();
    var age = $('#selected-animal-age').text();
    return {"type": type, "breed": breed, "size": size, "gender": gender, "age": age};
}

function createFilter(type, breed, size, gender, age) {
    var filterUrl = '';
    var additionalFilters = '';
    if (type !== 'Any') {
        additionalFilters += '&type=' + type
    }
    if (breed !== 'Any') {
        additionalFilters += '&breed=' + breed
    }
    if (size !== 'Any') {
        additionalFilters += '&size=' + size
    }
    if (gender !== 'Any') {
        additionalFilters += '&gender=' + gender
    }
    if (age !== 'Any') {
        additionalFilters += '&age=' + age
    }
    if (additionalFilters !== '') {
        filterUrl += additionalFilters.substring(1, additionalFilters.length + 1);
    }
    return filterUrl
}

function getAnimals(filterUrl) {
    fetch("http://127.0.0.1:5000/animals?" + filterUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (animals) {
            var animalsWrapper = document.createElement('div');
            animalsWrapper.id = "animals-wrapper";

            var animalsContainter = document.createElement('div');
            animalsContainter.className = "container";
            var animalsCardDeck = document.createElement('div');
            animalsCardDeck.className = "row";

            for (var i in animals) {
                var animalCard = document.createElement('div');
                animalCard.className = "card";
                var animalImage = document.createElement('img');
                animalImage.className = "card-img-top";
                animalImage.id = animals[i].id;
                animalImage.title = "click to see more about " + animals[i].name;
                animalImage.src = animals[i].img_url;
                animalImage.alt = animals[i].name;
                var animalCardBody = document.createElement('div');
                animalCardBody.className = "card-body";
                var animalName = document.createElement('h5');
                animalName.className = "card-title";
                animalName.textContent = animals[i].name;

                var animalGender = document.createElement('span');
                animalGender.className = "card-text";
                animalGender.textContent = animals[i].gender;

                var animalAge = document.createElement('span');
                animalAge.className = "card-text";
                animalAge.textContent = animals[i].age;

                var animalSize = document.createElement('span');
                animalSize.className = "card-text";
                animalSize.textContent = animals[i].size;
                animalCardBody.appendChild(animalName);
                animalCardBody.appendChild(animalGender);
                animalCardBody.appendChild(animalAge);
                animalCardBody.appendChild(animalSize);
                animalCard.appendChild(animalImage);
                animalCard.appendChild(animalCardBody);
                animalsCardDeck.appendChild(animalCard);
            }
            animalsWrapper.appendChild(animalsCardDeck);

            document.getElementById("animals").replaceChild(animalsWrapper,
                document.getElementById("animals-wrapper"));
        });
}