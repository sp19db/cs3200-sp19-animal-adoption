var profilePage = document.getElementById('profile-page');
var close = document.getElementsByClassName("close")[0];

$(document).on("click", '.card-img-top', function (e) {
    $(e.target).attr("id", function (i, value) {
        profilePage.style.display = "block";
        getChosenAnimalData(value);
    });

});

close.onclick = function () {
    profilePage.style.display = "none";
    clearProfilePage()
};

window.onclick = function (event) {
    if (event.target == profilePage) {
        profilePage.style.display = "none";
        clearProfilePage()
    }
};

function clearProfilePage() {
    var info = document.getElementById('animal-profile-wrapper');
    while (info.hasChildNodes()) {
        info.removeChild(info.firstChild);
    }
}

function createProfileDescription(title, text) {
    if (title === "br" && text === "br") {
        var br = document.createElement('br');
        return br;
    } else {
        var wrapper = document.createElement('div');
        wrapper.className = 'row';
        var titleContainer = document.createElement('p');
        titleContainer.className = "info-title col-2";
        titleContainer.innerText = title;
        var textContainer = document.createElement('p');
        textContainer.className = "info col-8";
        if (text === "" || text == "  ") {
            textContainer.innerText = "N/A"
        } else {
            textContainer.innerText = text;
        }
        wrapper.appendChild(titleContainer);
        wrapper.appendChild(textContainer);
        return wrapper;
    }

}

function initMap2(lat, lng) {
    var myLatLng = {lat: lat, lng: lng};

    var map = new google.maps.Map(document.getElementById('profile-map'), {
        zoom: 17,
        center: myLatLng
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Hello World!'
    });
}


function getChosenAnimalData(animalId) {
    var singleAnimalUrl = serverPathPrefix + 'animal?id=' + animalId;
    fetch(singleAnimalUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (animal) {
            var profileWrapper = document.createElement('div');
            profileWrapper.id = "animal-profile-wrapper";
            profileWrapper.className = "row";
            var profileLeftDiv = document.createElement('div');
            profileLeftDiv.className = "col-3";
            var image = document.createElement('img');
            image.className = 'profile-image';
            image.src = animal.animal_image;
            image.alt = animal.animal_name;
            profileLeftDiv.appendChild(image);
            var profileRightDiv = document.createElement('div');
            profileRightDiv.className = "col-5";
            var animalInfo = [["type", animal.type_name],
                ["breed", animal.breed_name],
                ["br", "br"],
                ["name", animal.animal_name],
                ["gender", animal.gender],
                ["age", animal.age],
                ["size", animal.size],
                ["color", animal.color],
                ["br", "br"],
                ["shelter", animal.shelter_name],
                ["phone", animal.phone_number],
                ["email", animal.email_address]
            ];
            for (var i = 0; i < animalInfo.length; i++) {
                var entry = createProfileDescription(animalInfo[i][0], animalInfo[i][1]);
                profileRightDiv.appendChild(entry);
            }
            var mapWrapper = document.createElement("div");
            mapWrapper.id = "profile-map";
            mapWrapper.className = "col-4";

            profileWrapper.appendChild(profileLeftDiv);
            profileWrapper.appendChild(profileRightDiv);
            profileWrapper.appendChild(mapWrapper);
            document.getElementsByClassName("profile-content")[0].replaceChild(profileWrapper,
                document.getElementById("animal-profile-wrapper"));
            if (animal.lat != null && animal.lng != null) {
                initMap2(animal.lat, animal.lng);
            }
        });


}

