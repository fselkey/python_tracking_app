function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteOrder(orderId) {
  fetch("/delete-order", {
    method: "POST",
    body: JSON.stringify({ orderId: orderId }),
  }).then((_res) => {
    window.location.href = "/order";
  });
}