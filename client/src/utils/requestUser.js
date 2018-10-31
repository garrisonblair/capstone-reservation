import axios from 'axios';
import settings from '../config/settings';
import {getTokenHeader} from './requestHeaders';

export function getMeRequest(headers) {

  return axios({
    method: "GET",
    url: `${settings.API_ROOT}/me`,
    headers
  });
}
