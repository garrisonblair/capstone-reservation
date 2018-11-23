import axios from 'axios';
import settings from '../config/settings';
import getTokenHeader from './requestHeaders';


function register(username) {
  const data = {
    username,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/register`,
    data,
  });
}

function login(username, password) {
  const data = {
    username,
    password,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/login`,
    data,
  });
}

function verify(token) {
  const data = {
    token,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/verify`,
    data,
  });
}

function getMyUser() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/me`,
    headers,
  });
}

function updateUser(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/user/${id}`,
    headers,
    data,
    withCredentials: true,
  });
}

function getBookings(params) {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/bookings`,
    params,
  });
}

function createBooking(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/booking`,
    headers,
    data,
    withCredentials: true,
  });
}

function updateBooking(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/booking/${id}`,
    headers,
    data,
  });
}

function createRecurringBooking(data) {
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
    url: `${settings.API_ROOT}/campons`,
    params,
  });
}

function createCampOn(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/campon`,
    headers,
    data,
    withCredentials: true,
  });
}

function getRooms() {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/rooms`,
  });
}

function createRoom(name, capacity, numberOfComputers) {
  const headers = getTokenHeader();
  const data = {
    name,
    capacity,
    number_of_computers: numberOfComputers,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/room`,
    headers,
    data,
    withCredentials: true,
  });
}

function updateRoom(id, name, capacity, numberOfComputers) {
  const headers = getTokenHeader();
  const data = {
    name,
    capacity,
    number_of_computers: numberOfComputers,
  };
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/room/${id}`,
    headers,
    data,
    withCredentials: true,
  });
}

function deleteRoom(id) {
  const headers = getTokenHeader();
  const data = {
    id,
  };
  return axios({
    method: 'DELETE',
    url: `${settings.API_ROOT}/room/${id}`,
    headers,
    data,
    withCredentials: true,
  });
}

function getAdminSettings() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/settings`,
    headers,
    withCredentials: true,
  });
}

function updateAdminSettings(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/settings`,
    headers,
    data,
    withCredentials: true,
  });
}

function getPrivileges() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/privilege_categories`,
    headers,
    withCredentials: true,
  });
}

function createPrivilege(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/privilege_category`,
    headers,
    data,
    withCredentials: true,
  });
}

const api = {
  register,
  login,
  verify,
  getMyUser,
  updateUser,
  getBookings,
  createBooking,
  updateBooking,
  createRecurringBooking,
  getCampOns,
  createCampOn,
  getRooms,
  createRoom,
  updateRoom,
  deleteRoom,
  getAdminSettings,
  updateAdminSettings,
  getPrivileges,
  createPrivilege,
};

export default api;
