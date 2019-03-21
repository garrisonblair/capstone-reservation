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

function resetPassword(username) {
  const data = {
    username,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/reset_password`,
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

function getUser(id) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/user/${id}`,
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

function getUserBookings(id) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/bookings/${id}`,
    headers,
    withCredentials: true,
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

function deleteBooking(id) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/booking/${id}/cancel_booking`,
    headers,
  });
}

function confirmBooking(booking) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/booking/${booking.id}/confirm`,
    headers,
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

function getRoomsForDate(date, startTime, endTime) {
  let params = null;
  params = {
    date,
    start_time: startTime,
    end_time: endTime,
  };
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/rooms`,
    params,
  });
}

function createRoom(
  name,
  capacity,
  numberOfComputers,
  hasTv,
  hasWindows,
  maxBookingDuration,
  maxRecurringBookingDuration,
) {
  const headers = getTokenHeader();
  const data = {
    name,
    capacity,
    number_of_computers: numberOfComputers,
    has_tv: hasTv,
    has_windows: hasWindows,
    max_booking_duration: maxBookingDuration,
    max_recurring_booking_duration: maxRecurringBookingDuration,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/room`,
    headers,
    data,
    withCredentials: true,
  });
}

function updateRoom(
  id,
  name,
  capacity,
  numberOfComputers,
  hasTv,
  hasWindows,
  maxBookingDuration,
  maxRecurringBookingDuration,
) {
  const headers = getTokenHeader();
  const data = {
    name,
    capacity,
    number_of_computers: numberOfComputers,
    has_tv: hasTv,
    has_windows: hasWindows,
    max_booking_duration: maxBookingDuration,
    max_recurring_booking_duration: maxRecurringBookingDuration,
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

function getCardReaders(roomId) {
  const headers = getTokenHeader();
  let params = null;
  if (roomId) {
    params = {
      room: roomId,
    };
  }
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/card_readers`,
    headers,
    params,
    withCredentials: true,
  });
}

function createCardReader(roomID) {
  const headers = getTokenHeader();

  const data = {
    room: roomID,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/card_reader`,
    headers,
    data,
    withCredentials: true,
  });
}

function deleteCardReader(cardReaderId) {
  const headers = getTokenHeader();
  return axios({
    method: 'DELETE',
    url: `${settings.API_ROOT}/card_reader/${cardReaderId}/delete`,
    headers,
    withCredentials: true,
  });
}

function getAdminSettings() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/getSettings`,
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

function getMyPrivileges() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/my_privileges`,
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

function updatePrivilege(id, data) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/privilege_category/${id}`,
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

function getGroupPrivileges(groupId) {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/group/${groupId}/privileges`,
    headers,
    withCredentials: true,
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

function getUsers(searchText, searchLimit, offset, isActive, isSuperUser, isStaff, sortTerm) {
  const headers = getTokenHeader();

  const params = {};
  if (searchText !== undefined) { params.search_term = searchText; }
  if (isActive !== undefined) { params.is_active = isActive ? 'True' : 'False'; }
  if (isSuperUser !== undefined) { params.is_superuser = isSuperUser ? 'True' : 'False'; }
  if (isStaff !== undefined) { params.is_staff = isStaff ? 'True' : 'False'; }
  if (searchLimit !== undefined) { params.limit = searchLimit; }
  if (offset !== undefined) { params.offset = offset; }
  if (sortTerm !== undefined) { params.sort_by = sortTerm; }
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/users`,
    params,
    headers,
    withCredentials: true,
  });
}

function canUserMakeRecurring(userId, userType) {
  const headers = getTokenHeader();

  const params = {
    pk: userId,
    type: userType,
  };
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/can_make_recurring`,
    params,
    headers,
    withCredentials: true,
  });
}

function addPrivilege(username, privilegeID) {
  const headers = getTokenHeader();
  const data = {
    users: username,
    privilege_category: privilegeID,
  };
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/assign_privilege`,
    headers,
    data,
    withCredentials: true,
  });
}

function assignIndividualPrivileges(userId) {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/assign_privileges/${userId}`,
    headers,
    withCredentials: true,
  });
}

function assignAllPrivileges() {
  const headers = getTokenHeader();
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/assign_privileges`,
    headers,
    withCredentials: true,
  });
}

function removePrivilege(username, privilegeID) {
  const headers = getTokenHeader();
  const data = {
    users: username,
    privilege_category: privilegeID,
  };
  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/remove_privilege`,
    headers,
    data,
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

function requestPrivilege(groupId, privilegeId) {
  const headers = getTokenHeader();
  const data = {
    group: groupId,
    privilege_category: privilegeId,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/request_privilege`,
    headers,
    data,
    withCredentials: true,
  });
}

function getPrivilegeRequests() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/privilege_requests`,
    headers,
    withCredentials: true,
  });
}

function cancelPrivilegeRequest(requestId) {
  const headers = getTokenHeader();
  return axios({
    method: 'DELETE',
    url: `${settings.API_ROOT}/cancel_request/${requestId}`,
    headers,
    withCredentials: true,
  });
}

function getGroupInvitations() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/group_invitations`,
    headers,
    withCredentials: true,
  });
}

function acceptInvitation(invitationId) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group_invitation/${invitationId}/accept`,
    headers,
    withCredentials: true,
  });
}

function approvePrivilegeRequest(requestId) {
  const headers = getTokenHeader();
  const data = {
    privilege_request: requestId,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/approve_privilege_request`,
    headers,
    data,
    withCredentials: true,
  });
}

function rejectInvitation(invitationId) {
  const headers = getTokenHeader();
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/group_invitation/${invitationId}/reject`,
    headers,
    withCredentials: true,
  });
}

function denyPrivilegeRequest(requestId, reason) {
  const headers = getTokenHeader();
  const data = {
    privilege_request: requestId,
    denial_reason: reason,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/deny_privilege_request`,
    headers,
    data,
    withCredentials: true,
  });
}

function getRoomStatistics(startDate, endDate) {
  const headers = getTokenHeader();
  const params = {};
  if (startDate.length !== 0) {
    params.start = startDate;
  }

  if (endDate.length !== 0) {
    params.end = endDate;
  }

  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/room_statistics`,
    headers,
    params,
    withCredentials: true,
  });
}

function getProgramStatistics(startDate, endDate, withProgram, withGradLevel, withCategories) {
  const headers = getTokenHeader();
  const params = {
    withProgram,
    withGradLevel,
    withCategories,
  };

  if (startDate.length !== 0) {
    params.start = startDate;
  }

  if (endDate.length !== 0) {
    params.end = endDate;
  }

  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/program_statistics`,
    headers,
    params,
    withCredentials: true,
  });
}

function createAnnouncement(title, content, startDate, endDate) {
  const headers = getTokenHeader();
  const data = {
    title,
    content,
    start_date: startDate,
    end_date: endDate,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/announcement`,
    headers,
    data,
    withCredentials: true,
  });
}

function getAllAnnouncements() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/announcements`,
    headers,
    withCredentials: true,
  });
}

function deleteAnnouncement(id) {
  const headers = getTokenHeader();
  return axios({
    method: 'DELETE',
    url: `${settings.API_ROOT}/announcement/delete/${id}`,
    headers,
    withCredentials: true,
  });
}

function updateAnnouncement(announcement) {
  const headers = getTokenHeader();
  const data = {
    title: announcement.title,
    content: announcement.content,
    start_date: announcement.start_date,
    end_date: announcement.end_date,
  };

  return axios({
    method: 'PATCH',
    url: `${settings.API_ROOT}/announcement/${announcement.id}`,
    headers,
    data,
    withCredentials: true,
  });
}

function postNotification(bookerId, rooms, date, rangeStart, rangeEnd, minBookingTime) {
  const headers = getTokenHeader();
  const data = {
    booker: bookerId,
    rooms,
    date,
    range_start: rangeStart,
    range_end: rangeEnd,
    minimum_booking_time: minBookingTime,
  };

  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/notify`,
    headers,
    data,
  });
}

function getCSV() {
  const headers = getTokenHeader();
  return axios({
    method: 'GET',
    url: `${settings.API_ROOT}/csv`,
    headers,
    withCredentials: true,
  });
}

function postCSV(model) {
  const headers = getTokenHeader();
  const data = {
    model,
  };
  return axios({
    method: 'POST',
    url: `${settings.API_ROOT}/csv`,
    headers,
    data,
    withCredentials: true,
  });
}

const api = {
  register,
  resetPassword,
  login,
  logout,
  verify,
  getUser,
  updateUser,
  getBookings,
  getUserBookings,
  createBooking,
  updateBooking,
  deleteBooking,
  confirmBooking,
  createRecurringBooking,
  getCampOns,
  createCampOn,
  getRooms,
  getRoomsForDate,
  createRoom,
  updateRoom,
  deleteRoom,
  getCardReaders,
  createCardReader,
  deleteCardReader,
  getAdminSettings,
  updateAdminSettings,
  getPrivileges,
  getMyPrivileges,
  createPrivilege,
  updatePrivilege,
  getMyGroups,
  createGroup,
  addMembersToGroup,
  leaveGroup,
  inviteMembers,
  revokeInvitation,
  removeMembersFromGroup,
  getGroupPrivileges,
  getLogEntries,
  getContentTypes,
  getUsers,
  canUserMakeRecurring,
  addPrivilege,
  assignIndividualPrivileges,
  assignAllPrivileges,
  removePrivilege,
  getBookers,
  requestPrivilege,
  getPrivilegeRequests,
  cancelPrivilegeRequest,
  getGroupInvitations,
  acceptInvitation,
  approvePrivilegeRequest,
  rejectInvitation,
  denyPrivilegeRequest,
  getRoomStatistics,
  getProgramStatistics,
  createAnnouncement,
  getAllAnnouncements,
  deleteAnnouncement,
  updateAnnouncement,
  postNotification,
  getCSV,
  postCSV,
};

export default api;
