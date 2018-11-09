import React from 'react';
import renderer from 'react-test-renderer';
import ReservationDetailsModal from '../../components/ReservationDetailsModal/index';

it('Shows ReservationDetailsModal', () => {
    const tree = renderer
        .create(<ReservationDetailsModal show={true}
            selectedRoomId="1"
            selectedRoomName="testname"
            selectedDate={new Date("2018-10-10")}
            selectedHour="12:00:00"
            selectedRoomCurrentBookings={[]}/>
            )
        .toJSON();
    expect(tree).toMatchSnapshot();
});
