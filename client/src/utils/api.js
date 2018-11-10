import axios from 'axios';
import settings from '../config/settings';
import {getTokenHeader} from './requestHeaders';


function register(username) {
  let data = {
    'username': `${username}`,
  };

  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/register`,
    data: data,
  })
}

function login(username, password) {
  let data = {
    username,
    password,
  }
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/login`,
    data: data,
  })
}

function verify(token) {
  const data = {
    'token': `${token}`,
  }
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/verify`,
    data: data,
  })
}

function getMyUser() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/me`,
    headers,
  })
}

function updateUser(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/user/${id}`,
    headers,
    data,
    withCredentials: true,
  })
}

function createCampOn(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/campon`,
    headers,
    data,
    withCredentials: true,
  })
}

function getBookings(params) {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/booking`,
    params: params,
  })
}

function createBooking(data){
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/booking`,
    headers,
    data,
    withCredentials: true,
  });
}

function updateBooking(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/booking`,
    data,
    headers,
  })
}

function createRecurringBooking(data){
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/recurring_booking`,
    headers,
    data,
    withCredentials: true,
  });
}

function getCampOns(params) {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/campon`,
    params: params,
  })
}

function getRooms() {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/room`,
  })
}

function getAdminSettings() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/settings`,
    headers,
    withCredentials: true,
  })
}

function updateAdminSettings(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/settings`,
    headers,
    data,
    withCredentials: true,
  })
}

function getPrivileges() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/privilege_categories`,
    headers,
    withCredentials: true,
  })
}

function createPrivilege(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/privilege_categories`,
    headers,
    data,
    withCredentials: true,
  })
}

const api = {
  register,
  login,
  verify,
  getMyUser,
  updateUser,
  createCampOn,
  getBookings,
  createBooking,
  updateBooking,
  createRecurringBooking,
  getCampOns,
  getRooms,
  getAdminSettings,
  updateAdminSettings,
  getPrivileges,
  createPrivilege
}

export default api;
