import React from 'react';
import renderer from 'react-test-renderer';
import Calendar from '../../components/Calendar/index';

it('Shows calendar', () => {
  const roomsMock = [{ id: 1, name: 'room 1' }, { id: 2, name: 'room 2' }];
  const bookingsMock = [{
    id: 1, student: '12345567', room: 1, date: '2018-10-09', start_time: '08:10:00', end_time: '09:50:00',
  }];
  const tree = renderer
    .create(<Calendar propsTestingRooms={roomsMock} propsTestingBookings={bookingsMock} />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});
