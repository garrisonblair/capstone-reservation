function getApiToken() {
  const user = JSON.parse(localStorage.getItem('CapstoneReservationUser'));
  return user? user.token: null;
}

export function getTokenHeader() {
  let token = getApiToken();
  return token
    ? {Authorization: `Token ${token}`}
    : {};
}
