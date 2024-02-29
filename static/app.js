let $faveBtn = $(".fave-btn");
const notificationDiv = $("#alert");

notificationDiv.hide();

$(document).ready(function () {
  console.log("page is loading");
  $("#loader").show();
});

$(window).on("load", function () {
  console.log("page has finished loading");
  $("#loader").hide();
});

$faveBtn.on("click", async function (e) {
  e.preventDefault();
  try {
    if ($(this).hasClass("faved")) {
      await delFave($(this));
    } else {
      await addFave($(this));
    }
  } catch (error) {
    handleError(error);
  }
});

async function delFave(plant) {
  let plant_id = plant.attr("id");
  try {
    let delRes = await axios.post(`/delete_favorite/${plant_id}`);
    if (delRes.status === 200) {
      plant.toggleClass("unfaved").removeClass("faved");
      let url = $(location)[0].href;
      if (url.includes("favorites")) {
        plant.closest(".card").remove();
      }
    } else {
      handleUnexpectedStatus(delRes);
    }
  } catch (error) {
    handleError(error);
  }
}

async function addFave(plant) {
  let plant_id = plant.attr("id");
  try {
    let addRes = await axios.post(`/add_favorite/${plant_id}`);
    if (addRes.status === 201) {
      plant.toggleClass("faved").removeClass("unfaved");
    } else {
      displayNotification("You must login or register to favorite a plant!");
    }
  } catch (error) {
    handleError(error);
  }
}
function displayNotification(message) {
  notificationDiv.text(message);
  notificationDiv.show();
}
function handleUnexpectedStatus(req) {
  console.error(`Unexpected status code. Response:`, req);
}

function handleError(error) {
  console.error("An error occurred:", error);
}

$(".adv-search-btn").on("click", function (e) {
  $(".adv-search-div").toggleClass("adv-search-form-h adv-search-form-v");
});
