import React from 'react';
import { shallow } from 'enzyme';
import ReservationDetailsModal from '../ReservationDetailsModal';
import { Header } from 'semantic-ui-react';


describe('ReservationDetailsModal', () => {
  it('renders without crashing', () => {
    shallow(<ReservationDetailsModal />);
  });

  it('should render this.props properly', () => {
    var testDate = new Date().toDateString();
    var testRoomNumber = 4;
    const wrapper = shallow(<ReservationDetailsModal roomNumber="testRoomNumber" date="testDate" />);

    // console.log(wrapper.find('Header'));
    expect(wrapper.contains(<Header>Room # {testRoomNumber}</Header>));
    expect(wrapper.contains(<p>Date: {testDate} </p>));

  })
})
