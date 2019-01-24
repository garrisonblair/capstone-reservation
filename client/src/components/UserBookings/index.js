/* eslint-disable no-console */
/* eslint-disable react/no-unused-state */
/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
// import PropTypes from 'prop-types';
import {
  Menu,
} from 'semantic-ui-react';
import api from '../../utils/api';
import storage from '../../utils/local-storage';
import Bookings from './Bookings';
import RecurringBookings from './RecurringBookings';


class UserBookings extends Component {
  state = {
    bookings: [],
    recurringBookings: [],
    campOns: [],
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
        console.log(campOns);
        console.log(recurringBookings);
        console.log(bookings);
        this.setState({
          campOns,
          recurringBookings,
          bookings,
        });
      });
  }

  handleItemClick = (activeItem) => {
    this.setState({
      activeItem,
    });
  }

  renderTab = (activeItem) => {
    const { bookings, recurringBookings } = this.state;
    const components = {
      bookings: <Bookings bookings={bookings} />,
      recurring: <RecurringBookings bookings={recurringBookings} />,
      campons: '',
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
