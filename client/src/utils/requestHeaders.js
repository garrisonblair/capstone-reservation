function getApiToken() {
  const user = JSON.parse(localStorage.getItem('CapstoneReservationUser'));
  return user ? user.token : null;
}

export default function getTokenHeader() {
  const token = getApiToken();
  return token
    ? { Authorization: `Token ${token}` }
    : {};
}
