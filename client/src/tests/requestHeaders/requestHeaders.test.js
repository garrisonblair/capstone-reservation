import React from 'react';
import {getTokenHeader} from '../../utils/requestHeaders';

it('should', () => {
    const token = "myTokenToTest";
    const localStorageObject = {
        "token":token
    };
    localStorage.setItem('CapstoneReservationUser',JSON.stringify(localStorageObject));
    const headers = getTokenHeader();
    expect(headers.Authorization).toEqual(`Token ${token}`);
});
