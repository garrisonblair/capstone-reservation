/* eslint-disable react/no-array-index-key */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Menu, Segment, Table } from 'semantic-ui-react';
import EmptySegment from '../EmptySegment';
import api from '../../utils/api';
import './Privileges.scss';

class Privileges extends Component {
  state = {
    privileges: {},
    activeItem: 'me',
    isLoading: false,
  }

  componentDidMount() {
    this.setState({ isLoading: true });
    api.getMyPrivileges()
      .then((r) => {
        this.setState({ isLoading: false });
        if (r.status === 200) {
          this.setState({ privileges: r.data });
        }
      });
  }

  handleItemClick = (activeItem) => {
    this.setState({
      activeItem,
    });
  }

  renderTabs = () => {
    const { privileges, activeItem } = this.state;
    if (Object.keys(privileges).length === 0) {
      return null;
    }

    return (
      Object.keys(privileges).map((privilege, index) => (
        <Menu.Item
          key={index}
          name={privilege}
          active={activeItem === privilege}
          onClick={() => this.handleItemClick(privilege)}
        />
      ))
    );
  }

  renderMaximumRecurringBookings = () => {
    let content = null;
    const { privileges, activeItem } = this.state;
    if (privileges.can_make_recurring_booking === true) {
      content = (
        <Table.Row>
          <Table.Cell textAlign="left">Maximum recurring bookings</Table.Cell>
          <Table.Cell>{privileges[activeItem].max_recurring_bookings}</Table.Cell>
        </Table.Row>
      );
    }
    return content;
  }

  renderTable = () => {
    const { privileges, activeItem, isLoading } = this.state;

    let component = (
      <EmptySegment loading={isLoading} message="No Privileges" />
    );

    if (Object.keys(privileges).length === 0) {
      return component;
    }

    component = (
      <div>
        <Menu tabular>
          {this.renderTabs()}
        </Menu>
        <Segment loading={isLoading}>
          <Table collapsing unstackable>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Definition</Table.HeaderCell>
                <Table.HeaderCell>Value</Table.HeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              <Table.Row>
                <Table.Cell textAlign="left">Maximum days until booking</Table.Cell>
                <Table.Cell>{privileges[activeItem].max_days_until_booking}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell textAlign="left">Maximum days with bookings</Table.Cell>
                <Table.Cell>{privileges[activeItem].max_num_days_with_bookings}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell textAlign="left">Maximum bookings for date</Table.Cell>
                <Table.Cell>{privileges[activeItem].max_num_bookings_for_date}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell textAlign="left">Booking start time</Table.Cell>
                <Table.Cell>{privileges[activeItem].booking_start_time}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell textAlign="left">Booking end time</Table.Cell>
                <Table.Cell>{privileges[activeItem].booking_end_time}</Table.Cell>
              </Table.Row>
              <Table.Row>
                <Table.Cell textAlign="left">Recurring bookings</Table.Cell>
                <Table.Cell>{privileges[activeItem].can_make_recurring_booking ? 'Yes' : 'No'}</Table.Cell>
              </Table.Row>
              {this.renderMaximumRecurringBookings()}
            </Table.Body>
          </Table>
        </Segment>
      </div>
    );
    return component;
  }

  render() {
    const { showTitle } = this.props;

    return (
      <div id="privileges">
        { showTitle ? <h1> My Privileges </h1> : null }
        {this.renderTable()}
      </div>
    );
  }
}

Privileges.propTypes = {
  showTitle: PropTypes.bool,
};

Privileges.defaultProps = {
  showTitle: false,
};

export default Privileges;
