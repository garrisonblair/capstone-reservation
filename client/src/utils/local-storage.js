function getUser() {
  if (!localStorage.CapstoneReservationUser) {
    return null;
  }
  return JSON.parse(localStorage.CapstoneReservationUser);
}

function saveUser(data) {
  localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
}

function getOrientation() {
  if (!localStorage.Orientation) {
    return null;
  }
  return parseInt(localStorage.Orientation, 10);
}

function saveOrientation(orientation) {
  localStorage.setItem('Orientation', orientation);
}

function checkAdmin() {
  if (localStorage.getItem('CapstoneReservationUser')) {
    return JSON.parse(localStorage.getItem('CapstoneReservationUser')).is_superuser;
  }
  return false;
}

const storage = {
  getUser,
  saveUser,
  getOrientation,
  saveOrientation,
  checkAdmin,
};

export default storage;
