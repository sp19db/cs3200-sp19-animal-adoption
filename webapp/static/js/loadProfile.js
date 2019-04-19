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
};

window.onclick = function (event) {
    if (event.target == profilePage) {
        profilePage.style.display = "none";
    }
};

function getChosenAnimalData(animalId) {
    var singleAnimalUrl = 'http://127.0.0.1:8000/animal?id=' + animalId;
    fetch(singleAnimalUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (animal) {
            var profileWrapper = document.createElement('div');
            profileWrapper.id = "animal-profile-wrapper";
            profileWrapper.className = "row";
            var profileLeftDiv = document.createElement('div');
            profileLeftDiv.className = "col";
            var image = document.createElement('img');
            image.src = animal.animal_image;
            image.alt = animal.animal_name;
            profileLeftDiv.appendChild(image);
            var profileRightDiv = document.createElement('div');
            profileRightDiv.className = "col";
            profileWrapper.appendChild(profileLeftDiv);
            profileWrapper.appendChild(profileRightDiv);
            document.getElementsByClassName("profile-content")[0].replaceChild(profileWrapper,
                document.getElementById("animal-profile-wrapper"));
        });


}

