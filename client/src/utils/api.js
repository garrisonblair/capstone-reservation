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

function getMyUser(token) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/me`,
    headers
  })
}

function updateUser(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/user/${id}`,
    headers,
    data,
    withCredentials: true
  })
}

function createCampOn(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/campon`,
    headers,
    data,
    withCredentials: true
  })
}

function getBookings(params) {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/booking`,
    params: params
  })
}

function createBooking(data){
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/booking`,
    headers,
    data,
    withCredentials: true
  });
}

function createRecurringBooking(data){
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/recurring_booking`,
    headers,
    data,
    withCredentials: true
  });
}

function getCampOns(params) {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/campon`,
    params: params
  })
}

function getRooms() {
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/room`
  })
}

function deleteRoom(id){
  const headers = getTokenHeader();
  return axios({
    method:'DELETE',
    url: `${settings.API_ROOT}/room`,
    headers,
    withCredentials:true
  })
}

function saveRoom(id, capacity, numOfComputers){
  const data = {
    "room_id":id,
    "capacity": capacity,
    "number_of_computers":numOfComputers
  }
  console.log(data);
  const headers = getTokenHeader();
  return axios({
    method:'POST',
    url: `${settings.API_ROOT}/room`,
    data,
    headers,
    withCredentials: true
  })
}

function getAdminSettings() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/settings`,
    headers,
    withCredentials: true
  })
}

function updateAdminSettings(data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/settings`,
    data,
    headers,
    withCredentials: true,
  })
}

const api = {
  register,
  login,
  verify,
  updateUser,
  createCampOn,
  getBookings,
  createBooking,
  createRecurringBooking,
  getCampOns,
  getRooms,
  deleteRoom,
  saveRoom,
  getAdminSettings,
  updateAdminSettings,
  getMyUser,
}

export default api;
