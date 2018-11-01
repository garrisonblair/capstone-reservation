import axios from 'axios';
import settings from '../config/settings';
import {getTokenHeader} from './requestHeaders';


function register(username) {
  let data = {
    'username': `${username}`
  };

  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/register`,
    data: data
  })
}

function login(username, password) {
  let data = {
    username,
    password
  }
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/login`,
    data: data
  })
}

function verify(token) {
  const data = {
    'token': `${token}`
  }
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/verify`,
    data: data
  })
}

function updateUser(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/user/${id}`,
    headers,
    data
  })
}

const api = {
  register,
  login,
  verify,
  updateUser
}

export default api;
