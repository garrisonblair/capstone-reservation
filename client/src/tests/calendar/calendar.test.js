/* eslint-disable no-undef */
import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter as Router } from 'react-router-dom';
import 'react-dates/initialize';
import Calendar from '../../components/Calendar/index';


it('Shows calendar', () => {
  const roomsMock = [{ id: 1, name: 'room 1' }, { id: 2, name: 'room 2' }];
  const bookingsMock = [{
    id: 1,
    student: '12345567',
    room: 1,
    date: '2018-10-09',
    start_time: '08:10:00',
    end_time: '09:50:00',
    booker: {
      username: 'Ken',
    },
  }];

  const tree = renderer
    .create(
      <Router>
        <Calendar propsTestingRooms={roomsMock} propsTestingBookings={bookingsMock} />
      </Router>,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
