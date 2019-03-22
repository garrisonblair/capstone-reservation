function getUser() {
  if (!localStorage.CapstoneReservationUser) {
    return null;
  }
  return JSON.parse(localStorage.CapstoneReservationUser);
}

function saveUser(data) {
  localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
}

function deleteUser() {
  localStorage.removeItem('CapstoneReservationUser');
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
  const user = getUser();
  return user && user.is_superuser;
}

const storage = {
  getUser,
  saveUser,
  deleteUser,
  getOrientation,
  saveOrientation,
  checkAdmin,
};

export default storage;
