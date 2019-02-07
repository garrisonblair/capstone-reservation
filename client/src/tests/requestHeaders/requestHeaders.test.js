import getTokenHeader from '../../utils/requestHeaders';

it('should expect "Token " with the stored token data', () => {
  const token = 'myTokenToTest';
  const localStorageObject = {
    token,
  };
  localStorage.setItem('CapstoneReservationUser', JSON.stringify(localStorageObject));
  const headers = getTokenHeader();
  expect(headers.Authorization).toEqual(`Token ${token}`);
});
