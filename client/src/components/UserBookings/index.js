import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import {
  Menu,
} from 'semantic-ui-react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import Bookings from './Bookings';
import RecurringBookings from './RecurringBookings';
import CampOns from './CampOns';


class UserBookings extends Component {
  state = {
    bookings: [],
    recurringBookings: [],
    campOns: [],
    allBookings: [],
    rooms: [],
    activeItem: 'bookings',
  }

  componentDidMount() {
    const user = storage.getUser();
    api.getUserBookings(user.id)
      .then(({ data }) => data)
      .then((data) => {
        const {
          campons: campOns,
          recurring_bookings: recurringBookings,
          standard_bookings: bookings,
        } = data;
        this.setState({
          campOns,
          recurringBookings,
          bookings,
        });
      });

    api.getBookings()
      .then((response) => {
        const { data: allBookings } = response;
        this.setState({
          allBookings,
        });
      });

    api.getRooms()
      .then((response) => {
        const { data: rooms } = response;
        this.setState({
          rooms,
        });
      });
  }

  handleItemClick = (activeItem) => {
    this.setState({
      activeItem,
    });
  }

  renderTab = (activeItem) => {
    const {
      bookings,
      recurringBookings,
      campOns,
      allBookings,
      rooms,
    } = this.state;

    const components = {
      bookings: <Bookings bookings={bookings} />,
      recurring: <RecurringBookings bookings={recurringBookings} />,
      campons: <CampOns rooms={rooms} allBookings={allBookings} campOns={campOns} />,
    };

    return components[activeItem];
  }

  render() {
    const { activeItem } = this.state;
    return (
      <div>
        <Menu tabular>
          <Menu.Item name="Bookings" active={activeItem === 'bookings'} onClick={() => this.handleItemClick('bookings')} />
          <Menu.Item name="Recurring Bookings" active={activeItem === 'recurring'} onClick={() => this.handleItemClick('recurring')} />
          <Menu.Item name="Camp Ons" active={activeItem === 'campons'} onClick={() => this.handleItemClick('campons')} />
        </Menu>
        {this.renderTab(activeItem)}
      </div>
    );
  }
}

export default UserBookings;