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

async function logout() {
  try {
    const headers = getTokenHeader();
    await axios({
      method: 'GET',
      url: `${settings.API_ROOT}/logout`,
      headers,
    });
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log(e);
  }
  localStorage.removeItem('CapstoneReservationUser');
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

function getMyGroups() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/groups`,
    headers,
  });
}

function createGroup(name) {
  const headers = getTokenHeader();
  const data = {
    name,
  };

  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group`,
    headers,
    data,
  });
}

function addMembersToGroup(id, members) {
  const headers = getTokenHeader();
  const data = {
    members,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group/${id}/add_members`,
    headers,
    data,
  });
}

function leaveGroup(id) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group/${id}/leave_group`,
    headers,
  });
}

function inviteMembers(groupId, members) {
  const headers = getTokenHeader();
  const data = {
    invited_bookers: members,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group/${groupId}/invite_members`,
    headers,
    data,
    withCredentials: true,
  });
}

function revokeInvitation(invitationId) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group_invitation/${invitationId}/revoke`,
    headers,
    withCredentials: true,
  });
}

function removeMembersFromGroup(groupId, members) {
  const headers = getTokenHeader();
  const data = {
    members,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group/${groupId}/remove_members`,
    headers,
    data,
  });
}

function getLogEntries(params) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/logentries`,
    headers,
    params,
    withCredentials: true,
  });
}

function getContentTypes() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/content_types`,
    headers,
    withCredentials: true,
  });
}

function getUsers(params) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/users`,
    params,
    headers,
    withCredentials: true,
  });
}

function getBookers() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/bookers`,
    headers,
    withCredentials: true,
  });
}

const api = {
  register,
  login,
  logout,
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
  getMyGroups,
  createGroup,
  addMembersToGroup,
  leaveGroup,
  inviteMembers,
  revokeInvitation,
  removeMembersFromGroup,
  getLogEntries,
  getContentTypes,
  getUsers,
  getBookers,
};

export default api;
