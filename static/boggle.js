"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $button = $("word-input-btn");

let gameId;

/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  const $tbody = $("<tbody></tbody>");
  for (let y = 0; y < board.length; y++) {
    const $trow = $("<tr></tr>");
    for (let x = 0; x < board[y].length; x++) {
      const $tdata = $(`<td>${board[y][x]}</td>`);
      $trow.append($tdata);
    }
    $tbody.append($trow);
  }
  $table.append($tbody);
  // loop over board and create the DOM tr/td structure
}

function handleResult(result, word) {
  $message.empty();
  $wordInput.val("");
  if (result === "not-word") {
    $message.text("Not a word!");
  }
  if (result === "not-on-board") {
    $message.text("Not on board! ");
  }
  if (result === "ok") {
    $playedWords.append(`<li>${word}</li>`);
  }
}

async function submitForm(evt) {
  evt.preventDefault();
  const word = $wordInput.val().toUpperCase();
  console.log(word);
  let response = await axios.post("/api/score-word", {
    game_id: gameId,
    word: word,
  });
  console.log(response.data);
  handleResult(response.data.result, word);
}

start();
$form.on("submit", submitForm);
