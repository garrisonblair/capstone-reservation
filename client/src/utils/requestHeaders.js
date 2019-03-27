import storage from './local-storage';

function getApiToken() {
  const user = storage.getUser();
  return user ? user.token : null;
}

export default function getTokenHeader() {
  const token = getApiToken();
  return token
    ? { Authorization: `Token ${token}` }
    : {};
}
