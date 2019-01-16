function getUser() {
  if (!localStorage.CapstoneReservationUser) {
    return null;
  }
  return JSON.parse(localStorage.CapstoneReservationUser);
}

function saveUser(data) {
  localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
}

const storage = {
  getUser,
  saveUser,
}

export default storage;
