import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Menu, Segment,
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
    isLoading: false,
  }

  componentDidMount() {
    const user = storage.getUser();
    this.setState({ isLoading: true });
    api.getUserBookings(user.id)
      .then(({ data }) => data)
      .then((data) => {
        this.setState({ isLoading: false });
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
    const { activeItem, isLoading } = this.state;
    const { vertical, tabular } = this.props;

    return (
      <div>
        <Menu vertical={vertical} tabular={tabular}>
          <Menu.Item name="Bookings" active={activeItem === 'bookings'} onClick={() => this.handleItemClick('bookings')} />
          <Menu.Item name="Recurring Bookings" active={activeItem === 'recurring'} onClick={() => this.handleItemClick('recurring')} />
          <Menu.Item name="Camp Ons" active={activeItem === 'campons'} onClick={() => this.handleItemClick('campons')} />
        </Menu>
        <Segment loading={isLoading} style={{ overflow: 'auto' }}>
          {this.renderTab(activeItem)}
        </Segment>
      </div>
    );
  }
}

UserBookings.propTypes = {
  vertical: PropTypes.bool,
  tabular: PropTypes.bool,
};

UserBookings.defaultProps = {
  vertical: false,
  tabular: true,
};

export default UserBookings;
