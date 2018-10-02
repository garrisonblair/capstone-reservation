import React from 'react';
import { shallow } from 'enzyme';
import ReservationDetailsModal from '../ReservationDetailsModal';

it('renders without crashing', () => {
  shallow(<ReservationDetailsModal />);
});
