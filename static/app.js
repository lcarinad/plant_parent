let $faveBtn = $(".fave-btn");
let url = "http://127.0.0.1:5000";

$faveBtn.on("click", async function (e) {
  e.preventDefault();
  try {
    console.log($(this));
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
    let delRes = await axios.post(`${url}/delete_favorite/${plant_id}`);
    if (delRes.status === 200) {
      console.log(delRes);
      plant.toggleClass("unfaved").removeClass("faved");
      let url = $(location)[0].href;
      console.log(url);
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
    let addRes = await axios.post(`${url}/add_favorite/${plant_id}`);
    if (addRes.status === 201) {
      plant.toggleClass("faved").removeClass("unfaved");
      console.log(addRes);
    } else {
      alert("You must login to favorite a plant!");
      handleUnexpectedStatus(addRes);
    }
  } catch (error) {
    handleError(error);
  }
}

function handleUnexpectedStatus(req) {
  console.log(`Unexpected status code. Response:`, req);
}

function handleError(error) {
  console.error("An error occurred:", error);
}

$(".adv-search-btn").on("click", function (e) {
  $(".adv-search-div").toggleClass("adv-search-form-h adv-search-form-v");
});
