import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter as Router } from 'react-router-dom';
import ReservationDetailsModal from '../../components/ReservationDetailsModal/index';

it('Shows ReservationDetailsModal', () => {
  const tree = renderer
    .create(
      <Router>
        <ReservationDetailsModal
          show
          selectedRoomId="1"
          selectedRoomName="testname"
          selectedDate={new Date('2018-10-10')}
          selectedHour="12:00:00"
          selectedRoomCurrentBookings={[]}
        />
      </Router>,
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
