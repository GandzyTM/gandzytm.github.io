const numDivs = 36;
const maxHits = 10;

let hits = 0;
let missHits = 0;
let firstHitTime = 0;

function round() {
  $(".game-field").removeClass("target");
  $(".game-field").removeClass("miss");

  let divSelector = randomDivId();
  $(divSelector).addClass("target");
  $(".target").text(hits + 1);

  if (hits === maxHits) {
    endGame();
  }
}

function endGame() {
  $('#game-fields').addClass("d-none");

  let totalPlayedMillis = getTimestamp() - firstHitTime;
  let totalPlayedSeconds = Number(totalPlayedMillis / 1000).toPrecision(3);
  $("#total-time-played").text(totalPlayedSeconds);
  let totalPoints = hits + missHits;
  $("#total-fails").text(" " + totalPoints);

  $("#end-game-message").removeClass("d-none");
}

function handleClick(event) {
  if ($(event.target).hasClass("target")) {
    hits = hits + 1;
    $(event.target).text("");
    round();
  } else {
    $(event.target).addClass("miss");
    missHits = missHits - 1;
  };
}

function init() {
  round();
  $(".game-field").click(handleClick);

  $("#start-game-btn").click(function(){
    firstHitTime = getTimestamp();
    $("#game-fields").removeClass('d-none');
    $("#start-game-btn").hide();
  
    $("#reload-btn").removeClass('d-none');
  });

  $("#reload-btn").click(function() {
    location.reload();
  });

}

$(document).ready(init);