import {getTokenHeader} from './requestHeaders';
import axios from 'axios';
import settings from '../config/settings';

export function getMeRequest(headers) {

  return axios({
    method: "GET",
    url: `${settings.API_ROOT}/me`,
    headers
  });
}
