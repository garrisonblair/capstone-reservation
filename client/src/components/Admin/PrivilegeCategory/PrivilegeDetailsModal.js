import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Button, Header, Icon, Modal,
} from 'semantic-ui-react';
import './PrivilegeDetailsModal.scss';


class PrivilegeDetailsModal extends Component {
  renderBoolean = boolean => (
    <Icon
      name={boolean ? 'check circle' : 'times circle'}
      color={boolean ? 'green' : 'red'}
    />
  )

  render() {
    const { show, onClose, privilege } = this.props;
    return (
      <Modal className="privilege-details-modal" open={show} onClose={onClose}>
        <Header>
          {privilege.name}
        </Header>
        <div className="privilege-details-modal__container">
          <p>
            <strong> Name: </strong>
            {privilege.name}
          </p>
          <p>
            <strong> Default: </strong>
            {this.renderBoolean(privilege.is_default)}
          </p>
          <p>
            <strong> Parent Category: </strong>
            {privilege.parent_category ? privilege.parent_category.name : '-'}
          </p>
          <p>
            <strong> Related Course: </strong>
            {privilege.related_course || '-'}
          </p>
          <p>
            <strong> Max Days Until Booking: </strong>
            {privilege.max_days_until_booking}
          </p>
          <p>
            <strong> Max Bookings per day: </strong>
            {privilege.max_num_bookings_for_date}
          </p>
          <p>
            <strong> Max days with bookings: </strong>
            {privilege.max_num_days_with_bookings}
          </p>
          <p>
            <strong> Max Recurring Bookings: </strong>
            {privilege.max_recurring_bookings}
          </p>
          <p>
            <strong> Recurring Booking Permission: </strong>
            {this.renderBoolean(privilege.can_make_recurring_booking)}
          </p>
          <p>
            <strong> Booking Start Time: </strong>
            {privilege.booking_start_time}
          </p>
          <p>
            <strong> Booking End Time: </strong>
            {privilege.booking_end_time}
          </p>
        </div>
        <div className="ui divider" />
        <div className="controls">
          <Button icon labelPosition="left" negative size="small" onClick={onClose}>
            <Icon name="x" />
            Close
          </Button>
        </div>
      </Modal>
    );
  }
}

PrivilegeDetailsModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  privilege: PropTypes.object.isRequired,
};


export default PrivilegeDetailsModal;
